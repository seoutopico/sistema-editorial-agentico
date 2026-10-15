#!/usr/bin/env python3
"""Descarga el archivo publicado de una newsletter de Substack y lo mantiene
actualizado en biblioteca/substack/.

Fase 1 del sistema editorial (ver ARQUITECTURA.md, secciones 2, 4, 8.1 y 10).
Python sin IA, solo biblioteca estandar. La funcion de red es inyectable para
poder probar con respuestas simuladas.

Codigos de salida:
  0  todo correcto
  1  termino, pero con errores parciales o paginacion incompleta
  2  no pudo ejecutarse (configuracion invalida o archivo inaccesible)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

TAMANO_PAGINA = 12
TOPE_PAGINAS = 500  # tope de seguridad de la paginacion


# ---------------------------------------------------------------------------
# Red
# ---------------------------------------------------------------------------

class ErrorRed(Exception):
    """Fallo de red o HTTP. `status` es el codigo HTTP si lo hay."""

    def __init__(self, mensaje: str, status: int | None = None):
        super().__init__(mensaje)
        self.status = status


def crear_fetch_urllib(timeout: float):
    """Devuelve una funcion fetch(url) -> objeto JSON usando urllib."""

    def fetch(url: str):
        peticion = urllib.request.Request(
            url, headers={"User-Agent": "recuperar-newsletters/1.0"}
        )
        try:
            with urllib.request.urlopen(peticion, timeout=timeout) as respuesta:
                return json.loads(respuesta.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise ErrorRed(f"HTTP {exc.code} en {url}", status=exc.code) from exc
        except urllib.error.URLError as exc:
            raise ErrorRed(f"Fallo de red en {url}: {exc.reason}") from exc
        except (TimeoutError, json.JSONDecodeError, ValueError) as exc:
            raise ErrorRed(f"Respuesta invalida de {url}: {exc}") from exc

    return fetch


def pedir_con_reintentos(fetch, url: str, intentos: int, pausa_base: float, dormir):
    """Pide una URL reintentando ante 429 y 5xx con espera creciente.

    Un 404 (u otro 4xx distinto de 429) no se reintenta: es un error
    definitivo de ese recurso.
    """
    ultimo_error = None
    for intento in range(1, max(1, intentos) + 1):
        try:
            return fetch(url)
        except ErrorRed as exc:
            ultimo_error = exc
            reintentable = exc.status is None or exc.status == 429 or exc.status >= 500
            if not reintentable or intento == intentos:
                raise
            dormir(pausa_base * (2 ** (intento - 1)))
    raise ultimo_error  # inalcanzable, por claridad


# ---------------------------------------------------------------------------
# HTML -> Markdown (html.parser, sin dependencias)
# ---------------------------------------------------------------------------

class ConversorMarkdown(HTMLParser):
    """Convierte el HTML del cuerpo a Markdown legible.

    Conserva titulos, parrafos, listas, enlaces, citas, codigo e imagenes
    (estas como enlaces de imagen).
    """

    _BLOQUES = {"p", "div", "figure", "section", "article"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.partes: list[str] = []
        self.pila_listas: list[dict] = []
        self.pila_enlaces: list[str] = []
        self.en_pre = False
        self.nivel_cita = 0

    # -- utilidades -----------------------------------------------------
    def _emitir(self, texto: str):
        if self.nivel_cita and "\n" in texto:
            prefijo = "> " * self.nivel_cita
            texto = texto.replace("\n", "\n" + prefijo)
        self.partes.append(texto)

    def _salto_bloque(self):
        self._emitir("\n\n")

    # -- eventos --------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._salto_bloque()
            self._emitir("#" * int(tag[1]) + " ")
        elif tag in self._BLOQUES:
            self._salto_bloque()
        elif tag == "br":
            self._emitir("\n")
        elif tag in ("ul", "ol"):
            self.pila_listas.append({"tipo": tag, "n": 0})
            if len(self.pila_listas) == 1:
                self._salto_bloque()
        elif tag == "li":
            sangria = "  " * (len(self.pila_listas) - 1)
            if self.pila_listas and self.pila_listas[-1]["tipo"] == "ol":
                self.pila_listas[-1]["n"] += 1
                vineta = f"{self.pila_listas[-1]['n']}. "
            else:
                vineta = "- "
            self._emitir("\n" + sangria + vineta)
        elif tag == "a":
            self.pila_enlaces.append(a.get("href", ""))
            self._emitir("[")
        elif tag == "img":
            alt = a.get("alt", "") or "imagen"
            src = a.get("src", "")
            if src:
                self._emitir(f"![{alt}]({src})")
        elif tag == "blockquote":
            self._salto_bloque()
            self.nivel_cita += 1
            self._emitir("> " * self.nivel_cita)
        elif tag == "pre":
            self._salto_bloque()
            self._emitir("```\n")
            self.en_pre = True
        elif tag == "code":
            if not self.en_pre:
                self._emitir("`")
        elif tag in ("strong", "b"):
            self._emitir("**")
        elif tag in ("em", "i"):
            self._emitir("*")
        elif tag == "hr":
            self._salto_bloque()
            self._emitir("---")
            self._salto_bloque()

    def handle_endtag(self, tag):
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6") or tag in self._BLOQUES:
            self._salto_bloque()
        elif tag in ("ul", "ol"):
            if self.pila_listas:
                self.pila_listas.pop()
            if not self.pila_listas:
                self._salto_bloque()
        elif tag == "a":
            href = self.pila_enlaces.pop() if self.pila_enlaces else ""
            self._emitir(f"]({href})")
        elif tag == "blockquote":
            self.nivel_cita = max(0, self.nivel_cita - 1)
            self._salto_bloque()
        elif tag == "pre":
            self.en_pre = False
            self._emitir("\n```")
            self._salto_bloque()
        elif tag == "code":
            if not self.en_pre:
                self._emitir("`")
        elif tag in ("strong", "b"):
            self._emitir("**")
        elif tag in ("em", "i"):
            self._emitir("*")

    def handle_data(self, data):
        if self.en_pre:
            self._emitir(data)
        else:
            self._emitir(re.sub(r"\s+", " ", data))

    def resultado(self) -> str:
        texto = "".join(self.partes)
        texto = re.sub(r"[ \t]+\n", "\n", texto)
        texto = re.sub(r"\n{3,}", "\n\n", texto)
        return texto.strip()


def html_a_markdown(html: str) -> str:
    conversor = ConversorMarkdown()
    conversor.feed(html or "")
    conversor.close()
    return conversor.resultado()


def normalizar_markdown(md: str) -> str:
    """Normalizacion previa a la huella: saltos de linea y espacios estables."""
    texto = (md or "").replace("\r\n", "\n").replace("\r", "\n")
    texto = re.sub(r"[ \t]+\n", "\n", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


def calcular_huella(md: str) -> str:
    return hashlib.sha256(normalizar_markdown(md).encode("utf-8")).hexdigest()


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
    escribir_atomico(ruta, json.dumps(datos, ensure_ascii=False, indent=2) + "\n")


# ---------------------------------------------------------------------------
# Configuracion
# ---------------------------------------------------------------------------

class ErrorConfiguracion(Exception):
    pass


def cargar_config(ruta_config: Path) -> dict:
    if not ruta_config.is_file():
        raise ErrorConfiguracion(f"No existe el archivo de configuracion: {ruta_config}")
    try:
        config = json.loads(ruta_config.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ErrorConfiguracion(f"Configuracion ilegible ({ruta_config}): {exc}") from exc

    substack = config.get("publicacion", {}).get("substack")
    if not substack or not str(substack).startswith("http"):
        raise ErrorConfiguracion("Falta 'publicacion.substack' (URL) en la configuracion.")
    red = config.get("red", {})
    for clave in ("timeout_segundos", "intentos", "pausa_segundos"):
        if clave not in red:
            raise ErrorConfiguracion(f"Falta 'red.{clave}' en la configuracion.")
    return config


# ---------------------------------------------------------------------------
# Proceso principal
# ---------------------------------------------------------------------------

def _ahora_utc() -> datetime:
    return datetime.now(timezone.utc)


def _iso(momento: datetime) -> str:
    return momento.strftime("%Y-%m-%dT%H:%M:%SZ")


def _escapar_yaml(texto: str) -> str:
    return '"' + str(texto).replace("\\", "\\\\").replace('"', '\\"') + '"'


def extraer_metricas(post: dict, capturado: str) -> dict:
    reacciones = post.get("reaction_count")
    if reacciones is None:
        valores = post.get("reactions") or {}
        reacciones = sum(v for v in valores.values() if isinstance(v, int)) if isinstance(valores, dict) else 0
    return {
        "reacciones": reacciones or 0,
        "comentarios": post.get("comment_count") or 0,
        "restacks": post.get("restacks") or 0,
        "fecha_captura": capturado,
    }


class Recuperador:
    def __init__(self, ruta_config: Path, fetch=None, dormir=time.sleep, ahora=_ahora_utc):
        self.ruta_config = Path(ruta_config)
        self.config = cargar_config(self.ruta_config)
        self.raiz = self.ruta_config.resolve().parent
        self.base = str(self.config["publicacion"]["substack"]).rstrip("/")
        red = self.config["red"]
        self.timeout = float(red["timeout_segundos"])
        self.intentos = int(red["intentos"])
        self.pausa = float(red["pausa_segundos"])
        self.fetch = fetch or crear_fetch_urllib(self.timeout)
        self.dormir = dormir
        self.ahora = ahora

        base_bib = self.raiz / "biblioteca" / "substack"
        self.dir_articulos = base_bib / "articulos"
        self.dir_control = base_bib / "control"
        self.ruta_inventario = self.dir_control / "inventario.json"
        self.dir_originales = self.dir_control / "originales"
        self.dir_historial = self.dir_control / "historial"
        self.dir_ejecuciones = self.dir_control / "ejecuciones"
        self.ruta_indice = base_bib / "INDICE.md"

    # -- red --------------------------------------------------------------
    def _pedir(self, url: str):
        return pedir_con_reintentos(self.fetch, url, self.intentos, self.pausa, self.dormir)

    # -- inventario ---------------------------------------------------------
    def _cargar_inventario(self) -> dict:
        if self.ruta_inventario.is_file():
            return json.loads(self.ruta_inventario.read_text(encoding="utf-8"))
        return {}

    # -- paginacion ---------------------------------------------------------
    def recorrer_archivo(self, limite: int | None, informe: dict) -> list[dict]:
        items: list[dict] = []
        offset = 0
        paginas = 0
        while paginas < TOPE_PAGINAS:
            url = f"{self.base}/api/v1/archive?sort=new&offset={offset}&limit={TAMANO_PAGINA}"
            try:
                pagina = self._pedir(url)
            except ErrorRed as exc:
                if paginas == 0:
                    raise  # el archivo es inaccesible: no se puede ejecutar
                informe["paginacion_completa"] = False
                informe["errores"].append(
                    {"tipo": "pagina", "offset": offset, "motivo": str(exc)}
                )
                informe["paginas_leidas"] = paginas
                return items
            paginas += 1
            if paginas > 1:
                self.dormir(self.pausa)
            if not pagina:
                informe["paginacion_completa"] = True
                informe["paginas_leidas"] = paginas
                return items
            items.extend(pagina)
            if limite is not None and len(items) >= limite:
                informe["paginacion_completa"] = True
                informe["paginas_leidas"] = paginas
                return items[:limite]
            offset += TAMANO_PAGINA
        informe["paginacion_completa"] = False
        informe["errores"].append(
            {"tipo": "paginacion", "motivo": f"Alcanzado el tope de seguridad de {TOPE_PAGINAS} paginas."}
        )
        informe["paginas_leidas"] = paginas
        return items

    # -- articulos ------------------------------------------------------
    def _clasificar(self, post: dict) -> tuple[str, str]:
        """Devuelve (estado, html del cuerpo disponible)."""
        cuerpo = post.get("body_html") or ""
        if not cuerpo:
            # Sin cuerpo integro: articulo de pago o truncado; se guarda lo que haya.
            return "extracto", post.get("truncated_body_text") or ""
        if bool(post.get("should_show_paywall")):
            return "extracto", cuerpo
        return "completo", cuerpo

    def _nombre_archivo(self, fecha: str, slug: str) -> str:
        dia = (fecha or "")[:10] or "sin-fecha"
        return f"{dia}-{slug}.md"

    def _contenido_articulo(self, reg: dict, cuerpo_md: str) -> str:
        lineas = [
            "---",
            f"id: {reg['id']}",
            f"titulo: {_escapar_yaml(reg['titulo'])}",
            f"subtitulo: {_escapar_yaml(reg.get('subtitulo') or '')}",
            f"fecha: {reg['fecha']}",
            f"url: {reg['url']}",
            f"tipo: {reg.get('tipo') or ''}",
            f"audiencia: {reg.get('audiencia') or ''}",
            f"estado: {reg['estado']}",
            f"huella: {reg['huella']}",
            "---",
            "",
            cuerpo_md,
            "",
        ]
        return "\n".join(lineas)

    def _mover_a_historial(self, id_post: str, ruta_actual: Path, marca: str):
        destino_dir = self.dir_historial / str(id_post)
        destino_dir.mkdir(parents=True, exist_ok=True)
        destino = destino_dir / f"{marca}.md"
        contador = 1
        while destino.exists():
            destino = destino_dir / f"{marca}-{contador}.md"
            contador += 1
        os.replace(ruta_actual, destino)

    def procesar_item(self, item: dict, inventario: dict, informe: dict, momento: str):
        slug = item.get("slug") or ""
        id_post = str(item.get("id"))
        url_post = f"{self.base}/api/v1/posts/{slug}"
        try:
            post = self._pedir(url_post)
        except ErrorRed as exc:
            informe["contadores"]["errores"] += 1
            informe["errores"].append({"tipo": "articulo", "id": id_post, "slug": slug, "motivo": str(exc)})
            if id_post in inventario:
                inventario[id_post]["ultima_comprobacion"] = momento
            return

        estado, cuerpo_html = self._clasificar(post)
        cuerpo_md = html_a_markdown(cuerpo_html)
        huella = calcular_huella(cuerpo_md)
        metricas = extraer_metricas(post, momento)
        fecha = (post.get("post_date") or item.get("post_date") or "")[:10]
        registro_nuevo = {
            "id": id_post,
            "slug": slug,
            "titulo": post.get("title") or item.get("title") or "",
            "subtitulo": post.get("subtitle") or item.get("subtitle") or "",
            "fecha": fecha,
            "url": post.get("canonical_url") or item.get("canonical_url") or "",
            "tipo": post.get("type") or item.get("type") or "",
            "audiencia": post.get("audience") or item.get("audience") or "",
            "estado": estado,
            "huella": huella,
        }
        nombre = self._nombre_archivo(fecha, slug)
        ruta_md = self.dir_articulos / nombre

        # guardar la respuesta original de la API
        escribir_json_atomico(self.dir_originales / f"{id_post}.json", post)

        existente = inventario.get(id_post)
        if estado == "extracto":
            informe["contadores"]["extractos"] += 1

        if existente is None:
            # Articulo nuevo
            escribir_atomico(ruta_md, self._contenido_articulo(registro_nuevo, cuerpo_md))
            inventario[id_post] = {
                **registro_nuevo,
                "archivo": f"biblioteca/substack/articulos/{nombre}",
                "metricas": metricas,
                "primera_descarga": momento,
                "ultima_comprobacion": momento,
                "ultima_modificacion": momento,
            }
            informe["contadores"]["nuevos"] += 1
            informe["cambios"].append({"tipo": "nuevo", "id": id_post, "slug": slug, "estado": estado})
            return

        ruta_anterior = self.raiz / existente["archivo"]

        if existente["estado"] == "completo" and estado != "completo":
            # Un extracto o error nunca sustituye una copia completa
            existente["metricas"] = metricas
            existente["ultima_comprobacion"] = momento
            informe["errores"].append({
                "tipo": "incidencia", "id": id_post, "slug": slug,
                "motivo": f"Se recibio un '{estado}' pero existe copia completa; no se toca.",
            })
            return

        if huella == existente["huella"]:
            # Sin cambios de contenido: solo metricas y comprobacion
            existente["metricas"] = metricas
            existente["ultima_comprobacion"] = momento
            if slug != existente["slug"] or nombre != Path(existente["archivo"]).name:
                # cambio de slug con el mismo id: se renombra, sin duplicar
                if ruta_anterior.is_file() and ruta_anterior != ruta_md:
                    self.dir_articulos.mkdir(parents=True, exist_ok=True)
                    os.replace(ruta_anterior, ruta_md)
                existente["slug"] = slug
                existente["url"] = registro_nuevo["url"]
                existente["archivo"] = f"biblioteca/substack/articulos/{nombre}"
                informe["cambios"].append({"tipo": "renombrado", "id": id_post, "slug": slug})
            informe["contadores"]["sin_cambios"] += 1
            return

        # Huella distinta: se conserva la version anterior en historial
        marca = re.sub(r"[^0-9TZ]", "", momento) or momento
        if ruta_anterior.is_file():
            self._mover_a_historial(id_post, ruta_anterior, marca)
        escribir_atomico(ruta_md, self._contenido_articulo(registro_nuevo, cuerpo_md))
        inventario[id_post] = {
            **registro_nuevo,
            "archivo": f"biblioteca/substack/articulos/{nombre}",
            "metricas": metricas,
            "primera_descarga": existente.get("primera_descarga", momento),
            "ultima_comprobacion": momento,
            "ultima_modificacion": momento,
        }
        informe["contadores"]["actualizados"] += 1
        informe["cambios"].append({"tipo": "actualizado", "id": id_post, "slug": slug, "estado": estado})

    # -- salidas ----------------------------------------------------------
    def generar_indice(self, inventario: dict):
        registros = sorted(inventario.values(), key=lambda r: r.get("fecha") or "", reverse=True)
        lineas = [
            "# Indice de la biblioteca de Substack",
            "",
            "| Fecha | Titulo | Estado | Archivo |",
            "|---|---|---|---|",
        ]
        for r in registros:
            titulo = str(r.get("titulo", "")).replace("|", "\\|")
            enlace = f"[{Path(r['archivo']).name}](articulos/{Path(r['archivo']).name})"
            lineas.append(f"| {r.get('fecha', '')} | {titulo} | {r.get('estado', '')} | {enlace} |")
        lineas.append("")
        escribir_atomico(self.ruta_indice, "\n".join(lineas))

    # -- ejecucion ----------------------------------------------------------
    def ejecutar(self, limite: int | None = None) -> int:
        inicio = self.ahora()
        run_id = inicio.strftime("%Y%m%dT%H%M%SZ")
        momento = _iso(inicio)
        informe = {
            "run_id": run_id,
            "inicio": momento,
            "fin": None,
            "limite": limite,
            "paginas_leidas": 0,
            "paginacion_completa": False,
            "contadores": {"nuevos": 0, "actualizados": 0, "sin_cambios": 0, "extractos": 0, "errores": 0},
            "cambios": [],
            "errores": [],
        }

        inventario = self._cargar_inventario()

        try:
            items = self.recorrer_archivo(limite, informe)
        except ErrorRed as exc:
            print(f"ERROR: el archivo de Substack es inaccesible: {exc}", file=sys.stderr)
            return 2

        for indice, item in enumerate(items):
            if indice > 0:
                self.dormir(self.pausa)
            self.procesar_item(item, inventario, informe, momento)

        escribir_json_atomico(self.ruta_inventario, inventario)
        self.generar_indice(inventario)
        informe["fin"] = _iso(self.ahora())
        escribir_json_atomico(self.dir_ejecuciones / f"{run_id}.json", informe)

        hubo_fallos = (
            not informe["paginacion_completa"]
            or informe["contadores"]["errores"] > 0
            or any(e["tipo"] in ("pagina", "paginacion", "incidencia") for e in informe["errores"])
        )

        c = informe["contadores"]
        print(f"Ejecucion {run_id}")
        print(f"  Articulos vistos: {len(items)} en {informe['paginas_leidas']} paginas")
        print(f"  Nuevos: {c['nuevos']} | Actualizados: {c['actualizados']} | Sin cambios: {c['sin_cambios']}")
        print(f"  Extractos: {c['extractos']} | Errores: {c['errores']}")
        if not informe["paginacion_completa"]:
            print("  AVISO: la paginacion quedo INCOMPLETA; el resultado es parcial.")
        for e in informe["errores"]:
            print(f"  - [{e['tipo']}] {e.get('slug', e.get('offset', ''))}: {e['motivo']}")
        if hubo_fallos:
            print("  Resultado: terminado CON ERRORES PARCIALES (codigo 1).")
            return 1
        print("  Resultado: todo correcto (codigo 0).")
        return 0


def main(argv=None) -> int:
    analizador = argparse.ArgumentParser(description="Recupera el archivo de una newsletter de Substack.")
    analizador.add_argument("--config", default="proyecto.config.json", help="Ruta a proyecto.config.json")
    analizador.add_argument("--limite", type=int, default=None, help="Procesa solo los n articulos mas recientes")
    argumentos = analizador.parse_args(argv)
    try:
        recuperador = Recuperador(Path(argumentos.config))
    except ErrorConfiguracion as exc:
        print(f"ERROR de configuracion: {exc}", file=sys.stderr)
        return 2
    return recuperador.ejecutar(limite=argumentos.limite)


if __name__ == "__main__":
    sys.exit(main())
