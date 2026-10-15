#!/usr/bin/env python3
"""Pruebas de recuperar_newsletters.py con datos simulados.

La funcion de red se inyecta: nunca se accede a internet. Cada prueba trabaja
en una carpeta temporal con su propio proyecto.config.json.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

import recuperar_newsletters as rn

BASE = "https://ejemplo.substack.com"


def post_simulado(id_post, slug, fecha="2026-01-10", titulo=None, cuerpo=None,
                  reacciones=5, comentarios=2, restacks=1, audiencia="everyone",
                  paywall=False):
    return {
        "id": id_post,
        "slug": slug,
        "title": titulo or f"Titulo {id_post}",
        "subtitle": f"Subtitulo {id_post}",
        "post_date": f"{fecha}T08:00:00.000Z",
        "canonical_url": f"{BASE}/p/{slug}",
        "audience": audiencia,
        "type": "newsletter",
        "reaction_count": reacciones,
        "comment_count": comentarios,
        "restacks": restacks,
        "should_show_paywall": paywall,
        "body_html": cuerpo if cuerpo is not None else f"<p>Cuerpo del articulo {id_post}.</p>",
    }


class FetchFalso:
    """Fetch simulado: sirve el archivo paginado y los posts por slug."""

    def __init__(self, posts, fallo_en_offset=None):
        self.posts = posts  # lista de dicts de post_simulado
        self.fallo_en_offset = fallo_en_offset
        self.urls = []

    def __call__(self, url):
        self.urls.append(url)
        if "/api/v1/archive" in url:
            offset = int(url.split("offset=")[1].split("&")[0])
            if self.fallo_en_offset is not None and offset == self.fallo_en_offset:
                raise rn.ErrorRed(f"HTTP 500 en {url}", status=500)
            pagina = self.posts[offset:offset + rn.TAMANO_PAGINA]
            return [
                {k: p[k] for k in ("id", "slug", "title", "subtitle", "post_date",
                                   "canonical_url", "audience", "type")}
                for p in pagina
            ]
        if "/api/v1/posts/" in url:
            slug = url.rsplit("/", 1)[1]
            for p in self.posts:
                if p["slug"] == slug:
                    return p
            raise rn.ErrorRed(f"HTTP 404 en {url}", status=404)
        raise AssertionError(f"URL inesperada: {url}")


class BaseTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        config = {
            "publicacion": {"nombre": "Prueba", "substack": BASE, "idioma": "es"},
            "red": {"timeout_segundos": 5, "intentos": 2, "pausa_segundos": 0},
        }
        self.ruta_config = self.raiz / "proyecto.config.json"
        self.ruta_config.write_text(json.dumps(config), encoding="utf-8")
        self.biblioteca = self.raiz / "biblioteca" / "substack"

    def ejecutar(self, fetch, limite=None):
        recuperador = rn.Recuperador(self.ruta_config, fetch=fetch, dormir=lambda s: None)
        return recuperador.ejecutar(limite=limite)

    def inventario(self):
        return json.loads((self.biblioteca / "control" / "inventario.json").read_text(encoding="utf-8"))

    def informes(self):
        carpeta = self.biblioteca / "control" / "ejecuciones"
        return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(carpeta.glob("*.json"))]


class TestPrimeraEjecucion(BaseTest):
    def test_guarda_articulos_inventario_indice_e_informe(self):
        posts = [post_simulado(1, "uno"), post_simulado(2, "dos", fecha="2026-01-12")]
        codigo = self.ejecutar(FetchFalso(posts))
        self.assertEqual(codigo, 0)

        articulos = sorted(p.name for p in (self.biblioteca / "articulos").glob("*.md"))
        self.assertEqual(articulos, ["2026-01-10-uno.md", "2026-01-12-dos.md"])

        contenido = (self.biblioteca / "articulos" / "2026-01-10-uno.md").read_text(encoding="utf-8")
        self.assertIn("id: 1", contenido)
        self.assertIn("estado: completo", contenido)
        self.assertIn("Cuerpo del articulo 1.", contenido)

        inv = self.inventario()
        self.assertEqual(set(inv.keys()), {"1", "2"})
        self.assertEqual(inv["1"]["estado"], "completo")
        self.assertIn("huella", inv["1"])
        self.assertEqual(inv["1"]["metricas"]["reacciones"], 5)

        indice = (self.biblioteca / "INDICE.md").read_text(encoding="utf-8")
        self.assertIn("Titulo 1", indice)
        # orden: el mas reciente primero
        self.assertLess(indice.index("2026-01-12"), indice.index("2026-01-10"))

        self.assertTrue((self.biblioteca / "control" / "originales" / "1.json").is_file())
        informes = self.informes()
        self.assertEqual(len(informes), 1)
        self.assertEqual(informes[0]["contadores"]["nuevos"], 2)
        self.assertTrue(informes[0]["paginacion_completa"])


class TestIdempotencia(BaseTest):
    def test_repetir_no_duplica_ni_reescribe(self):
        posts = [post_simulado(1, "uno")]
        self.assertEqual(self.ejecutar(FetchFalso(posts)), 0)
        ruta = self.biblioteca / "articulos" / "2026-01-10-uno.md"
        mtime_antes = ruta.stat().st_mtime_ns

        self.assertEqual(self.ejecutar(FetchFalso(posts)), 0)
        archivos = list((self.biblioteca / "articulos").glob("*.md"))
        self.assertEqual(len(archivos), 1)
        self.assertEqual(ruta.stat().st_mtime_ns, mtime_antes, "el archivo no debe reescribirse")
        informes = self.informes()
        self.assertEqual(informes[-1]["contadores"]["sin_cambios"], 1)
        self.assertEqual(informes[-1]["contadores"]["nuevos"], 0)


class TestHistorial(BaseTest):
    def test_articulo_modificado_conserva_version_anterior(self):
        posts = [post_simulado(1, "uno", cuerpo="<p>Version original.</p>")]
        self.ejecutar(FetchFalso(posts))

        posts2 = [post_simulado(1, "uno", cuerpo="<p>Version corregida.</p>")]
        self.assertEqual(self.ejecutar(FetchFalso(posts2)), 0)

        historial = list((self.biblioteca / "control" / "historial" / "1").glob("*.md"))
        self.assertEqual(len(historial), 1)
        self.assertIn("Version original.", historial[0].read_text(encoding="utf-8"))
        actual = (self.biblioteca / "articulos" / "2026-01-10-uno.md").read_text(encoding="utf-8")
        self.assertIn("Version corregida.", actual)
        self.assertEqual(self.informes()[-1]["contadores"]["actualizados"], 1)


class TestProteccionCopiaCompleta(BaseTest):
    def test_extracto_no_sustituye_copia_completa(self):
        posts = [post_simulado(1, "uno", cuerpo="<p>Cuerpo completo.</p>")]
        self.ejecutar(FetchFalso(posts))

        # ahora llega como extracto (paywall)
        posts2 = [post_simulado(1, "uno", cuerpo="<p>Solo un trozo.</p>", paywall=True, audiencia="only_paid")]
        codigo = self.ejecutar(FetchFalso(posts2))

        actual = (self.biblioteca / "articulos" / "2026-01-10-uno.md").read_text(encoding="utf-8")
        self.assertIn("Cuerpo completo.", actual)
        self.assertNotIn("Solo un trozo.", actual)
        inv = self.inventario()
        self.assertEqual(inv["1"]["estado"], "completo")
        informe = self.informes()[-1]
        self.assertTrue(any(e["tipo"] == "incidencia" for e in informe["errores"]))
        self.assertEqual(codigo, 1, "una incidencia no puede presentarse como 'sin novedades'")

    def test_error_de_articulo_no_sustituye_copia_completa(self):
        posts = [post_simulado(1, "uno", cuerpo="<p>Cuerpo completo.</p>")]
        self.ejecutar(FetchFalso(posts))

        fetch = FetchFalso(posts)
        original = fetch.__call__

        def con_fallo(url):
            if "/api/v1/posts/" in url:
                raise rn.ErrorRed(f"HTTP 404 en {url}", status=404)
            return original(url)

        codigo = self.ejecutar(con_fallo)
        actual = (self.biblioteca / "articulos" / "2026-01-10-uno.md").read_text(encoding="utf-8")
        self.assertIn("Cuerpo completo.", actual)
        self.assertEqual(self.informes()[-1]["contadores"]["errores"], 1)
        self.assertEqual(codigo, 1)


class TestPaginacion(BaseTest):
    def test_sigue_hasta_pagina_vacia(self):
        posts = [post_simulado(i, f"post-{i}") for i in range(1, 31)]  # 30 posts, 3 paginas
        fetch = FetchFalso(posts)
        self.assertEqual(self.ejecutar(fetch), 0)
        paginas = [u for u in fetch.urls if "/archive" in u]
        self.assertEqual(len(paginas), 4, "3 paginas con datos + 1 vacia")
        self.assertEqual(len(self.inventario()), 30)
        self.assertTrue(self.informes()[-1]["paginacion_completa"])

    def test_pagina_fallida_deja_ejecucion_incompleta_con_codigo_1(self):
        posts = [post_simulado(i, f"post-{i}") for i in range(1, 31)]
        fetch = FetchFalso(posts, fallo_en_offset=12)  # falla la segunda pagina
        codigo = self.ejecutar(fetch)
        self.assertEqual(codigo, 1)
        informe = self.informes()[-1]
        self.assertFalse(informe["paginacion_completa"])
        self.assertTrue(any(e["tipo"] == "pagina" and "HTTP 500" in e["motivo"] for e in informe["errores"]))
        # los articulos de la primera pagina si se guardaron
        self.assertEqual(len(self.inventario()), 12)


class TestCambioDeSlug(BaseTest):
    def test_mismo_id_con_slug_nuevo_no_duplica(self):
        posts = [post_simulado(1, "titulo-viejo")]
        self.ejecutar(FetchFalso(posts))

        posts2 = [post_simulado(1, "titulo-nuevo")]
        self.assertEqual(self.ejecutar(FetchFalso(posts2)), 0)

        archivos = sorted(p.name for p in (self.biblioteca / "articulos").glob("*.md"))
        self.assertEqual(archivos, ["2026-01-10-titulo-nuevo.md"], "no debe haber duplicados")
        inv = self.inventario()
        self.assertEqual(len(inv), 1)
        self.assertEqual(inv["1"]["slug"], "titulo-nuevo")


class TestMetricas(BaseTest):
    def test_metricas_se_actualizan_sin_contar_como_cambio(self):
        posts = [post_simulado(1, "uno", reacciones=5)]
        self.ejecutar(FetchFalso(posts))
        ruta = self.biblioteca / "articulos" / "2026-01-10-uno.md"
        mtime_antes = ruta.stat().st_mtime_ns

        posts2 = [post_simulado(1, "uno", reacciones=42, comentarios=7)]
        self.assertEqual(self.ejecutar(FetchFalso(posts2)), 0)

        inv = self.inventario()
        self.assertEqual(inv["1"]["metricas"]["reacciones"], 42)
        self.assertEqual(inv["1"]["metricas"]["comentarios"], 7)
        informe = self.informes()[-1]
        self.assertEqual(informe["contadores"]["sin_cambios"], 1)
        self.assertEqual(informe["contadores"]["actualizados"], 0)
        self.assertEqual(ruta.stat().st_mtime_ns, mtime_antes, "el articulo no debe reescribirse")


class TestConversionMarkdown(unittest.TestCase):
    def test_conserva_titulos_listas_y_enlaces(self):
        html = (
            "<h2>Un titulo</h2>"
            "<p>Parrafo con <a href='https://ejemplo.com'>un enlace</a> y <strong>negrita</strong>.</p>"
            "<ul><li>Primero</li><li>Segundo</li></ul>"
            "<ol><li>Uno</li><li>Dos</li></ol>"
            "<blockquote><p>Una cita.</p></blockquote>"
            "<pre><code>print('hola')</code></pre>"
            "<p><img src='https://ejemplo.com/foto.png' alt='Foto'></p>"
        )
        md = rn.html_a_markdown(html)
        self.assertIn("## Un titulo", md)
        self.assertIn("[un enlace](https://ejemplo.com)", md)
        self.assertIn("**negrita**", md)
        self.assertIn("- Primero", md)
        self.assertIn("- Segundo", md)
        self.assertIn("1. Uno", md)
        self.assertIn("2. Dos", md)
        self.assertIn("> Una cita.", md)
        self.assertIn("print('hola')", md)
        self.assertIn("```", md)
        self.assertIn("![Foto](https://ejemplo.com/foto.png)", md)

    def test_huella_estable_ante_normalizacion(self):
        a = rn.calcular_huella("Hola\n\n\nMundo \n")
        b = rn.calcular_huella("Hola\r\n\r\n\r\nMundo\r\n")
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main(verbosity=2)
