#!/usr/bin/env python3
"""Explora canales de YouTube: lista videos, calcula senales, selecciona
candidatos, descarga y limpia subtitulos y guarda las fichas externas.

Primera parte de la fase 2 del sistema editorial (ver ARQUITECTURA.md,
secciones 2, 4, 5, 6, 8.2 y 10). Python sin IA, solo biblioteca estandar;
la unica herramienta externa es yt-dlp, invocada como subproceso.

Reparto: el script hace lo repetible (listar canales, calcular senales,
seleccionar candidatos, descargar y limpiar subtitulos, validar y guardar).
El modelo solo el juicio (clasificar relevancia, rellenar fichas); entrega un
JSON y el script lo valida y lo guarda. El modelo nunca escribe en
biblioteca/ directamente.

Comandos:
  recoger                        lista los canales y actualiza meta.json,
                                 metricas.jsonl y las senales
  relevancia-pendiente           JSON con los videos sin clasificar, la linea
                                 editorial, los recursos y los temas existentes
  guardar-relevancia <json>      valida y guarda las clasificaciones del modelo
  candidatos                     seleccion determinista y metadatos completos
  subtitulos <video_id>...       descarga subtitulos y genera transcripcion.md
  pendientes-ficha               videos con transcripcion y sin ficha al dia,
                                 mas los subtemas existentes con frecuencias
  guardar-ficha <id> <json>      valida la ficha del modelo y la guarda
  clasificar-titulos             reprocesa los meta.json existentes y guarda la
                                 formula de titulo de cada video (sin yt-dlp)
  mapa                           regenera biblioteca/youtube/mapa-videos.md

Codigos de salida:
  0  todo correcto
  1  errores parciales (algun canal o video fallo; los datos validos se
     conservan)
  2  no pudo ejecutarse (falta yt-dlp, la configuracion o canales.md)
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
import unicodedata
from datetime import date, datetime, timezone
from pathlib import Path

INSTRUCCION_INSTALACION = (
    "yt-dlp no esta disponible. Instalalo con: pip install yt-dlp"
)

# Campos de la ficha externa que impone el script desde meta.json. Si el JSON
# del modelo los incluye, se ignoran.
CAMPOS_OBJETIVOS_FICHA = ("id", "fuente", "url", "autor", "fecha", "huella", "senales")

# Campos de juicio que entrega el modelo.
CAMPOS_JUICIO_FICHA = (
    "tema",
    "subtemas",
    "tesis",
    "afirmaciones",
    "entidades",
    "demuestra",
    "promete_sin_demostrar",
    "preguntas_abiertas",
    "avisos_transcripcion",
)

DIAS_SENAL_COMPLETA = 7       # un video mas joven no entra en la mediana
MINIMO_VIDEOS_MEDIANA = 5     # por debajo, mediana_poco_fiable
SEGUNDOS_POR_PARRAFO = 30     # agrupacion de la transcripcion
MAX_DESCRIPCION_RELEVANCIA = 500

PATRON_CANAL = re.compile(
    r"https?://(?:www\.)?youtube\.com/(@[A-Za-z0-9._-]+|channel/UC[A-Za-z0-9_-]+)"
)
PATRON_URL = re.compile(r"https?://\S+")
PATRON_TIEMPO_VTT = re.compile(
    r"(\d{1,2}:)?\d{2}:\d{2}[.,]\d{3}\s*-->\s*(\d{1,2}:)?\d{2}:\d{2}[.,]\d{3}"
)


class ErrorEjecucion(Exception):
    """El comando no pudo ejecutarse (codigo de salida 2)."""


class YtDlpNoDisponible(ErrorEjecucion):
    pass


# ---------------------------------------------------------------------------
# yt-dlp: resolucion e invocacion (una unica funcion inyectable)
# ---------------------------------------------------------------------------

def resolver_comando_ytdlp() -> list[str]:
    """Devuelve el comando base de yt-dlp.

    Intenta el ejecutable `yt-dlp`; si no esta en el PATH, usa el modulo de
    Python (`python -m yt_dlp`). Si tampoco existe, falla con la instruccion
    de instalacion.
    """
    ejecutable = shutil.which("yt-dlp")
    if ejecutable:
        return [ejecutable]
    if importlib.util.find_spec("yt_dlp") is not None:
        return [sys.executable, "-m", "yt_dlp"]
    raise YtDlpNoDisponible(INSTRUCCION_INSTALACION)


def crear_ejecutor_real(timeout_segundos: float):
    """Crea la funcion real que invoca yt-dlp como subproceso.

    Firma de la funcion: ejecutar(args: list[str]) -> (codigo, stdout, stderr).
    En las pruebas se inyecta una funcion simulada con la misma firma.
    """
    comando_base = resolver_comando_ytdlp()

    def ejecutar(args: list[str]) -> tuple[int, str, str]:
        proceso = subprocess.run(
            comando_base + list(args),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_segundos,
        )
        return proceso.returncode, proceso.stdout or "", proceso.stderr or ""

    return ejecutar


# ---------------------------------------------------------------------------
# Escritura segura
# ---------------------------------------------------------------------------

def escribir_atomico(ruta: Path, contenido: str):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    descriptor, tmp = tempfile.mkstemp(dir=ruta.parent, suffix=".tmp")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as f:
            f.write(contenido)
        os.replace(tmp, ruta)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def escribir_json_atomico(ruta: Path, datos):
    escribir_atomico(ruta, json.dumps(datos, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


# ---------------------------------------------------------------------------
# Validacion contra el esquema (biblioteca estandar, sin dependencias)
# ---------------------------------------------------------------------------

_TIPOS = {
    "object": dict,
    "array": list,
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "null": type(None),
}


def validar_contra_esquema(dato, esquema: dict, ruta: str = "ficha") -> list[str]:
    """Valida tipos, campos obligatorios y valores permitidos.

    Soporta el subconjunto de JSON Schema de `ficha-externa.schema.json`:
    type (simple o lista, con "null"), required, properties, enum, items,
    minItems, maxItems y minLength.
    """
    errores: list[str] = []

    tipo = esquema.get("type")
    if tipo:
        tipos = tipo if isinstance(tipo, list) else [tipo]
        esperados = tuple(_TIPOS[t] for t in tipos)
        numerico = any(t in ("integer", "number") for t in tipos)
        if isinstance(dato, bool) and numerico and "boolean" not in tipos:
            errores.append(f"{ruta}: se esperaba {'/'.join(tipos)} y llego un booleano")
            return errores
        if not isinstance(dato, esperados):
            errores.append(
                f"{ruta}: se esperaba {'/'.join(tipos)} y llego {type(dato).__name__}"
            )
            return errores

    if "enum" in esquema and dato not in esquema["enum"]:
        permitidos = ", ".join(repr(v) for v in esquema["enum"])
        errores.append(f"{ruta}: valor {dato!r} no permitido; debe ser uno de: {permitidos}")

    if isinstance(dato, str) and "minLength" in esquema and len(dato.strip()) < esquema["minLength"]:
        errores.append(f"{ruta}: no puede estar vacio")

    if isinstance(dato, dict):
        for obligatorio in esquema.get("required", []):
            if obligatorio not in dato:
                errores.append(f"{ruta}: falta el campo obligatorio '{obligatorio}'")
        for clave, subesquema in esquema.get("properties", {}).items():
            if clave in dato:
                errores.extend(validar_contra_esquema(dato[clave], subesquema, f"{ruta}.{clave}"))

    if isinstance(dato, list):
        if "minItems" in esquema and len(dato) < esquema["minItems"]:
            errores.append(f"{ruta}: necesita al menos {esquema['minItems']} elemento(s)")
        if "maxItems" in esquema and len(dato) > esquema["maxItems"]:
            errores.append(f"{ruta}: admite como mucho {esquema['maxItems']} elemento(s)")
        subesquema = esquema.get("items")
        if subesquema:
            for i, elemento in enumerate(dato):
                errores.extend(validar_contra_esquema(elemento, subesquema, f"{ruta}[{i}]"))

    return errores


# ---------------------------------------------------------------------------
# canales.md
# ---------------------------------------------------------------------------

def leer_canales(texto: str) -> tuple[list[str], list[dict]]:
    """Extrae las URLs de canal de canales.md.

    Acepta `https://www.youtube.com/@handle` y
    `https://www.youtube.com/channel/UC...`. El texto que no es una URL se
    ignora. Una URL que no se reconoce como canal es un error de esa linea y
    no detiene a las demas.
    """
    canales: list[str] = []
    errores: list[dict] = []
    vistos: set[str] = set()
    for linea in texto.splitlines():
        for url in PATRON_URL.findall(linea):
            url_limpia = url.rstrip(").,;")
            coincidencia = PATRON_CANAL.match(url_limpia)
            if coincidencia:
                normalizada = f"https://www.youtube.com/{coincidencia.group(1)}"
                if normalizada not in vistos:
                    vistos.add(normalizada)
                    canales.append(normalizada)
            else:
                errores.append({
                    "url": url_limpia,
                    "motivo": "URL no reconocida: se esperaba youtube.com/@handle o youtube.com/channel/UC...",
                })
    return canales, errores


# ---------------------------------------------------------------------------
# Limpieza de VTT
# ---------------------------------------------------------------------------

def _tiempo_a_segundos(marca: str) -> float:
    partes = marca.replace(",", ".").split(":")
    segundos = 0.0
    for parte in partes:
        segundos = segundos * 60 + float(parte)
    return segundos


def _formato_mmss(segundos: float) -> str:
    total = int(segundos)
    return f"{total // 60:02d}:{total % 60:02d}"


def limpiar_vtt(texto_vtt: str) -> str:
    """Convierte un VTT en parrafos limpios con marcas de tiempo [mm:ss].

    Quita etiquetas y estilos, elimina las lineas repetidas que producen los
    subtitulos automaticos y agrupa el texto aproximadamente cada 30 segundos.
    """
    cues: list[tuple[float, str]] = []  # (segundos de inicio, linea de texto)
    inicio_actual: float | None = None
    en_bloque_ignorado = False

    for linea in texto_vtt.splitlines():
        linea = linea.strip("﻿").rstrip()
        sin_espacios = linea.strip()
        if not sin_espacios:
            en_bloque_ignorado = False
            inicio_actual = None
            continue
        if sin_espacios.startswith(("WEBVTT", "Kind:", "Language:", "NOTE", "STYLE", "REGION")):
            en_bloque_ignorado = sin_espacios.startswith(("NOTE", "STYLE", "REGION"))
            continue
        if en_bloque_ignorado:
            continue
        tiempo = PATRON_TIEMPO_VTT.search(sin_espacios)
        if tiempo:
            inicio_actual = _tiempo_a_segundos(sin_espacios.split("-->")[0].strip().split()[0])
            continue
        if inicio_actual is None:
            continue  # identificador de cue u otra linea fuera de un cue
        # Texto del cue: fuera etiquetas (<c>, <00:00:01.000>, estilos).
        texto = re.sub(r"<[^>]*>", "", sin_espacios)
        texto = texto.replace("&nbsp;", " ").replace("&amp;", "&")
        texto = re.sub(r"\s+", " ", texto).strip()
        if texto:
            cues.append((inicio_actual, texto))

    # Los subtitulos automaticos repiten la misma linea en cues consecutivos.
    lineas: list[tuple[float, str]] = []
    for inicio, texto in cues:
        if lineas and lineas[-1][1] == texto:
            continue
        lineas.append((inicio, texto))

    # Agrupar en parrafos de ~30 segundos.
    parrafos: list[str] = []
    actual: list[str] = []
    inicio_parrafo = 0.0
    for inicio, texto in lineas:
        if not actual:
            inicio_parrafo = inicio
        elif inicio - inicio_parrafo >= SEGUNDOS_POR_PARRAFO:
            parrafos.append(f"[{_formato_mmss(inicio_parrafo)}] " + " ".join(actual))
            actual = []
            inicio_parrafo = inicio
        actual.append(texto)
    if actual:
        parrafos.append(f"[{_formato_mmss(inicio_parrafo)}] " + " ".join(actual))

    return "\n\n".join(parrafos) + ("\n" if parrafos else "")


# ---------------------------------------------------------------------------
# Formulas de titulo
#
# Clasifica las palabras del titulo, no el porque real del exito del video
# (ver la nota de references/formulas-titulo.json). Gana la formula con mas
# patrones coincidentes; en empate, la primera del archivo; sin coincidencias,
# "sin clasificar".
# ---------------------------------------------------------------------------

RUTA_FORMULAS = Path(__file__).resolve().parent.parent / "references" / "formulas-titulo.json"
SIN_CLASIFICAR = "sin clasificar"

_cache_formulas: dict[str, list[tuple[str, list[re.Pattern]]]] = {}


def _normalizar_titulo(texto: str) -> str:
    """Minusculas y sin acentos, para que los patrones valgan en ambos casos."""
    descompuesto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")


def cargar_formulas(ruta: Path = RUTA_FORMULAS) -> list[tuple[str, list[re.Pattern]]]:
    """Carga y compila las formulas de titulo (con cache por ruta)."""
    clave = str(ruta)
    if clave not in _cache_formulas:
        datos = json.loads(Path(ruta).read_text(encoding="utf-8"))
        _cache_formulas[clave] = [
            (
                formula["nombre"],
                [re.compile(p, re.IGNORECASE) for p in formula["patrones"]],
            )
            for formula in datos["formulas"]
        ]
    return _cache_formulas[clave]


def clasificar_titulo(titulo: str, formulas=None) -> str:
    """Devuelve la formula con mas patrones coincidentes o "sin clasificar"."""
    if not titulo or not titulo.strip():
        return SIN_CLASIFICAR
    formulas = formulas if formulas is not None else cargar_formulas()
    normalizado = _normalizar_titulo(titulo)
    mejor_nombre = SIN_CLASIFICAR
    mejor_puntos = 0
    for nombre, patrones in formulas:
        puntos = sum(1 for patron in patrones if patron.search(normalizado))
        if puntos > mejor_puntos:  # empate: gana la primera del archivo
            mejor_nombre, mejor_puntos = nombre, puntos
    return mejor_nombre


def recuento_formulas(metas: dict[str, dict], formulas, interes: str = "alto") -> dict[str, int]:
    """Recuento de formulas entre los videos con el interes indicado.

    Ordenado de mas a menos videos (desempate alfabetico), clasificando el
    titulo actual aunque el meta.json todavia no tenga formula_titulo.
    """
    recuento: dict[str, int] = {}
    for meta in metas.values():
        if (meta.get("senales") or {}).get("interes") != interes:
            continue
        formula = clasificar_titulo(meta.get("titulo") or "", formulas)
        recuento[formula] = recuento.get(formula, 0) + 1
    return dict(sorted(recuento.items(), key=lambda par: (-par[1], par[0])))


# ---------------------------------------------------------------------------
# Explorador
# ---------------------------------------------------------------------------

class Explorador:
    def __init__(self, raiz: Path, hoy: date | None = None, ejecutar_ytdlp=None):
        self.raiz = Path(raiz)
        self.hoy = hoy or date.today()
        self._ejecutar_ytdlp = ejecutar_ytdlp  # inyectable en pruebas
        self._llamadas_ytdlp: list[list[str]] = []

        self.ruta_config = self.raiz / "proyecto.config.json"
        base = self.raiz / "biblioteca" / "youtube"
        self.ruta_canales = base / "canales.md"
        self.dir_videos = base / "videos"
        self.ruta_mapa = base / "mapa-videos.md"
        self.dir_control = base / "control"
        self.ruta_metricas = self.dir_control / "metricas.jsonl"
        self.dir_ejecuciones = self.dir_control / "ejecuciones"
        self.dir_fichas_propias = self.raiz / "biblioteca" / "substack" / "fichas"
        self.ruta_esquema = (
            Path(__file__).resolve().parent.parent / "references" / "ficha-externa.schema.json"
        )
        self.ruta_formulas = RUTA_FORMULAS
        self._config: dict | None = None

    @property
    def formulas(self):
        return cargar_formulas(self.ruta_formulas)

    # -- infraestructura ------------------------------------------------------
    @property
    def config(self) -> dict:
        if self._config is None:
            if not self.ruta_config.is_file():
                raise ErrorEjecucion(
                    f"No existe {self.ruta_config}. Ejecuta antes el prompt 00 (crear estructura)."
                )
            self._config = json.loads(self.ruta_config.read_text(encoding="utf-8"))
        return self._config

    @property
    def cfg_youtube(self) -> dict:
        return self.config.get("youtube", {})

    def ytdlp(self, args: list[str]) -> tuple[int, str, str]:
        """Unica puerta de entrada a yt-dlp. Registra cada llamada."""
        if self._ejecutar_ytdlp is None:
            timeout = self.config.get("red", {}).get("timeout_segundos", 30)
            self._ejecutar_ytdlp = crear_ejecutor_real(timeout)
        self._llamadas_ytdlp.append(list(args))
        return self._ejecutar_ytdlp(list(args))

    def asegurar_ytdlp(self):
        """Falla con codigo 2 antes de tocar ningun dato si falta yt-dlp."""
        if self._ejecutar_ytdlp is None:
            timeout = self.config.get("red", {}).get("timeout_segundos", 30)
            self._ejecutar_ytdlp = crear_ejecutor_real(timeout)

    def ahora_utc(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def guardar_informe(self, comando: str, datos: dict) -> Path:
        run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        ruta = self.dir_ejecuciones / f"{run_id}.json"
        sufijo = 2
        while ruta.exists():
            ruta = self.dir_ejecuciones / f"{run_id}-{sufijo}.json"
            sufijo += 1
        informe = {
            "run_id": ruta.stem,
            "comando": comando,
            "fecha_utc": self.ahora_utc(),
            "llamadas_ytdlp": self._llamadas_ytdlp,
        }
        informe.update(datos)
        escribir_json_atomico(ruta, informe)
        return ruta

    # -- acceso a los videos ---------------------------------------------------
    def ruta_meta(self, video_id: str) -> Path:
        return self.dir_videos / video_id / "meta.json"

    def cargar_meta(self, video_id: str) -> dict | None:
        ruta = self.ruta_meta(video_id)
        if not ruta.is_file():
            return None
        return json.loads(ruta.read_text(encoding="utf-8"))

    def guardar_meta(self, meta: dict):
        escribir_json_atomico(self.ruta_meta(meta["id"]), meta)

    def cargar_metas(self) -> dict[str, dict]:
        metas: dict[str, dict] = {}
        if not self.dir_videos.is_dir():
            return metas
        for carpeta in sorted(self.dir_videos.iterdir()):
            ruta = carpeta / "meta.json"
            if not ruta.is_file():
                continue
            try:
                metas[carpeta.name] = json.loads(ruta.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                print(f"AVISO: meta.json ilegible, se ignora: {ruta} ({exc})", file=sys.stderr)
        return metas

    def ruta_transcripcion(self, video_id: str) -> Path:
        return self.dir_videos / video_id / "transcripcion.md"

    def ruta_ficha(self, video_id: str) -> Path:
        return self.dir_videos / video_id / "ficha.json"

    def huella_transcripcion(self, video_id: str) -> str | None:
        ruta = self.ruta_transcripcion(video_id)
        if not ruta.is_file():
            return None
        return hashlib.sha256(ruta.read_bytes()).hexdigest()

    def anotar_metrica(self, video_id: str, estadisticas: dict):
        linea = {"id": video_id, "fecha_captura": estadisticas.get("fecha_captura")}
        linea["visualizaciones"] = estadisticas.get("visualizaciones")
        for campo in ("likes", "comentarios"):
            if estadisticas.get(campo) is not None:
                linea[campo] = estadisticas[campo]
        self.ruta_metricas.parent.mkdir(parents=True, exist_ok=True)
        with self.ruta_metricas.open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(linea, ensure_ascii=False, sort_keys=True) + "\n")

    # -- senales ---------------------------------------------------------------
    def _dias(self, meta: dict) -> int | None:
        fecha = meta.get("fecha")
        if not fecha:
            return None
        try:
            return (self.hoy - date.fromisoformat(fecha)).days
        except ValueError:
            return None

    def recalcular_senales(self, metas: dict[str, dict] | None = None):
        """Recalcula las senales de todos los videos, canal por canal."""
        metas = metas if metas is not None else self.cargar_metas()
        minimo_largo = self.cfg_youtube.get("duracion_minima_segundos", 180)

        por_canal: dict[str, list[dict]] = {}
        for meta in metas.values():
            clave = meta.get("canal_url") or meta.get("canal") or ""
            por_canal.setdefault(clave, []).append(meta)

        for grupo in por_canal.values():
            # Primera pasada: datos por video.
            for meta in grupo:
                duracion = meta.get("duracion_segundos")
                dias = self._dias(meta)
                meta["_formato_largo"] = duracion is not None and duracion >= minimo_largo
                meta["_dias"] = dias
                meta["_incompleta"] = dias is None or dias < DIAS_SENAL_COMPLETA

            # Mediana del canal: formato largo, 7 dias o mas y con visualizaciones.
            pool = [
                m["estadisticas"]["visualizaciones"]
                for m in grupo
                if m["_formato_largo"]
                and not m["_incompleta"]
                and (m.get("estadisticas") or {}).get("visualizaciones") is not None
            ]
            mediana = statistics.median(pool) if pool else None
            poco_fiable = len(pool) < MINIMO_VIDEOS_MEDIANA

            for meta in grupo:
                visualizaciones = (meta.get("estadisticas") or {}).get("visualizaciones")
                multiplo = None
                if visualizaciones is not None and mediana:
                    multiplo = round(visualizaciones / mediana, 2)

                if meta["_incompleta"] or multiplo is None:
                    interes = "sin_datos"
                elif multiplo >= 2:
                    interes = "alto"
                elif multiplo >= 1:
                    interes = "medio"
                else:
                    interes = "bajo"

                likes = (meta.get("estadisticas") or {}).get("likes")
                comentarios = (meta.get("estadisticas") or {}).get("comentarios")
                interaccion = None
                interaccion_motivo = None
                if not meta.get("metadatos_completos"):
                    interaccion_motivo = "metadatos incompletos: solo listado plano"
                elif likes is None or comentarios is None:
                    interaccion_motivo = "likes ocultos o comentarios desactivados"
                elif visualizaciones:
                    interaccion = round((likes + comentarios) / visualizaciones, 4)
                else:
                    interaccion_motivo = "sin visualizaciones registradas"

                meta["formula_titulo"] = clasificar_titulo(
                    meta.get("titulo") or "", self.formulas
                )
                meta["senales"] = {
                    "formato_largo": meta["_formato_largo"],
                    "dias": meta["_dias"],
                    "senal_incompleta": meta["_incompleta"],
                    "mediana_canal": mediana,
                    "mediana_poco_fiable": poco_fiable,
                    "multiplo_mediana": multiplo,
                    "interes": interes,
                    "interaccion": interaccion,
                    "interaccion_motivo": interaccion_motivo,
                }
                for temporal in ("_formato_largo", "_dias", "_incompleta"):
                    meta.pop(temporal, None)
                self.guardar_meta(meta)

    def en_ventana(self, meta: dict) -> bool:
        dias = (meta.get("senales") or {}).get("dias")
        return dias is not None and dias <= self.cfg_youtube.get("ventana_dias", 60)

    # -- temas existentes -------------------------------------------------------
    def temas_existentes(self, metas: dict[str, dict] | None = None) -> list[str]:
        """Temas de las fichas propias, las fichas externas y las relevancias."""
        temas: set[str] = set()
        if self.dir_fichas_propias.is_dir():
            for ruta in self.dir_fichas_propias.glob("*.json"):
                try:
                    tema = json.loads(ruta.read_text(encoding="utf-8")).get("tema")
                except (json.JSONDecodeError, UnicodeDecodeError):
                    continue
                if tema:
                    temas.add(tema)
        metas = metas if metas is not None else self.cargar_metas()
        for video_id, meta in metas.items():
            tema = (meta.get("relevancia") or {}).get("tema")
            if tema:
                temas.add(tema)
            ruta_ficha = self.ruta_ficha(video_id)
            if ruta_ficha.is_file():
                try:
                    tema_ficha = json.loads(ruta_ficha.read_text(encoding="utf-8")).get("tema")
                except (json.JSONDecodeError, UnicodeDecodeError):
                    continue
                if tema_ficha:
                    temas.add(tema_ficha)
        return sorted(temas, key=str.casefold)

    def subtemas_existentes(self, metas: dict[str, dict] | None = None) -> dict[str, int]:
        """Subtemas de las fichas propias y de las fichas de video guardadas,
        con su frecuencia, ordenados de mas a menos usados (desempate
        alfabetico). Sirven para que el modelo reutilice el vocabulario de la
        biblioteca al rellenar fichas nuevas."""
        recuento: dict[str, int] = {}

        def sumar(ruta: Path):
            try:
                subtemas = json.loads(ruta.read_text(encoding="utf-8")).get("subtemas") or []
            except (json.JSONDecodeError, UnicodeDecodeError):
                return
            for subtema in subtemas:
                if isinstance(subtema, str) and subtema.strip():
                    limpio = subtema.strip()
                    recuento[limpio] = recuento.get(limpio, 0) + 1

        if self.dir_fichas_propias.is_dir():
            for ruta in sorted(self.dir_fichas_propias.glob("*.json")):
                sumar(ruta)
        metas = metas if metas is not None else self.cargar_metas()
        for video_id in sorted(metas):
            ruta_ficha = self.ruta_ficha(video_id)
            if ruta_ficha.is_file():
                sumar(ruta_ficha)
        return dict(sorted(recuento.items(), key=lambda par: (-par[1], par[0].casefold())))

    # -- comando: recoger --------------------------------------------------------
    def cmd_recoger(self) -> int:
        self.asegurar_ytdlp()
        if not self.ruta_canales.is_file():
            raise ErrorEjecucion(
                f"No existe {self.ruta_canales}. Ejecuta antes el prompt 00 (crear estructura)."
            )
        canales, errores_url = leer_canales(self.ruta_canales.read_text(encoding="utf-8"))
        if not canales and not errores_url:
            raise ErrorEjecucion(f"No hay ningun canal en {self.ruta_canales}.")

        n_videos = self.cfg_youtube.get("videos_por_canal", 30)
        fallidos = list(errores_url)
        correctos: list[str] = []
        nuevos: list[str] = []
        actualizados: list[str] = []

        for url_canal in canales:
            codigo, salida, error = self.ytdlp([
                "--flat-playlist",
                "-J",
                "--extractor-args",
                "youtubetab:approximate_date",
                "--playlist-end",
                str(n_videos),
                f"{url_canal}/videos",
            ])
            if codigo != 0:
                fallidos.append({
                    "url": url_canal,
                    "motivo": (error.strip().splitlines() or [f"yt-dlp devolvio codigo {codigo}"])[-1],
                })
                continue
            try:
                datos = json.loads(salida)
            except json.JSONDecodeError as exc:
                fallidos.append({"url": url_canal, "motivo": f"respuesta no es JSON: {exc}"})
                continue

            canal_nombre = (
                datos.get("channel") or datos.get("uploader") or datos.get("title") or url_canal
            )
            entradas = [e for e in (datos.get("entries") or []) if e and e.get("id")]
            for entrada in entradas[:n_videos]:
                video_id = str(entrada["id"])
                captura = {
                    "fecha_captura": self.ahora_utc(),
                    "visualizaciones": entrada.get("view_count"),
                    "likes": None,
                    "comentarios": None,
                }
                meta = self.cargar_meta(video_id)
                if meta is None:
                    fecha_bruta = entrada.get("upload_date")
                    fecha = None
                    if fecha_bruta and re.fullmatch(r"\d{8}", str(fecha_bruta)):
                        fecha = f"{fecha_bruta[:4]}-{fecha_bruta[4:6]}-{fecha_bruta[6:]}"
                    elif entrada.get("timestamp"):
                        # Algunas versiones de yt-dlp dan la fecha aproximada
                        # del listado plano como epoch en "timestamp".
                        try:
                            fecha = datetime.fromtimestamp(
                                int(entrada["timestamp"]), timezone.utc
                            ).strftime("%Y-%m-%d")
                        except (ValueError, OSError, OverflowError):
                            fecha = None
                    meta = {
                        "id": video_id,
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                        "canal": canal_nombre,
                        "canal_url": url_canal,
                        "titulo": entrada.get("title") or "",
                        "duracion_segundos": entrada.get("duration"),
                        "fecha": fecha,
                        "fecha_precision": "aproximada" if fecha else "desconocida",
                        "metadatos_completos": False,
                        "estadisticas": captura,
                    }
                    nuevos.append(video_id)
                else:
                    # Solo estadisticas y senales; relevancia, transcripcion y
                    # ficha no se tocan. Las senales se recalculan al final.
                    meta["estadisticas"] = captura
                    if meta.get("duracion_segundos") is None:
                        meta["duracion_segundos"] = entrada.get("duration")
                    actualizados.append(video_id)
                self.guardar_meta(meta)
                self.anotar_metrica(video_id, captura)
            correctos.append(url_canal)

        self.recalcular_senales()

        informe = {
            "canales": {
                "pedidos": canales + [e["url"] for e in errores_url],
                "correctos": correctos,
                "fallidos": fallidos,
            },
            "videos_nuevos": nuevos,
            "videos_actualizados": actualizados,
        }
        ruta_informe = self.guardar_informe("recoger", informe)

        print(json.dumps(informe | {"informe": str(ruta_informe)}, ensure_ascii=False, indent=2))
        if fallidos:
            print(
                f"ADVERTENCIA: {len(fallidos)} canal(es) con error; sus datos anteriores se conservan.",
                file=sys.stderr,
            )
            return 1
        return 0

    # -- comando: relevancia-pendiente --------------------------------------------
    def cmd_relevancia_pendiente(self) -> int:
        metas = self.cargar_metas()
        pendientes = []
        for video_id, meta in sorted(metas.items()):
            senales = meta.get("senales") or {}
            if not senales.get("formato_largo"):
                continue
            if not self.en_ventana(meta):
                continue
            if meta.get("relevancia"):
                continue
            video = {"id": video_id, "canal": meta.get("canal", ""), "titulo": meta.get("titulo", "")}
            descripcion = meta.get("descripcion")
            if descripcion:
                video["descripcion"] = descripcion[:MAX_DESCRIPCION_RELEVANCIA]
            pendientes.append(video)

        resultado = {
            "videos": pendientes,
            "linea_editorial": self.config.get("linea_editorial", {}),
            "recursos": self.config.get("recursos", {}),
            "temas_existentes": self.temas_existentes(metas),
        }
        if not pendientes:
            resultado["mensaje"] = "No hay videos pendientes de clasificar."
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        return 0

    # -- comando: guardar-relevancia ------------------------------------------------
    def cmd_guardar_relevancia(self, ruta_json: Path) -> int:
        ruta_json = Path(ruta_json)
        if not ruta_json.is_file():
            print(f"No existe el archivo JSON del modelo: {ruta_json}", file=sys.stderr)
            return 1
        try:
            clasificaciones = json.loads(ruta_json.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            print(f"El JSON del modelo es ilegible: {exc}", file=sys.stderr)
            return 1
        if not isinstance(clasificaciones, list):
            print("El JSON del modelo debe ser una lista de clasificaciones.", file=sys.stderr)
            return 1

        metas = self.cargar_metas()
        errores: list[str] = []
        for i, item in enumerate(clasificaciones):
            donde = f"clasificacion[{i}]"
            if not isinstance(item, dict):
                errores.append(f"{donde}: debe ser un objeto")
                continue
            video_id = item.get("id")
            if not video_id or str(video_id) not in metas:
                errores.append(f"{donde}: el id {video_id!r} no existe en biblioteca/youtube/videos")
            if not isinstance(item.get("relevante"), bool):
                errores.append(f"{donde}: 'relevante' debe ser true o false")
            if not str(item.get("motivo") or "").strip():
                errores.append(f"{donde}: falta el 'motivo'")
            if item.get("relevante") is True and not str(item.get("tema") or "").strip():
                errores.append(f"{donde}: un video relevante necesita 'tema'")

        if errores:
            print("Clasificaciones no validas; no se escribe nada:", file=sys.stderr)
            for error in errores:
                print(f"  - {error}", file=sys.stderr)
            return 1

        guardadas: list[str] = []
        omitidas: list[str] = []
        for item in clasificaciones:
            video_id = str(item["id"])
            meta = metas[video_id]
            if meta.get("relevancia"):
                omitidas.append(video_id)  # un video ya clasificado no se repite
                continue
            meta["relevancia"] = {
                "relevante": item["relevante"],
                "tema": str(item.get("tema") or "").strip() or None,
                "motivo": str(item["motivo"]).strip(),
                "fecha": self.ahora_utc(),
            }
            self.guardar_meta(meta)
            guardadas.append(video_id)

        informe = {"relevancias_guardadas": guardadas, "relevancias_omitidas_ya_clasificadas": omitidas}
        self.guardar_informe("guardar-relevancia", informe)
        print(json.dumps(informe, ensure_ascii=False, indent=2))
        return 0

    # -- comando: candidatos -----------------------------------------------------
    def cmd_candidatos(self) -> int:
        self.asegurar_ytdlp()
        metas = self.cargar_metas()

        # Canales por tema, contando solo videos relevantes.
        canales_por_tema: dict[str, set[str]] = {}
        for meta in metas.values():
            relevancia = meta.get("relevancia") or {}
            if relevancia.get("relevante") and relevancia.get("tema"):
                canales_por_tema.setdefault(relevancia["tema"], set()).add(
                    meta.get("canal_url") or meta.get("canal") or ""
                )

        rango_interes = {"alto": 3, "medio": 2, "bajo": 1, "sin_datos": 0}
        elegibles: list[dict] = []
        for video_id, meta in metas.items():
            relevancia = meta.get("relevancia") or {}
            senales = meta.get("senales") or {}
            if not relevancia.get("relevante"):
                continue
            if not senales.get("formato_largo"):
                continue
            if not self.en_ventana(meta):
                continue
            if self.ruta_ficha(video_id).is_file():
                continue
            tema = relevancia.get("tema")
            n_canales = len(canales_por_tema.get(tema, set())) if tema else 0
            interes = senales.get("interes", "sin_datos")
            motivos = []
            if interes in ("medio", "alto"):
                motivos.append(f"interes {interes}")
            if n_canales >= 2:
                motivos.append(f"tema '{tema}' en {n_canales} canales")
            if not motivos:
                continue
            elegibles.append({
                "id": video_id,
                "meta": meta,
                "interes": interes,
                "n_canales_tema": n_canales,
                "multiplo": senales.get("multiplo_mediana"),
                "motivo": " y ".join(motivos),
            })

        elegibles.sort(
            key=lambda c: (
                -rango_interes.get(c["interes"], 0),
                -c["n_canales_tema"],
                -(c["multiplo"] if c["multiplo"] is not None else float("-inf")),
                c["id"],
            )
        )
        limite = self.cfg_youtube.get("candidatos_por_ejecucion", 10)
        seleccion = elegibles[:limite]

        # Completar metadatos de cada candidato con yt-dlp -J.
        errores: list[dict] = []
        candidatos_informe: list[dict] = []
        for candidato in seleccion:
            meta = candidato["meta"]
            codigo, salida, error = self.ytdlp(["-J", meta["url"]])
            if codigo != 0:
                errores.append({
                    "id": candidato["id"],
                    "motivo": (error.strip().splitlines() or [f"yt-dlp devolvio codigo {codigo}"])[-1],
                })
            else:
                try:
                    datos = json.loads(salida)
                except json.JSONDecodeError as exc:
                    datos = None
                    errores.append({"id": candidato["id"], "motivo": f"respuesta no es JSON: {exc}"})
                if datos:
                    fecha_bruta = str(datos.get("upload_date") or "")
                    if re.fullmatch(r"\d{8}", fecha_bruta):
                        meta["fecha"] = f"{fecha_bruta[:4]}-{fecha_bruta[4:6]}-{fecha_bruta[6:]}"
                        meta["fecha_precision"] = "exacta"
                    if datos.get("description") is not None:
                        meta["descripcion"] = datos["description"]
                    if datos.get("duration") is not None:
                        meta["duracion_segundos"] = datos["duration"]
                    captura = {
                        "fecha_captura": self.ahora_utc(),
                        "visualizaciones": datos.get("view_count"),
                        "likes": datos.get("like_count"),
                        "comentarios": datos.get("comment_count"),
                    }
                    meta["estadisticas"] = captura
                    meta["metadatos_completos"] = True
                    self.guardar_meta(meta)
                    self.anotar_metrica(candidato["id"], captura)

        # Recalcular dias, interaccion y el resto de senales con los datos nuevos.
        metas = self.cargar_metas()
        self.recalcular_senales(metas)
        metas = self.cargar_metas()

        for candidato in seleccion:
            meta = metas[candidato["id"]]
            candidatos_informe.append({
                "id": candidato["id"],
                "canal": meta.get("canal", ""),
                "titulo": meta.get("titulo", ""),
                "url": meta.get("url", ""),
                "tema": (meta.get("relevancia") or {}).get("tema"),
                "formula_titulo": meta.get("formula_titulo")
                or clasificar_titulo(meta.get("titulo") or "", self.formulas),
                "motivo": candidato["motivo"],
                "senales": meta.get("senales"),
            })

        informe = {
            "candidatos": candidatos_informe,
            "elegibles_totales": len(elegibles),
            "limite": limite,
            # Que patron de titulo domina en el nicho entre los videos con
            # interes alto de esta ejecucion. Clasifica las palabras del
            # titulo, no el porque real del exito (ver formulas-titulo.json).
            "formulas_dominantes_interes_alto": recuento_formulas(metas, self.formulas),
            "errores_metadatos": errores,
        }
        ruta_informe = self.guardar_informe("candidatos", informe)
        print(json.dumps(informe | {"informe": str(ruta_informe)}, ensure_ascii=False, indent=2))
        return 1 if errores else 0

    # -- comando: subtitulos -------------------------------------------------------
    def _descargar_vtt(self, meta: dict, automaticos: bool) -> tuple[int, str]:
        idiomas = self.cfg_youtube.get("idiomas_subtitulos", ["es", "en"])
        carpeta = self.dir_videos / meta["id"]
        carpeta.mkdir(parents=True, exist_ok=True)
        modo = "--write-auto-subs" if automaticos else "--write-subs"
        args = [
            "--skip-download",
            modo,
            "--sub-langs",
            ",".join(idiomas),
            "--paths",
            str(carpeta),
            "-o",
            "subtitulos.%(ext)s",
            meta["url"],
        ]
        # YouTube limita las descargas de subtitulos en rafaga (HTTP 429):
        # se reintenta con pausa creciente segun la configuracion de red.
        cfg_red = self.config.get("red", {})
        intentos = max(1, int(cfg_red.get("intentos", 3)))
        pausa = float(cfg_red.get("pausa_segundos", 0.5))
        codigo, error = 1, ""
        for intento in range(1, intentos + 1):
            codigo, error = self.ytdlp(args)[:2]
            if codigo == 0 or "429" not in error:
                break
            if intento < intentos:
                time.sleep(pausa * (2 ** intento) * 10)
        return codigo, error

    def _descargar_vtt_alternativo(self, meta: dict) -> tuple[str, str] | None:
        """Via alternativa cuando yt-dlp falla (p. ej. HTTP 429): descarga la
        transcripcion con youtube-transcript-api, que usa otro endpoint, y la
        guarda como VTT en la carpeta del video. Devuelve (idioma, origen) o
        None si tampoco esta disponible."""
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
        except ImportError:
            return None
        idiomas = self.cfg_youtube.get("idiomas_subtitulos", ["es", "en"])
        try:
            api = YouTubeTranscriptApi()
            lista = api.list(meta["id"])
            elegido = None
            for manual in (True, False):  # manuales primero, automaticos despues
                for idioma in idiomas:
                    for t in lista:
                        if t.is_generated != (not manual):
                            continue
                        if t.language_code == idioma or t.language_code.startswith(idioma + "-"):
                            elegido = (t, "manuales" if manual else "automaticos")
                            break
                    if elegido:
                        break
                if elegido:
                    break
            if not elegido:
                return None
            transcripcion, origen = elegido
            datos = transcripcion.fetch()
        except Exception:
            return None

        def marca(segundos: float) -> str:
            h = int(segundos // 3600)
            m = int(segundos % 3600 // 60)
            s = segundos % 60
            return f"{h:02d}:{m:02d}:{s:06.3f}"

        lineas = ["WEBVTT", ""]
        for snippet in datos.snippets:
            inicio = snippet.start
            fin = inicio + (snippet.duration or 0)
            lineas.append(f"{marca(inicio)} --> {marca(fin)}")
            lineas.append(snippet.text.replace("\n", " "))
            lineas.append("")
        idioma = datos.language_code
        carpeta = self.dir_videos / meta["id"]
        carpeta.mkdir(parents=True, exist_ok=True)
        escribir_atomico(carpeta / f"subtitulos.{idioma}.vtt", "\n".join(lineas))
        return idioma, origen

    def _elegir_vtt(self, video_id: str) -> tuple[Path, str] | None:
        carpeta = self.dir_videos / video_id
        disponibles: dict[str, Path] = {}
        for ruta in carpeta.glob("subtitulos.*.vtt"):
            idioma = ruta.name[len("subtitulos."):-len(".vtt")]
            disponibles[idioma] = ruta
        for idioma in self.cfg_youtube.get("idiomas_subtitulos", ["es", "en"]):
            for disponible, ruta in sorted(disponibles.items()):
                if disponible == idioma or disponible.startswith(idioma + "-"):
                    return ruta, disponible
        return None

    def cmd_subtitulos(self, video_ids: list[str]) -> int:
        self.asegurar_ytdlp()
        obtenidos: list[dict] = []
        no_disponibles: list[dict] = []
        errores: list[dict] = []
        omitidos: list[str] = []

        for video_id in video_ids:
            meta = self.cargar_meta(video_id)
            if meta is None:
                errores.append({"id": video_id, "motivo": "no existe en biblioteca/youtube/videos"})
                continue
            if self.ruta_transcripcion(video_id).is_file():
                omitidos.append(video_id)  # ya tiene transcripcion; no se repite
                continue

            eleccion = None
            origen = None
            fallo = None
            for automaticos in (False, True):  # manuales primero, automaticos despues
                codigo, error = self._descargar_vtt(meta, automaticos)
                if codigo != 0:
                    fallo = (error.strip().splitlines() or [f"yt-dlp devolvio codigo {codigo}"])[-1]
                    break
                eleccion = self._elegir_vtt(video_id)
                if eleccion:
                    origen = "automaticos" if automaticos else "manuales"
                    break
            if fallo:
                # Via alternativa: otro endpoint que suele esquivar los
                # limites de descarga (HTTP 429) del que usa yt-dlp.
                alternativo = self._descargar_vtt_alternativo(meta)
                if alternativo:
                    eleccion = self._elegir_vtt(video_id)
                    origen = alternativo[1]
                    fallo = None
                if fallo:
                    errores.append({"id": video_id, "motivo": fallo})
                    continue

            if not eleccion:
                idiomas = ", ".join(self.cfg_youtube.get("idiomas_subtitulos", ["es", "en"]))
                meta["subtitulos"] = {
                    "disponibles": False,
                    "motivo": f"sin subtitulos manuales ni automaticos en {idiomas}",
                    "fecha": self.ahora_utc(),
                }
                self.guardar_meta(meta)
                no_disponibles.append({"id": video_id, "motivo": meta["subtitulos"]["motivo"]})
                continue

            ruta_vtt, idioma = eleccion
            transcripcion = limpiar_vtt(ruta_vtt.read_text(encoding="utf-8"))
            if not transcripcion.strip():
                meta["subtitulos"] = {
                    "disponibles": False,
                    "motivo": f"el VTT ({idioma}) no contiene texto",
                    "fecha": self.ahora_utc(),
                }
                self.guardar_meta(meta)
                no_disponibles.append({"id": video_id, "motivo": meta["subtitulos"]["motivo"]})
                continue

            escribir_atomico(self.ruta_transcripcion(video_id), transcripcion)
            meta["subtitulos"] = {
                "disponibles": True,
                "idioma": idioma,
                "origen": origen,
                "archivo": ruta_vtt.name,
                "fecha": self.ahora_utc(),
            }
            self.guardar_meta(meta)
            obtenidos.append({"id": video_id, "idioma": idioma, "origen": origen})

        informe = {
            "subtitulos_obtenidos": obtenidos,
            "subtitulos_no_disponibles": no_disponibles,
            "omitidos_con_transcripcion": omitidos,
            "errores": errores,
        }
        ruta_informe = self.guardar_informe("subtitulos", informe)
        print(json.dumps(informe | {"informe": str(ruta_informe)}, ensure_ascii=False, indent=2))
        return 1 if errores else 0

    # -- comando: pendientes-ficha ----------------------------------------------
    def cmd_pendientes_ficha(self) -> int:
        metas = self.cargar_metas()
        pendientes = []
        for video_id, meta in sorted(metas.items()):
            huella = self.huella_transcripcion(video_id)
            if huella is None:
                continue
            ruta_ficha = self.ruta_ficha(video_id)
            if not ruta_ficha.is_file():
                motivo = "sin ficha"
            else:
                try:
                    ficha = json.loads(ruta_ficha.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    ficha = {}
                if ficha.get("huella") == huella:
                    continue
                motivo = "huella distinta: la transcripcion cambio despues de la ficha"
            pendientes.append({
                "id": video_id,
                "canal": meta.get("canal", ""),
                "titulo": meta.get("titulo", ""),
                "tema": (meta.get("relevancia") or {}).get("tema"),
                "transcripcion": str(self.ruta_transcripcion(video_id)),
                "motivo": motivo,
            })
        resultado = {
            "pendientes": pendientes,
            # Vocabulario de la biblioteca (fichas propias y fichas de video
            # guardadas) con frecuencias, para que el modelo reutilice los
            # subtemas en lugar de inventar sinonimos.
            "subtemas_existentes": self.subtemas_existentes(metas),
        }
        if not pendientes:
            resultado["mensaje"] = "No hay fichas pendientes: todas estan al dia."
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        return 0

    # -- comando: guardar-ficha ----------------------------------------------------
    def cmd_guardar_ficha(self, video_id: str, ruta_json: Path) -> int:
        meta = self.cargar_meta(video_id)
        if meta is None:
            print(f"El id {video_id!r} no existe en biblioteca/youtube/videos; no se escribe nada.", file=sys.stderr)
            return 1
        huella = self.huella_transcripcion(video_id)
        if huella is None:
            print(
                f"El video {video_id} no tiene transcripcion.md; la ficha necesita su huella. "
                "Ejecuta antes el comando subtitulos.",
                file=sys.stderr,
            )
            return 1

        ruta_json = Path(ruta_json)
        if not ruta_json.is_file():
            print(f"No existe el archivo JSON del modelo: {ruta_json}", file=sys.stderr)
            return 1
        try:
            juicio = json.loads(ruta_json.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            print(f"El JSON del modelo es ilegible: {exc}", file=sys.stderr)
            return 1
        if not isinstance(juicio, dict):
            print("El JSON del modelo debe ser un objeto.", file=sys.stderr)
            return 1

        ignorados = sorted(set(juicio) & set(CAMPOS_OBJETIVOS_FICHA))
        senales = meta.get("senales") or {}
        ficha = {campo: juicio[campo] for campo in CAMPOS_JUICIO_FICHA if campo in juicio}
        ficha.update({
            "id": str(meta["id"]),
            "fuente": "youtube",
            "url": meta.get("url", ""),
            "autor": meta.get("canal", ""),
            "fecha": meta.get("fecha"),
            "huella": huella,
            "senales": {
                "multiplo_mediana": senales.get("multiplo_mediana"),
                "interaccion": senales.get("interaccion"),
                "dias": senales.get("dias"),
            },
        })

        esquema = json.loads(self.ruta_esquema.read_text(encoding="utf-8"))
        errores = validar_contra_esquema(ficha, esquema)
        if errores:
            print("Ficha invalida; no se escribe nada:", file=sys.stderr)
            for error in errores:
                print(f"  - {error}", file=sys.stderr)
            return 1

        escribir_json_atomico(self.ruta_ficha(video_id), ficha)
        self.guardar_informe("guardar-ficha", {"fichas_guardadas": [video_id]})
        mensaje = f"Ficha guardada en biblioteca/youtube/videos/{video_id}/ficha.json"
        if ignorados:
            mensaje += f" (campos objetivos del JSON del modelo ignorados: {', '.join(ignorados)})"
        print(mensaje)
        return 0

    # -- comando: clasificar-titulos --------------------------------------------
    def cmd_clasificar_titulos(self) -> int:
        """Reprocesa los meta.json existentes y guarda su formula de titulo.

        Comando ligero: no llama a yt-dlp ni toca estadisticas, senales,
        relevancia, transcripciones ni fichas. Sirve para clasificar videos
        recogidos antes de que existiera el clasificador o tras cambiar
        references/formulas-titulo.json.
        """
        metas = self.cargar_metas()
        clasificados = 0
        cambiados: list[str] = []
        for video_id, meta in sorted(metas.items()):
            formula = clasificar_titulo(meta.get("titulo") or "", self.formulas)
            if meta.get("formula_titulo") != formula:
                meta["formula_titulo"] = formula
                self.guardar_meta(meta)
                cambiados.append(video_id)
            clasificados += 1

        informe = {
            "videos_clasificados": clasificados,
            "videos_actualizados": cambiados,
            "formulas_dominantes_interes_alto": recuento_formulas(metas, self.formulas),
        }
        self.guardar_informe("clasificar-titulos", informe)
        print(json.dumps(informe, ensure_ascii=False, indent=2))
        return 0

    # -- comando: mapa --------------------------------------------------------------
    def cargar_fichas(self, metas: dict[str, dict]) -> dict[str, dict]:
        """Fichas al dia: su huella coincide con la transcripcion actual."""
        fichas: dict[str, dict] = {}
        for video_id in metas:
            ruta = self.ruta_ficha(video_id)
            if not ruta.is_file():
                continue
            try:
                ficha = json.loads(ruta.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                print(f"AVISO: ficha.json ilegible, se ignora: {ruta} ({exc})", file=sys.stderr)
                continue
            if ficha.get("huella") != self.huella_transcripcion(video_id):
                continue
            fichas[video_id] = ficha
        return fichas

    def generar_mapa(self) -> str:
        """Regenera mapa-videos.md a partir de las fichas y sus meta.json.

        Vista legible por humanos de lo que han capturado las fichas de video.
        Determinista: los mismos datos producen el mismo archivo.
        """
        metas = self.cargar_metas()
        fichas = self.cargar_fichas(metas)

        def orden_video(video_id: str):
            return (metas.get(video_id, {}).get("fecha") or "", video_id)

        # Candidatos sin ficha todavia: con transcripcion pendiente de ficha
        # (o ficha desactualizada) o marcados sin subtitulos.
        pendientes: list[tuple[str, str]] = []  # (video_id, motivo)
        for video_id, meta in metas.items():
            if video_id in fichas:
                continue
            if self.ruta_transcripcion(video_id).is_file():
                if self.ruta_ficha(video_id).is_file():
                    pendientes.append((video_id, "la transcripcion cambio despues de la ficha"))
                else:
                    pendientes.append((video_id, "con transcripcion, ficha pendiente"))
            elif (meta.get("subtitulos") or {}).get("disponibles") is False:
                motivo = (meta["subtitulos"].get("motivo") or "sin subtitulos").strip()
                pendientes.append((video_id, motivo))
        pendientes.sort(key=lambda p: orden_video(p[0]))

        temas: dict[str, list[str]] = {}
        for video_id, ficha in fichas.items():
            temas.setdefault(ficha.get("tema") or "(sin tema)", []).append(video_id)

        lineas = [
            "# Mapa de videos de YouTube",
            "",
            f"Generado el {self.hoy.isoformat()} a partir de {len(fichas)} ficha(s). "
            f"Videos recogidos sin ficha: {len(metas) - len(fichas)}.",
            "",
            "## Temas",
            "",
        ]
        if not temas:
            lineas.append("No hay fichas todavia.")
            lineas.append("")

        for tema in sorted(temas, key=str.casefold):
            ids = sorted(temas[tema], key=orden_video)
            canales = sorted(
                {metas[i].get("canal") or fichas[i].get("autor") or "" for i in ids} - {""},
                key=str.casefold,
            )
            lineas.append(f"### {tema}")
            lineas.append("")
            lineas.append(f"- Videos: {len(ids)}")
            if canales:
                lineas.append(f"- Canales: {', '.join(canales)}")
            lineas.append("")
            for video_id in ids:
                meta = metas[video_id]
                ficha = fichas[video_id]
                senales = meta.get("senales") or {}
                partes = []
                if senales.get("multiplo_mediana") is not None:
                    partes.append(f"x{senales['multiplo_mediana']} de la mediana")
                if senales.get("interes"):
                    partes.append(f"interes {senales['interes']}")
                if senales.get("dias") is not None:
                    partes.append(f"{senales['dias']} dias")
                partes.append(
                    "formula: "
                    + clasificar_titulo(meta.get("titulo") or "", self.formulas)
                )
                titulo = meta.get("titulo") or video_id
                canal = meta.get("canal") or ficha.get("autor") or ""
                cabecera = f"- **{meta.get('fecha') or 'sin fecha'}** — [{titulo}]({meta.get('url', '')})"
                if canal:
                    cabecera += f" — {canal}"
                if partes:
                    cabecera += f" ({' · '.join(partes)})"
                lineas.append(cabecera)
                lineas.append(f"  - Tesis: {(ficha.get('tesis') or '').strip() or '(sin tesis)'}")
                demuestra = (ficha.get("demuestra") or "").strip()
                lineas.append(f"  - Demuestra: {demuestra or '(nada demostrado en pantalla)'}")
                promete = (ficha.get("promete_sin_demostrar") or "").strip()
                lineas.append(f"  - Promete sin demostrar: {promete or '(nada)'}")
                preguntas = [p.strip() for p in ficha.get("preguntas_abiertas") or [] if p.strip()]
                if preguntas:
                    lineas.append("  - Preguntas abiertas:")
                    lineas.extend(f"    - {p}" for p in preguntas)
            lineas.append("")

        # Formulas de titulo dominantes entre los videos de interes alto.
        # Clasifican las palabras del titulo, no el porque real del exito.
        recuento = recuento_formulas(metas, self.formulas)
        lineas.append("## Formulas dominantes entre los videos de interes alto")
        lineas.append("")
        if recuento:
            total = sum(recuento.values())
            lineas.append(
                f"Sobre {total} video(s) con interes alto. La formula clasifica las "
                "palabras del titulo, no el porque real del exito del video."
            )
            lineas.append("")
            for formula, cuantos in recuento.items():
                lineas.append(f"- {formula}: {cuantos}")
        else:
            lineas.append("No hay videos con interes alto todavia.")
        lineas.append("")

        if pendientes:
            lineas.append("## Videos candidatos sin ficha todavia (el mapa NO esta completo)")
            lineas.append("")
            for video_id, motivo in pendientes:
                meta = metas[video_id]
                lineas.append(
                    f"- {meta.get('fecha') or 'sin fecha'} — "
                    f"[{meta.get('titulo') or video_id}]({meta.get('url', '')}) — "
                    f"{meta.get('canal', '')} ({motivo})"
                )
            lineas.append("")
        else:
            lineas.append("## Cobertura")
            lineas.append("")
            lineas.append("Todos los videos candidatos tienen ficha al dia.")
            lineas.append("")

        contenido = "\n".join(lineas)
        escribir_atomico(self.ruta_mapa, contenido)
        return contenido

    def cmd_mapa(self) -> int:
        self.generar_mapa()
        print(f"Mapa regenerado en {self.ruta_mapa}")
        return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Explora canales de YouTube y mantiene biblioteca/youtube/."
    )
    parser.add_argument(
        "comando",
        choices=[
            "recoger",
            "relevancia-pendiente",
            "guardar-relevancia",
            "candidatos",
            "subtitulos",
            "pendientes-ficha",
            "guardar-ficha",
            "clasificar-titulos",
            "mapa",
        ],
    )
    parser.add_argument("resto", nargs="*", help="Argumentos del comando")
    parser.add_argument("--raiz", default=".", help="Raiz del proyecto (contiene biblioteca/)")
    parser.add_argument("--hoy", default=None, help="Fecha YYYY-MM-DD para calculos de fecha (pruebas)")
    args = parser.parse_args(argv)

    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    hoy = date.fromisoformat(args.hoy) if args.hoy else None
    explorador = Explorador(Path(args.raiz), hoy=hoy)

    try:
        if args.comando == "recoger":
            return explorador.cmd_recoger()
        if args.comando == "relevancia-pendiente":
            return explorador.cmd_relevancia_pendiente()
        if args.comando == "guardar-relevancia":
            if len(args.resto) != 1:
                print("Uso: guardar-relevancia <archivo.json>", file=sys.stderr)
                return 2
            return explorador.cmd_guardar_relevancia(Path(args.resto[0]))
        if args.comando == "candidatos":
            return explorador.cmd_candidatos()
        if args.comando == "subtitulos":
            if not args.resto:
                print("Uso: subtitulos <video_id>...", file=sys.stderr)
                return 2
            return explorador.cmd_subtitulos(args.resto)
        if args.comando == "pendientes-ficha":
            return explorador.cmd_pendientes_ficha()
        if args.comando == "guardar-ficha":
            if len(args.resto) != 2:
                print("Uso: guardar-ficha <video_id> <archivo.json>", file=sys.stderr)
                return 2
            return explorador.cmd_guardar_ficha(args.resto[0], Path(args.resto[1]))
        if args.comando == "clasificar-titulos":
            return explorador.cmd_clasificar_titulos()
        if args.comando == "mapa":
            return explorador.cmd_mapa()
    except ErrorEjecucion as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    return 2  # inalcanzable


if __name__ == "__main__":
    sys.exit(main())
