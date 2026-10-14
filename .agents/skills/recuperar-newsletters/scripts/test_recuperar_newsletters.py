"""Pruebas con transporte simulado; ninguna conexión real."""
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit
import recuperar_newsletters as app

BASE = "https://ejemplo.substack.com"
CONFIG = {"publicacion": {"substack": BASE},
          "red": {"timeout_segundos": 2, "intentos": 3, "pausa_segundos": 0}}


def post(key=1, **changes):
    result = {"id": key, "slug": f"articulo-{key}", "title": f"Artículo {key}",
              "subtitle": "Subtítulo", "type": "newsletter", "audience": "everyone",
              "post_date": "2026-01-01T10:00:00Z", "canonical_url": f"{BASE}/p/articulo-{key}",
              "body_html": "<h2>Contenido</h2><p>Texto completo.</p>",
              "reaction_count": 2, "comment_count": 3, "restack_count": 4}
    result.update(changes)
    return result


class Response(io.BytesIO):
    status = 200
    headers = {"Content-Type": "application/json"}

    def __init__(self, value, url):
        self.url = url
        super().__init__(value if isinstance(value, bytes) else app.encoded(value))

    def geturl(self):
        return self.url


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.project = Path(temp.name).resolve()
        self.root = self.project / "biblioteca/substack"
        self.config = copy.deepcopy(CONFIG)
        guard = patch("socket.socket.connect", side_effect=AssertionError("Red real prohibida"))
        guard.start()
        self.addCleanup(guard.stop)

    def run_archive(self, items=None, pages=None, details=None, **options):
        items = [post()] if items is None else items
        pages = {0: items, len(items): []} if pages is None else pages
        details = {p["slug"]: p for p in items} if details is None else details
        calls = []
        def opener(request, timeout):
            calls.append((request.full_url, timeout))
            parsed = urlsplit(request.full_url)
            if parsed.path.endswith("/archive"):
                query = parse_qs(parsed.query)
                self.assertEqual(["12"], query["limit"])
                self.assertEqual(["new"], query["sort"])
                value = pages[int(query["offset"][0])]
            else:
                value = details[parsed.path.rsplit("/", 1)[-1]]
            if isinstance(value, Exception):
                raise value
            return Response(value, request.full_url)
        archive = app.Archive(self.project, self.config, opener=opener, sleep=lambda _: None, **options)
        report = archive.run()
        self.assertEqual(report, json.loads(archive.report_path.read_text(encoding="utf-8")))
        return archive, report, calls

    def row(self, key="1"):
        return json.loads((self.root / "control/inventario.json").read_text(encoding="utf-8"))["articulos"][key]

    def article(self):
        return self.root / self.row()["archivo"]

    def snapshot(self):
        article = self.article()
        return article.read_bytes(), article.stat().st_mtime_ns

    def test_first_run_outputs_schema_and_index_order(self):
        archive, report, _ = self.run_archive([post(), post(2, post_date="2026-02-01T10:00:00Z")])
        self.assertEqual(0, report["codigo_salida"])
        self.assertEqual(2, report["contadores"]["nuevos"])
        self.assertRegex(report["run_id"], r"^\d{8}T\d{6}Z$")
        self.assertEqual(report["run_id"] + ".json", archive.report_path.name)
        row = self.row()
        self.assertTrue({"id", "slug", "titulo", "fecha", "url", "archivo", "estado", "huella",
                         "metricas_publicas", "primera_descarga", "ultima_comprobacion", "ultima_modificacion"} <= row.keys())
        self.assertEqual("articulos/2026-01-01-articulo-1.md", row["archivo"])
        self.assertEqual(post(), json.loads((self.root / "control/originales/1.json").read_text(encoding="utf-8")))
        front, body = self.article().read_text(encoding="utf-8")[4:].split("\n---\n\n", 1)
        fields = dict((k, json.loads(v)) for k, v in (line.split(": ", 1) for line in front.splitlines()))
        self.assertEqual({"id", "titulo", "subtitulo", "fecha", "url", "tipo", "audiencia", "estado", "huella"}, fields.keys())
        self.assertEqual(app.digest(body.encode("utf-8")), fields["huella"])
        index = (self.root / "INDICE.md").read_text(encoding="utf-8")
        self.assertLess(index.index("2026-02-01"), index.index("2026-01-01"))
        self.assertIn(row["archivo"], index)

    def test_idempotency_and_unique_reports(self):
        first, _, _ = self.run_archive()
        before = self.snapshot()
        _, report, _ = self.run_archive()
        self.assertEqual(before, self.snapshot())
        self.assertEqual(1, report["contadores"]["sin_cambios"])
        self.assertEqual(1, len(list((self.root / "articulos").glob("*.md"))))
        self.assertEqual([], list((self.root / "control/historial").rglob("*.md")))
        self.assertEqual(2, len(list((self.root / "control/ejecuciones").glob("*.json"))))
        self.assertTrue(first.report_path.exists())

    def test_change_archives_previous_version(self):
        self.run_archive()
        before, first = self.snapshot()[0], self.row()
        _, report, _ = self.run_archive([post(body_html="<p>Nuevo</p>")])
        saved = list((self.root / "control/historial/1").glob("*.md"))
        self.assertEqual(1, len(saved))
        self.assertEqual(before, saved[0].read_bytes())
        self.assertEqual(1, report["contadores"]["actualizados"])
        self.assertNotEqual(first["huella"], self.row()["huella"])
        self.assertEqual(first["primera_descarga"], self.row()["primera_descarga"])

    def test_preview_error_and_wrong_id_preserve_complete(self):
        self.run_archive()
        before, old = self.snapshot(), self.row()
        for variant in (post(audience="only_paid", body_html="<p>Extracto</p>"),
                        post(is_truncated=True), post(body_html=None, description="Extracto"),
                        post(body_html=""), post(id=999), URLError("sin red")):
            with self.subTest(variant=str(variant)):
                _, report, _ = self.run_archive(details={"articulo-1": variant})
                self.assertEqual(1, report["codigo_salida"])
                self.assertEqual(before, self.snapshot())
                for field in ("estado", "huella", "archivo", "ultima_modificacion"):
                    self.assertEqual(old[field], self.row()[field])
                self.assertIn(self.row()["ultimo_intento"]["estado"], ("extracto", "error"))

    def test_short_pages_until_empty(self):
        items = [post(1), post(2), post(3)]
        _, report, calls = self.run_archive(items, pages={0: items[:1], 1: items[1:], 3: []})
        self.assertTrue(report["paginacion_completa"])
        self.assertEqual([1, 2, 0], [p["cantidad"] for p in report["paginas"]])
        self.assertEqual(3, report["paginas_leidas"])
        self.assertEqual(6, len(calls))

    def test_later_page_failure_partial_exit_one(self):
        _, report, calls = self.run_archive(pages={0: [post()], 1: URLError("fallo página")})
        self.assertFalse(report["paginacion_completa"])
        self.assertEqual(1, report["codigo_salida"])
        self.assertEqual(1, report["contadores"]["nuevos"])
        self.assertIn("fallo", report["motivo_paginacion"])
        self.assertEqual(3, sum("offset=1&" in url for url, _ in calls))

    def test_first_page_failure_or_invalid_response_exit_two(self):
        for value in (URLError("inaccesible"), {"error": "blocked"}, b"<html>no JSON</html>"):
            _, report, _ = self.run_archive(pages={0: value})
            self.assertEqual(2, report["codigo_salida"])
            self.assertTrue(report["fatal"])
            self.assertFalse(report["paginacion_completa"])
        self.assertFalse((self.root / "control/inventario.json").exists())

    def test_slug_and_title_change_no_duplicate_no_rewrite(self):
        self.run_archive()
        before, relative = self.snapshot(), self.row()["archivo"]
        _, report, _ = self.run_archive([post(slug="nuevo-slug", title="Título nuevo")])
        self.assertEqual(before, self.snapshot())
        self.assertEqual(relative, self.row()["archivo"])
        self.assertEqual("nuevo-slug", self.row()["slug"])
        self.assertEqual(1, report["contadores"]["sin_cambios"])
        self.assertEqual(1, len(list((self.root / "articulos").glob("*.md"))))

    def test_metrics_without_content_change(self):
        self.run_archive()
        before, first = self.snapshot(), self.row()
        _, report, _ = self.run_archive([post(reaction_count=80, comment_count=90, restack_count=100)])
        self.assertEqual(before, self.snapshot())
        self.assertEqual(1, report["contadores"]["sin_cambios"])
        metrics = self.row()["metricas_publicas"]
        self.assertEqual((80, 90, 100), (metrics["reacciones"], metrics["comentarios"], metrics["restacks"]))
        self.assertGreaterEqual(metrics["fecha_captura"], first["metricas_publicas"]["fecha_captura"])
        self.assertEqual(first["ultima_modificacion"], self.row()["ultima_modificacion"])
        self.assertEqual(80, json.loads((self.root / "control/originales/1.json").read_text(encoding="utf-8"))["reaction_count"])

    def test_limit_only_recent_posts(self):
        items = [post(i) for i in range(12, 0, -1)]
        _, report, calls = self.run_archive(items, pages={0: items}, limite=5)
        self.assertEqual(5, report["contadores"]["nuevos"])
        self.assertEqual(6, len(calls))
        self.assertEqual(1, report["codigo_salida"])
        self.assertIn("Límite solicitado", report["motivo_paginacion"])
        self.assertTrue((self.root / "articulos/2026-01-01-articulo-12.md").exists())
        self.assertFalse((self.root / "articulos/2026-01-01-articulo-7.md").exists())

    def test_safety_limit_repetition_and_overlap(self):
        for options, pages in (({"max_pages": 1}, {0: [post()]}),
                               ({}, {0: [post()], 1: [post()]}),
                               ({}, {0: [post(), post(2)], 2: [post(2), post(3)], 4: []})):
            _, report, _ = self.run_archive([post(), post(2), post(3)], pages=pages, **options)
            self.assertFalse(report["paginacion_completa"])
            self.assertEqual(1, report["codigo_salida"])
            self.assertTrue(report["motivo_paginacion"])

    def test_new_error_then_recovery(self):
        _, report, _ = self.run_archive(details={"articulo-1": URLError("fallo")})
        self.assertEqual(1, report["contadores"]["errores"])
        self.assertEqual("error", self.row()["estado"])
        self.assertIsNone(self.row()["archivo"])
        _, report, _ = self.run_archive()
        self.assertEqual(1, report["contadores"]["nuevos"])
        self.assertEqual("completo", self.row()["estado"])

    def test_preview_then_upgrade_same_body(self):
        _, report, _ = self.run_archive([post(audience="only_paid")])
        self.assertEqual("extracto", self.row()["estado"])
        self.assertEqual(1, report["contadores"]["extractos"])
        before = self.snapshot()[0]
        self.run_archive()
        self.assertEqual("completo", self.row()["estado"])
        self.assertEqual(before, next((self.root / "control/historial/1").glob("*.md")).read_bytes())

    def test_empty_archive(self):
        _, report, _ = self.run_archive([], pages={0: []})
        self.assertEqual(0, report["codigo_salida"])
        self.assertTrue(report["paginacion_completa"])

    def test_404_article_error_no_retry(self):
        error = HTTPError(BASE, 404, "Not found", {}, None)
        _, report, calls = self.run_archive(details={"articulo-1": error})
        self.assertEqual(1, report["codigo_salida"])
        self.assertEqual(1, report["contadores"]["errores"])
        self.assertEqual(1, sum("/posts/" in url for url, _ in calls))

    def test_corrupt_or_missing_inventory_preserves_articles(self):
        self.run_archive()
        inventory, article = self.root / "control/inventario.json", self.article()
        before = article.read_bytes()
        for action in ("corrupt", "missing"):
            if action == "corrupt":
                inventory.write_text("{malformado", encoding="utf-8")
            else:
                inventory.unlink()
            _, report, calls = self.run_archive(pages={})
            self.assertEqual(2, report["codigo_salida"])
            self.assertEqual([], calls)
            self.assertEqual(before, article.read_bytes())

    def test_other_publication_and_local_edits_preserved(self):
        self.run_archive()
        article = self.article()
        before = article.read_bytes()
        self.config["publicacion"]["substack"] = "https://otra.substack.com"
        _, report, calls = self.run_archive(pages={})
        self.assertEqual(2, report["codigo_salida"])
        self.assertEqual([], calls)
        self.assertEqual(before, article.read_bytes())
        self.config = copy.deepcopy(CONFIG)
        article.write_text("Edición manual", encoding="utf-8")
        _, report, calls = self.run_archive(pages={})
        self.assertEqual(2, report["codigo_salida"])
        self.assertEqual([], calls)
        self.assertEqual("Edición manual", article.read_text(encoding="utf-8"))


