#!/usr/bin/env python3
"""Recupera todo lo publicado en una newsletter de Substack y lo mantiene en
biblioteca/substack/. Python sin IA y solo biblioteca estándar.

Uso:
    python .agents/skills/recuperar-newsletters/scripts/recuperar_newsletters.py
        [--config proyecto.config.json] [--limite N]

Códigos de salida: 0 correcto, 1 errores parciales o paginación incompleta,
2 no pudo ejecutarse.
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
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Callable

TAMANO_PAGINA = 12
MAX_PAGINAS = 1000  # tope de seguridad: 12.000 artículos
CARPETA_SALIDA = Path("biblioteca") / "substack"
USER_AGENT = "recuperar-newsletters/1.0 (+uso personal; sin IA)"

# Tipo de la función de red inyectable: (url, timeout) -> (código HTTP, cuerpo).
# Debe lanzar OSError (o subclase) ante fallos de conexión o timeout.
FuncionRed = Callable[[str, float], "tuple[int, bytes]"]


class ErrorConfiguracion(Exception):
    pass


# --------------------------------------------------------------------------
# Red
# --------------------------------------------------------------------------

def obtener_http(url: str, timeout: float) -> tuple[int, bytes]:
    """Implementación real de la red con urllib."""
    peticion = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(peticion, timeout=timeout) as respuesta:
            return respuesta.status, respuesta.read()
    except urllib.error.HTTPError as error:
        return error.code, error.read() if error.fp else b""


class ClienteSubstack:
    """Pide JSON con timeout, reintentos con espera creciente y pausa entre peticiones."""

    def __init__(self, base: str, red: dict, obtener: FuncionRed,
                 dormir: Callable[[float], None]):
        self.base = base.rstrip("/")
        self.timeout = float(red["timeout_segundos"])
        self.intentos = int(red["intentos"])
        self.pausa = float(red["pausa_segundos"])
        self.obtener = obtener
        self.dormir = dormir
        self._primera = True

    def pedir_json(self, ruta: str):
        """Devuelve (datos, None) si va bien o (None, motivo) si falla."""
        url = self.base + ruta
        motivo = "sin intentos"
        for intento in range(self.intentos):
            if intento > 0:  # espera creciente: 1x, 2x, 4x... (mínimo 1 s)
                self.dormir(max(self.pausa, 1.0) * (2 ** (intento - 1)))
            elif not self._primera:  # pausa entre peticiones
                self.dormir(self.pausa)
            self._primera = False
            try:
                estado, cuerpo = self.obtener(url, self.timeout)
            except (OSError, ValueError) as error:  # conexión, timeout, URL
                motivo = f"fallo de red: {error.__class__.__name__}: {error}"
                continue
            if estado == 200:
                try:
                    return json.loads(cuerpo.decode("utf-8")), None
                except (UnicodeDecodeError, json.JSONDecodeError) as error:
                    motivo = f"respuesta no es JSON válido: {error}"
                    continue
            motivo = f"HTTP {estado}"
            if estado == 429 or 500 <= estado <= 599:
                continue
            return None, motivo  # 404 y otros 4xx: no se reintenta
        return None, f"{motivo} tras {self.intentos} intentos"


# --------------------------------------------------------------------------
# HTML a Markdown
# --------------------------------------------------------------------------

class _ConversorMarkdown(HTMLParser):
    BLOQUES = {"p", "div", "section", "article", "figure", "figcaption", "header",
               "footer", "table", "thead", "tbody", "tr", "dl", "dt", "dd"}
    IGNORAR = {"script", "style", "svg", "button", "form", "noscript", "head", "title"}
    INLINE = {"a": "", "strong": "**", "b": "**", "em": "*", "i": "*",
              "code": "`", "s": "~~", "del": "~~", "strike": "~~"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.bloques: list[tuple[str, str]] = []
        self.pila: list[list] = [["", None, []]]  # [etiqueta, atributo, trozos]
        self.listas: list[list] = []  # [tipo, contador]
        self.cita = 0
        self.ignorar = 0
        self.pre: list[str] | None = None
        self.tipo = "p"
        self.prefijo = ""

    # -- utilidades
    def _emitir(self, texto: str):
        self.pila[-1][2].append(texto)

    def _cerrar_inline(self, etiqueta: str, attr):
        trozos = "".join(self.pila.pop()[2])
        if etiqueta == "a":
            limpio = trozos.strip()
            if not attr or not limpio:
                self._emitir(trozos)
            elif re.fullmatch(r"(!\[[^\]]*\]\([^)]*\)\s*)+", limpio):
                self._emitir(limpio)  # enlace que solo envuelve imágenes
            else:
                self._emitir(f"[{limpio}]({attr})")
            return
        marca = self.INLINE[etiqueta]
        limpio = trozos.strip()
        if not limpio:
            self._emitir(trozos)
            return
        inicio = " " if trozos[:1].isspace() else ""
        fin = " " if trozos[-1:].isspace() else ""
        self._emitir(f"{inicio}{marca}{limpio}{marca}{fin}")

    def _vaciar(self):
        while len(self.pila) > 1:
            etiqueta, attr, _ = self.pila[-1]
            self._cerrar_inline(etiqueta, attr)
        texto = "".join(self.pila[0][2])
        self.pila[0][2] = []
        lineas = [re.sub(r"[ \t]+", " ", l).strip() for l in texto.split("\n")]
        lineas = [l for l in lineas if l]
        if not lineas:
            return
        if self.tipo == "li":
            sangria = " " * len(self.prefijo)
            cuerpo = "\n".join([self.prefijo + lineas[0]] + [sangria + l for l in lineas[1:]])
            self.prefijo = sangria  # el resto del mismo elemento continúa sangrado
        else:
            cuerpo = "\n".join(lineas)
            if self.prefijo:
                cuerpo = self.prefijo + cuerpo
        self._anadir_bloque(self.tipo, cuerpo)

    def _anadir_bloque(self, tipo: str, cuerpo: str):
        if self.cita:
            marca = "> " * self.cita
            cuerpo = "\n".join((marca + l).rstrip() for l in cuerpo.split("\n"))
        self.bloques.append((tipo, cuerpo))

    # -- eventos
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.ignorar or tag in self.IGNORAR:
            if tag in self.IGNORAR:
                self.ignorar += 1
            return
        if self.pre is not None:
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._vaciar()
            self.tipo, self.prefijo = "h", "#" * int(tag[1]) + " "
        elif tag in ("ul", "ol"):
            self._vaciar()
            self.listas.append([tag, 0])
        elif tag == "li":
            self._vaciar()
            nivel = max(len(self.listas), 1)
            tipo, _ = self.listas[-1] if self.listas else ("ul", 0)
            if self.listas:
                self.listas[-1][1] += 1
            marca = f"{self.listas[-1][1]}. " if tipo == "ol" else "- "
            self.tipo, self.prefijo = "li", "   " * (nivel - 1) + marca
        elif tag == "blockquote":
            self._vaciar()
            self.cita += 1
        elif tag == "pre":
            self._vaciar()
            self.pre = []
        elif tag == "br":
            self._emitir("\n")
        elif tag == "hr":
            self._vaciar()
            self._anadir_bloque("hr", "---")
        elif tag == "img":
            src = a.get("src") or ""
            if src:
                alt = (a.get("alt") or a.get("title") or "imagen").replace("]", "")
                self._emitir(f"![{alt}]({src})")
        elif tag == "iframe":
            src = a.get("src") or ""
            if src:
                self._vaciar()
                self._anadir_bloque("p", f"[Contenido incrustado]({src})")
        elif tag in self.INLINE:
            self.pila.append([tag, a.get("href") if tag == "a" else None, []])
        elif tag in ("td", "th"):
            self._emitir(" | ")
        elif tag in self.BLOQUES:
            if self.tipo == "li":
                if "".join(self.pila[-1][2]).strip():
                    self._emitir("\n")
            else:
                self._vaciar()

    def handle_endtag(self, tag):
        if tag in self.IGNORAR:
            self.ignorar = max(self.ignorar - 1, 0)
            return
        if self.ignorar:
            return
        if self.pre is not None:
            if tag == "pre":
                codigo = "".join(self.pre).strip("\n")
                self.pre = None
                self._anadir_bloque("pre", "```\n" + codigo + "\n```")
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._vaciar()
            self.tipo, self.prefijo = "p", ""
        elif tag in ("ul", "ol"):
            self._vaciar()
            if self.listas:
                self.listas.pop()
            if self.listas:
                self.tipo, self.prefijo = "li", "   " * len(self.listas)
            else:
                self.tipo, self.prefijo = "p", ""
        elif tag == "li":
            self._vaciar()
            if self.listas:
                self.tipo, self.prefijo = "li", "   " * len(self.listas)
            else:
                self.tipo, self.prefijo = "p", ""
        elif tag == "blockquote":
            self._vaciar()
            self.cita = max(self.cita - 1, 0)
        elif tag in self.INLINE:
            if any(n[0] == tag for n in self.pila[1:]):
                while len(self.pila) > 1:
                    etiqueta, attr, _ = self.pila[-1]
                    self._cerrar_inline(etiqueta, attr)
                    if etiqueta == tag:
                        break
        elif tag in self.BLOQUES and self.tipo != "li":
            self._vaciar()

    def handle_data(self, data):
        if self.ignorar:
            return
        if self.pre is not None:
            self.pre.append(data)
            return
        self._emitir(re.sub(r"\s+", " ", data))

    def resultado(self) -> str:
        self._vaciar()
        salida: list[str] = []
        anterior = None
        for tipo, cuerpo in self.bloques:
            if salida:
                salida.append("\n" if tipo == "li" and anterior == "li" else "\n\n")
            salida.append(cuerpo)
            anterior = tipo
        return "".join(salida).strip() + "\n" if salida else ""


def html_a_markdown(html: str) -> str:
    conversor = _ConversorMarkdown()
    conversor.feed(html or "")
    conversor.close()
    return conversor.resultado()


def normalizar(markdown: str) -> str:
    texto = unicodedata.normalize("NFC", markdown).replace("\r\n", "\n").replace("\r", "\n")
    texto = "\n".join(l.rstrip() for l in texto.split("\n"))
    texto = re.sub(r"\n{3,}", "\n\n", texto).strip()
    return texto + "\n" if texto else ""


def huella(markdown: str) -> str:
    return "sha256:" + hashlib.sha256(normalizar(markdown).encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------
# Archivos
# --------------------------------------------------------------------------

def escribir_atomico(ruta: Path, contenido: str) -> None:
    """Escribe en un temporal de la misma carpeta y lo renombra."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporal = tempfile.mkstemp(dir=ruta.parent, prefix=".tmp-", suffix=ruta.suffix)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as archivo:
            archivo.write(contenido)
            archivo.flush()
            os.fsync(archivo.fileno())
        os.replace(temporal, ruta)
    except BaseException:
        try:
            os.unlink(temporal)
        except OSError:
            pass
        raise


