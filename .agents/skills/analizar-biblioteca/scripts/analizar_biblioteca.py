#!/usr/bin/env python3
"""Convierte los articulos descargados en fichas con esquema fijo y genera el
mapa de temas y las metricas de estilo de la publicacion.

Segunda parte de la fase 1 del sistema editorial (ver ARQUITECTURA.md,
secciones 2, 4, 6, 8.1 y 10). Python sin IA, solo biblioteca estandar.

Reparto: el script detecta pendientes, impone los datos objetivos del
inventario, valida contra el esquema, guarda de forma atomica y agrega las
fichas en el mapa. El modelo solo entrega un JSON con los campos de juicio;
nunca escribe archivos de la biblioteca directamente.

Comandos:
  pendientes                  lista en JSON los articulos que necesitan ficha,
                              mas los temas, subtemas y entidades existentes
                              con sus frecuencias (para reutilizar vocabulario)
  guardar <id> <archivo.json> valida y guarda la ficha de un articulo; avisa
                              si un subtema o entidad se parece a uno ya usado
  vocabulario                 JSON con temas, subtemas y entidades (termino,
                              frecuencia, articulos) y los pares casi-duplicados
                              del corpus (seccion 'sospechosos')
  mapa                        regenera biblioteca/mapa-temas.md
  metricas-estilo             metricas objetivas de los articulos completos
  guardar-estilo <archivo.md> escribe biblioteca/estilo.md conservando
                              la seccion '## Reglas aprendidas'

Codigos de salida:
  0  todo correcto
  1  la operacion fallo sin destruir datos (validacion, ficha invalida...)
  2  no pudo ejecutarse (falta el inventario o la biblioteca)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import sys
import tempfile
import unicodedata
from difflib import SequenceMatcher
from datetime import date, timedelta
from pathlib import Path

# Campos de la ficha que rellena el script desde el inventario. El modelo no
# puede modificarlos: si su JSON los incluye, se ignoran.
CAMPOS_OBJETIVOS = ("id", "url", "fecha", "titulo", "huella", "basada_en", "metricas_publicas")

# Campos de juicio que entrega el modelo.
CAMPOS_JUICIO = ("tema", "subtemas", "enfoque", "tesis", "entidades", "nivel")

DIAS_TEMA_SIN_TOCAR = 183  # ~6 meses
MAX_ENTIDADES_POR_TEMA = 5
MAX_ENTIDADES_GLOBALES = 10

# Control de vocabulario: dos terminos con similitud difusa >= este umbral
# (tras normalizar minusculas y tildes) se consideran casi-duplicados.
UMBRAL_SIMILITUD = 0.85

# Campos de la ficha sujetos a control de vocabulario: (tipo singular, campo).
CAMPOS_VOCABULARIO = (("tema", "tema"), ("subtema", "subtemas"), ("entidad", "entidades"))


def normalizar_termino(termino: str) -> str:
    """Minusculas, sin tildes y con espacios colapsados, para comparar."""
    plano = unicodedata.normalize("NFD", termino.casefold())
    plano = "".join(c for c in plano if not unicodedata.combining(c))
    return " ".join(plano.split())


def similitud(a: str, b: str) -> float:
    """Similitud difusa [0, 1] entre dos terminos ya normalizados o no."""
    return SequenceMatcher(None, normalizar_termino(a), normalizar_termino(b)).ratio()


# ---------------------------------------------------------------------------
# Escritura segura
# ---------------------------------------------------------------------------

def escribir_atomico(ruta: Path, contenido: str):
    """Escribe en un temporal del mismo directorio y renombra."""
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
}


def validar_contra_esquema(dato, esquema: dict, ruta: str = "ficha") -> list[str]:
    """Valida tipos, campos obligatorios y valores permitidos.

    Devuelve la lista de errores (vacia si la ficha es valida). Soporta el
    subconjunto de JSON Schema que usa `ficha-articulo.schema.json`:
    type, required, properties, enum, items, minItems, maxItems y minLength.
    """
    errores: list[str] = []

    tipo = esquema.get("type")
    if tipo:
        esperado = _TIPOS[tipo]
        if isinstance(dato, bool) and tipo in ("integer", "number"):
            errores.append(f"{ruta}: se esperaba {tipo} y llego un booleano")
            return errores
        if not isinstance(dato, esperado):
            errores.append(f"{ruta}: se esperaba {tipo} y llego {type(dato).__name__}")
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
# Acceso a la biblioteca
# ---------------------------------------------------------------------------

class ErrorBiblioteca(Exception):
    pass


class Analizador:
    def __init__(self, raiz: Path, hoy: date | None = None):
        self.raiz = Path(raiz)
        self.hoy = hoy or date.today()
        base = self.raiz / "biblioteca"
        self.ruta_inventario = base / "substack" / "control" / "inventario.json"
        self.dir_fichas = base / "substack" / "fichas"
        self.ruta_mapa = base / "mapa-temas.md"
        self.ruta_estilo = base / "estilo.md"
        self.ruta_esquema = Path(__file__).resolve().parent.parent / "references" / "ficha-articulo.schema.json"

    # -- entradas -----------------------------------------------------------
    def cargar_inventario(self) -> dict:
        if not self.ruta_inventario.is_file():
            raise ErrorBiblioteca(
                f"No existe {self.ruta_inventario}. Ejecuta antes la skill recuperar-newsletters."
            )
        return json.loads(self.ruta_inventario.read_text(encoding="utf-8"))

    def cargar_esquema(self) -> dict:
        return json.loads(self.ruta_esquema.read_text(encoding="utf-8"))

    def cargar_fichas(self) -> dict[str, dict]:
        """Devuelve {id: ficha} con las fichas legibles; ignora las corruptas avisando."""
        fichas: dict[str, dict] = {}
        if not self.dir_fichas.is_dir():
            return fichas
        for ruta in sorted(self.dir_fichas.glob("*.json")):
            try:
                ficha = json.loads(ruta.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                print(f"AVISO: ficha ilegible, se ignora: {ruta} ({exc})", file=sys.stderr)
                continue
            fichas[str(ficha.get("id", ruta.stem))] = ficha
        return fichas

    def cuerpo_articulo(self, registro: dict) -> str | None:
        """Cuerpo del articulo sin el frontmatter, o None si el archivo falta."""
        ruta = self.raiz / registro["archivo"]
        if not ruta.is_file():
            return None
        texto = ruta.read_text(encoding="utf-8")
        partes = re.split(r"^---\s*$", texto, maxsplit=2, flags=re.MULTILINE)
        return (partes[2] if len(partes) == 3 else texto).strip()

    # -- vocabulario ----------------------------------------------------------
    @staticmethod
    def _frecuencias(fichas: dict[str, dict], campo: str) -> dict[str, list[str]]:
        """{termino: [ids de articulo]} para un campo de la ficha.

        `tema` es un string; `subtemas` y `entidades`, listas. Cada articulo
        cuenta una sola vez por termino aunque lo repita.
        """
        frec: dict[str, list[str]] = {}
        for id_post, ficha in fichas.items():
            valores = ficha.get(campo)
            if isinstance(valores, str):
                valores = [valores]
            for termino in dict.fromkeys(v for v in (valores or []) if v):
                frec.setdefault(termino, []).append(id_post)
        return frec

    @staticmethod
    def _lista_frecuencias(frec: dict[str, list[str]], clave: str) -> list[dict]:
        """Lista [{<clave>, articulos}] ordenada por frecuencia descendente."""
        return [
            {clave: termino, "articulos": len(ids)}
            for termino, ids in sorted(frec.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        ]

    def _avisos_vocabulario(self, ficha: dict, fichas_existentes: dict[str, dict]) -> list[str]:
        """Avisos por subtemas o entidades casi-duplicados de otros ya usados.

        Una coincidencia exacta tras normalizar es reutilizacion correcta y no
        avisa. Un casi-duplicado avisa pero no bloquea: la decision es de quien
        guarda, que puede corregir el JSON y reguardar.
        """
        avisos: list[str] = []
        for tipo, campo in (("subtema", "subtemas"), ("entidad", "entidades")):
            frec = self._frecuencias(fichas_existentes, campo)
            exactos = {normalizar_termino(t) for t in frec}
            for termino in dict.fromkeys(ficha.get(campo) or []):
                if normalizar_termino(termino) in exactos:
                    continue
                mejor, mejor_ratio = None, UMBRAL_SIMILITUD
                for existente in sorted(frec):
                    ratio = similitud(termino, existente)
                    if ratio >= mejor_ratio:
                        mejor, mejor_ratio = existente, ratio
                if mejor is not None:
                    avisos.append(
                        f"AVISO: {tipo} {termino!r} se parece a {mejor!r} ya usado "
                        f"({len(frec[mejor])} articulo(s)); reutiliza el existente "
                        "o reguarda si de verdad es distinto"
                    )
        return avisos

    def vocabulario(self) -> dict:
        """Vocabulario completo del corpus y pares casi-duplicados."""
        fichas = self.cargar_fichas()
        resultado: dict = {}
        sospechosos: list[dict] = []
        plural = {"tema": "temas", "subtema": "subtemas", "entidad": "entidades"}
        for tipo, campo in CAMPOS_VOCABULARIO:
            frec = self._frecuencias(fichas, campo)
            resultado[plural[tipo]] = [
                {"termino": termino, "frecuencia": len(ids), "articulos": sorted(ids)}
                for termino, ids in sorted(frec.items(), key=lambda kv: (-len(kv[1]), kv[0]))
            ]
            terminos = sorted(frec)
            for i, a in enumerate(terminos):
                for b in terminos[i + 1:]:
                    ratio = similitud(a, b)
                    if ratio >= UMBRAL_SIMILITUD:
                        sospechosos.append({
                            "tipo": tipo,
                            "termino_a": a,
                            "termino_b": b,
                            "similitud": round(ratio, 3),
                            "articulos_a": len(frec[a]),
                            "articulos_b": len(frec[b]),
                        })
        sospechosos.sort(key=lambda p: (-p["similitud"], p["tipo"], p["termino_a"], p["termino_b"]))
        resultado["sospechosos"] = sospechosos
        return resultado

    # -- pendientes -----------------------------------------------------------
    def pendientes(self) -> dict:
        inventario = self.cargar_inventario()
        fichas = self.cargar_fichas()

        pendientes = []
        for id_post, registro in sorted(inventario.items(), key=lambda kv: (kv[1].get("fecha") or "", kv[0])):
            ficha = fichas.get(id_post)
            if ficha is None:
                motivo = "sin ficha"
            elif ficha.get("huella") != registro.get("huella"):
                motivo = "huella cambiada: el contenido se modifico despues de la ultima ficha"
            else:
                continue
            pendientes.append({
                "id": id_post,
                "titulo": registro.get("titulo", ""),
                "fecha": registro.get("fecha", ""),
                "estado": registro.get("estado", ""),
                "archivo": registro.get("archivo", ""),
                "motivo": motivo,
            })

        resultado = {
            "pendientes": pendientes,
            "temas_existentes": self._lista_frecuencias(self._frecuencias(fichas, "tema"), "tema"),
            "subtemas_existentes": self._lista_frecuencias(self._frecuencias(fichas, "subtemas"), "subtema"),
            "entidades_existentes": self._lista_frecuencias(self._frecuencias(fichas, "entidades"), "entidad"),
        }
        if not pendientes:
            resultado["mensaje"] = "No hay articulos pendientes: todas las fichas estan al dia."
        return resultado

    # -- guardar --------------------------------------------------------------
    def guardar(self, id_post: str, ruta_json: Path) -> tuple[bool, str]:
        """Combina, valida y guarda la ficha. Devuelve (exito, mensaje)."""
        inventario = self.cargar_inventario()
        registro = inventario.get(str(id_post))
        if registro is None:
            return False, f"El id {id_post!r} no existe en el inventario; no se escribe nada."

        ruta_json = Path(ruta_json)
        if not ruta_json.is_file():
            return False, f"No existe el archivo JSON del modelo: {ruta_json}"
        try:
            juicio = json.loads(ruta_json.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            return False, f"El JSON del modelo es ilegible: {exc}"
        if not isinstance(juicio, dict):
            return False, "El JSON del modelo debe ser un objeto."

        ignorados = sorted(set(juicio) & set(CAMPOS_OBJETIVOS))

        ficha = {campo: juicio[campo] for campo in CAMPOS_JUICIO if campo in juicio}
        ficha.update({
            "id": str(registro["id"]),
            "url": registro.get("url", ""),
            "fecha": registro.get("fecha", ""),
            "titulo": registro.get("titulo", ""),
            "huella": registro.get("huella", ""),
            "basada_en": "extracto" if registro.get("estado") == "extracto" else "completo",
            "metricas_publicas": {
                "reacciones": (registro.get("metricas") or {}).get("reacciones", 0),
                "comentarios": (registro.get("metricas") or {}).get("comentarios", 0),
                "restacks": (registro.get("metricas") or {}).get("restacks", 0),
            },
        })

        errores = validar_contra_esquema(ficha, self.cargar_esquema())
        if errores:
            detalle = "\n".join(f"  - {e}" for e in errores)
            return False, f"Ficha invalida; no se escribe nada:\n{detalle}"

        # Control de vocabulario contra las demas fichas (no contra la version
        # anterior de esta misma), antes de escribir la nueva.
        fichas_existentes = {
            i: f for i, f in self.cargar_fichas().items() if i != ficha["id"]
        }
        avisos = self._avisos_vocabulario(ficha, fichas_existentes)

        escribir_json_atomico(self.dir_fichas / f"{ficha['id']}.json", ficha)
        mensaje = f"Ficha guardada en biblioteca/substack/fichas/{ficha['id']}.json"
        if ignorados:
            mensaje += f" (campos objetivos del JSON del modelo ignorados: {', '.join(ignorados)})"
        if avisos:
            mensaje += "\n" + "\n".join(avisos)
        return True, mensaje

    # -- mapa -----------------------------------------------------------------
    def mapa(self) -> str:
        inventario = self.cargar_inventario()
        fichas_todas = self.cargar_fichas()
        # Solo cuentan las fichas al dia de articulos que siguen en el inventario.
        fichas = {
            i: f for i, f in fichas_todas.items()
            if i in inventario and f.get("huella") == inventario[i].get("huella")
        }
        sin_ficha = [
            registro for id_post, registro in inventario.items() if id_post not in fichas
        ]
        sin_ficha.sort(key=lambda r: (r.get("fecha") or "", str(r.get("id"))))

        temas: dict[str, list[dict]] = {}
        for ficha in fichas.values():
            temas.setdefault(ficha.get("tema", "(sin tema)"), []).append(ficha)

        entidades_globales: dict[str, int] = {}
        for ficha in fichas.values():
            for entidad in ficha.get("entidades", []):
                entidades_globales[entidad] = entidades_globales.get(entidad, 0) + 1

        corte = (self.hoy - timedelta(days=DIAS_TEMA_SIN_TOCAR)).isoformat()

        lineas = [
            "# Mapa de temas",
            "",
            f"Generado el {self.hoy.isoformat()} a partir de {len(fichas)} ficha(s).",
            "",
        ]

        lineas.append("## Temas")
        lineas.append("")
        if not temas:
            lineas.append("No hay fichas todavia.")
            lineas.append("")
        for tema in sorted(temas, key=str.casefold):
            grupo = sorted(temas[tema], key=lambda f: (f.get("fecha") or "", f.get("id")))
            fechas = [f.get("fecha") for f in grupo if f.get("fecha")]
            enfoques = sorted({f.get("enfoque", "") for f in grupo if f.get("enfoque")})
            frec: dict[str, int] = {}
            for f in grupo:
                for entidad in f.get("entidades", []):
                    frec[entidad] = frec.get(entidad, 0) + 1
            top = sorted(frec.items(), key=lambda kv: (-kv[1], kv[0]))[:MAX_ENTIDADES_POR_TEMA]
            frec_sub: dict[str, int] = {}
            for f in grupo:
                for subtema in f.get("subtemas", []):
                    frec_sub[subtema] = frec_sub.get(subtema, 0) + 1
            subtemas_orden = sorted(frec_sub.items(), key=lambda kv: (-kv[1], kv[0]))
            lineas.append(f"### {tema}")
            lineas.append("")
            lineas.append(f"- Articulos: {len(grupo)}")
            if fechas:
                lineas.append(f"- Primera fecha: {min(fechas)} · Ultima fecha: {max(fechas)}")
            if enfoques:
                lineas.append(f"- Enfoques: {', '.join(enfoques)}")
            if subtemas_orden:
                lineas.append("- Subtemas tratados: " + " · ".join(
                    f"{s} ({n})" if n > 1 else s for s, n in subtemas_orden
                ))
            if top:
                lineas.append("- Entidades mas frecuentes: " + ", ".join(f"{e} ({n})" for e, n in top))
            lineas.append("")
            for f in grupo:
                titulo = f.get("titulo") or f.get("id")
                etiqueta = " · ".join(x for x in (f.get("enfoque"), f.get("nivel")) if x)
                lineas.append(f"- **{f.get('fecha', '')}** — [{titulo}]({f.get('url', '')}) ({etiqueta})")
                tesis = (f.get("tesis") or "").strip()
                if tesis:
                    lineas.append(f"  - {tesis}")
            lineas.append("")

        lineas.append(f"## Temas sin tocar en los ultimos 6 meses (desde {corte})")
        lineas.append("")
        frios = []
        for tema in sorted(temas, key=str.casefold):
            fechas = [f.get("fecha") for f in temas[tema] if f.get("fecha")]
            if fechas and max(fechas) < corte:
                frios.append(f"- {tema} (ultimo articulo: {max(fechas)})")
        lineas.extend(frios if frios else ["Ninguno."])
        lineas.append("")

        lineas.append("## Entidades mas frecuentes en toda la biblioteca")
        lineas.append("")
        top_global = sorted(entidades_globales.items(), key=lambda kv: (-kv[1], kv[0]))[:MAX_ENTIDADES_GLOBALES]
        lineas.extend([f"- {e}: {n} articulo(s)" for e, n in top_global] if top_global else ["Ninguna."])
        lineas.append("")

        if sin_ficha:
            lineas.append("## Articulos sin ficha (el mapa NO esta completo)")
            lineas.append("")
            for r in sin_ficha:
                lineas.append(f"- {r.get('fecha', '')} — {r.get('titulo', '')} (id {r.get('id')})")
            lineas.append("")
        else:
            lineas.append("## Cobertura")
            lineas.append("")
            lineas.append("Todos los articulos del inventario tienen ficha al dia: el mapa esta completo.")
            lineas.append("")

        contenido = "\n".join(lineas)
        escribir_atomico(self.ruta_mapa, contenido)
        return contenido

    # -- metricas de estilo -----------------------------------------------------
    def metricas_estilo(self) -> dict:
        inventario = self.cargar_inventario()
        completos = [
            r for r in inventario.values() if r.get("estado") == "completo"
        ]
        completos.sort(key=lambda r: (r.get("fecha") or "", str(r.get("id"))))

        palabras_por_articulo: list[int] = []
        secciones_por_articulo: list[int] = []
        longitudes_frase: list[float] = []
        con_listas = con_citas = con_imagenes = 0
        analizados = 0

        for registro in completos:
            cuerpo = self.cuerpo_articulo(registro)
            if cuerpo is None:
                continue
            analizados += 1
            palabras_por_articulo.append(len(cuerpo.split()))
            secciones_por_articulo.append(
                len(re.findall(r"^#{1,6}\s", cuerpo, flags=re.MULTILINE))
            )
            if re.search(r"^\s*([-*]|\d+\.)\s", cuerpo, flags=re.MULTILINE):
                con_listas += 1
            if re.search(r"^\s*>", cuerpo, flags=re.MULTILINE):
                con_citas += 1
            if "![" in cuerpo:
                con_imagenes += 1

            texto_plano = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", cuerpo)
            texto_plano = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", texto_plano)
            texto_plano = re.sub(r"^#{1,6}\s.*$", "", texto_plano, flags=re.MULTILINE)
            texto_plano = re.sub(r"[`*>_#]", "", texto_plano)
            frases = [f.strip() for f in re.split(r"[.!?]+", texto_plano) if f.strip()]
            if frases:
                longitudes_frase.append(
                    sum(len(f.split()) for f in frases) / len(frases)
                )

        def media(valores):
            return round(sum(valores) / len(valores), 1) if valores else 0

        return {
            "articulos_completos_analizados": analizados,
            "extractos_ignorados": len(inventario) - len(completos),
            "palabras": {
                "media": media(palabras_por_articulo),
                "mediana": statistics.median(palabras_por_articulo) if palabras_por_articulo else 0,
            },
            "secciones": {"media": media(secciones_por_articulo)},
            "frases": {"longitud_media_palabras": media(longitudes_frase)},
            "uso": {
                "articulos_con_listas": con_listas,
                "articulos_con_citas": con_citas,
                "articulos_con_imagenes": con_imagenes,
            },
        }

    # -- guardar estilo -----------------------------------------------------------
    def guardar_estilo(self, ruta_md: Path) -> tuple[bool, str]:
        ruta_md = Path(ruta_md)
        if not ruta_md.is_file():
            return False, f"No existe el archivo de estilo: {ruta_md}"
        nuevo = ruta_md.read_text(encoding="utf-8")

        reglas = None
        if self.ruta_estilo.is_file():
            actual = self.ruta_estilo.read_text(encoding="utf-8")
            encontrado = re.search(
                r"^## Reglas aprendidas\s*$.*?(?=^## |\Z)", actual, flags=re.MULTILINE | re.DOTALL
            )
            if encontrado:
                reglas = encontrado.group(0).rstrip() + "\n"

        if reglas is not None:
            patron = re.compile(r"^## Reglas aprendidas\s*$.*?(?=^## |\Z)", flags=re.MULTILINE | re.DOTALL)
            if patron.search(nuevo):
                nuevo = patron.sub(lambda _m: reglas, nuevo, count=1)
            else:
                nuevo = nuevo.rstrip() + "\n\n" + reglas

        escribir_atomico(self.ruta_estilo, nuevo)
        detalle = " (seccion '## Reglas aprendidas' conservada)" if reglas is not None else ""
        return True, f"Guia de estilo guardada en biblioteca/estilo.md{detalle}"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    analizador_args = argparse.ArgumentParser(
        description="Analiza la biblioteca: fichas, mapa de temas y metricas de estilo."
    )
    analizador_args.add_argument("comando", choices=["pendientes", "guardar", "vocabulario", "mapa", "metricas-estilo", "guardar-estilo"])
    analizador_args.add_argument("resto", nargs="*", help="Argumentos del comando")
    analizador_args.add_argument("--raiz", default=".", help="Raiz del proyecto (contiene biblioteca/)")
    analizador_args.add_argument("--hoy", default=None, help="Fecha YYYY-MM-DD para calculos de fecha (pruebas)")
    args = analizador_args.parse_args(argv)

    hoy = date.fromisoformat(args.hoy) if args.hoy else None
    analizador = Analizador(Path(args.raiz), hoy=hoy)

    try:
        if args.comando == "pendientes":
            print(json.dumps(analizador.pendientes(), ensure_ascii=False, indent=2))
            return 0

        if args.comando == "guardar":
            if len(args.resto) != 2:
                print("Uso: guardar <id> <archivo.json>", file=sys.stderr)
                return 2
            exito, mensaje = analizador.guardar(args.resto[0], Path(args.resto[1]))
            print(mensaje, file=sys.stdout if exito else sys.stderr)
            return 0 if exito else 1

        if args.comando == "vocabulario":
            print(json.dumps(analizador.vocabulario(), ensure_ascii=False, indent=2))
            return 0

        if args.comando == "mapa":
            analizador.mapa()
            print(f"Mapa regenerado en {analizador.ruta_mapa}")
            return 0

        if args.comando == "metricas-estilo":
            print(json.dumps(analizador.metricas_estilo(), ensure_ascii=False, indent=2))
            return 0

        if args.comando == "guardar-estilo":
            if len(args.resto) != 1:
                print("Uso: guardar-estilo <archivo.md>", file=sys.stderr)
                return 2
            exito, mensaje = analizador.guardar_estilo(Path(args.resto[0]))
            print(mensaje, file=sys.stdout if exito else sys.stderr)
            return 0 if exito else 1
    except ErrorBiblioteca as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    return 2  # inalcanzable


if __name__ == "__main__":
    sys.exit(main())