class UtilityTests(unittest.TestCase):
    def test_markdown_structure(self):
        html = ('<h2>Título</h2><p>A &amp; B <a href="/p/otro">enlace</a></p>'
                '<ul><li>Uno</li><li>Dos</li></ul><ol><li>Primero</li></ol>'
                '<blockquote><p>Cita</p><p>Otra línea</p></blockquote>'
                '<p>Usa <code>print()</code></p><pre><code>  a\n  b</code></pre>'
                '<img src="/foto.jpg" alt="Foto"><script>oculto()</script>')
        text = app.readable(html, BASE)
        for expected in ("## Título", "A & B", f"[enlace](<{BASE}/p/otro>)",
                         "- Uno", "- Dos", "1. Primero", "> Cita", "> Otra línea",
                         "  a\n  b", f"[Foto](<{BASE}/foto.jpg>)"):
            self.assertIn(expected, text)
        self.assertNotIn("oculto", text)
        self.assertIn(chr(96) + "print()" + chr(96), text)

    def test_conservative_classification(self):
        for changes in ({"audience": None}, {"audience": "only_paid"}, {"is_preview": True},
                        {"is_truncated": True}, {"free_unlock_required": True},
                        {"body_html": '<div class="paywall">Texto</div>'}):
            self.assertEqual("extracto", app.classify(post(**changes), BASE)[0])
        self.assertEqual("completo", app.classify(post(), BASE)[0])
        self.assertEqual("error", app.classify(post(body_html=""), BASE)[0])

    def test_retry_backoff_timeout_and_pause(self):
        for status in (429, 503):
            calls, sleeps, records = [], [], []
            def opener(request, timeout):
                calls.append(timeout)
                if len(calls) < 3:
                    raise HTTPError(request.full_url, status, "retry", {}, None)
                return Response([], request.full_url)
            client = app.Client({"timeout_segundos": 7, "intentos": 3, "pausa_segundos": 0.25},
                                lambda *args: records.append(args), opener, sleeps.append)
            value, _ = client(BASE)
            self.assertEqual([], value)
            self.assertEqual([7, 7, 7], calls)
            self.assertEqual([0.25, 1, 0.25, 2, 0.25], sleeps)
            self.assertEqual(3, len(records))

    def test_atomic_failure_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "articulo.md"
            target.write_bytes(b"anterior")
            with patch.object(app.os, "replace", side_effect=OSError("interrupción")):
                with self.assertRaises(OSError):
                    app.atomic_write(target, b"nuevo")
            self.assertEqual(b"anterior", target.read_bytes())
            self.assertEqual([target], list(Path(directory).iterdir()))

    def test_missing_metrics_unknown(self):
        self.assertIsNone(app.Archive.metrics({})["reacciones"])
        self.assertEqual(5, app.Archive.metrics({"reactions": {"heart": 3, "like": 2}})["reacciones"])

    def test_config_validation_and_custom_path_without_network(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "alternativa.json").write_bytes(app.encoded(CONFIG))
            with patch("socket.socket.connect", side_effect=AssertionError("No usar red")):
                self.assertEqual(0, app.main(["--project-root", str(project), "--config",
                                             "alternativa.json", "--validar-config"]))
                config = copy.deepcopy(CONFIG)
                config["red"]["intentos"] = 0
                (project / "proyecto.config.json").write_bytes(app.encoded(config))
                self.assertEqual(2, app.main(["--project-root", str(project), "--validar-config"]))
            self.assertFalse((project / "biblioteca").exists())

    def test_paths_cannot_escape_project(self):
        root = Path(tempfile.gettempdir()).resolve() / "proyecto"
        for relative in ("../fuera", str(root.parent), "."):
            with self.assertRaises(ValueError):
                app.inside(root, relative)


if __name__ == "__main__":
    unittest.main()
