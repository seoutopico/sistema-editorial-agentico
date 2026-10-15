#!/usr/bin/env python3
"""Cruza las fichas externas con las fichas propias y las decisiones anteriores
y gestiona el ciclo de vida de las oportunidades.

Parte "script" de la skill detectar-oportunidades (fase 2 de ARQUITECTURA.md).
El modelo solo aporta juicio (leer los artículos parecidos, decidir cobertura y
aportación, redactar la propuesta); este script hace todo lo repetible:
agrupar fichas, calcular señales, buscar parecidos con BM25, aplicar las
cuatro condiciones de la sección 8.4 y guardar con escrituras atómicas.

Comandos:
  agrupar                                   agrupa fichas externas y escribe control/grupos.json
  pendientes                                paquetes JSON de los grupos que necesitan evaluación
  guardar-evaluacion <archivo.json>         valida el juicio del modelo y aplica las 4 condiciones
  guardar-oportunidad <grupo_id> <archivo.md>   crea la oportunidad (encabezado del script + cuerpo del modelo)
  guardar-oportunidad <grupo_id> --actualizar <oportunidad_id>   añade evidencias nuevas
  indice                                    regenera biblioteca/oportunidades/INDICE.md (con calendario sugerido)

Códigos de salida:
  0  correcto
  1  errores parciales (p. ej. una ficha no válida que se omite y se informa)
  2  no pudo ejecutarse
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
import tempfile
import unicodedata
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

CODIGO_OK = 0
CODIGO_PARCIAL = 1
CODIGO_FATAL = 2

SECCIONES_OPORTUNIDAD = [
    "## La oportunidad",
    "## Por qué ahora (evidencias)",
    "## Qué hemos publicado y qué falta",
    "## Qué aportaríamos",
    "## Qué hay que investigar o probar",
    "## Riesgos",
]

ORDEN_INTERES = {"alto": 3, "medio": 2, "bajo": 1, "sin_datos": 0}
ORDEN_COBERTURA = {"nuevo": 0, "ampliación": 1, "cubierto": 2}
ESTADOS_OPORTUNIDAD = ("propuesta", "aceptada", "descartada", "publicada")
ESTADOS_ACTIVOS = ("propuesta", "aceptada", "publicada")

# Carpetas de biblioteca/ que no son fuentes de fichas externas.
CARPETAS_NO_FUENTE = {"substack", "oportunidades", "contenidos"}

STOPWORDS = {
    # español
    "de", "la", "el", "en", "y", "a", "los", "las", "que", "un", "una",
    "del", "por", "con", "para", "se", "su", "al", "es", "como", "mas",
    "pero", "sus", "le", "ya", "o", "fue", "este", "ha", "si", "porque",
    "esta", "son", "entre", "esta", "cuando", "muy", "sin", "sobre",
    "tambien", "me", "hasta", "hay", "donde", "desde", "todo", "nos",
    "durante", "todos", "uno", "les", "ni", "contra", "otros", "ese",
    "eso", "ante", "ellos", "esto", "antes", "algunos", "unos", "otro",
    "otras", "otra", "tanto", "esa", "estos", "mucho", "nada", "muchos",
    "cual", "poco", "ella", "estar", "estas", "algunas", "algo", "lo",
    # inglés
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with",
    "is", "are", "was", "were", "be", "been", "it", "this", "that",
    "these", "those", "as", "at", "by", "from", "not", "no", "do", "does",
    "did", "can", "could", "will", "would", "should", "how", "what", "your",
}


# ---------------------------------------------------------------------------
# Utilidades de texto
# ---------------------------------------------------------------------------

def quitar_tildes(texto: str) -> str:
    descompuesto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in descompuesto if not unicodedata.combining(c))


def normalizar_tema(texto: str) -> str:
    """Minúsculas, sin tildes y sin espacios sobrantes."""
    limpio = quitar_tildes(texto).lower()
    return re.sub(r"\s+", " ", limpio).strip()


def slug(texto: str) -> str:
    base = normalizar_tema(texto)
    base = re.sub(r"[^a-z0-9]+", "-", base).strip("-")
    return base or "sin-tema"


def tokenizar(texto: str) -> list[str]:
    """Minúsculas, sin tildes, sin signos y sin palabras vacías (es/en)."""
    limpio = quitar_tildes(texto).lower()
    tokens = re.findall(r"[a-z0-9]+", limpio)
    return [t for t in tokens if len(t) > 1 and t not in STOPWORDS]


def sha256_texto(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def huella_json(dato) -> str:
    return sha256_texto(json.dumps(dato, ensure_ascii=False, sort_keys=True))


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    union = a | b
    return len(a & b) / len(union)


def lunes_siguiente(hoy: str) -> date:
    """El lunes de la semana siguiente a la fecha dada (ISO YYYY-MM-DD)."""
    fecha = date.fromisoformat(hoy)
    return fecha + timedelta(days=7 - fecha.weekday())


# ---------------------------------------------------------------------------
# Escrituras atómicas
# ---------------------------------------------------------------------------

def escribir_atomico(ruta: Path, contenido: str):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    descriptor, tmp = tempfile.mkstemp(dir=ruta.parent, suffix=".tmp")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as f:
            f.write(contenido)
        os.replace(tmp, ruta)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def escribir_json_atomico(ruta: Path, datos):
    escribir_atomico(ruta, json.dumps(datos, ensure_ascii=False, indent=2) + "\n")


# ---------------------------------------------------------------------------
# Validación contra esquema (subconjunto de JSON Schema, sin dependencias)
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


def validar_contra_esquema(dato, esquema: dict, ruta: str = "raiz") -> list[str]:
    errores: list[str] = []
    tipo = esquema.get("type")
    if tipo:
        tipos = tipo if isinstance(tipo, list) else [tipo]
        esperados = tuple(_TIPOS[t] for t in tipos)
        numerico = any(t in ("integer", "number") for t in tipos)
        if isinstance(dato, bool) and numerico and "boolean" not in tipos:
            errores.append(f"{ruta}: se esperaba {'/'.join(tipos)} y llegó un booleano")
            return errores
        if not isinstance(dato, esperados):
            errores.append(f"{ruta}: se esperaba {'/'.join(tipos)} y llegó {type(dato).__name__}")
            return errores

    if "enum" in esquema and dato not in esquema["enum"]:
        permitidos = ", ".join(repr(v) for v in esquema["enum"])
        errores.append(f"{ruta}: valor {dato!r} no permitido; debe ser uno de: {permitidos}")

    if isinstance(dato, str) and "minLength" in esquema and len(dato.strip()) < esquema["minLength"]:
        errores.append(f"{ruta}: no puede estar vacío")

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
        subesquema = esquema.get("items")
        if subesquema:
            for i, elemento in enumerate(dato):
                errores.extend(validar_contra_esquema(elemento, subesquema, f"{ruta}[{i}]"))

    return errores


# ---------------------------------------------------------------------------
# BM25 en Python puro
# ---------------------------------------------------------------------------

class BM25:
    def __init__(self, documentos: dict[str, str], k1: float = 1.5, b: float = 0.75):
        """documentos: id -> texto. Tokeniza con `tokenizar`."""
        self.k1 = k1
        self.b = b
        self.tokens: dict[str, list[str]] = {did: tokenizar(t) for did, t in documentos.items()}
        self.n = len(self.tokens)
        self.longitudes = {did: len(toks) for did, toks in self.tokens.items()}
        total = sum(self.longitudes.values())
        self.media = (total / self.n) if self.n else 0.0
        self.frecuencias: dict[str, Counter] = {did: Counter(toks) for did, toks in self.tokens.items()}
        df: Counter = Counter()
        for toks in self.tokens.values():
            for termino in set(toks):
                df[termino] += 1
        self.idf = {
            t: math.log(1 + (self.n - f + 0.5) / (f + 0.5)) for t, f in df.items()
        }

    def puntuar(self, consulta: str) -> list[tuple[str, float]]:
        """Devuelve [(id, puntuación)] en orden descendente, determinista."""
        q = tokenizar(consulta)
        resultados = []
        for did in self.tokens:
            tf = self.frecuencias[did]
            dl = self.longitudes[did]
            puntuacion = 0.0
            for termino in q:
                if termino not in tf:
                    continue
                idf = self.idf.get(termino, 0.0)
                f = tf[termino]
                denominador = f + self.k1 * (1 - self.b + self.b * dl / self.media) if self.media else f
                puntuacion += idf * f * (self.k1 + 1) / denominador
            resultados.append((did, round(puntuacion, 6)))
        resultados.sort(key=lambda par: (-par[1], par[0]))
        return resultados


# ---------------------------------------------------------------------------
# Unión-búsqueda para agrupar fichas
# ---------------------------------------------------------------------------

class UnionBusqueda:
    def __init__(self, elementos):
        self.padre = {e: e for e in elementos}

    def raiz(self, e):
        while self.padre[e] != e:
            self.padre[e] = self.padre[self.padre[e]]
            e = self.padre[e]
        return e

    def unir(self, a, b):
        ra, rb = self.raiz(a), self.raiz(b)
        if ra != rb:
            # Determinista: la raíz menor alfabéticamente gana.
            if rb < ra:
                ra, rb = rb, ra
            self.padre[rb] = ra


# ---------------------------------------------------------------------------
# Frontmatter de las oportunidades (YAML plano, sin dependencias)
# ---------------------------------------------------------------------------

def parsear_frontmatter(texto: str) -> tuple[dict, str]:
    """Devuelve (encabezado, cuerpo). Soporta claves simples y listas en línea."""
    lineas = texto.splitlines()
    if not lineas or lineas[0].strip() != "---":
        return {}, texto
    encabezado: dict = {}
    fin = None
    for i, linea in enumerate(lineas[1:], start=1):
        if linea.strip() == "---":
            fin = i
            break
        coincidencia = re.match(r"^([A-Za-z_][\w]*):\s*(.*)$", linea)
        if not coincidencia:
            continue
        clave, bruto = coincidencia.group(1), coincidencia.group(2).strip()
        if bruto.startswith("[") and bruto.endswith("]"):
            interior = bruto[1:-1].strip()
            valor = [v.strip().strip("'\"") for v in interior.split(",") if v.strip()] if interior else []
        elif bruto.startswith('"') and bruto.endswith('"') and len(bruto) >= 2:
            valor = bruto[1:-1]
        elif re.fullmatch(r"-?\d+", bruto):
            valor = int(bruto)
        else:
            valor = bruto
        encabezado[clave] = valor
    cuerpo = "\n".join(lineas[fin + 1:]) if fin is not None else ""
    return encabezado, cuerpo.strip("\n")


def componer_frontmatter(encabezado: dict) -> str:
    lineas = ["---"]
    for clave, valor in encabezado.items():
        if isinstance(valor, list):
            lineas.append(f"{clave}: [{', '.join(str(v) for v in valor)}]")
        elif isinstance(valor, str) and valor == "":
            lineas.append(f'{clave}: ""')
        else:
            lineas.append(f"{clave}: {valor}")
    lineas.append("---")
    return "\n".join(lineas)


def validar_cuerpo_oportunidad(cuerpo: str) -> list[str]:
    """Comprueba que estén las seis secciones de la plantilla, en orden y con contenido."""
    errores = []
    posiciones = []
    for seccion in SECCIONES_OPORTUNIDAD:
        patron = re.compile(rf"^{re.escape(seccion)}\s*$", re.MULTILINE)
        coincidencia = patron.search(cuerpo)
        if not coincidencia:
            errores.append(f"falta la sección '{seccion}'")
            posiciones.append(None)
        else:
            posiciones.append(coincidencia.start())
    validas = [p for p in posiciones if p is not None]
    if validas != sorted(validas):
        errores.append("las secciones no están en el orden de la plantilla")
    # Contenido no vacío entre secciones.
    cortes = re.split(r"^##\s+.*$", cuerpo, flags=re.MULTILINE)
    encabezados = re.findall(r"^##\s+(.*)$", cuerpo, flags=re.MULTILINE)
    for encabezado_md, contenido in zip(encabezados, cortes[1:]):
        seccion = f"## {encabezado_md.strip()}"
        if seccion in SECCIONES_OPORTUNIDAD and not contenido.strip():
            errores.append(f"la sección '{seccion}' está vacía")
    return errores


# ---------------------------------------------------------------------------
# Señales
# ---------------------------------------------------------------------------

def derivar_interes(multiplo) -> str:
    """Mismos umbrales que explorar-youtube (ARQUITECTURA 8.2)."""
    if multiplo is None:
        return "sin_datos"
    if multiplo >= 2:
        return "alto"
    if multiplo >= 1:
        return "medio"
    return "bajo"


def mejor_interes(fichas: list[dict]) -> str:
    valores = [derivar_interes((f.get("senales") or {}).get("multiplo_mediana")) for f in fichas]
    return max(valores, key=lambda v: ORDEN_INTERES[v]) if valores else "sin_datos"


# ---------------------------------------------------------------------------
# Detector
# ---------------------------------------------------------------------------

CAMPOS_FICHA_EXTERNA = ("id", "fuente", "autor", "huella", "tema", "tesis", "entidades", "senales")


class Detector:
    def __init__(self, ruta_config: Path, hoy: str | None = None):
        self.ruta_config = Path(ruta_config)
        if not self.ruta_config.is_file():
            raise RuntimeError(f"No existe el archivo de configuración: {self.ruta_config}")
        try:
            self.config = json.loads(self.ruta_config.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Configuración ilegible ({self.ruta_config}): {exc}") from exc
        if "linea_editorial" not in self.config:
            raise RuntimeError("proyecto.config.json no tiene el bloque 'linea_editorial'")
        self.raiz = self.ruta_config.resolve().parent
        self.hoy = hoy or date.today().isoformat()
        self.dir_biblioteca = self.raiz / "biblioteca"
        self.dir_oportunidades = self.dir_biblioteca / "oportunidades"
        self.dir_control = self.dir_oportunidades / "control"
        self.dir_evaluaciones = self.dir_control / "evaluaciones"
        self.ruta_grupos = self.dir_control / "grupos.json"
        self.ruta_indice = self.dir_oportunidades / "INDICE.md"
        self.dir_fichas_propias = self.dir_biblioteca / "substack" / "fichas"
        self.ruta_inventario = self.dir_biblioteca / "substack" / "control" / "inventario.json"
        self.ruta_esquema_evaluacion = (
            Path(__file__).resolve().parent.parent / "references" / "evaluacion.schema.json"
        )
        self.avisos: list[str] = []

    def avisar(self, mensaje: str):
        self.avisos.append(mensaje)
        print(f"AVISO: {mensaje}", file=sys.stderr)

    # -- carga de datos ------------------------------------------------------

    def cargar_fichas_externas(self) -> list[dict]:
        """Todas las `biblioteca/<fuente>/**/ficha.json`, sin rutas fijas por fuente."""
        fichas = []
        if not self.dir_biblioteca.is_dir():
            return fichas
        for carpeta in sorted(self.dir_biblioteca.iterdir()):
            if not carpeta.is_dir() or carpeta.name in CARPETAS_NO_FUENTE:
                continue
            for ruta in sorted(carpeta.rglob("ficha.json")):
                try:
                    ficha = json.loads(ruta.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError) as exc:
                    self.avisar(f"ficha externa ilegible, se omite: {ruta} ({exc})")
                    continue
                faltan = [c for c in CAMPOS_FICHA_EXTERNA if c not in ficha]
                if faltan:
                    self.avisar(f"ficha externa sin campos {faltan}, se omite: {ruta}")
                    continue
                fichas.append(ficha)
        fichas.sort(key=lambda f: (f["fuente"], f["id"]))
        return fichas

    def cargar_fichas_propias(self) -> list[dict]:
        fichas = []
        if not self.dir_fichas_propias.is_dir():
            return fichas
        for ruta in sorted(self.dir_fichas_propias.glob("*.json")):
            try:
                ficha = json.loads(ruta.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                self.avisar(f"ficha propia ilegible, se omite: {ruta} ({exc})")
                continue
            if "id" not in ficha or "tema" not in ficha:
                self.avisar(f"ficha propia sin id o tema, se omite: {ruta}")
                continue
            fichas.append(ficha)
        fichas.sort(key=lambda f: str(f["id"]))
        return fichas

    def cargar_inventario(self) -> dict:
        if not self.ruta_inventario.is_file():
            return {}
        try:
            return json.loads(self.ruta_inventario.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            self.avisar(f"inventario ilegible: {self.ruta_inventario} ({exc})")
            return {}

    def cargar_oportunidades(self) -> list[dict]:
        """Encabezado + cuerpo de cada oportunidad existente."""
        oportunidades = []
        if not self.dir_oportunidades.is_dir():
            return oportunidades
        for ruta in sorted(self.dir_oportunidades.glob("*.md")):
            if ruta.name == "INDICE.md":
                continue
            encabezado, cuerpo = parsear_frontmatter(ruta.read_text(encoding="utf-8"))
            if "id" not in encabezado or "estado" not in encabezado:
                self.avisar(f"oportunidad sin id o estado en el encabezado, se omite: {ruta}")
                continue
            if encabezado["estado"] not in ESTADOS_OPORTUNIDAD:
                self.avisar(f"oportunidad con estado desconocido '{encabezado['estado']}', se omite: {ruta}")
                continue
            oportunidades.append({"ruta": ruta, "encabezado": encabezado, "cuerpo": cuerpo})
        return oportunidades

    # -- agrupar --------------------------------------------------------------

    @staticmethod
    def _entidad_dominante(miembros: list[dict]) -> str | None:
        """La entidad más repetida del grupo; el eje de su historia.

        Empates: primero la que aparece antes en las listas de entidades de las
        fichas (suelen ir de más a menos central), después la menor
        alfabéticamente. Se excluyen las entidades que son el propio autor de
        una ficha (el nombre del canal no es el eje del contenido).
        """
        autores = {normalizar_tema(f["autor"]) for f in miembros if f.get("autor")}
        frecuencia: Counter = Counter()
        primera_posicion: dict[str, int] = {}
        for f in miembros:
            for posicion, entidad in enumerate(f.get("entidades", [])):
                e = normalizar_tema(entidad)
                if not e or e in autores:
                    continue
                frecuencia[e] += 1
                if e not in primera_posicion or posicion < primera_posicion[e]:
                    primera_posicion[e] = posicion
        if not frecuencia:
            return None
        return min(frecuencia, key=lambda e: (-frecuencia[e], primera_posicion[e], e))

    def agrupar_fichas(self, fichas: list[dict]) -> list[dict]:
        ids = [f"{f['fuente']}:{f['id']}" for f in fichas]
        por_id = dict(zip(ids, fichas))
        union = UnionBusqueda(ids)
        entidades_norm = {
            i: {normalizar_tema(e) for e in por_id[i].get("entidades", []) if e.strip()}
            for i in ids
        }
        # Grano fino: dos fichas solo comparten grupo si comparten entidades
        # DISCRIMINANTES. Una entidad que aparece en muchas fichas (ChatGPT,
        # OpenAI, Claude...) es un comodin del nicho y no señala historia
        # comun; solo cuentan las entidades presentes en pocas fichas. Con
        # ellas, dos fichas se unen si su Jaccard es >= 0.5 o comparten 2 o
        # mas (las listas largas hunden el Jaccard aunque la historia sea la
        # misma). Compartir la etiqueta de tema no basta. Sin esa afinidad,
        # cada ficha es su propio grupo.
        frecuencia_entidad: dict[str, int] = {}
        for i in ids:
            for e in entidades_norm[i]:
                frecuencia_entidad[e] = frecuencia_entidad.get(e, 0) + 1
        tope_ubicua = max(3, round(0.25 * len(ids)))
        discriminantes = {
            i: {e for e in entidades_norm[i] if frecuencia_entidad[e] <= tope_ubicua}
            for i in ids
        }
        for a_pos, a in enumerate(ids):
            for b in ids[a_pos + 1:]:
                comunes = discriminantes[a] & discriminantes[b]
                if jaccard(discriminantes[a], discriminantes[b]) >= 0.5 or len(comunes) >= 2:
                    union.unir(a, b)

        por_raiz: dict[str, list[dict]] = {}
        for i in ids:
            por_raiz.setdefault(union.raiz(i), []).append(por_id[i])

        # La regla de interés por canales se mide a nivel de TEMA: cuántos
        # autores distintos hablan del tema, aunque sus fichas queden en
        # grupos distintos por no compartir entidades.
        autores_por_tema: dict[str, set] = {}
        for f in fichas:
            autores_por_tema.setdefault(normalizar_tema(f["tema"]), set()).add(f["autor"])

        grupos = []
        for miembros in por_raiz.values():
            miembros.sort(key=lambda f: (f["fuente"], f["id"]))
            # Tema más frecuente (normalizado); en empate, el menor alfabéticamente.
            recuento = Counter(normalizar_tema(f["tema"]) for f in miembros)
            maximo = max(recuento.values())
            tema_normalizado = min(t for t, c in recuento.items() if c == maximo)
            # Variante original del tema elegido, de la primera ficha que lo usa.
            tema = next(f["tema"] for f in miembros if normalizar_tema(f["tema"]) == tema_normalizado)
            autores = sorted({f["autor"] for f in miembros})
            temas_grupo = set(recuento)
            autores_tema = set()
            for t in temas_grupo:
                autores_tema |= autores_por_tema.get(t, set())
            canales_tema = len(autores_tema)
            multiplos = [
                (f.get("senales") or {}).get("multiplo_mediana")
                for f in miembros
                if (f.get("senales") or {}).get("multiplo_mediana") is not None
            ]
            fechas = [f["fecha"] for f in miembros if f.get("fecha")]
            interes = mejor_interes(miembros)
            canales = len(autores)
            # grupo_id = slug del tema + entidad/eje dominante, estable y
            # determinista (p. ej. "herramientas-de-ia-qwen-3-8"). Si la
            # entidad ya está contenida en el slug del tema, no se repite.
            base = slug(tema_normalizado)
            dominante = self._entidad_dominante(miembros)
            sufijo = slug(dominante) if dominante else ""
            grupo_id = f"{base}-{sufijo}" if sufijo and sufijo not in base else base
            grupo = {
                "grupo_id": grupo_id,
                "tema": tema,
                "fichas": [f"{f['fuente']}:{f['id']}" for f in miembros],
                "senales": {
                    "fichas": len(miembros),
                    "canales": canales,
                    "canales_tema": canales_tema,
                    "autores": autores,
                    "mejor_interes": interes,
                    "mayor_multiplo": max(multiplos) if multiplos else None,
                    "fecha_mas_reciente": max(fechas) if fechas else None,
                    "interes_real": interes in ("medio", "alto") or canales_tema >= 2,
                },
                "huella_fichas": huella_json(sorted((f["id"], f["huella"]) for f in miembros)),
            }
            grupos.append(grupo)
        grupos.sort(key=lambda g: (g["grupo_id"], g["fichas"]))
        # Dos grupos distintos pueden coincidir en tema y entidad dominante sin
        # compartir entidades suficientes: se desambiguan con un ordinal.
        vistos: Counter = Counter()
        for grupo in grupos:
            vistos[grupo["grupo_id"]] += 1
            if vistos[grupo["grupo_id"]] > 1:
                grupo["grupo_id"] = f"{grupo['grupo_id']}-{vistos[grupo['grupo_id']]}"
        grupos.sort(key=lambda g: g["grupo_id"])
        return grupos

    def cmd_agrupar(self) -> int:
        fichas = self.cargar_fichas_externas()
        grupos = self.agrupar_fichas(fichas)
        escribir_json_atomico(self.ruta_grupos, {"generado": self.hoy, "grupos": grupos})
        print(json.dumps(
            {
                "fichas_externas": len(fichas),
                "grupos": len(grupos),
                "con_interes_real": sum(1 for g in grupos if g["senales"]["interes_real"]),
                "archivo": str(self.ruta_grupos.relative_to(self.raiz)),
            },
            ensure_ascii=False, indent=2,
        ))
        return CODIGO_PARCIAL if self.avisos else CODIGO_OK

    # -- parecidos (BM25) -----------------------------------------------------

    @staticmethod
    def _texto_ficha_propia(ficha: dict) -> str:
        partes = [
            ficha.get("titulo", ""),
            ficha.get("tema", ""),
            " ".join(ficha.get("subtemas", [])),
            ficha.get("tesis", ""),
            " ".join(ficha.get("entidades", [])),
        ]
        return " ".join(p for p in partes if p)

    @staticmethod
    def _consulta_grupo(fichas_grupo: list[dict]) -> str:
        partes = []
        for f in fichas_grupo:
            partes.append(f.get("tema", ""))
            partes.append(f.get("tesis", ""))
            partes.append(" ".join(f.get("entidades", [])))
        return " ".join(p for p in partes if p)

    def articulos_parecidos(self, fichas_grupo: list[dict], propias: list[dict], inventario: dict) -> list[dict]:
        if not propias:
            return []
        bm25 = BM25({str(f["id"]): self._texto_ficha_propia(f) for f in propias})
        por_id = {str(f["id"]): f for f in propias}
        resultado = []
        for post_id, puntuacion in bm25.puntuar(self._consulta_grupo(fichas_grupo))[:5]:
            registro = inventario.get(post_id) or {}
            ruta_texto = registro.get("archivo")
            if not ruta_texto:
                self.avisar(f"el inventario no tiene la ruta del artículo {post_id}")
            resultado.append({
                "post_id": post_id,
                "puntuacion": puntuacion,
                "ficha": por_id[post_id],
                "ruta_texto": ruta_texto,
            })
        return resultado

    def oportunidades_parecidas(self, fichas_grupo: list[dict], oportunidades: list[dict],
                                grupo_id: str) -> list[dict]:
        # La propuesta pendiente de decisión que salió de este mismo grupo no es
        # una "decisión parecida": si contara, crear la propuesta dejaría el
        # grupo otra vez pendiente. En cuanto la persona la acepta o descarta,
        # vuelve al contexto y el grupo se reevalúa con esa decisión delante.
        oportunidades = [
            o for o in oportunidades
            if not (o["encabezado"].get("grupo_id") == grupo_id
                    and o["encabezado"]["estado"] == "propuesta")
        ]
        if not oportunidades:
            return []
        documentos = {}
        for o in oportunidades:
            enc = o["encabezado"]
            # Tema y "título": el id lleva el slug del tema con el que se creó.
            documentos[str(enc["id"])] = f"{enc.get('tema', '')} {str(enc['id']).replace('-', ' ')}"
        bm25 = BM25(documentos)
        por_id = {str(o["encabezado"]["id"]): o for o in oportunidades}
        resultado = []
        for oid, puntuacion in bm25.puntuar(self._consulta_grupo(fichas_grupo)):
            if puntuacion <= 0 or len(resultado) >= 5:
                continue
            enc = por_id[oid]["encabezado"]
            resultado.append({
                "id": oid,
                "estado": enc["estado"],
                "motivo": enc.get("motivo_estado", ""),
                "tema": enc.get("tema", ""),
                "puntuacion": puntuacion,
            })
        return resultado

    # -- contexto y pendientes -------------------------------------------------

    @staticmethod
    def contexto_evaluacion(grupo: dict, fichas_grupo: list[dict], articulos: list[dict], parecidas: list[dict]) -> dict:
        return {
            "fichas": sorted([f["id"], f["huella"]] for f in fichas_grupo),
            "articulos": sorted([a["post_id"], a["ficha"].get("huella", "")] for a in articulos),
            "oportunidades": sorted([p["id"], p["estado"], p["motivo"]] for p in parecidas),
        }

    def _preparar(self):
        fichas = self.cargar_fichas_externas()
        grupos = self.agrupar_fichas(fichas)
        por_clave = {f"{f['fuente']}:{f['id']}": f for f in fichas}
        propias = self.cargar_fichas_propias()
        inventario = self.cargar_inventario()
        oportunidades = self.cargar_oportunidades()
        return grupos, por_clave, propias, inventario, oportunidades

    def construir_paquete(self, grupo: dict, por_clave: dict, propias: list[dict],
                          inventario: dict, oportunidades: list[dict]) -> dict:
        fichas_grupo = [por_clave[c] for c in grupo["fichas"]]
        articulos = self.articulos_parecidos(fichas_grupo, propias, inventario)
        parecidas = self.oportunidades_parecidas(fichas_grupo, oportunidades, grupo["grupo_id"])
        contexto = self.contexto_evaluacion(grupo, fichas_grupo, articulos, parecidas)
        return {
            "grupo_id": grupo["grupo_id"],
            "tema": grupo["tema"],
            "senales": grupo["senales"],
            "fichas": fichas_grupo,
            "articulos_parecidos": articulos,
            "oportunidades_parecidas": parecidas,
            "linea_editorial": self.config["linea_editorial"],
            "contexto": contexto,
            "huella_contexto": huella_json(contexto),
        }

    def _motivo_pendiente(self, grupo_id: str, contexto: dict) -> str | None:
        """None si la evaluación guardada sigue vigente; si no, el motivo."""
        ruta = self.dir_evaluaciones / f"{grupo_id}.json"
        if not ruta.is_file():
            return "sin_evaluacion"
        try:
            guardada = json.loads(ruta.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return "evaluacion_ilegible"
        anterior = guardada.get("contexto", {})
        if anterior.get("fichas") != contexto["fichas"]:
            return "fichas_cambiadas"
        if anterior.get("articulos") != contexto["articulos"]:
            return "articulos_cambiados"
        if anterior.get("oportunidades") != contexto["oportunidades"]:
            return "decisiones_cambiadas"
        return None

    def cmd_pendientes(self) -> int:
        grupos, por_clave, propias, inventario, oportunidades = self._preparar()
        paquetes = []
        for grupo in grupos:
            paquete = self.construir_paquete(grupo, por_clave, propias, inventario, oportunidades)
            motivo = self._motivo_pendiente(grupo["grupo_id"], paquete["contexto"])
            if motivo:
                paquete["motivo_pendiente"] = motivo
                paquetes.append(paquete)
        print(json.dumps(paquetes, ensure_ascii=False, indent=2))
        return CODIGO_PARCIAL if self.avisos else CODIGO_OK

    # -- guardar-evaluacion -----------------------------------------------------

    def cmd_guardar_evaluacion(self, archivo: Path) -> int:
        archivo = Path(archivo)
        if not archivo.is_file():
            print(f"ERROR: no existe el archivo {archivo}", file=sys.stderr)
            return CODIGO_FATAL
        try:
            evaluacion = json.loads(archivo.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"ERROR: JSON ilegible: {exc}", file=sys.stderr)
            return CODIGO_FATAL

        esquema = json.loads(self.ruta_esquema_evaluacion.read_text(encoding="utf-8"))
        errores = validar_contra_esquema(evaluacion, esquema, "evaluacion")
        if errores:
            print("ERROR: la evaluación no cumple el esquema:", file=sys.stderr)
            for e in errores:
                print(f"  - {e}", file=sys.stderr)
            return CODIGO_FATAL

        grupos, por_clave, propias, inventario, oportunidades = self._preparar()
        por_grupo = {g["grupo_id"]: g for g in grupos}
        grupo = por_grupo.get(evaluacion["grupo_id"])
        if grupo is None:
            print(f"ERROR: el grupo '{evaluacion['grupo_id']}' no existe en el agrupamiento actual", file=sys.stderr)
            return CODIGO_FATAL

        paquete = self.construir_paquete(grupo, por_clave, propias, inventario, oportunidades)

        # El modelo debe haber leído los artículos del paquete.
        ids_paquete = {a["post_id"] for a in paquete["articulos_parecidos"]}
        faltan = sorted(ids_paquete - set(evaluacion["articulos_comparados"]))
        if faltan:
            print(
                "ERROR: articulos_comparados no incluye todos los artículos del paquete; "
                f"faltan: {', '.join(faltan)}",
                file=sys.stderr,
            )
            return CODIGO_FATAL

        # parecida_a debe apuntar a una oportunidad conocida.
        por_oportunidad = {str(o["encabezado"]["id"]): o for o in oportunidades}
        parecida = evaluacion.get("parecida_a")
        if parecida is not None and parecida not in por_oportunidad:
            print(f"ERROR: parecida_a apunta a una oportunidad desconocida: {parecida}", file=sys.stderr)
            return CODIGO_FATAL

        # Las cuatro condiciones de ARQUITECTURA.md 8.4.
        aportacion = evaluacion.get("aportacion")
        condiciones = {
            "interes_real": {
                "cumple": bool(grupo["senales"]["interes_real"]),
                "detalle": (
                    f"mejor_interes={grupo['senales']['mejor_interes']}, "
                    f"canales={grupo['senales']['canales']}, "
                    f"canales_tema={grupo['senales']['canales_tema']}"
                ),
            },
            "encaje": {
                "cumple": evaluacion["encaje"] is True,
                "detalle": evaluacion["motivo"],
            },
            "no_cubierto": {
                "cumple": evaluacion["cobertura"] in ("nuevo", "ampliación"),
                "detalle": f"cobertura={evaluacion['cobertura']}",
            },
            "aportacion": {
                "cumple": bool(aportacion and str(aportacion).strip()),
                "detalle": aportacion or "sin aportación",
            },
        }
        es_oportunidad = all(c["cumple"] for c in condiciones.values())
        accion = "proponer" if es_oportunidad else "descartar"
        motivo_descarte = None
        if not es_oportunidad:
            fallidas = [n for n, c in condiciones.items() if not c["cumple"]]
            motivo_descarte = f"no cumple: {', '.join(fallidas)}"

        # Reglas sobre oportunidades parecidas.
        if parecida is not None and es_oportunidad:
            estado = por_oportunidad[parecida]["encabezado"]["estado"]
            if estado == "descartada":
                razon = evaluacion.get("razon_nueva")
                if not (razon and str(razon).strip()):
                    es_oportunidad = False
                    accion = "descartar"
                    motivo_descarte = (
                        f"parecida a la oportunidad descartada '{parecida}' y sin razon_nueva"
                    )
            elif estado in ESTADOS_ACTIVOS:
                es_oportunidad = False
                accion = f"actualizar:{parecida}"
                motivo_descarte = (
                    f"ya existe la oportunidad '{parecida}' en estado {estado}: "
                    "añadir las evidencias nuevas con guardar-oportunidad --actualizar"
                )

        resultado = {
            "grupo_id": grupo["grupo_id"],
            "fecha": self.hoy,
            "evaluacion": evaluacion,
            "condiciones": condiciones,
            "es_oportunidad": es_oportunidad,
            "accion": accion,
            "motivo_descarte": motivo_descarte,
            "contexto": paquete["contexto"],
            "huella_contexto": paquete["huella_contexto"],
        }
        escribir_json_atomico(self.dir_evaluaciones / f"{grupo['grupo_id']}.json", resultado)
        print(json.dumps(
            {
                "grupo_id": grupo["grupo_id"],
                "es_oportunidad": es_oportunidad,
                "accion": accion,
                "condiciones": {n: c["cumple"] for n, c in condiciones.items()},
                "motivo_descarte": motivo_descarte,
            },
            ensure_ascii=False, indent=2,
        ))
        return CODIGO_PARCIAL if self.avisos else CODIGO_OK

    # -- guardar-oportunidad ----------------------------------------------------

    def _evidencias_grupo(self, fichas_grupo: list[dict]) -> list[str]:
        evidencias = []
        for ficha in fichas_grupo:
            for afirmacion in ficha.get("afirmaciones", []):
                marca = afirmacion.get("marca")
                if marca:
                    evidencias.append(f"{ficha['fuente']}:{ficha['id']}@{marca}")
        # Deduplicar conservando el orden (fichas ya ordenadas por fuente, id).
        vistas = set()
        unicas = []
        for e in evidencias:
            if e not in vistas:
                vistas.add(e)
                unicas.append(e)
        return unicas

    def _buscar_oportunidad(self, oportunidades: list[dict], oportunidad_id: str) -> dict | None:
        for o in oportunidades:
            if str(o["encabezado"]["id"]) == oportunidad_id:
                return o
        return None

    def cmd_guardar_oportunidad(self, grupo_id: str, archivo: Path | None,
                                actualizar: str | None = None) -> int:
        grupos, por_clave, propias, inventario, oportunidades = self._preparar()
        por_grupo = {g["grupo_id"]: g for g in grupos}
        grupo = por_grupo.get(grupo_id)
        if grupo is None:
            print(f"ERROR: el grupo '{grupo_id}' no existe en el agrupamiento actual", file=sys.stderr)
            return CODIGO_FATAL
        fichas_grupo = [por_clave[c] for c in grupo["fichas"]]

        if actualizar:
            return self._actualizar_oportunidad(actualizar, fichas_grupo, oportunidades)

        if archivo is None:
            print("ERROR: falta el archivo .md con el cuerpo de la oportunidad", file=sys.stderr)
            return CODIGO_FATAL

        ruta_evaluacion = self.dir_evaluaciones / f"{grupo_id}.json"
        if not ruta_evaluacion.is_file():
            print(f"ERROR: el grupo '{grupo_id}' no tiene evaluación guardada", file=sys.stderr)
            return CODIGO_FATAL
        guardada = json.loads(ruta_evaluacion.read_text(encoding="utf-8"))
        if not guardada.get("es_oportunidad"):
            print(
                f"ERROR: la evaluación de '{grupo_id}' no cumple las cuatro condiciones "
                f"({guardada.get('motivo_descarte')})",
                file=sys.stderr,
            )
            return CODIGO_FATAL

        archivo = Path(archivo)
        if not archivo.is_file():
            print(f"ERROR: no existe el archivo {archivo}", file=sys.stderr)
            return CODIGO_FATAL
        _, cuerpo = parsear_frontmatter(archivo.read_text(encoding="utf-8"))
        errores = validar_cuerpo_oportunidad(cuerpo)
        if errores:
            print("ERROR: el cuerpo no sigue la plantilla:", file=sys.stderr)
            for e in errores:
                print(f"  - {e}", file=sys.stderr)
            return CODIGO_FATAL

        oportunidad_id = f"{self.hoy}-{grupo_id}"
        ruta_destino = self.dir_oportunidades / f"{oportunidad_id}.md"
        existente = self._buscar_oportunidad(oportunidades, oportunidad_id)
        if existente and existente["encabezado"]["estado"] != "propuesta":
            print(
                f"ERROR: la oportunidad '{oportunidad_id}' está en estado "
                f"'{existente['encabezado']['estado']}' y no se sobrescribe; el estado lo cambia la persona",
                file=sys.stderr,
            )
            return CODIGO_FATAL

        evaluacion = guardada["evaluacion"]
        encabezado = {
            "id": oportunidad_id,
            "estado": "propuesta",
            "motivo_estado": "",
            "tema": grupo["tema"],
            "grupo_id": grupo_id,
            "interes": grupo["senales"]["mejor_interes"],
            "canales": grupo["senales"]["canales"],
            "cobertura": evaluacion["cobertura"],
            "evidencias": self._evidencias_grupo(fichas_grupo),
            "relacionados": [f"substack:{pid}" for pid in sorted(evaluacion["articulos_comparados"])],
        }
        contenido = componer_frontmatter(encabezado) + "\n" + cuerpo.strip() + "\n"
        escribir_atomico(ruta_destino, contenido)
        print(json.dumps(
            {
                "oportunidad": oportunidad_id,
                "archivo": str(ruta_destino.relative_to(self.raiz)),
                "evidencias": len(encabezado["evidencias"]),
                "sobrescrita": bool(existente),
            },
            ensure_ascii=False, indent=2,
        ))
        return CODIGO_PARCIAL if self.avisos else CODIGO_OK

    def _actualizar_oportunidad(self, oportunidad_id: str, fichas_grupo: list[dict],
                                oportunidades: list[dict]) -> int:
        existente = self._buscar_oportunidad(oportunidades, oportunidad_id)
        if existente is None:
            print(f"ERROR: no existe la oportunidad '{oportunidad_id}'", file=sys.stderr)
            return CODIGO_FATAL
        encabezado = existente["encabezado"]
        if encabezado["estado"] == "descartada":
            print(
                f"ERROR: la oportunidad '{oportunidad_id}' está descartada; "
                "no se le añaden evidencias",
                file=sys.stderr,
            )
            return CODIGO_FATAL
        actuales = list(encabezado.get("evidencias", []))
        nuevas = [e for e in self._evidencias_grupo(fichas_grupo) if e not in actuales]
        encabezado["evidencias"] = actuales + nuevas
        contenido = componer_frontmatter(encabezado) + "\n" + existente["cuerpo"].strip() + "\n"
        escribir_atomico(existente["ruta"], contenido)
        print(json.dumps(
            {
                "oportunidad": oportunidad_id,
                "evidencias_nuevas": nuevas,
                "evidencias_totales": len(encabezado["evidencias"]),
                "estado": encabezado["estado"],
            },
            ensure_ascii=False, indent=2,
        ))
        return CODIGO_PARCIAL if self.avisos else CODIGO_OK

    # -- indice -----------------------------------------------------------------

    def cmd_indice(self) -> int:
        oportunidades = self.cargar_oportunidades()

        def clave_propuesta(o):
            enc = o["encabezado"]
            return (
                -ORDEN_INTERES.get(enc.get("interes", "sin_datos"), 0),
                -(enc.get("canales") or 0),
                ORDEN_COBERTURA.get(enc.get("cobertura", "cubierto"), 9),
                str(enc["id"]),
            )

        propuestas = sorted(
            (o for o in oportunidades if o["encabezado"]["estado"] == "propuesta"),
            key=clave_propuesta,
        )
        lineas = ["# Oportunidades", "", "## Propuestas (por prioridad)", ""]
        if propuestas:
            lineas += [
                "| Oportunidad | Tema | Interés | Canales | Cobertura |",
                "|---|---|---|---|---|",
            ]
            for o in propuestas:
                enc = o["encabezado"]
                enlace = f"[{enc['id']}]({o['ruta'].name})"
                lineas.append(
                    f"| {enlace} | {enc.get('tema', '')} | {enc.get('interes', '')} "
                    f"| {enc.get('canales', '')} | {enc.get('cobertura', '')} |"
                )
        else:
            lineas.append("No hay propuestas pendientes.")
        for estado, titulo in (
            ("aceptada", "Aceptadas"),
            ("publicada", "Publicadas"),
            ("descartada", "Descartadas"),
        ):
            del_estado = sorted(
                (o for o in oportunidades if o["encabezado"]["estado"] == estado),
                key=lambda o: str(o["encabezado"]["id"]),
            )
            lineas += ["", f"## {titulo}", ""]
            if del_estado:
                for o in del_estado:
                    enc = o["encabezado"]
                    motivo = enc.get("motivo_estado") or "sin motivo registrado"
                    lineas.append(f"- [{enc['id']}]({o['ruta'].name}) — {motivo}")
            else:
                lineas.append("Ninguna.")

        # Calendario sugerido: aceptadas primero y después propuestas, en su
        # orden de prioridad, una por semana a partir del lunes que viene.
        aceptadas = sorted(
            (o for o in oportunidades if o["encabezado"]["estado"] == "aceptada"),
            key=clave_propuesta,
        )
        programables = aceptadas + propuestas
        lineas += ["", "## Calendario sugerido", ""]
        if programables:
            lineas += [
                "Es una sugerencia, no un compromiso: la persona decide qué se publica y cuándo. "
                "Asigna una oportunidad por semana a partir de la próxima: primero las aceptadas "
                "y después las propuestas, en su orden de prioridad.",
                "",
                "| Semana del | Oportunidad | Estado | Tema |",
                "|---|---|---|---|",
            ]
            lunes = lunes_siguiente(self.hoy)
            for o in programables:
                enc = o["encabezado"]
                lineas.append(
                    f"| {lunes.isoformat()} | [{enc['id']}]({o['ruta'].name}) "
                    f"| {enc['estado']} | {enc.get('tema', '')} |"
                )
                lunes += timedelta(days=7)
        else:
            lineas.append("Nada que programar: no hay oportunidades aceptadas ni propuestas.")
        lineas.append("")
        escribir_atomico(self.ruta_indice, "\n".join(lineas))
        print(json.dumps(
            {
                "archivo": str(self.ruta_indice.relative_to(self.raiz)),
                "propuestas": len(propuestas),
                "total": len(oportunidades),
            },
            ensure_ascii=False, indent=2,
        ))
        return CODIGO_PARCIAL if self.avisos else CODIGO_OK


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    for flujo in (sys.stdout, sys.stderr):
        if hasattr(flujo, "reconfigure"):
            try:
                flujo.reconfigure(encoding="utf-8")
            except (ValueError, OSError):
                pass

    analizador = argparse.ArgumentParser(
        description="Cruza fichas externas, fichas propias y decisiones y gestiona las oportunidades."
    )
    analizador.add_argument(
        "--config", default="proyecto.config.json",
        help="Ruta de proyecto.config.json (por defecto, el del directorio actual).",
    )
    analizador.add_argument(
        "--hoy", default=None,
        help="Fecha YYYY-MM-DD para ids y registros (por defecto, la de hoy). Útil en pruebas.",
    )
    subcomandos = analizador.add_subparsers(dest="comando", required=True)
    subcomandos.add_parser("agrupar", help="Agrupa las fichas externas y escribe control/grupos.json.")
    subcomandos.add_parser("pendientes", help="Paquetes JSON de los grupos que necesitan evaluación.")
    p_eval = subcomandos.add_parser("guardar-evaluacion", help="Valida y guarda la evaluación del modelo.")
    p_eval.add_argument("archivo", help="JSON con la evaluación, según evaluacion.schema.json.")
    p_op = subcomandos.add_parser("guardar-oportunidad", help="Crea una oportunidad o le añade evidencias.")
    p_op.add_argument("grupo_id")
    p_op.add_argument("archivo", nargs="?", default=None, help="Markdown con el cuerpo (plantilla).")
    p_op.add_argument("--actualizar", metavar="OPORTUNIDAD_ID", default=None,
                      help="Añade las evidencias del grupo a una oportunidad existente.")
    subcomandos.add_parser("indice", help="Regenera biblioteca/oportunidades/INDICE.md.")

    args = analizador.parse_args(argv)
    try:
        detector = Detector(Path(args.config), hoy=args.hoy)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return CODIGO_FATAL

    try:
        if args.comando == "agrupar":
            return detector.cmd_agrupar()
        if args.comando == "pendientes":
            return detector.cmd_pendientes()
        if args.comando == "guardar-evaluacion":
            return detector.cmd_guardar_evaluacion(Path(args.archivo))
        if args.comando == "guardar-oportunidad":
            archivo = Path(args.archivo) if args.archivo else None
            return detector.cmd_guardar_oportunidad(args.grupo_id, archivo, args.actualizar)
        if args.comando == "indice":
            return detector.cmd_indice()
    except OSError as exc:
        print(f"ERROR: no pudo ejecutarse: {exc}", file=sys.stderr)
        return CODIGO_FATAL
    return CODIGO_FATAL


if __name__ == "__main__":
    sys.exit(main())
