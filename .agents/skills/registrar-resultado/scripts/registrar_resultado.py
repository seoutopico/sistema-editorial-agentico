#!/usr/bin/env python3
"""registrar-resultado: cierra el ciclo editorial (fase 5 de ARQUITECTURA.md).

Enlaza cada contenido con su artículo publicado, guarda las métricas como
serie, recopila las decisiones sobre oportunidades y guarda las reglas de
estilo que el modelo deriva de las correcciones de la persona.

Uso (desde la raíz del proyecto):

  python .agents/skills/registrar-resultado/scripts/registrar_resultado.py <comando>

Comandos:
  decisiones                        regenera biblioteca/decisiones.md
  buscar-publicado <oportunidad_id> propone los 3 artículos publicados más
                                    parecidos al borrador; no enlaza nada
  enlazar <oportunidad_id> <post_id>
                                    escribe resultado.json, pasa la oportunidad
                                    a 'publicada' y enlaza las piezas
  metricas                          acumula las métricas públicas (y el CSV de
                                    estadísticas si existe) en resultado.json
  diferencias <oportunidad_id>      JSON con los párrafos eliminados, añadidos
                                    y modificados entre borrador y publicado
  guardar-reglas <archivo.json>     añade reglas a '## Reglas aprendidas' de
                                    biblioteca/estilo.md, sin duplicar

Códigos de salida: 0 correcto · 1 avisos · 2 no pudo ejecutarse o la
validación falló. Las escrituras son atómicas.
"""

from __future__ import annotations

import argparse
import csv
import difflib
import json
import os
import re
import sys
import subprocess
import tempfile
import unicodedata
from datetime import date, datetime
from pathlib import Path

CODIGO_OK = 0
CODIGO_AVISOS = 1
CODIGO_FATAL = 2

SECCION_REGLAS = "## Reglas aprendidas"
ESTADOS = ("propuesta", "aceptada", "publicada", "descartada")


# ---------------------------------------------------------------------------
# Utilidades
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


def parsear_frontmatter(texto: str) -> tuple[dict, str]:
    """Devuelve (encabezado, cuerpo). Claves simples y listas en línea."""
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


def actualizar_frontmatter(texto: str, cambios: dict) -> str:
    """Cambia (o inserta) claves del frontmatter sin tocar el resto del archivo."""
    lineas = texto.splitlines()
    if not lineas or lineas[0].strip() != "---":
        raise ValueError("el archivo no tiene frontmatter")
    fin = next((i for i, l in enumerate(lineas[1:], start=1) if l.strip() == "---"), None)
    if fin is None:
        raise ValueError("frontmatter sin cerrar")
    pendientes = dict(cambios)
    for i in range(1, fin):
        coincidencia = re.match(r"^([A-Za-z_][\w]*):", lineas[i])
        if coincidencia and coincidencia.group(1) in pendientes:
            clave = coincidencia.group(1)
            lineas[i] = f"{clave}: {pendientes.pop(clave)}"
    for clave, valor in pendientes.items():
        lineas.insert(fin, f"{clave}: {valor}")
        fin += 1
    resultado = "\n".join(lineas)
    if texto.endswith("\n") and not resultado.endswith("\n"):
        resultado += "\n"
    return resultado


