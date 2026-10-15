#!/usr/bin/env python3
"""Prepara, valida y guarda la investigación de una oportunidad aceptada.

Parte "script" de la skill investigar-tema (primera parte de la fase 3 de
ARQUITECTURA.md). El modelo busca fuentes en internet, verifica afirmaciones
y redacta; este script hace lo repetible: comprobar que la oportunidad está
aceptada, reunir las afirmaciones a verificar, validar y guardar las fuentes,
comprobar que los enlaces responden y validar que cada afirmación tiene
estado y fuente antes de guardar la investigación.

Comandos (desde la raíz del proyecto):
  preparar <id>                          comprueba la oportunidad, crea contenidos/<id>/ y genera afirmaciones.json
  guardar-fuentes <id> <archivo.json>    valida las fuentes y las añade a fuentes.json conservando las anteriores
  comprobar-enlaces <id>                 pide cada URL y registra el código y la fecha en fuentes.json
  guardar-investigacion <id> <archivo.md>  valida la investigación y la guarda con el encabezado del script
  guardar-revision <id> <archivo.md>     guarda el informe del verificador en revision.md

Códigos de salida:
  0  correcto
  1  avisos (p. ej. enlaces rotos o una evidencia que no se pudo resolver)
  2  no pudo ejecutarse o la validación falló

Las escrituras son atómicas. Nunca se sobrescribe una investigación con
`estado: aprobada`: la aprobación la marca la persona en el encabezado.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import time
import unicodedata
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

CODIGO_OK = 0
CODIGO_AVISOS = 1
CODIGO_FATAL = 2

SECCIONES_INVESTIGACION = [
    "## Pregunta de investigación",
    "## Resumen",
    "## Verificación de afirmaciones",
    "## Hallazgos nuevos",
    "## Contradicciones y límites",
    "## Prueba práctica",
    "## Ángulo propuesto",
    "## Fuentes",
]

ESTADOS_AFIRMACION = ("verificada", "refutada", "sin_confirmar")
SECCION_INVESTIGAR = "## Qué hay que investigar o probar"


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def quitar_tildes(texto: str) -> str:
    descompuesto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in descompuesto if not unicodedata.combining(c))


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


def extraer_seccion(cuerpo: str, titulo: str) -> str:
    """Devuelve el contenido de una sección `## …` (sin el título)."""
    patron = re.compile(
        rf"^{re.escape(titulo)}\s*$(.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL
    )
    coincidencia = patron.search(cuerpo)
    return coincidencia.group(1).strip() if coincidencia else ""


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

    if isinstance(dato, str):
        if "minLength" in esquema and len(dato.strip()) < esquema["minLength"]:
            errores.append(f"{ruta}: no puede estar vacío")
        if "pattern" in esquema and not re.fullmatch(esquema["pattern"], dato):
            errores.append(f"{ruta}: {dato!r} no cumple el formato {esquema['pattern']}")

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
# Red (sustituible en pruebas)
# ---------------------------------------------------------------------------

def pedir_url(url: str, timeout: float) -> tuple[int | None, str | None]:
    """Devuelve (código HTTP, None) o (None, error). HEAD, y GET si HEAD no se acepta."""
    for metodo in ("HEAD", "GET"):
        peticion = urllib.request.Request(
            url, method=metodo, headers={"User-Agent": "investigar-tema/1.0"}
        )
        try:
            with urllib.request.urlopen(peticion, timeout=timeout) as respuesta:
                return respuesta.status, None
        except urllib.error.HTTPError as exc:
            if metodo == "HEAD" and exc.code in (403, 405, 501):
                continue  # el servidor no acepta HEAD: probar con GET
            return exc.code, None
        except Exception as exc:  # URLError, timeout, etc.
            error = str(exc)
    return None, error


# ---------------------------------------------------------------------------
# Investigador
# ---------------------------------------------------------------------------

class Investigador:
    def __init__(self, ruta_config: Path, hoy: str | None = None):
        self.ruta_config = Path(ruta_config)
        if not self.ruta_config.is_file():
            raise RuntimeError(f"No existe el archivo de configuración: {self.ruta_config}")
        try:
            self.config = json.loads(self.ruta_config.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Configuración ilegible ({self.ruta_config}): {exc}") from exc
        self.raiz = self.ruta_config.resolve().parent
        self.hoy = hoy or date.today().isoformat()
        self.dir_biblioteca = self.raiz / "biblioteca"
        self.dir_oportunidades = self.dir_biblioteca / "oportunidades"
        self.dir_contenidos = self.dir_biblioteca / "contenidos"
        self.ruta_inventario = self.dir_biblioteca / "substack" / "control" / "inventario.json"
        self.ruta_esquema_fuentes = (
            Path(__file__).resolve().parent.parent / "references" / "fuentes.schema.json"
        )
        red = self.config.get("red", {})
        self.timeout = red.get("timeout_segundos", 30)
        self.intentos = red.get("intentos", 3)
        self.pausa = red.get("pausa_segundos", 0.5)
        self.avisos: list[str] = []

    def avisar(self, mensaje: str):
        self.avisos.append(mensaje)
        print(f"AVISO: {mensaje}", file=sys.stderr)

    def _fatal(self, mensaje: str) -> int:
        print(f"ERROR: {mensaje}", file=sys.stderr)
        return CODIGO_FATAL

    def _salida(self) -> int:
        return CODIGO_AVISOS if self.avisos else CODIGO_OK

    # -- carga de datos ------------------------------------------------------

    def dir_contenido(self, oportunidad_id: str) -> Path:
        return self.dir_contenidos / oportunidad_id

    def cargar_oportunidad(self, oportunidad_id: str) -> tuple[dict, str] | None:
        ruta = self.dir_oportunidades / f"{oportunidad_id}.md"
        if not ruta.is_file():
            return None
        return parsear_frontmatter(ruta.read_text(encoding="utf-8"))

    def cargar_fichas_externas(self) -> dict[str, dict]:
        """Todas las fichas externas, indexadas por `fuente:id`."""
        fichas: dict[str, dict] = {}
        if not self.dir_biblioteca.is_dir():
            return fichas
        no_fuente = {"substack", "oportunidades", "contenidos"}
        for carpeta in sorted(self.dir_biblioteca.iterdir()):
            if not carpeta.is_dir() or carpeta.name in no_fuente:
                continue
            for ruta in sorted(carpeta.rglob("ficha.json")):
                try:
                    ficha = json.loads(ruta.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError) as exc:
                    self.avisar(f"ficha externa ilegible, se omite: {ruta} ({exc})")
                    continue
                if "id" not in ficha or "fuente" not in ficha:
                    self.avisar(f"ficha externa sin id o fuente, se omite: {ruta}")
                    continue
                fichas[f"{ficha['fuente']}:{ficha['id']}"] = ficha
        return fichas

    def cargar_json(self, ruta: Path):
        try:
            return json.loads(ruta.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"archivo ilegible: {ruta} ({exc})") from exc

    # -- preparar ------------------------------------------------------------

    def extraer_afirmaciones(self, oportunidad_id: str, encabezado: dict, cuerpo: str,
                             fichas: dict[str, dict]) -> tuple[list[dict], list[str]]:
        """Afirmaciones de las evidencias citadas y de la sección de investigación."""
        afirmaciones: list[dict] = []
        citadas: list[str] = []
        evidencias = encabezado.get("evidencias", [])
        if isinstance(evidencias, str):
            evidencias = [evidencias] if evidencias else []
        vistas = set()
        for evidencia in evidencias:
            if evidencia in vistas:
                continue
            vistas.add(evidencia)
            coincidencia = re.fullmatch(r"([^:@]+):([^@]+)@(.+)", evidencia)
            if not coincidencia:
                self.avisar(f"evidencia con formato desconocido, se omite: {evidencia}")
                continue
            fuente, ficha_id, marca = coincidencia.groups()
            ficha = fichas.get(f"{fuente}:{ficha_id}")
            if ficha is None:
                self.avisar(f"no se encontró la ficha externa de la evidencia {evidencia}")
                continue
            if f"{fuente}:{ficha_id}" not in citadas:
                citadas.append(f"{fuente}:{ficha_id}")
            encontrada = next(
                (a for a in ficha.get("afirmaciones", []) if a.get("marca") == marca), None
            )
            if encontrada is None:
                self.avisar(f"la ficha {fuente}:{ficha_id} no tiene una afirmación en la marca {marca}")
                continue
            afirmaciones.append({
                "texto": encontrada["texto"],
                "origen": evidencia,
                "tipo": encontrada.get("tipo", "dato"),
            })
        # Lo que la oportunidad pide comprobar.
        seccion = extraer_seccion(cuerpo, SECCION_INVESTIGAR)
        elementos = re.findall(r"^\s*(?:[-*]|\d+[.)])\s+(.+)$", seccion, re.MULTILINE)
        if not elementos:
            elementos = [l.strip() for l in seccion.splitlines() if l.strip()]
        for texto in elementos:
            afirmaciones.append({
                "texto": texto.strip(),
                "origen": f"oportunidad:{oportunidad_id}",
                "tipo": "a_comprobar",
            })
        for i, afirmacion in enumerate(afirmaciones, start=1):
            afirmacion["id"] = f"a{i}"
        # id primero, para que el archivo se lea bien.
        afirmaciones = [
            {"id": a["id"], "texto": a["texto"], "origen": a["origen"], "tipo": a["tipo"]}
            for a in afirmaciones
        ]
        return afirmaciones, citadas

    def rutas_relacionados(self, encabezado: dict) -> list[dict]:
        inventario = {}
        if self.ruta_inventario.is_file():
            try:
                inventario = json.loads(self.ruta_inventario.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                self.avisar(f"inventario ilegible: {self.ruta_inventario} ({exc})")
        relacionados = encabezado.get("relacionados", [])
        if isinstance(relacionados, str):
            relacionados = [relacionados] if relacionados else []
        resultado = []
        for referencia in relacionados:
            post_id = referencia.split(":", 1)[1] if ":" in referencia else referencia
            registro = inventario.get(post_id) or {}
            ruta = registro.get("archivo")
            if not ruta:
                self.avisar(f"el inventario no tiene la ruta del artículo relacionado {referencia}")
            resultado.append({"referencia": referencia, "ruta_texto": ruta})
        return resultado

    def cmd_preparar(self, oportunidad_id: str) -> int:
        cargada = self.cargar_oportunidad(oportunidad_id)
        if cargada is None:
            return self._fatal(
                f"no existe la oportunidad biblioteca/oportunidades/{oportunidad_id}.md"
            )
        encabezado, cuerpo = cargada
        estado = encabezado.get("estado", "(sin estado)")
        if estado != "aceptada":
            return self._fatal(
                f"la oportunidad '{oportunidad_id}' tiene estado '{estado}' y solo se "
                "investiga una oportunidad con estado 'aceptada'; el estado lo cambia "
                "la persona en el encabezado"
            )

        carpeta = self.dir_contenido(oportunidad_id)
        carpeta.mkdir(parents=True, exist_ok=True)
        ruta_investigacion = carpeta / "investigacion.md"
        ruta_afirmaciones = carpeta / "afirmaciones.json"
        investigacion_existente = ruta_investigacion.is_file()
        if investigacion_existente:
            self.avisar(
                f"ya existe una investigación en {ruta_investigacion}; no se toca y se "
                "conserva afirmaciones.json tal como está"
            )

        fichas = self.cargar_fichas_externas()
        if investigacion_existente and ruta_afirmaciones.is_file():
            afirmaciones = self.cargar_json(ruta_afirmaciones)
            citadas = sorted({
                a["origen"].rsplit("@", 1)[0]
                for a in afirmaciones
                if not a["origen"].startswith("oportunidad:")
            })
        else:
            afirmaciones, citadas = self.extraer_afirmaciones(
                oportunidad_id, encabezado, cuerpo, fichas
            )
            escribir_json_atomico(ruta_afirmaciones, afirmaciones)

        paquete = {
            "oportunidad": {
                "id": oportunidad_id,
                "ruta": str(self.dir_oportunidades / f"{oportunidad_id}.md"),
                "encabezado": encabezado,
                "cuerpo": cuerpo,
            },
            "afirmaciones": afirmaciones,
            "fichas_citadas": [fichas[c] for c in citadas if c in fichas],
            "articulos_relacionados": self.rutas_relacionados(encabezado),
            "investigacion_existente": investigacion_existente,
        }
        print(json.dumps(paquete, ensure_ascii=False, indent=2))
        return self._salida()

    # -- guardar-fuentes -----------------------------------------------------

    def _cargar_estado_contenido(self, oportunidad_id: str) -> tuple[Path, list[dict]]:
        carpeta = self.dir_contenido(oportunidad_id)
        ruta_afirmaciones = carpeta / "afirmaciones.json"
        if not ruta_afirmaciones.is_file():
            raise RuntimeError(
                f"no existe {ruta_afirmaciones}; ejecuta antes 'preparar {oportunidad_id}'"
            )
        return carpeta, self.cargar_json(ruta_afirmaciones)

    def cmd_guardar_fuentes(self, oportunidad_id: str, archivo: Path) -> int:
        try:
            carpeta, afirmaciones = self._cargar_estado_contenido(oportunidad_id)
            nuevas = self.cargar_json(Path(archivo))
        except RuntimeError as exc:
            return self._fatal(str(exc))

        esquema = json.loads(self.ruta_esquema_fuentes.read_text(encoding="utf-8"))
        errores = validar_contra_esquema(nuevas, esquema, "fuentes")

        ruta_fuentes = carpeta / "fuentes.json"
        existentes: list[dict] = []
        if ruta_fuentes.is_file():
            try:
                existentes = self.cargar_json(ruta_fuentes)
            except RuntimeError as exc:
                return self._fatal(str(exc))

        ids_existentes = {f["id"] for f in existentes}
        ids_afirmaciones = {a["id"] for a in afirmaciones}
        vistos: set[str] = set()
        for i, fuente in enumerate(nuevas if isinstance(nuevas, list) else []):
            if not isinstance(fuente, dict):
                continue
            fid = fuente.get("id")
            if fid in vistos:
                errores.append(f"fuentes[{i}]: id duplicado en el archivo: '{fid}'")
            elif fid in ids_existentes:
                errores.append(f"fuentes[{i}]: id '{fid}' ya existe en fuentes.json")
            if isinstance(fid, str):
                vistos.add(fid)
            for campo in ("respalda", "contradice"):
                for aid in fuente.get(campo, []):
                    if aid not in ids_afirmaciones:
                        errores.append(
                            f"fuentes[{i}].{campo}: la afirmación '{aid}' no existe en afirmaciones.json"
                        )

        if errores:
            print("ERROR: las fuentes no se guardan:", file=sys.stderr)
            for e in errores:
                print(f"  - {e}", file=sys.stderr)
            return CODIGO_FATAL

        escribir_json_atomico(ruta_fuentes, existentes + nuevas)
        print(json.dumps({
            "fuentes_anadidas": len(nuevas),
            "fuentes_totales": len(existentes) + len(nuevas),
            "archivo": str(ruta_fuentes),
        }, ensure_ascii=False, indent=2))
        return self._salida()

    # -- comprobar-enlaces ---------------------------------------------------

    def cmd_comprobar_enlaces(self, oportunidad_id: str) -> int:
        carpeta = self.dir_contenido(oportunidad_id)
        ruta_fuentes = carpeta / "fuentes.json"
        if not ruta_fuentes.is_file():
            return self._fatal(
                f"no existe {ruta_fuentes}; guarda fuentes antes con 'guardar-fuentes'"
            )
        try:
            fuentes = self.cargar_json(ruta_fuentes)
        except RuntimeError as exc:
            return self._fatal(str(exc))

        rotos = 0
        for fuente in fuentes:
            codigo, error = None, None
            for intento in range(self.intentos):
                codigo, error = pedir_url(fuente["url"], self.timeout)
                if codigo is not None:
                    break
                if intento < self.intentos - 1:
                    time.sleep(self.pausa)
            fuente["comprobacion"] = {"codigo": codigo, "fecha": self.hoy}
            if error is not None:
                fuente["comprobacion"]["error"] = error
            if codigo is None or codigo >= 400:
                rotos += 1
                detalle = error if codigo is None else f"HTTP {codigo}"
                self.avisar(
                    f"enlace roto en la fuente {fuente['id']} ({fuente['url']}): {detalle}; "
                    "la fuente se conserva"
                )
        escribir_json_atomico(ruta_fuentes, fuentes)
        print(json.dumps({
            "fuentes_comprobadas": len(fuentes),
            "enlaces_rotos": rotos,
            "archivo": str(ruta_fuentes),
        }, ensure_ascii=False, indent=2))
        return self._salida()

    # -- guardar-investigacion -----------------------------------------------

    @staticmethod
    def parsear_tabla_verificacion(seccion: str) -> dict[str, dict]:
        """Filas `| a1 | texto | estado | f1, f2 | nota |` → {a1: {estado, fuentes}}."""
        filas: dict[str, dict] = {}
        for linea in seccion.splitlines():
            limpia = linea.strip()
            if not limpia.startswith("|"):
                continue
            celdas = [c.strip() for c in limpia.strip("|").split("|")]
            if len(celdas) < 4 or not re.fullmatch(r"a\d+", celdas[0]):
                continue
            fuentes = [
                f for f in re.split(r"[,\s]+", celdas[3]) if re.fullmatch(r"f\d+", f)
            ]
            filas[celdas[0]] = {"estado": celdas[2], "fuentes": fuentes}
        return filas

    def validar_investigacion(self, cuerpo: str, afirmaciones: list[dict],
                              fuentes: list[dict]) -> list[str]:
        errores: list[str] = []

        # 1. Secciones obligatorias de la plantilla, en orden y con contenido.
        posiciones = []
        for seccion in SECCIONES_INVESTIGACION:
            coincidencia = re.search(rf"^{re.escape(seccion)}\s*$", cuerpo, re.MULTILINE)
            if not coincidencia:
                errores.append(f"falta la sección '{seccion}'")
                posiciones.append(None)
            else:
                posiciones.append(coincidencia.start())
                if not extraer_seccion(cuerpo, seccion):
                    errores.append(f"la sección '{seccion}' está vacía")
        validas = [p for p in posiciones if p is not None]
        if validas != sorted(validas):
            errores.append("las secciones no están en el orden de la plantilla")

        # 2. Tabla de verificación: cada afirmación con estado y fuentes.
        tabla = self.parsear_tabla_verificacion(
            extraer_seccion(cuerpo, "## Verificación de afirmaciones")
        )
        por_fuente = {f["id"]: f for f in fuentes}
        for afirmacion in afirmaciones:
            aid = afirmacion["id"]
            fila = tabla.get(aid)
            if fila is None:
                errores.append(f"la afirmación '{aid}' no aparece en la tabla de verificación")
                continue
            if fila["estado"] not in ESTADOS_AFIRMACION:
                errores.append(
                    f"la afirmación '{aid}' tiene estado '{fila['estado']}'; debe ser uno de: "
                    + ", ".join(ESTADOS_AFIRMACION)
                )
                continue
            if fila["estado"] in ("verificada", "refutada"):
                citadas = fila["fuentes"]
                if not citadas:
                    errores.append(f"la afirmación '{aid}' está '{fila['estado']}' sin ninguna fuente")
                    continue
                desconocidas = [f for f in citadas if f not in por_fuente]
                if desconocidas:
                    errores.append(
                        f"la afirmación '{aid}' cita fuentes que no están en fuentes.json: "
                        + ", ".join(desconocidas)
                    )
                    continue
                no_video = [
                    f for f in citadas
                    if quitar_tildes(por_fuente[f].get("tipo", "")) != "video"
                ]
                if not no_video:
                    errores.append(
                        f"la afirmación '{aid}' está '{fila['estado']}' solo con fuentes de "
                        "tipo vídeo; el vídeo de origen no basta para verificarse a sí mismo"
                    )

        # 3. Toda referencia [f<n>] del texto debe existir en fuentes.json.
        for ref in sorted(set(re.findall(r"\[(f\d+)\]", cuerpo))):
            if ref not in por_fuente:
                errores.append(f"la referencia [{ref}] no existe en fuentes.json")

        return errores

    def cmd_guardar_investigacion(self, oportunidad_id: str, archivo: Path) -> int:
        try:
            carpeta, afirmaciones = self._cargar_estado_contenido(oportunidad_id)
        except RuntimeError as exc:
            return self._fatal(str(exc))
        ruta_fuentes = carpeta / "fuentes.json"
        if not ruta_fuentes.is_file():
            return self._fatal(
                f"no existe {ruta_fuentes}; guarda fuentes antes con 'guardar-fuentes'"
            )
        archivo = Path(archivo)
        if not archivo.is_file():
            return self._fatal(f"no existe el archivo {archivo}")
        try:
            fuentes = self.cargar_json(ruta_fuentes)
        except RuntimeError as exc:
            return self._fatal(str(exc))

        ruta_investigacion = carpeta / "investigacion.md"
        if ruta_investigacion.is_file():
            encabezado_actual, _ = parsear_frontmatter(
                ruta_investigacion.read_text(encoding="utf-8")
            )
            if encabezado_actual.get("estado") == "aprobada":
                return self._fatal(
                    "la investigación existente tiene estado 'aprobada' y no se sobrescribe; "
                    "la aprobación la marca la persona en el encabezado"
                )

        contenido = archivo.read_text(encoding="utf-8")
        encabezado_modelo, cuerpo = parsear_frontmatter(contenido)
        if encabezado_modelo:
            self.avisar("el archivo traía un encabezado; se descarta: el encabezado lo escribe el script")

        errores = self.validar_investigacion(cuerpo, afirmaciones, fuentes)
        if errores:
            print("ERROR: la investigación no se guarda:", file=sys.stderr)
            for e in errores:
                print(f"  - {e}", file=sys.stderr)
            return CODIGO_FATAL

        encabezado = {
            "oportunidad": oportunidad_id,
            "estado": "pendiente_aprobacion",
            "fecha": self.hoy,
        }
        escribir_atomico(
            ruta_investigacion, componer_frontmatter(encabezado) + "\n" + cuerpo.strip() + "\n"
        )
        tabla = self.parsear_tabla_verificacion(
            extraer_seccion(cuerpo, "## Verificación de afirmaciones")
        )
        recuento = {estado: 0 for estado in ESTADOS_AFIRMACION}
        for fila in tabla.values():
            if fila["estado"] in recuento:
                recuento[fila["estado"]] += 1
        print(json.dumps({
            "archivo": str(ruta_investigacion),
            "estado": "pendiente_aprobacion",
            "afirmaciones": recuento,
        }, ensure_ascii=False, indent=2))
        return self._salida()

    # -- guardar-revision ----------------------------------------------------

    def cmd_guardar_revision(self, oportunidad_id: str, archivo: Path) -> int:
        carpeta = self.dir_contenido(oportunidad_id)
        if not carpeta.is_dir():
            return self._fatal(
                f"no existe {carpeta}; ejecuta antes 'preparar {oportunidad_id}'"
            )
        archivo = Path(archivo)
        if not archivo.is_file():
            return self._fatal(f"no existe el archivo {archivo}")
        contenido = archivo.read_text(encoding="utf-8").strip()
        if not contenido:
            return self._fatal("el informe del verificador está vacío")
        ruta = carpeta / "revision.md"
        escribir_atomico(ruta, contenido + "\n")
        print(json.dumps({"archivo": str(ruta)}, ensure_ascii=False, indent=2))
        return self._salida()


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
        description="Prepara, valida y guarda la investigación de una oportunidad aceptada."
    )
    analizador.add_argument(
        "--config", default="proyecto.config.json",
        help="Ruta de proyecto.config.json (por defecto, el del directorio actual).",
    )
    analizador.add_argument(
        "--hoy", default=None,
        help="Fecha YYYY-MM-DD para los registros (por defecto, la de hoy). Útil en pruebas.",
    )
    subcomandos = analizador.add_subparsers(dest="comando", required=True)
    p = subcomandos.add_parser("preparar", help="Comprueba la oportunidad y genera afirmaciones.json.")
    p.add_argument("oportunidad_id")
    p = subcomandos.add_parser("guardar-fuentes", help="Valida y añade fuentes a fuentes.json.")
    p.add_argument("oportunidad_id")
    p.add_argument("archivo", help="JSON con la lista de fuentes, según fuentes.schema.json.")
    p = subcomandos.add_parser("comprobar-enlaces", help="Registra el código de respuesta de cada URL.")
    p.add_argument("oportunidad_id")
    p = subcomandos.add_parser("guardar-investigacion", help="Valida y guarda investigacion.md.")
    p.add_argument("oportunidad_id")
    p.add_argument("archivo", help="Markdown con el cuerpo (plantilla-investigacion.md).")
    p = subcomandos.add_parser("guardar-revision", help="Guarda el informe del verificador en revision.md.")
    p.add_argument("oportunidad_id")
    p.add_argument("archivo", help="Markdown con el informe del verificador.")

    args = analizador.parse_args(argv)
    try:
        investigador = Investigador(Path(args.config), hoy=args.hoy)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return CODIGO_FATAL

    try:
        if args.comando == "preparar":
            return investigador.cmd_preparar(args.oportunidad_id)
        if args.comando == "guardar-fuentes":
            return investigador.cmd_guardar_fuentes(args.oportunidad_id, Path(args.archivo))
        if args.comando == "comprobar-enlaces":
            return investigador.cmd_comprobar_enlaces(args.oportunidad_id)
        if args.comando == "guardar-investigacion":
            return investigador.cmd_guardar_investigacion(args.oportunidad_id, Path(args.archivo))
        if args.comando == "guardar-revision":
            return investigador.cmd_guardar_revision(args.oportunidad_id, Path(args.archivo))
    except OSError as exc:
        print(f"ERROR: no pudo ejecutarse: {exc}", file=sys.stderr)
        return CODIGO_FATAL
    return CODIGO_FATAL


if __name__ == "__main__":
    sys.exit(main())
