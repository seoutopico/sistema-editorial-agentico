#!/usr/bin/env python3
"""Prepara, valida y guarda las piezas de cada canal de publicación.

Parte "script" de la skill adaptar-contenido (fase 4 de ARQUITECTURA.md).
El modelo adapta el contenido principal aprobado a cada canal siguiendo su
plantilla; este script hace lo repetible: comprobar que el principal está
aprobado, saber qué canales hay que preparar, comprobar los límites que
declara cada plantilla y guardar las piezas.

Cada canal es un archivo en `references/canales/<canal>.md` cuyo encabezado
declara los límites (`max_caracteres`, `min_caracteres`, `enlace_obligatorio`,
`max_hashtags` y, si la pieza tiene campos, `campos` con límites por campo).
Añadir un canal es añadir su plantilla y su nombre en `canales_salida` de
`proyecto.config.json`, sin tocar este código.

Comandos (desde la raíz del proyecto):
  preparar <id>                        comprueba el principal aprobado y devuelve los canales pendientes
  guardar <id> <canal> <archivo.md>    valida la pieza del modelo y la escribe en piezas/<canal>.md
  comprobar <id>                       revisa todas las piezas actuales sin modificar nada
  enlazar <id> <url>                   sustituye {{enlace}} por la URL publicada en todas las piezas

Códigos de salida:
  0  correcto
  1  avisos
  2  no pudo ejecutarse o la validación falló

Las escrituras son atómicas. Una pieza con `estado: aprobado` no se
sobrescribe nunca; una pieza en borrador solo se sustituye con `--reemplazar`.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import date
from pathlib import Path

CODIGO_OK = 0
CODIGO_AVISOS = 1
CODIGO_FATAL = 2

MARCADOR_ENLACE = "{{enlace}}"

# Un hashtag es `#palabra` que no forma parte de un encabezado Markdown
# (`# Título`, `## Sección`) ni de una URL (`…/p#seccion`).
PATRON_HASHTAG = re.compile(r"(?<![\w#&/])#(\w+)")


# ---------------------------------------------------------------------------
# Utilidades (compartidas con las demás skills por copia: cada skill es autónoma)
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


def parsear_frontmatter(texto: str) -> tuple[dict, str]:
    """Devuelve (encabezado, cuerpo). Claves simples, listas en línea y booleanos."""
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
        elif bruto.lower() in ("true", "false"):
            valor = bruto.lower() == "true"
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


def extraer_campo(cuerpo: str, campo: str) -> str | None:
    """El texto bajo `## <campo>` (sin distinguir mayúsculas), o None si falta."""
    patron = re.compile(
        rf"^##\s+{re.escape(campo)}\s*$(.*?)(?=^##\s|\Z)",
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    coincidencia = patron.search(cuerpo)
    return coincidencia.group(1).strip() if coincidencia else None


def contar_hashtags(texto: str) -> int:
    return len(PATRON_HASHTAG.findall(texto))


def tiene_enlace(texto: str) -> bool:
    return MARCADOR_ENLACE in texto or bool(re.search(r"https?://\S+", texto))


# ---------------------------------------------------------------------------
# Validación por límites de plantilla
# ---------------------------------------------------------------------------

CLAVES_LIMITES = ("canal", "campos", "enlace_obligatorio", "max_hashtags")


def limites_de_plantilla(encabezado: dict) -> dict:
    """Solo las claves de límites del encabezado de la plantilla."""
    limites = {}
    for clave, valor in encabezado.items():
        if clave in CLAVES_LIMITES or clave.startswith(("max_caracteres", "min_caracteres")):
            limites[clave] = valor
    return limites


def _comprobar_longitud(texto: str, minimo, maximo, donde: str, errores: list[str]):
    n = len(texto.strip())
    if isinstance(maximo, int) and n > maximo:
        errores.append(f"{donde} tiene {n} caracteres y el máximo es {maximo}")
    if isinstance(minimo, int) and n < minimo:
        errores.append(f"{donde} tiene {n} caracteres y el mínimo es {minimo}")


def validar_pieza(cuerpo: str, limites: dict) -> list[str]:
    """Errores de la pieza frente a los límites de su plantilla."""
    errores: list[str] = []
    campos = limites.get("campos") or []

    if campos:
        # Pieza con campos (p. ej. substack): los límites se aplican a cada campo,
        # con `max_caracteres_<campo>` / `min_caracteres_<campo>` por encima de
        # los generales.
        for campo in campos:
            texto = extraer_campo(cuerpo, campo)
            if texto is None:
                errores.append(f"falta la sección '## {campo}' que pide la plantilla")
                continue
            if not texto:
                errores.append(f"la sección '## {campo}' está vacía")
                continue
            _comprobar_longitud(
                texto,
                limites.get(f"min_caracteres_{campo}", limites.get("min_caracteres")),
                limites.get(f"max_caracteres_{campo}", limites.get("max_caracteres")),
                f"el campo '{campo}'",
                errores,
            )
    else:
        _comprobar_longitud(
            cuerpo,
            limites.get("min_caracteres"),
            limites.get("max_caracteres"),
            "la pieza",
            errores,
        )

    if limites.get("enlace_obligatorio") and not tiene_enlace(cuerpo):
        errores.append(
            "la plantilla exige un enlace y la pieza no tiene ninguno; usa "
            f"{MARCADOR_ENLACE} si la URL publicada todavía no existe"
        )

    max_hashtags = limites.get("max_hashtags")
    if isinstance(max_hashtags, int):
        n = contar_hashtags(cuerpo)
        if n > max_hashtags:
            errores.append(f"la pieza tiene {n} hashtags y el máximo es {max_hashtags}")

    return errores


# ---------------------------------------------------------------------------
# Adaptador
# ---------------------------------------------------------------------------

class Adaptador:
    def __init__(self, ruta_config: Path, dir_canales: Path | None = None,
                 hoy: str | None = None):
        self.ruta_config = Path(ruta_config)
        if not self.ruta_config.is_file():
            raise RuntimeError(f"No existe el archivo de configuración: {self.ruta_config}")
        try:
            self.config = json.loads(self.ruta_config.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Configuración ilegible ({self.ruta_config}): {exc}") from exc
        self.raiz = self.ruta_config.resolve().parent
        self.hoy = hoy or date.today().isoformat()
        self.dir_contenidos = self.raiz / "biblioteca" / "contenidos"
        self.ruta_estilo = self.raiz / "biblioteca" / "estilo.md"
        self.dir_canales = Path(dir_canales) if dir_canales else (
            Path(__file__).resolve().parent.parent / "references" / "canales"
        )
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

    def dir_piezas(self, contenido_id: str) -> Path:
        return self.dir_contenidos / contenido_id / "piezas"

    def canales_salida(self) -> list[str] | int:
        canales = self.config.get("canales_salida")
        if not isinstance(canales, list) or not canales:
            return self._fatal(
                "proyecto.config.json no tiene la lista 'canales_salida'; "
                "añádela con los canales a preparar (p. ej. [\"substack\", \"linkedin\", \"notes\"])"
            )
        return [str(c) for c in canales]

    def ruta_plantilla(self, canal: str) -> Path:
        return self.dir_canales / f"{canal}.md"

    def cargar_plantilla(self, canal: str) -> tuple[dict, str] | int:
        """(límites, texto de la plantilla) o un código de error si falta."""
        ruta = self.ruta_plantilla(canal)
        if not ruta.is_file():
            return self._fatal(
                f"el canal '{canal}' está en canales_salida pero no tiene plantilla; "
                f"crea {ruta} con su encabezado de límites"
            )
        encabezado, cuerpo = parsear_frontmatter(ruta.read_text(encoding="utf-8"))
        if encabezado.get("canal") != canal:
            self.avisar(
                f"la plantilla {ruta.name} declara canal "
                f"'{encabezado.get('canal', '(sin canal)')}' y debería declarar '{canal}'"
            )
        return limites_de_plantilla(encabezado), cuerpo

    def comprobar_principal_aprobado(self, contenido_id: str) -> Path | int:
        """La ruta de principal.md si está aprobado; código de error si no."""
        ruta = self.dir_contenidos / contenido_id / "principal.md"
        if not ruta.is_file():
            return self._fatal(
                f"no existe biblioteca/contenidos/{contenido_id}/principal.md; "
                "ejecuta antes la skill redactar-contenido"
            )
        encabezado, _ = parsear_frontmatter(ruta.read_text(encoding="utf-8"))
        estado = encabezado.get("estado", "(sin estado)")
        if estado != "aprobado":
            return self._fatal(
                f"principal.md de '{contenido_id}' tiene estado '{estado}' y solo se "
                "adapta un principal con estado 'aprobado'; la aprobación la marca "
                "la persona en el encabezado"
            )
        return ruta

    # -- preparar ------------------------------------------------------------

    def cmd_preparar(self, contenido_id: str) -> int:
        ruta_principal = self.comprobar_principal_aprobado(contenido_id)
        if isinstance(ruta_principal, int):
            return ruta_principal
        canales = self.canales_salida()
        if isinstance(canales, int):
            return canales

        if not self.ruta_estilo.is_file():
            self.avisar(
                "no existe biblioteca/estilo.md; conviene generarlo con la skill "
                "analizar-biblioteca para adaptar con la voz de la publicación"
            )

        detalle = {}
        for canal in canales:
            plantilla = self.cargar_plantilla(canal)
            if isinstance(plantilla, int):
                return plantilla
            limites, _ = plantilla
            ruta_pieza = self.dir_piezas(contenido_id) / f"{canal}.md"
            estado_pieza = None
            if ruta_pieza.is_file():
                encabezado, _ = parsear_frontmatter(ruta_pieza.read_text(encoding="utf-8"))
                estado_pieza = encabezado.get("estado", "(sin estado)")
            detalle[canal] = {
                "plantilla": str(self.ruta_plantilla(canal)),
                "limites": limites,
                "tiene_pieza": ruta_pieza.is_file(),
                "estado_pieza": estado_pieza,
            }

        print(json.dumps({
            "principal": str(ruta_principal),
            "estilo": str(self.ruta_estilo),
            "estilo_existe": self.ruta_estilo.is_file(),
            "canales": detalle,
            "pendientes": [c for c, d in detalle.items() if not d["tiene_pieza"]],
        }, ensure_ascii=False, indent=2))
        return self._salida()

    # -- guardar ---------------------------------------------------------------

    def cmd_guardar(self, contenido_id: str, canal: str, archivo: Path,
                    reemplazar: bool) -> int:
        ruta_principal = self.comprobar_principal_aprobado(contenido_id)
        if isinstance(ruta_principal, int):
            return ruta_principal
        canales = self.canales_salida()
        if isinstance(canales, int):
            return canales
        if canal not in canales:
            return self._fatal(
                f"el canal '{canal}' no está en canales_salida "
                f"({', '.join(canales)}); añádelo en proyecto.config.json"
            )
        plantilla = self.cargar_plantilla(canal)
        if isinstance(plantilla, int):
            return plantilla
        limites, _ = plantilla

        archivo = Path(archivo)
        if not archivo.is_file():
            return self._fatal(f"no existe el archivo {archivo}")
        encabezado_modelo, cuerpo = parsear_frontmatter(archivo.read_text(encoding="utf-8"))
        if encabezado_modelo:
            self.avisar(
                "el archivo del modelo traía un encabezado; se ignora porque "
                "el encabezado de la pieza lo escribe el script"
            )
        cuerpo = cuerpo.strip()
        if not cuerpo:
            return self._fatal(f"el archivo {archivo} está vacío")

        # Una pieza aprobada no se sobrescribe nunca; un borrador, solo con --reemplazar.
        ruta_pieza = self.dir_piezas(contenido_id) / f"{canal}.md"
        if ruta_pieza.is_file():
            encabezado_actual, _ = parsear_frontmatter(ruta_pieza.read_text(encoding="utf-8"))
            if encabezado_actual.get("estado") == "aprobado":
                return self._fatal(
                    f"la pieza {canal}.md tiene estado 'aprobado' y no se sobrescribe; "
                    "la aprobación la marca la persona en el encabezado"
                )
            if not reemplazar:
                return self._fatal(
                    f"ya existe un borrador en piezas/{canal}.md; para sustituirlo "
                    "ejecuta guardar con --reemplazar"
                )

        errores = validar_pieza(cuerpo, limites)
        if errores:
            print(f"ERROR: la pieza de '{canal}' no se guarda:", file=sys.stderr)
            for e in errores:
                print(f"  - {e}", file=sys.stderr)
            return CODIGO_FATAL

        encabezado = {
            "canal": canal,
            "contenido": contenido_id,
            "estado": "borrador",
            "fecha": self.hoy,
        }
        escribir_atomico(ruta_pieza, componer_frontmatter(encabezado) + "\n" + cuerpo + "\n")

        print(json.dumps({
            "archivo": str(ruta_pieza),
            "canal": canal,
            "estado": "borrador",
            "caracteres": len(cuerpo),
            "enlace_pendiente": MARCADOR_ENLACE in cuerpo,
            "avisos": self.avisos,
        }, ensure_ascii=False, indent=2))
        return self._salida()

    # -- comprobar -------------------------------------------------------------

    def cmd_comprobar(self, contenido_id: str) -> int:
        canales = self.canales_salida()
        if isinstance(canales, int):
            return canales
        dir_piezas = self.dir_piezas(contenido_id)
        rutas = sorted(dir_piezas.glob("*.md")) if dir_piezas.is_dir() else []
        if not rutas:
            return self._fatal(
                f"no hay piezas en biblioteca/contenidos/{contenido_id}/piezas/; "
                "guárdalas antes con 'guardar'"
            )

        informe = {}
        hay_errores = False
        for ruta in rutas:
            encabezado, cuerpo = parsear_frontmatter(ruta.read_text(encoding="utf-8"))
            canal = str(encabezado.get("canal") or ruta.stem)
            errores: list[str] = []
            avisos_pieza: list[str] = []
            ruta_plantilla = self.ruta_plantilla(canal)
            if not ruta_plantilla.is_file():
                errores.append(f"no existe la plantilla {ruta_plantilla} de su canal")
            else:
                encabezado_plantilla, _ = parsear_frontmatter(
                    ruta_plantilla.read_text(encoding="utf-8")
                )
                errores = validar_pieza(cuerpo, limites_de_plantilla(encabezado_plantilla))
            if canal not in canales:
                avisos_pieza.append("su canal ya no está en canales_salida")
            if MARCADOR_ENLACE in cuerpo:
                avisos_pieza.append(
                    f"tiene {MARCADOR_ENLACE} pendiente; tras publicar, ejecuta 'enlazar'"
                )
            hay_errores = hay_errores or bool(errores)
            for aviso in avisos_pieza:
                self.avisos.append(f"{ruta.name}: {aviso}")
            informe[ruta.name] = {
                "canal": canal,
                "estado": encabezado.get("estado", "(sin estado)"),
                "caracteres": len(cuerpo.strip()),
                "errores": errores,
                "avisos": avisos_pieza,
            }

        sin_pieza = [c for c in canales if not (dir_piezas / f"{c}.md").is_file()]
        print(json.dumps({
            "piezas": informe,
            "canales_sin_pieza": sin_pieza,
        }, ensure_ascii=False, indent=2))
        if hay_errores:
            return CODIGO_FATAL
        return CODIGO_AVISOS if self.avisos or sin_pieza else CODIGO_OK

    # -- enlazar ---------------------------------------------------------------

    def cmd_enlazar(self, contenido_id: str, url: str) -> int:
        if not re.fullmatch(r"https?://\S+", url):
            return self._fatal(f"'{url}' no parece una URL (debe empezar por http:// o https://)")
        dir_piezas = self.dir_piezas(contenido_id)
        rutas = sorted(dir_piezas.glob("*.md")) if dir_piezas.is_dir() else []
        if not rutas:
            return self._fatal(
                f"no hay piezas en biblioteca/contenidos/{contenido_id}/piezas/"
            )

        resultado = {}
        total = 0
        for ruta in rutas:
            texto = ruta.read_text(encoding="utf-8")
            apariciones = texto.count(MARCADOR_ENLACE)
            if apariciones:
                escribir_atomico(ruta, texto.replace(MARCADOR_ENLACE, url))
                total += apariciones
            resultado[ruta.name] = apariciones
        if total == 0:
            self.avisar(f"ninguna pieza contenía {MARCADOR_ENLACE}; no se cambió nada")

        print(json.dumps({
            "url": url,
            "sustituciones": resultado,
            "total": total,
            "avisos": self.avisos,
        }, ensure_ascii=False, indent=2))
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
        description="Prepara, valida y guarda las piezas de cada canal de publicación."
    )
    analizador.add_argument(
        "--config", default="proyecto.config.json",
        help="Ruta de proyecto.config.json (por defecto, el del directorio actual).",
    )
    analizador.add_argument(
        "--canales", default=None,
        help="Carpeta de plantillas de canal (por defecto, references/canales de la skill).",
    )
    analizador.add_argument(
        "--hoy", default=None,
        help="Fecha YYYY-MM-DD para el encabezado (por defecto, la de hoy). Útil en pruebas.",
    )
    subcomandos = analizador.add_subparsers(dest="comando", required=True)
    p = subcomandos.add_parser("preparar", help="Comprueba el principal aprobado y devuelve los canales.")
    p.add_argument("contenido_id")
    p = subcomandos.add_parser("guardar", help="Valida la pieza del modelo y la escribe en piezas/<canal>.md.")
    p.add_argument("contenido_id")
    p.add_argument("canal")
    p.add_argument("archivo", help="Markdown del modelo con la pieza, sin encabezado.")
    p.add_argument("--reemplazar", action="store_true",
                   help="Sustituye un borrador existente (nunca una pieza aprobada).")
    p = subcomandos.add_parser("comprobar", help="Revisa todas las piezas actuales sin modificar nada.")
    p.add_argument("contenido_id")
    p = subcomandos.add_parser("enlazar", help="Sustituye {{enlace}} por la URL publicada en todas las piezas.")
    p.add_argument("contenido_id")
    p.add_argument("url")

    args = analizador.parse_args(argv)
    try:
        adaptador = Adaptador(
            Path(args.config),
            dir_canales=Path(args.canales) if args.canales else None,
            hoy=args.hoy,
        )
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return CODIGO_FATAL

    try:
        if args.comando == "preparar":
            return adaptador.cmd_preparar(args.contenido_id)
        if args.comando == "guardar":
            return adaptador.cmd_guardar(
                args.contenido_id, args.canal, Path(args.archivo), args.reemplazar
            )
        if args.comando == "comprobar":
            return adaptador.cmd_comprobar(args.contenido_id)
        if args.comando == "enlazar":
            return adaptador.cmd_enlazar(args.contenido_id, args.url)
    except OSError as exc:
        print(f"ERROR: no pudo ejecutarse: {exc}", file=sys.stderr)
        return CODIGO_FATAL
    return CODIGO_FATAL


if __name__ == "__main__":
    sys.exit(main())
