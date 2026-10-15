#!/usr/bin/env python3
"""Prepara, valida y guarda la redacción del contenido principal.

Parte "script" de la skill redactar-contenido (segunda parte de la fase 3 de
ARQUITECTURA.md). El modelo escribe el texto con la voz de `estilo.md` y
propone los títulos; este script hace lo repetible: comprobar que la
investigación está aprobada, preparar el material, guardar el borrador
original intacto y comprobar citas, enlaces y longitud.

Comandos (desde la raíz del proyecto):
  preparar <id>                      comprueba que la investigación está aprobada y devuelve el material
  guardar <id> <archivo.md>          valida el texto del modelo y escribe principal.md y principal.borrador.md
  comprobar <id>                     repite las comprobaciones sobre principal.md sin modificar nada

Códigos de salida:
  0  correcto
  1  avisos (p. ej. longitud fuera de rango)
  2  no pudo ejecutarse o la validación falló

Las escrituras son atómicas. Un `principal.md` con `estado: aprobado` no se
toca nunca; un borrador existente solo se sustituye con `--reemplazar`.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
import tempfile
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

CODIGO_OK = 0
CODIGO_AVISOS = 1
CODIGO_FATAL = 2

SECCION_VERIFICACION = "## Verificación de afirmaciones"
SECCION_FUENTES = "## Fuentes"


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
    patron = re.compile(
        rf"^{re.escape(titulo)}\s*$(.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL
    )
    coincidencia = patron.search(cuerpo)
    return coincidencia.group(1).strip() if coincidencia else ""


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


def contar_palabras(cuerpo: str) -> int:
    """Palabras del texto sin enlaces de imagen ni URLs de los enlaces."""
    texto = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", cuerpo)
    texto = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", texto)
    return len(texto.split())


# ---------------------------------------------------------------------------
# Redactor
# ---------------------------------------------------------------------------

class Redactor:
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
        self.ruta_estilo = self.dir_biblioteca / "estilo.md"
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

    def cargar_json(self, ruta: Path):
        try:
            return json.loads(ruta.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"archivo ilegible: {ruta} ({exc})") from exc

    def cargar_inventario(self) -> dict:
        if not self.ruta_inventario.is_file():
            return {}
        try:
            return self.cargar_json(self.ruta_inventario)
        except RuntimeError as exc:
            self.avisar(str(exc))
            return {}

    def cargar_investigacion(self, oportunidad_id: str) -> tuple[dict, str] | None:
        ruta = self.dir_contenido(oportunidad_id) / "investigacion.md"
        if not ruta.is_file():
            return None
        return parsear_frontmatter(ruta.read_text(encoding="utf-8"))

    def comprobar_aprobada(self, oportunidad_id: str) -> tuple[dict, str] | int:
        """Investigación cargada si está aprobada; código de error si no."""
        cargada = self.cargar_investigacion(oportunidad_id)
        if cargada is None:
            return self._fatal(
                f"no existe biblioteca/contenidos/{oportunidad_id}/investigacion.md; "
                "ejecuta antes la skill investigar-tema"
            )
        encabezado, cuerpo = cargada
        estado = encabezado.get("estado", "(sin estado)")
        if estado != "aprobada":
            return self._fatal(
                f"la investigación de '{oportunidad_id}' tiene estado '{estado}' y solo "
                "se redacta con una investigación con estado 'aprobada'; la aprobación "
                "la marca la persona en el encabezado"
            )
        return encabezado, cuerpo

    def metricas_estilo(self) -> dict | None:
        """Las métricas de estilo, calculadas con el script de analizar-biblioteca."""
        ruta = (
            Path(__file__).resolve().parent.parent.parent
            / "analizar-biblioteca" / "scripts" / "analizar_biblioteca.py"
        )
        if not ruta.is_file():
            self.avisar(f"no se encontró la skill analizar-biblioteca en {ruta}")
            return None
        spec = importlib.util.spec_from_file_location("analizar_biblioteca", ruta)
        modulo = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(modulo)
            return modulo.Analizador(self.raiz).metricas_estilo()
        except Exception as exc:
            self.avisar(f"no se pudieron calcular las métricas de estilo: {exc}")
            return None

    def articulos_relacionados(self, oportunidad_id: str) -> list[dict]:
        """Artículos propios citados en la oportunidad, con título y URL."""
        ruta = self.dir_oportunidades / f"{oportunidad_id}.md"
        if not ruta.is_file():
            self.avisar(f"no existe la oportunidad biblioteca/oportunidades/{oportunidad_id}.md")
            return []
        encabezado, _ = parsear_frontmatter(ruta.read_text(encoding="utf-8"))
        relacionados = encabezado.get("relacionados", [])
        if isinstance(relacionados, str):
            relacionados = [relacionados] if relacionados else []
        inventario = self.cargar_inventario()
        resultado = []
        for referencia in relacionados:
            post_id = referencia.split(":", 1)[1] if ":" in referencia else referencia
            registro = inventario.get(post_id) or {}
            if not registro:
                self.avisar(f"el inventario no tiene el artículo relacionado {referencia}")
            resultado.append({
                "referencia": referencia,
                "titulo": registro.get("titulo"),
                "url": registro.get("url"),
            })
        return resultado

    # -- preparar ------------------------------------------------------------

    def cmd_preparar(self, oportunidad_id: str) -> int:
        cargada = self.comprobar_aprobada(oportunidad_id)
        if isinstance(cargada, int):
            return cargada
        encabezado, _ = cargada

        carpeta = self.dir_contenido(oportunidad_id)
        ruta_fuentes = carpeta / "fuentes.json"
        if not ruta_fuentes.is_file():
            return self._fatal(
                f"no existe {ruta_fuentes}; la investigación aprobada debería traer sus fuentes"
            )

        if not self.ruta_estilo.is_file():
            self.avisar(
                "no existe biblioteca/estilo.md; conviene generarlo con la skill "
                "analizar-biblioteca antes de redactar para escribir con la voz de la publicación"
            )

        paquete = {
            "rutas": {
                "oportunidad": str(self.dir_oportunidades / f"{oportunidad_id}.md"),
                "investigacion": str(carpeta / "investigacion.md"),
                "fuentes": str(ruta_fuentes),
                "estilo": str(self.ruta_estilo),
            },
            "estilo_existe": self.ruta_estilo.is_file(),
            "metricas_estilo": self.metricas_estilo(),
            "articulos_relacionados": self.articulos_relacionados(
                str(encabezado.get("oportunidad", oportunidad_id))
            ),
        }
        print(json.dumps(paquete, ensure_ascii=False, indent=2))
        return self._salida()

    # -- comprobaciones ------------------------------------------------------

    def url_es_propia(self, url: str) -> bool:
        base = (self.config.get("publicacion") or {}).get("substack", "")
        host_propio = urlparse(base).hostname
        if not host_propio:
            return False
        return urlparse(url).hostname == host_propio

    def comprobar_texto(self, cuerpo: str, fuentes: list[dict],
                        tabla: dict[str, dict]) -> tuple[list[str], list[str]]:
        """Devuelve (errores, avisos) sobre citas, enlaces y longitud."""
        errores: list[str] = []
        avisos: list[str] = []
        por_fuente = {f.get("id"): f for f in fuentes}
        estados = {aid: fila["estado"] for aid, fila in tabla.items()}

        # 1. Cada cita [f<n>] existe en fuentes.json.
        citadas = sorted(set(re.findall(r"\[(f\d+)\]", cuerpo)))
        for ref in citadas:
            if ref not in por_fuente:
                errores.append(f"la cita [{ref}] no existe en fuentes.json")

        # 2. No se cita una fuente que solo respalde afirmaciones refutadas.
        for ref in citadas:
            fuente = por_fuente.get(ref)
            if fuente is None:
                continue
            respalda = fuente.get("respalda", [])
            contradice = fuente.get("contradice", [])
            if respalda and not contradice and all(
                estados.get(aid) == "refutada" for aid in respalda
            ):
                errores.append(
                    f"la fuente [{ref}] solo respalda afirmaciones refutadas "
                    f"({', '.join(respalda)}) y no puede citarse como apoyo"
                )

        # 3. Los enlaces a artículos propios apuntan a URLs del inventario.
        urls_inventario = {
            registro.get("url") for registro in self.cargar_inventario().values()
        }
        for texto_enlace, url in re.findall(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)\)", cuerpo):
            if self.url_es_propia(url) and url not in urls_inventario:
                errores.append(
                    f"el enlace interno '{texto_enlace}' apunta a {url}, "
                    "que no está en el inventario de artículos propios"
                )

        # 4. Longitud: entre el 60 % y el 140 % de la mediana propia (aviso).
        palabras = contar_palabras(cuerpo)
        metricas = self.metricas_estilo()
        mediana = ((metricas or {}).get("palabras") or {}).get("mediana") or 0
        if mediana > 0:
            minimo, maximo = round(mediana * 0.6), round(mediana * 1.4)
            if not minimo <= palabras <= maximo:
                avisos.append(
                    f"el texto tiene {palabras} palabras, fuera del rango {minimo}-{maximo} "
                    f"(60 %-140 % de la mediana propia, {mediana})"
                )
        else:
            avisos.append(
                "no se pudo comprobar la longitud: no hay mediana de artículos propios"
            )

        # 5. El texto termina con una sección de fuentes (aviso).
        if not extraer_seccion(cuerpo, SECCION_FUENTES):
            avisos.append(f"el texto no tiene la sección final '{SECCION_FUENTES}'")

        return errores, avisos

    def _cargar_material_comprobacion(self, oportunidad_id: str):
        """(fuentes, tabla de verificación) o un código de error."""
        cargada = self.comprobar_aprobada(oportunidad_id)
        if isinstance(cargada, int):
            return cargada
        _, cuerpo_investigacion = cargada
        ruta_fuentes = self.dir_contenido(oportunidad_id) / "fuentes.json"
        if not ruta_fuentes.is_file():
            return self._fatal(f"no existe {ruta_fuentes}")
        try:
            fuentes = self.cargar_json(ruta_fuentes)
        except RuntimeError as exc:
            return self._fatal(str(exc))
        tabla = parsear_tabla_verificacion(
            extraer_seccion(cuerpo_investigacion, SECCION_VERIFICACION)
        )
        return fuentes, tabla

    # -- guardar ---------------------------------------------------------------

    def cmd_guardar(self, oportunidad_id: str, archivo: Path, reemplazar: bool) -> int:
        material = self._cargar_material_comprobacion(oportunidad_id)
        if isinstance(material, int):
            return material
        fuentes, tabla = material

        archivo = Path(archivo)
        if not archivo.is_file():
            return self._fatal(f"no existe el archivo {archivo}")
        encabezado_modelo, cuerpo = parsear_frontmatter(archivo.read_text(encoding="utf-8"))

        # Bloque inicial del modelo: título elegido y alternativos.
        titulo = encabezado_modelo.get("titulo")
        alternativos = encabezado_modelo.get("titulos_alternativos", [])
        if isinstance(alternativos, str):
            alternativos = [alternativos] if alternativos else []
        if not titulo or not alternativos:
            return self._fatal(
                "el archivo del modelo debe empezar con un bloque `---` con `titulo` y "
                "`titulos_alternativos` (el título elegido y dos alternativos)"
            )
        if len(alternativos) != 2:
            self.avisar(
                f"se esperaban dos títulos alternativos y llegaron {len(alternativos)}"
            )

        # Un principal.md aprobado no se toca; un borrador, solo con --reemplazar.
        carpeta = self.dir_contenido(oportunidad_id)
        ruta_principal = carpeta / "principal.md"
        if ruta_principal.is_file():
            encabezado_actual, _ = parsear_frontmatter(
                ruta_principal.read_text(encoding="utf-8")
            )
            if encabezado_actual.get("estado") == "aprobado":
                return self._fatal(
                    "principal.md tiene estado 'aprobado' y no se toca; la aprobación "
                    "la marca la persona en el encabezado"
                )
            if not reemplazar:
                return self._fatal(
                    "ya existe un borrador en principal.md; para sustituirlo ejecuta "
                    "guardar con --reemplazar (principal.borrador.md pasará a ser el nuevo borrador)"
                )

        primera_linea = cuerpo.splitlines()[0].strip() if cuerpo.strip() else ""
        if primera_linea != f"# {titulo}":
            cuerpo = f"# {titulo}\n\n{cuerpo.strip()}"

        errores, avisos = self.comprobar_texto(cuerpo, fuentes, tabla)
        for aviso in avisos:
            self.avisar(aviso)
        if errores:
            print("ERROR: el texto no se guarda:", file=sys.stderr)
            for e in errores:
                print(f"  - {e}", file=sys.stderr)
            return CODIGO_FATAL

        encabezado = {
            "oportunidad": oportunidad_id,
            "estado": "borrador",
            "fecha": self.hoy,
            "titulos_alternativos": alternativos,
        }
        contenido = componer_frontmatter(encabezado) + "\n" + cuerpo.strip() + "\n"
        escribir_atomico(ruta_principal, contenido)
        escribir_atomico(carpeta / "principal.borrador.md", contenido)

        print(json.dumps({
            "archivo": str(ruta_principal),
            "borrador": str(carpeta / "principal.borrador.md"),
            "estado": "borrador",
            "palabras": contar_palabras(cuerpo),
            "avisos": self.avisos,
        }, ensure_ascii=False, indent=2))
        return self._salida()

    # -- comprobar -------------------------------------------------------------

    def cmd_comprobar(self, oportunidad_id: str) -> int:
        material = self._cargar_material_comprobacion(oportunidad_id)
        if isinstance(material, int):
            return material
        fuentes, tabla = material

        ruta_principal = self.dir_contenido(oportunidad_id) / "principal.md"
        if not ruta_principal.is_file():
            return self._fatal(f"no existe {ruta_principal}; guarda el texto antes con 'guardar'")
        encabezado, cuerpo = parsear_frontmatter(ruta_principal.read_text(encoding="utf-8"))

        errores, avisos = self.comprobar_texto(cuerpo, fuentes, tabla)
        if not encabezado.get("titulos_alternativos"):
            avisos.append("el encabezado no tiene titulos_alternativos")

        print(json.dumps({
            "archivo": str(ruta_principal),
            "estado": encabezado.get("estado", "(sin estado)"),
            "palabras": contar_palabras(cuerpo),
            "errores": errores,
            "avisos": avisos + self.avisos,
        }, ensure_ascii=False, indent=2))
        if errores:
            return CODIGO_FATAL
        return CODIGO_AVISOS if avisos or self.avisos else CODIGO_OK


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
        description="Prepara, valida y guarda la redacción del contenido principal."
    )
    analizador.add_argument(
        "--config", default="proyecto.config.json",
        help="Ruta de proyecto.config.json (por defecto, el del directorio actual).",
    )
    analizador.add_argument(
        "--hoy", default=None,
        help="Fecha YYYY-MM-DD para el encabezado (por defecto, la de hoy). Útil en pruebas.",
    )
    subcomandos = analizador.add_subparsers(dest="comando", required=True)
    p = subcomandos.add_parser("preparar", help="Comprueba la investigación aprobada y devuelve el material.")
    p.add_argument("oportunidad_id")
    p = subcomandos.add_parser("guardar", help="Valida el texto del modelo y escribe principal.md y su borrador.")
    p.add_argument("oportunidad_id")
    p.add_argument("archivo", help="Markdown del modelo con el bloque inicial de títulos.")
    p.add_argument("--reemplazar", action="store_true",
                   help="Sustituye un borrador existente (nunca un principal.md aprobado).")
    p = subcomandos.add_parser("comprobar", help="Repite las comprobaciones sobre principal.md sin modificar nada.")
    p.add_argument("oportunidad_id")

    args = analizador.parse_args(argv)
    try:
        redactor = Redactor(Path(args.config), hoy=args.hoy)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return CODIGO_FATAL

    try:
        if args.comando == "preparar":
            return redactor.cmd_preparar(args.oportunidad_id)
        if args.comando == "guardar":
            return redactor.cmd_guardar(args.oportunidad_id, Path(args.archivo), args.reemplazar)
        if args.comando == "comprobar":
            return redactor.cmd_comprobar(args.oportunidad_id)
    except OSError as exc:
        print(f"ERROR: no pudo ejecutarse: {exc}", file=sys.stderr)
        return CODIGO_FATAL
    return CODIGO_FATAL


if __name__ == "__main__":
    sys.exit(main())