def normalizar(texto: str) -> str:
    """Minúsculas, sin tildes, sin puntuación y con espacios colapsados."""
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = texto.lower()
    texto = re.sub(r"[^\w\s]", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def similitud(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, normalizar(a), normalizar(b)).ratio()


def solo_fecha(valor) -> str:
    return str(valor or "")[:10]


def dias_entre(fecha_inicio: str, fecha_fin: str) -> int | None:
    try:
        inicio = date.fromisoformat(solo_fecha(fecha_inicio))
        fin = date.fromisoformat(solo_fecha(fecha_fin))
    except ValueError:
        return None
    return (fin - inicio).days


def primer_titulo(cuerpo: str) -> str:
    coincidencia = re.search(r"^#\s+(.+)$", cuerpo, re.MULTILINE)
    return coincidencia.group(1).strip() if coincidencia else ""


def parrafos(cuerpo: str) -> list[str]:
    """Bloques separados por líneas en blanco, sin el H1 del título."""
    bloques = [b.strip() for b in re.split(r"\n\s*\n", cuerpo) if b.strip()]
    return [b for b in bloques if not re.match(r"^#\s+", b)]


def contar_palabras(cuerpo: str) -> int:
    texto = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", cuerpo)
    texto = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", texto)
    return len(texto.split())


def imprimir_json(datos):
    print(json.dumps(datos, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# Registrador
# ---------------------------------------------------------------------------

class Registrador:
    def __init__(self, ruta_config: Path, hoy: str | None = None):
        self.ruta_config = Path(ruta_config)
        if not self.ruta_config.is_file():
            raise RuntimeError(f"no existe el archivo de configuración: {self.ruta_config}")
        try:
            json.loads(self.ruta_config.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise RuntimeError(f"configuración ilegible ({self.ruta_config}): {exc}")
        self.raiz = self.ruta_config.resolve().parent
        self.hoy = hoy or datetime.now().strftime("%Y-%m-%d")
        self.avisos: list[str] = []

        biblioteca = self.raiz / "biblioteca"
        self.dir_oportunidades = biblioteca / "oportunidades"
        self.dir_contenidos = biblioteca / "contenidos"
        self.dir_articulos = biblioteca / "substack" / "articulos"
        self.dir_estadisticas = biblioteca / "substack" / "control" / "estadisticas"
        self.ruta_inventario = biblioteca / "substack" / "control" / "inventario.json"
        self.ruta_decisiones = biblioteca / "decisiones.md"
        self.ruta_estilo = biblioteca / "estilo.md"

    # -- infraestructura ----------------------------------------------------

    def avisar(self, mensaje: str):
        self.avisos.append(mensaje)
        print(f"AVISO: {mensaje}", file=sys.stderr)

    def _fatal(self, mensaje: str) -> int:
        print(f"ERROR: {mensaje}", file=sys.stderr)
        return CODIGO_FATAL

    def _salida(self) -> int:
        return CODIGO_AVISOS if self.avisos else CODIGO_OK

    def cargar_inventario(self) -> dict | None:
        if not self.ruta_inventario.is_file():
            return None
        return json.loads(self.ruta_inventario.read_text(encoding="utf-8"))

    def ruta_oportunidad(self, oportunidad_id: str) -> Path | None:
        directa = self.dir_oportunidades / f"{oportunidad_id}.md"
        if directa.is_file():
            return directa
        if self.dir_oportunidades.is_dir():
            for ruta in sorted(self.dir_oportunidades.glob("*.md")):
                encabezado, _ = parsear_frontmatter(ruta.read_text(encoding="utf-8"))
                if encabezado.get("id") == oportunidad_id:
                    return ruta
        return None

    def leer_oportunidades(self) -> list[dict]:
        resultado = []
        if not self.dir_oportunidades.is_dir():
            return resultado
        for ruta in sorted(self.dir_oportunidades.glob("*.md")):
            if ruta.name == "INDICE.md":
                continue
            encabezado, _ = parsear_frontmatter(ruta.read_text(encoding="utf-8"))
            if not encabezado.get("id") or not encabezado.get("estado"):
                self.avisar(f"{ruta.name}: sin 'id' o 'estado' en el encabezado; se omite")
                continue
            encabezado["_archivo"] = ruta.name
            resultado.append(encabezado)
        return resultado

    def ruta_resultado(self, oportunidad_id: str) -> Path:
        return self.dir_contenidos / oportunidad_id / "resultado.json"

    def cargar_resultado(self, oportunidad_id: str) -> dict:
        ruta = self.ruta_resultado(oportunidad_id)
        if ruta.is_file():
            return json.loads(ruta.read_text(encoding="utf-8"))
        return {}

    def cargar_principal(self, oportunidad_id: str, borrador: bool = False):
        """(encabezado, cuerpo) de principal.md o principal.borrador.md."""
        nombre = "principal.borrador.md" if borrador else "principal.md"
        ruta = self.dir_contenidos / oportunidad_id / nombre
        if not ruta.is_file():
            return None
        return parsear_frontmatter(ruta.read_text(encoding="utf-8"))

    # -- decisiones ----------------------------------------------------------

    def cmd_decisiones(self) -> int:
        inventario = self.cargar_inventario() or {}
        oportunidades = self.leer_oportunidades()
        grupos: dict[str, list[dict]] = {estado: [] for estado in ESTADOS}
        for oportunidad in oportunidades:
            estado = str(oportunidad["estado"]).strip()
            if estado not in grupos:
                self.avisar(
                    f"{oportunidad['_archivo']}: estado desconocido '{estado}'; se omite"
                )
                continue
            grupos[estado].append(oportunidad)
        for lista in grupos.values():
            lista.sort(key=lambda o: str(o["id"]))

        lineas = [
            "# Decisiones",
            "",
            "Generado por `registrar-resultado decisiones` a partir del encabezado",
            "de `biblioteca/oportunidades/*.md`. No editar a mano.",
            "",
        ]

        def describir(oportunidad: dict) -> str:
            detalles = []
            if oportunidad.get("interes"):
                detalles.append(f"interés: {oportunidad['interes']}")
            if oportunidad.get("cobertura"):
                detalles.append(f"cobertura: {oportunidad['cobertura']}")
            sufijo = f" ({', '.join(detalles)})" if detalles else ""
            return f"- {oportunidad['id']}{sufijo}"

        lineas.append("## Propuestas")
        lineas.append("")
        lineas.extend(describir(o) for o in grupos["propuesta"]) if grupos["propuesta"] else lineas.append("(ninguna)")
        lineas.append("")

        lineas.append("## Aceptadas")
        lineas.append("")
        lineas.extend(describir(o) for o in grupos["aceptada"]) if grupos["aceptada"] else lineas.append("(ninguna)")
        lineas.append("")

        lineas.append("## Publicadas")
        lineas.append("")
        if grupos["publicada"]:
            for oportunidad in grupos["publicada"]:
                post_id = str(oportunidad.get("articulo", "")).strip()
                registro = inventario.get(post_id) if post_id else None
                if registro:
                    titulo = registro.get("titulo", post_id)
                    url = registro.get("url", "")
                    lineas.append(f"- {oportunidad['id']} — [{titulo}]({url})")
                else:
                    lineas.append(f"- {oportunidad['id']} — SIN ENLACE al artículo publicado")
                    self.avisar(
                        f"{oportunidad['id']}: publicada sin artículo enlazado en el inventario"
                    )
        else:
            lineas.append("(ninguna)")
        lineas.append("")

        lineas.append("## Descartadas")
        lineas.append("")
        sin_motivo = 0
        if grupos["descartada"]:
            for oportunidad in grupos["descartada"]:
                motivo = str(oportunidad.get("motivo_estado", "")).strip()
                if motivo:
                    lineas.append(f"- {oportunidad['id']} — motivo: {motivo}")
                else:
                    sin_motivo += 1
                    lineas.append(
                        f"- {oportunidad['id']} — SIN MOTIVO: un descarte sin motivo "
                        "no enseña nada al siguiente cruce"
                    )
        else:
            lineas.append("(ninguna)")
        lineas.append("")

        escribir_atomico(self.ruta_decisiones, "\n".join(lineas))
        if sin_motivo:
            self.avisar(f"{sin_motivo} descarte(s) sin motivo_estado")
        imprimir_json({
            "archivo": "biblioteca/decisiones.md",
            "propuestas": len(grupos["propuesta"]),
            "aceptadas": len(grupos["aceptada"]),
            "publicadas": len(grupos["publicada"]),
            "descartadas": len(grupos["descartada"]),
            "descartes_sin_motivo": sin_motivo,
            "avisos": self.avisos,
        })
        return self._salida()

    # -- buscar-publicado ----------------------------------------------------

    def titulos_borrador(self, oportunidad_id: str):
        """(titulos, fecha_borrador) a partir de principal.md (o el borrador)."""
        principal = self.cargar_principal(oportunidad_id) or self.cargar_principal(
            oportunidad_id, borrador=True
        )
        if principal is None:
            return None
        encabezado, cuerpo = principal
        titulos = []
        titulo_h1 = primer_titulo(cuerpo)
        if titulo_h1:
            titulos.append(titulo_h1)
        alternativos = encabezado.get("titulos_alternativos", [])
        if isinstance(alternativos, list):
            titulos.extend(str(t) for t in alternativos)
        vistos = set()
        unicos = []
        for titulo in titulos:
            clave = normalizar(titulo)
            if clave and clave not in vistos:
                vistos.add(clave)
                unicos.append(titulo)
        return unicos, solo_fecha(encabezado.get("fecha"))

    def cmd_buscar_publicado(self, oportunidad_id: str) -> int:
        inventario = self.cargar_inventario()
        if inventario is None:
            return self._fatal(f"no existe el inventario: {self.ruta_inventario}")
        datos = self.titulos_borrador(oportunidad_id)
        if datos is None:
            return self._fatal(
                f"no existe biblioteca/contenidos/{oportunidad_id}/principal.md"
            )
        titulos, fecha_borrador = datos
        if not titulos:
            return self._fatal("el contenido no tiene título ni titulos_alternativos")
        if not fecha_borrador:
            self.avisar("el borrador no tiene fecha; se comparan todos los artículos")

        candidatos = []
        for post_id, registro in inventario.items():
            fecha_post = solo_fecha(registro.get("fecha"))
            if fecha_borrador and fecha_post and fecha_post < fecha_borrador:
                continue
            titulo_post = str(registro.get("titulo", ""))
            puntuacion = max((similitud(t, titulo_post) for t in titulos), default=0.0)
            candidatos.append({
                "post_id": str(post_id),
                "titulo": titulo_post,
                "fecha": fecha_post,
                "url": registro.get("url", ""),
                "puntuacion": round(puntuacion, 3),
            })
        candidatos.sort(key=lambda c: (-c["puntuacion"], c["fecha"], c["post_id"]))
        if not candidatos:
            self.avisar("ningún artículo del inventario es posterior al borrador")
        imprimir_json({
            "oportunidad": oportunidad_id,
            "titulos_borrador": titulos,
            "fecha_borrador": fecha_borrador,
            "candidatos": candidatos[:3],
            "nota": "Este comando no enlaza nada: confirmar y ejecutar 'enlazar'.",
            "avisos": self.avisos,
        })
        return self._salida()

    # -- enlazar --------------------------------------------------------------

    def cmd_enlazar(self, oportunidad_id: str, post_id: str) -> int:
        inventario = self.cargar_inventario()
        if inventario is None:
            return self._fatal(f"no existe el inventario: {self.ruta_inventario}")
        registro = inventario.get(post_id)
        if registro is None:
            return self._fatal(f"el post_id '{post_id}' no existe en el inventario")
        ruta_oportunidad = self.ruta_oportunidad(oportunidad_id)
        if ruta_oportunidad is None:
            return self._fatal(f"no existe la oportunidad '{oportunidad_id}'")

        # 1. resultado.json (conserva métricas y reglas si ya existían)
        resultado = self.cargar_resultado(oportunidad_id)
        resultado["articulo"] = {
            "id": str(post_id),
            "titulo": registro.get("titulo", ""),
            "url": registro.get("url", ""),
            "fecha_publicacion": solo_fecha(registro.get("fecha")),
        }
        resultado["enlazado"] = self.hoy
        escribir_json_atomico(self.ruta_resultado(oportunidad_id), resultado)

        # 2. la oportunidad pasa a publicada
        texto = ruta_oportunidad.read_text(encoding="utf-8")
        try:
            nuevo = actualizar_frontmatter(
                texto, {"estado": "publicada", "articulo": post_id}
            )
        except ValueError as exc:
            return self._fatal(f"{ruta_oportunidad.name}: {exc}")
        escribir_atomico(ruta_oportunidad, nuevo)

        # 3. enlazar las piezas, si las hay
        url = str(registro.get("url", ""))
        dir_piezas = self.dir_contenidos / oportunidad_id / "piezas"
        piezas = sorted(dir_piezas.glob("*.md")) if dir_piezas.is_dir() else []
        piezas_enlazadas = False
        if piezas and url:
            script = (
                self.raiz / ".agents" / "skills" / "adaptar-contenido"
                / "scripts" / "adaptar_contenido.py"
            )
            if script.is_file():
                proceso = subprocess.run(
                    [sys.executable, str(script), "--config", str(self.ruta_config),
                     "enlazar", oportunidad_id, url],
                    capture_output=True, text=True,
                )
                piezas_enlazadas = proceso.returncode in (CODIGO_OK, CODIGO_AVISOS)
                if not piezas_enlazadas:
                    self.avisar(
                        "no se pudieron enlazar las piezas: "
                        + (proceso.stderr or proceso.stdout).strip()
                    )
            else:
                self.avisar("hay piezas pero falta la skill adaptar-contenido")
        elif piezas and not url:
            self.avisar("hay piezas pero el artículo no tiene URL en el inventario")

        imprimir_json({
            "oportunidad": oportunidad_id,
            "estado": "publicada",
            "articulo": resultado["articulo"],
            "resultado": f"biblioteca/contenidos/{oportunidad_id}/resultado.json",
            "piezas": len(piezas),
            "piezas_enlazadas": piezas_enlazadas,
            "avisos": self.avisos,
        })
        return self._salida()

    # -- metricas --------------------------------------------------------------

    def _leer_csv_estadisticas(self):
        """Mapa por post_id y por título normalizado → {aperturas, clics, archivo}."""
        por_id: dict[str, dict] = {}
        por_titulo: dict[str, dict] = {}
        archivos = sorted(self.dir_estadisticas.glob("*.csv")) if self.dir_estadisticas.is_dir() else []
        alias = {
            "id": ("post_id", "id", "post id"),
            "titulo": ("title", "titulo", "título", "post title"),
            "aperturas": ("opens", "aperturas", "unique opens", "unique_opens", "opened"),
            "clics": ("clicks", "clics", "unique clicks", "unique_clicks"),
        }
        for ruta in archivos:
            with ruta.open(encoding="utf-8-sig", newline="") as f:
                lector = csv.DictReader(f)
                if not lector.fieldnames:
                    continue
                columnas = {}
                for campo, nombres in alias.items():
                    for col in lector.fieldnames:
                        if col and col.strip().lower() in nombres:
                            columnas[campo] = col
                            break
                if "aperturas" not in columnas and "clics" not in columnas:
                    self.avisar(f"{ruta.name}: sin columnas de aperturas ni clics; se omite")
                    continue

                def entero(fila, campo):
                    bruto = str(fila.get(columnas.get(campo, ""), "") or "").strip()
                    try:
                        return int(float(bruto.replace(",", "")))
                    except ValueError:
                        return None

                for fila in lector:
                    datos = {
                        "aperturas": entero(fila, "aperturas"),
                        "clics": entero(fila, "clics"),
                        "archivo": ruta.name,
                    }
                    identificador = str(fila.get(columnas.get("id", ""), "") or "").strip()
                    titulo = str(fila.get(columnas.get("titulo", ""), "") or "").strip()
                    if identificador:
                        por_id[identificador] = datos
                    if titulo:
                        por_titulo[normalizar(titulo)] = datos
        return por_id, por_titulo, len(archivos)

    def cmd_metricas(self) -> int:
        inventario = self.cargar_inventario()
        if inventario is None:
            return self._fatal(f"no existe el inventario: {self.ruta_inventario}")
        por_id, por_titulo, n_csv = self._leer_csv_estadisticas()
        if n_csv == 0:
            print(
                "Nota: sin CSV en biblioteca/substack/control/estadisticas/; "
                "solo métricas públicas.",
                file=sys.stderr,
            )

        informe = []
        directorios = sorted(self.dir_contenidos.iterdir()) if self.dir_contenidos.is_dir() else []
        for directorio in directorios:
            if not directorio.is_dir():
                continue
            oportunidad_id = directorio.name
            resultado = self.cargar_resultado(oportunidad_id)
            articulo = resultado.get("articulo")
            if not articulo:
                continue
            registro = inventario.get(str(articulo.get("id")))
            if registro is None:
                self.avisar(
                    f"{oportunidad_id}: el artículo enlazado "
                    f"'{articulo.get('id')}' ya no está en el inventario"
                )
                continue
            metricas = resultado.setdefault("metricas", {})
            capturas = metricas.setdefault("capturas", [])
            fuente = registro.get("metricas", {}) or {}
            fecha_captura = solo_fecha(fuente.get("fecha_captura")) or self.hoy
            nueva = None
            if not any(solo_fecha(c.get("fecha_captura")) == fecha_captura for c in capturas):
                nueva = {
                    "fecha_captura": fecha_captura,
                    "reacciones": fuente.get("reacciones", 0),
                    "comentarios": fuente.get("comentarios", 0),
                    "restacks": fuente.get("restacks", 0),
                }
                capturas.append(nueva)
                capturas.sort(key=lambda c: solo_fecha(c.get("fecha_captura")))

            # días desde la publicación e hitos de 7 y 30 días
            fecha_publicacion = solo_fecha(articulo.get("fecha_publicacion"))
            for captura in capturas:
                captura["dias"] = dias_entre(fecha_publicacion, captura.get("fecha_captura"))
                captura.pop("hito", None)
            for hito, objetivo, tolerancia in (("7d", 7, 3), ("30d", 30, 7)):
                con_dias = [c for c in capturas if isinstance(c.get("dias"), int)]
                cercanas = [c for c in con_dias if abs(c["dias"] - objetivo) <= tolerancia]
                if cercanas:
                    mejor = min(cercanas, key=lambda c: (abs(c["dias"] - objetivo), c["dias"]))
                    marcas = mejor.get("hito")
                    mejor["hito"] = f"{marcas},{hito}" if marcas else hito

            # estadísticas privadas del CSV, si las hay
            estadisticas = por_id.get(str(articulo.get("id"))) or por_titulo.get(
                normalizar(articulo.get("titulo", ""))
            )
            if estadisticas:
                metricas["estadisticas"] = {
                    "aperturas": estadisticas["aperturas"],
                    "clics": estadisticas["clics"],
                    "archivo": estadisticas["archivo"],
                    "fecha_captura": self.hoy,
                }

            escribir_json_atomico(self.ruta_resultado(oportunidad_id), resultado)
            informe.append({
                "oportunidad": oportunidad_id,
                "articulo": articulo.get("id"),
                "capturas": len(capturas),
                "captura_nueva": nueva is not None,
                "estadisticas_csv": bool(estadisticas),
            })

        imprimir_json({
            "contenidos": informe,
            "csv_encontrados": n_csv,
            "avisos": self.avisos,
        })
        return self._salida()

    # -- diferencias -------------------------------------------------------------

    def cmd_diferencias(self, oportunidad_id: str) -> int:
        borrador = self.cargar_principal(oportunidad_id, borrador=True)
        if borrador is None:
            return self._fatal(
                f"no existe biblioteca/contenidos/{oportunidad_id}/principal.borrador.md"
            )
        resultado = self.cargar_resultado(oportunidad_id)
        articulo = resultado.get("articulo")
        if not articulo:
            return self._fatal(
                f"'{oportunidad_id}' no está enlazado a un artículo: ejecutar antes 'enlazar'"
            )
        inventario = self.cargar_inventario() or {}
        registro = inventario.get(str(articulo.get("id")))
        if registro is None or not registro.get("archivo"):
            return self._fatal(
                f"el artículo '{articulo.get('id')}' no tiene archivo en el inventario"
            )
        ruta_publicado = self.raiz / registro["archivo"]
        if not ruta_publicado.is_file():
            return self._fatal(f"no existe el artículo publicado: {registro['archivo']}")

        encabezado_borrador, cuerpo_borrador = borrador
        encabezado_publicado, cuerpo_publicado = parsear_frontmatter(
            ruta_publicado.read_text(encoding="utf-8")
        )

        alternativos = encabezado_borrador.get("titulos_alternativos", [])
        titulo_antes = primer_titulo(cuerpo_borrador) or (
            str(alternativos[0]) if alternativos else ""
        )
        titulo_despues = str(
            encabezado_publicado.get("titulo") or primer_titulo(cuerpo_publicado) or ""
        )

        antes = parrafos(cuerpo_borrador)
        despues = parrafos(cuerpo_publicado)
        comparador = difflib.SequenceMatcher(
            None, [normalizar(p) for p in antes], [normalizar(p) for p in despues]
        )
        eliminados, anadidos, modificados = [], [], []
        for etiqueta, i1, i2, j1, j2 in comparador.get_opcodes():
            if etiqueta == "equal":
                continue
            bloque_antes = antes[i1:i2]
            bloque_despues = despues[j1:j2]
            if etiqueta == "delete":
                eliminados.extend(bloque_antes)
            elif etiqueta == "insert":
                anadidos.extend(bloque_despues)
            else:  # replace: se empareja por similitud; el resto queda suelto
                usados: set[int] = set()
                for parrafo_antes in bloque_antes:
                    mejor_j, mejor_ratio = None, 0.0
                    for j, parrafo_despues in enumerate(bloque_despues):
                        if j in usados:
                            continue
                        ratio = similitud(parrafo_antes, parrafo_despues)
                        if ratio > mejor_ratio:
                            mejor_j, mejor_ratio = j, ratio
                    if mejor_j is not None and mejor_ratio >= 0.6:
                        usados.add(mejor_j)
                        modificados.append({
                            "antes": parrafo_antes,
                            "despues": bloque_despues[mejor_j],
                        })
                    else:
                        eliminados.append(parrafo_antes)
                anadidos.extend(
                    p for j, p in enumerate(bloque_despues) if j not in usados
                )

        palabras_antes = contar_palabras(cuerpo_borrador)
        palabras_despues = contar_palabras(cuerpo_publicado)
        imprimir_json({
            "oportunidad": oportunidad_id,
            "articulo": articulo.get("id"),
            "titulo": {
                "antes": titulo_antes,
                "despues": titulo_despues,
                "cambiado": normalizar(titulo_antes) != normalizar(titulo_despues),
            },
            "longitud": {
                "palabras_borrador": palabras_antes,
                "palabras_publicado": palabras_despues,
                "diferencia": palabras_despues - palabras_antes,
            },
            "eliminados": eliminados,
            "anadidos": anadidos,
            "modificados": modificados,
            "avisos": self.avisos,
        })
        return self._salida()

    # -- guardar-reglas ------------------------------------------------------------

    @staticmethod
    def _normalizar_regla(texto: str) -> str:
        """Texto de la regla sin la coletilla '(fecha, origen: …)'."""
        texto = re.sub(r"\(\s*\d{4}-\d{2}-\d{2}\s*,\s*origen:[^)]*\)\s*$", "", texto.strip())
        return normalizar(texto)

    def _reglas_existentes(self, lineas: list[str], inicio: int, fin: int) -> set[str]:
        existentes = set()
        for linea in lineas[inicio:fin]:
            coincidencia = re.match(r"^-\s+(.*)$", linea)
            if coincidencia:
                clave = self._normalizar_regla(coincidencia.group(1))
                if clave:
                    existentes.add(clave)
        return existentes

    def cmd_guardar_reglas(self, archivo: Path) -> int:
        if not archivo.is_file():
            return self._fatal(f"no existe el archivo de reglas: {archivo}")
        try:
            reglas = json.loads(archivo.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            return self._fatal(f"JSON ilegible: {exc}")
        if not isinstance(reglas, list) or not reglas:
            return self._fatal("se espera una lista JSON con al menos una regla")
        for i, regla in enumerate(reglas):
            if not isinstance(regla, dict):
                return self._fatal(f"la regla {i} no es un objeto")
            for campo in ("regla", "ejemplo_antes", "ejemplo_despues", "origen"):
                if not str(regla.get(campo, "")).strip():
                    return self._fatal(f"la regla {i} no tiene '{campo}'")
        if not self.ruta_estilo.is_file():
            return self._fatal(
                "no existe biblioteca/estilo.md: generarlo antes con analizar-biblioteca"
            )

        texto = self.ruta_estilo.read_text(encoding="utf-8")
        lineas = texto.split("\n")
        indice_seccion = next(
            (i for i, l in enumerate(lineas) if l.strip() == SECCION_REGLAS), None
        )
        if indice_seccion is None:
            self.avisar(f"estilo.md no tenía '{SECCION_REGLAS}'; se añade al final")
            if lineas and lineas[-1].strip():
                lineas.append("")
            lineas.extend([SECCION_REGLAS, ""])
            indice_seccion = len(lineas) - 2
        fin_seccion = next(
            (i for i in range(indice_seccion + 1, len(lineas))
             if re.match(r"^##\s", lineas[i])),
            len(lineas),
        )
        existentes = self._reglas_existentes(lineas, indice_seccion + 1, fin_seccion)

        anadidas, repetidas = [], []
        bloque: list[str] = []
        for regla in reglas:
            clave = self._normalizar_regla(regla["regla"])
            if clave in existentes:
                repetidas.append(regla["regla"])
                continue
            existentes.add(clave)
            anadidas.append(regla)
            bloque.extend([
                f"- {str(regla['regla']).strip()} ({self.hoy}, origen: {regla['origen']})",
                f"  - Antes: «{str(regla['ejemplo_antes']).strip()}»",
                f"  - Después: «{str(regla['ejemplo_despues']).strip()}»",
            ])

        if anadidas:
            insercion = fin_seccion
            while insercion > indice_seccion + 1 and not lineas[insercion - 1].strip():
                insercion -= 1
            if insercion > indice_seccion + 1 and lineas[insercion - 1].strip():
                bloque = [""] + bloque
            cola = lineas[insercion:]
            if not cola or cola[0].strip():
                bloque = bloque + [""]
            lineas[insercion:insercion] = bloque
            escribir_atomico(self.ruta_estilo, "\n".join(lineas))

            # anotar en resultado.json de cada contenido de origen
            por_origen: dict[str, list[str]] = {}
            for regla in anadidas:
                por_origen.setdefault(str(regla["origen"]), []).append(
                    str(regla["regla"]).strip()
                )
            for origen, textos in por_origen.items():
                if not (self.dir_contenidos / origen).is_dir():
                    self.avisar(
                        f"no existe biblioteca/contenidos/{origen}/: "
                        "la regla queda solo en estilo.md"
                    )
                    continue
                resultado = self.cargar_resultado(origen)
                guardadas = resultado.setdefault("reglas", [])
                claves = {self._normalizar_regla(r.get("regla", "")) for r in guardadas}
                for texto_regla in textos:
                    if self._normalizar_regla(texto_regla) not in claves:
                        guardadas.append({"regla": texto_regla, "fecha": self.hoy})
                escribir_json_atomico(self.ruta_resultado(origen), resultado)

        for repetida in repetidas:
            self.avisar(f"regla repetida, no se añade: {repetida}")
        imprimir_json({
            "anadidas": [r["regla"] for r in anadidas],
            "repetidas": repetidas,
            "archivo": "biblioteca/estilo.md",
            "avisos": self.avisos,
        })
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
        description="Cierra el ciclo: enlaza lo publicado, guarda métricas, "
                    "decisiones y reglas de estilo."
    )
    analizador.add_argument(
        "--config", default="proyecto.config.json",
        help="Ruta de proyecto.config.json (por defecto, el del directorio actual).",
    )
    analizador.add_argument(
        "--hoy", default=None,
        help="Fecha YYYY-MM-DD para fechas de registro (por defecto, la de hoy). Útil en pruebas.",
    )
    subcomandos = analizador.add_subparsers(dest="comando", required=True)
    subcomandos.add_parser("decisiones", help="Regenera biblioteca/decisiones.md.")
    p = subcomandos.add_parser("buscar-publicado", help="Propone el artículo publicado; no enlaza.")
    p.add_argument("oportunidad_id")
    p = subcomandos.add_parser("enlazar", help="Enlaza el contenido con el artículo publicado.")
    p.add_argument("oportunidad_id")
    p.add_argument("post_id")
    subcomandos.add_parser("metricas", help="Acumula las métricas públicas y el CSV si existe.")
    p = subcomandos.add_parser("diferencias", help="Diff por párrafos entre borrador y publicado.")
    p.add_argument("oportunidad_id")
    p = subcomandos.add_parser("guardar-reglas", help="Añade reglas a '## Reglas aprendidas'.")
    p.add_argument("archivo", help="JSON con la lista de reglas del modelo.")

    args = analizador.parse_args(argv)
    try:
        registrador = Registrador(Path(args.config), hoy=args.hoy)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return CODIGO_FATAL

    try:
        if args.comando == "decisiones":
            return registrador.cmd_decisiones()
        if args.comando == "buscar-publicado":
            return registrador.cmd_buscar_publicado(args.oportunidad_id)
        if args.comando == "enlazar":
            return registrador.cmd_enlazar(args.oportunidad_id, args.post_id)
        if args.comando == "metricas":
            return registrador.cmd_metricas()
        if args.comando == "diferencias":
            return registrador.cmd_diferencias(args.oportunidad_id)
        if args.comando == "guardar-reglas":
            return registrador.cmd_guardar_reglas(Path(args.archivo))
    except OSError as exc:
        print(f"ERROR: no pudo ejecutarse: {exc}", file=sys.stderr)
        return CODIGO_FATAL
    return CODIGO_FATAL


if __name__ == "__main__":
    sys.exit(main())