def escribir_si_cambia(ruta: Path, contenido: str) -> bool:
    if ruta.exists() and ruta.read_text(encoding="utf-8") == contenido:
        return False
    escribir_atomico(ruta, contenido)
    return True


def a_json(datos) -> str:
    return json.dumps(datos, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def _yaml(valor) -> str:
    if valor is None:
        return "null"
    if isinstance(valor, bool):
        return "true" if valor else "false"
    if isinstance(valor, (int, float)):
        return str(valor)
    return json.dumps(str(valor), ensure_ascii=False)  # cadena entre comillas dobles: YAML válido


def slug_seguro(slug: str) -> str:
    limpio = re.sub(r"[^A-Za-z0-9._-]+", "-", slug or "").strip("-.")
    return limpio[:120] or "sin-slug"


# --------------------------------------------------------------------------
# Configuración
# --------------------------------------------------------------------------

def leer_config(ruta: Path) -> dict:
    if not ruta.is_file():
        raise ErrorConfiguracion(f"no existe el archivo de configuración: {ruta}")
    try:
        config = json.loads(ruta.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ErrorConfiguracion(f"no se puede leer {ruta}: {error}") from error
    substack = (config.get("publicacion") or {}).get("substack")
    if not isinstance(substack, str) or not re.match(r"^https?://[^/\s]+", substack):
        raise ErrorConfiguracion("publicacion.substack debe ser una URL http(s)")
    red = config.get("red") or {}
    try:
        timeout = float(red["timeout_segundos"])
        intentos = int(red["intentos"])
        pausa = float(red["pausa_segundos"])
    except (KeyError, TypeError, ValueError) as error:
        raise ErrorConfiguracion(
            "red.timeout_segundos, red.intentos y red.pausa_segundos son obligatorios y numéricos"
        ) from error
    if timeout <= 0 or intentos < 1 or pausa < 0:
        raise ErrorConfiguracion("red: timeout > 0, intentos >= 1 y pausa >= 0")
    return {"substack": substack.rstrip("/"),
            "red": {"timeout_segundos": timeout, "intentos": intentos, "pausa_segundos": pausa}}


# --------------------------------------------------------------------------
# Datos del artículo
# --------------------------------------------------------------------------

def _entero(valor) -> int:
    try:
        return int(valor or 0)
    except (TypeError, ValueError):
        return 0


def metricas(post: dict, capturadas: str) -> dict:
    reacciones = post.get("reaction_count")
    if reacciones is None and isinstance(post.get("reactions"), dict):
        reacciones = sum(_entero(v) for v in post["reactions"].values())
    restacks = post.get("restacks")
    if restacks is None:
        restacks = post.get("restack_count")
    return {"reacciones": _entero(reacciones), "comentarios": _entero(post.get("comment_count")),
            "restacks": _entero(restacks), "capturadas": capturadas}


def clasificar(post: dict) -> tuple[str, str, str]:
    """Devuelve (estado, cuerpo_markdown, motivo) con estado completo o extracto."""
    html = post.get("body_html") or ""
    audiencia = post.get("audience") or "everyone"
    if html.strip():
        cuerpo = html_a_markdown(html)
    else:
        texto = post.get("truncated_body_text") or post.get("description") or ""
        cuerpo = normalizar(texto)
    if audiencia != "everyone":
        return "extracto", cuerpo, f"audiencia '{audiencia}' (de pago o restringido)"
    if not html.strip():
        return "extracto", cuerpo, "la API no devuelve body_html"
    if re.search(r'class="[^"]*\bpaywall\b', html) or post.get("is_truncated"):
        return "extracto", cuerpo, "cuerpo truncado por el muro de pago"
    if not cuerpo.strip():
        return "extracto", cuerpo, "cuerpo vacío tras la conversión"
    return "completo", cuerpo, ""


def contenido_articulo(post: dict, estado: str, cuerpo: str, firma: str) -> str:
    campos = [
        ("id", post.get("id")),
        ("titulo", post.get("title") or ""),
        ("subtitulo", post.get("subtitle") or ""),
        ("fecha", post.get("post_date") or ""),
        ("url", post.get("canonical_url") or ""),
        ("tipo", post.get("type") or ""),
        ("audiencia", post.get("audience") or ""),
        ("estado", estado),
        ("huella", firma),
    ]
    cabecera = "\n".join(f"{clave}: {_yaml(valor)}" for clave, valor in campos)
    return f"---\n{cabecera}\n---\n\n{normalizar(cuerpo)}"


def nombre_archivo(post: dict) -> str:
    fecha = (post.get("post_date") or "")[:10]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fecha):
        fecha = "0000-00-00"
    return f"{fecha}-{slug_seguro(post.get('slug') or str(post.get('id')))}.md"


# --------------------------------------------------------------------------
# Ejecución
# --------------------------------------------------------------------------

def _iso(momento: datetime) -> str:
    return momento.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Ejecucion:
    def __init__(self, raiz: Path, config: dict, obtener: FuncionRed,
                 dormir: Callable[[float], None], reloj: Callable[[], datetime],
                 limite: int | None, max_paginas: int):
        self.raiz = raiz
        self.config = config
        self.reloj = reloj
        self.limite = limite
        self.max_paginas = max_paginas
        self.cliente = ClienteSubstack(config["substack"], config["red"], obtener, dormir)
        self.salida = raiz / CARPETA_SALIDA
        self.dir_articulos = self.salida / "articulos"
        self.dir_control = self.salida / "control"
        inicio = reloj()
        self.run_id = inicio.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self.informe = {
            "run_id": self.run_id,
            "inicio": _iso(inicio),
            "fin": None,
            "publicacion": config["substack"],
            "limite": limite,
            "estado": "en_curso",
            "codigo_salida": None,
            "paginacion": {"paginas_leidas": 0, "terminada": False, "estado": "pendiente",
                           "motivo": ""},
            "articulos_en_archivo": 0,
            "contadores": {"nuevos": 0, "actualizados": 0, "sin_cambios": 0,
                           "extractos": 0, "errores": 0},
            "cambios": [],
            "incidencias": [],
            "errores": [],
        }
        self.inventario = self._leer_inventario()

    # -- inventario
    def _ruta_inventario(self) -> Path:
        return self.dir_control / "inventario.json"

    def _leer_inventario(self) -> dict:
        ruta = self._ruta_inventario()
        if ruta.exists():
            try:
                datos = json.loads(ruta.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
                raise ErrorConfiguracion(f"inventario ilegible, no se toca: {ruta}: {error}") from error
            if not isinstance(datos, dict) or not isinstance(datos.get("articulos", {}), dict):
                raise ErrorConfiguracion(f"inventario con formato inesperado, no se toca: {ruta}")
            datos.setdefault("articulos", {})
            return datos
        return {"version": 1, "publicacion": self.config["substack"], "articulos": {}}

    def _rel(self, ruta: Path) -> str:
        return ruta.relative_to(self.raiz).as_posix()

    # -- paginación
    def recorrer_archivo(self) -> list[dict] | None:
        pag = self.informe["paginacion"]
        vistos: dict[str, dict] = {}
        offset = 0
        while True:
            if pag["paginas_leidas"] >= self.max_paginas:
                pag.update(estado="incompleta", motivo=f"tope de seguridad de {self.max_paginas} páginas alcanzado")
                self._error("paginacion", f"offset={offset}", pag["motivo"])
                break
            datos, motivo = self.cliente.pedir_json(
                f"/api/v1/archive?sort=new&offset={offset}&limit={TAMANO_PAGINA}")
            if datos is not None and isinstance(datos, dict):
                datos = datos.get("posts")
            if datos is not None and not isinstance(datos, list):
                datos, motivo = None, "la página del archivo no es una lista"
            if datos is None:
                if pag["paginas_leidas"] == 0:
                    pag.update(estado="fallida", motivo=f"archivo inaccesible (offset={offset}): {motivo}")
                    self._error("paginacion", f"offset={offset}", motivo)
                    return None
                pag.update(estado="incompleta", motivo=f"falló la página offset={offset}: {motivo}")
                self._error("paginacion", f"offset={offset}", motivo)
                break
            pag["paginas_leidas"] += 1
            if not datos:
                pag.update(estado="completa", terminada=True, motivo="página vacía alcanzada")
                break
            for item in datos:
                if isinstance(item, dict) and item.get("id") is not None and item.get("slug"):
                    vistos.setdefault(str(item["id"]), item)
            offset += len(datos)
            if self.limite is not None and len(vistos) >= self.limite:
                pag.update(estado="limitada", motivo=f"detenida por --limite {self.limite}")
                break
        lista = list(vistos.values())
        if self.limite is not None:
            lista = lista[: self.limite]
        self.informe["articulos_en_archivo"] = len(lista)
        return lista

    # -- registro
    def _error(self, ambito: str, referencia: str, motivo: str, **extra):
        self.informe["errores"].append({"ambito": ambito, "referencia": referencia,
                                        "motivo": motivo, **extra})

    def _cambio(self, tipo: str, registro: dict, motivo: str):
        self.informe["cambios"].append({"tipo": tipo, "id": registro["id"], "slug": registro["slug"],
                                        "archivo": registro["archivo"], "motivo": motivo})

    def _incidencia(self, id_: str, slug: str, motivo: str, ahora: str):
        self.informe["incidencias"].append({"id": id_, "slug": slug, "motivo": motivo})
        registro = self.inventario["articulos"].get(id_)
        if registro is not None:
            registro["ultima_incidencia"] = {"fecha": ahora, "motivo": motivo}

    # -- artículo
    def procesar(self, item: dict):
        cont = self.informe["contadores"]
        id_ = str(item["id"])
        slug = item["slug"]
        ahora = _iso(self.reloj())
        existente = self.inventario["articulos"].get(id_)

        post, motivo = self.cliente.pedir_json(f"/api/v1/posts/{slug}")
        if post is not None and (not isinstance(post, dict) or str(post.get("id")) != id_):
            post, motivo = None, "la respuesta no corresponde al id del archivo"
        if post is None:
            cont["errores"] += 1
            self._error("articulo", slug, motivo, id=id_)
            if existente:
                self._incidencia(id_, slug, f"error al obtenerlo ({motivo}); se conserva la copia", ahora)
            return

        estado, cuerpo, motivo_estado = clasificar(post)
        firma = huella(cuerpo)
        if estado == "extracto":
            cont["extractos"] += 1
        texto = contenido_articulo(post, estado, cuerpo, firma)
        datos_metricas = metricas(post, ahora)

        if existente and existente.get("estado") == "completo" and estado != "completo":
            existente["metricas"] = datos_metricas
            existente["ultima_comprobacion"] = ahora
            cont["sin_cambios"] += 1
            self._incidencia(id_, slug, f"llega como extracto ({motivo_estado}); se conserva la copia completa", ahora)
            return

        destino = self._destino(post, id_)
        anterior = self.raiz / existente["archivo"] if existente else None

        if existente is None:
            escribir_atomico(destino, texto)
            registro = {
                "id": post.get("id"), "slug": slug, "titulo": post.get("title") or "",
                "fecha": post.get("post_date") or "", "url": post.get("canonical_url") or "",
                "archivo": self._rel(destino), "estado": estado, "huella": firma,
                "metricas": datos_metricas, "primera_descarga": ahora,
                "ultima_comprobacion": ahora, "ultima_modificacion": ahora,
                "slugs_anteriores": [], "ultima_incidencia": None,
            }
            self.inventario["articulos"][id_] = registro
            cont["nuevos"] += 1
            self._cambio("nuevo", registro, estado if not motivo_estado else f"{estado}: {motivo_estado}")
        elif existente.get("huella") == firma and anterior.exists() \
                and anterior.read_text(encoding="utf-8") == texto and anterior == destino:
            cont["sin_cambios"] += 1
        elif existente.get("huella") == firma and anterior.exists():
            # Mismo contenido, distinto slug, título u otros metadatos: se reescribe sin historial.
            escribir_atomico(destino, texto)
            if anterior != destino:
                anterior.unlink()
            cont["actualizados"] += 1
            motivos = self._diferencias(existente, post, destino)
            self._actualizar_registro(existente, post, destino, estado, firma, ahora, contenido=False)
            self._cambio("metadatos", existente, motivos)
        else:
            if anterior is not None and anterior.exists():
                self._guardar_historial(id_, anterior)
                motivo_cambio = "contenido modificado; versión anterior en historial"
            else:
                motivo_cambio = "archivo local ausente; se vuelve a guardar"
            escribir_atomico(destino, texto)
            if anterior is not None and anterior != destino and anterior.exists():
                anterior.unlink()
            cont["actualizados"] += 1
            self._actualizar_registro(existente, post, destino, estado, firma, ahora, contenido=True)
            self._cambio("contenido", existente, motivo_cambio)

        registro = self.inventario["articulos"][id_]
        registro["metricas"] = datos_metricas
        registro["ultima_comprobacion"] = ahora
        escribir_si_cambia(self.dir_control / "originales" / f"{id_}.json", a_json(post))

    def _destino(self, post: dict, id_: str) -> Path:
        destino = self.dir_articulos / nombre_archivo(post)
        ocupado = any(r.get("archivo") == self._rel(destino) and k != id_
                      for k, r in self.inventario["articulos"].items())
        if ocupado:
            destino = destino.with_name(f"{destino.stem}-{id_}.md")
        return destino

    def _diferencias(self, registro: dict, post: dict, destino: Path) -> str:
        cambios = []
        if registro.get("slug") != post.get("slug"):
            cambios.append(f"slug '{registro.get('slug')}' -> '{post.get('slug')}'")
        if registro.get("titulo") != (post.get("title") or ""):
            cambios.append("título")
        if registro.get("archivo") != self._rel(destino) and not cambios:
            cambios.append("nombre de archivo")
        return "metadatos cambiados: " + (", ".join(cambios) or "cabecera") + "; mismo contenido"

    def _actualizar_registro(self, registro, post, destino, estado, firma, ahora, contenido):
        if registro.get("slug") != post.get("slug"):
            registro.setdefault("slugs_anteriores", []).append(registro.get("slug"))
        registro.update(slug=post.get("slug"), titulo=post.get("title") or "",
                        fecha=post.get("post_date") or "", url=post.get("canonical_url") or "",
                        archivo=self._rel(destino), estado=estado, huella=firma)
        if contenido:
            registro["ultima_modificacion"] = ahora

    def _guardar_historial(self, id_: str, anterior: Path):
        carpeta = self.dir_control / "historial" / id_
        ruta = carpeta / f"{self.run_id}.md"
        n = 1
        while ruta.exists():
            n += 1
            ruta = carpeta / f"{self.run_id}-{n}.md"
        escribir_atomico(ruta, anterior.read_text(encoding="utf-8"))

    # -- índice
    def generar_indice(self):
        registros = sorted(self.inventario["articulos"].values(),
                           key=lambda r: (r.get("fecha") or "", str(r.get("id"))), reverse=True)
        lineas = ["# Índice de artículos publicados", "",
                  "Generado por `recuperar-newsletters`. No se edita a mano.", "",
                  f"Total: {len(registros)} artículos.", "",
                  "| Fecha | Título | Estado | Archivo |", "|---|---|---|---|"]
        for r in registros:
            titulo = (r.get("titulo") or "").replace("|", "\\|")
            archivo = Path(r["archivo"]).name
            lineas.append(f"| {(r.get('fecha') or '')[:10]} | {titulo} | {r.get('estado')} | "
                          f"[{archivo}](articulos/{archivo}) |")
        escribir_si_cambia(self.salida / "INDICE.md", "\n".join(lineas) + "\n")

    def guardar(self):
        self.inventario["publicacion"] = self.config["substack"]
        self.inventario["articulos"] = dict(sorted(self.inventario["articulos"].items()))
        escribir_si_cambia(self._ruta_inventario(), a_json(self.inventario))
        self.generar_indice()

    def guardar_informe(self, estado: str, codigo: int):
        self.informe.update(fin=_iso(self.reloj()), estado=estado, codigo_salida=codigo)
        ruta = self.dir_control / "ejecuciones" / f"{self.run_id}.json"
        n = 1
        while ruta.exists():
            n += 1
            ruta = ruta.with_name(f"{self.run_id}-{n}.json")
        escribir_atomico(ruta, a_json(self.informe))
        self.informe["ruta_informe"] = self._rel(ruta)

    def ejecutar(self) -> int:
        try:
            lista = self.recorrer_archivo()
            if lista is None:
                self.guardar_informe("fallida", 2)
                return 2
            for item in lista:
                self.procesar(item)
            self.guardar()
        except KeyboardInterrupt:
            self.guardar()
            self.informe["paginacion"]["motivo"] += " (ejecución interrumpida)"
            self.guardar_informe("interrumpida", 1)
            raise
        incompleta = self.informe["paginacion"]["estado"] == "incompleta"
        codigo = 1 if incompleta or self.informe["contadores"]["errores"] else 0
        self.guardar_informe("con_errores" if codigo else "correcta", codigo)
        return codigo


def ejecutar(raiz: Path, config: dict, obtener: FuncionRed = obtener_http,
             dormir: Callable[[float], None] = time.sleep,
             reloj: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
             limite: int | None = None, max_paginas: int = MAX_PAGINAS) -> tuple[int, dict]:
    ejecucion = Ejecucion(raiz, config, obtener, dormir, reloj, limite, max_paginas)
    codigo = ejecucion.ejecutar()
    return codigo, ejecucion.informe


def resumen(informe: dict) -> str:
    c, p = informe["contadores"], informe["paginacion"]
    lineas = [
        f"Ejecución {informe['run_id']}: {informe['estado']} (código {informe['codigo_salida']})",
        f"Paginación: {p['estado']}, {p['paginas_leidas']} páginas leídas. {p['motivo']}",
        f"Artículos revisados: {informe['articulos_en_archivo']}",
        f"Nuevos: {c['nuevos']} | Actualizados: {c['actualizados']} | Sin cambios: {c['sin_cambios']} | "
        f"Extractos: {c['extractos']} | Errores: {c['errores']}",
    ]
    for cambio in informe["cambios"]:
        lineas.append(f"  + [{cambio['tipo']}] {cambio['archivo']}: {cambio['motivo']}")
    for incidencia in informe["incidencias"]:
        lineas.append(f"  ! {incidencia['slug']}: {incidencia['motivo']}")
    for error in informe["errores"]:
        lineas.append(f"  x [{error['ambito']}] {error['referencia']}: {error['motivo']}")
    if informe["codigo_salida"] == 2:
        lineas.append("NO SE PUDO CONSULTAR SUBSTACK: no se ha comprobado si hay novedades. "
                      "No se ha modificado ningún artículo.")
    elif p["estado"] == "incompleta" or c["errores"]:
        lineas.append("ATENCIÓN: resultado parcial. Esto no significa que no haya novedades.")
    elif not informe["cambios"]:
        lineas.append("Archivo recorrido sin errores: sin novedades.")
    if informe.get("ruta_informe"):
        lineas.append(f"Informe: {informe['ruta_informe']}")
    return "\n".join(lineas)


def main(argv: list[str] | None = None, obtener: FuncionRed = obtener_http) -> int:
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description="Recupera y actualiza los artículos de Substack.")
    parser.add_argument("--config", default="proyecto.config.json",
                        help="ruta de la configuración; su carpeta es la raíz del proyecto")
    parser.add_argument("--limite", type=int, default=None,
                        help="procesa solo los N artículos más recientes")
    args = parser.parse_args(argv)
    if args.limite is not None and args.limite < 1:
        print("Error de configuración: --limite debe ser >= 1", file=sys.stderr)
        return 2
    ruta = Path(args.config).resolve()
    try:
        config = leer_config(ruta)
    except ErrorConfiguracion as error:
        print(f"Error de configuración: {error}", file=sys.stderr)
        return 2
    try:
        codigo, informe = ejecutar(ruta.parent, config, obtener=obtener, limite=args.limite)
    except ErrorConfiguracion as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    print(resumen(informe))
    return codigo


if __name__ == "__main__":
    sys.exit(main())
