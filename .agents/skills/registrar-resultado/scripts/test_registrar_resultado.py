"""Pruebas de registrar_resultado.py con una biblioteca ficticia en una
carpeta temporal. Nunca tocan biblioteca/ ni la red."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from registrar_resultado import Registrador, parsear_frontmatter

HOY = "2026-10-14"


def escribir(ruta: Path, contenido: str):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(contenido, encoding="utf-8")


BORRADOR = """---
oportunidad: 2026-09-01-agentes-investigacion
estado: borrador
fecha: 2026-09-20
titulos_alternativos: [Agentes que investigan por ti, Investigar con agentes]
---
# Agentes que investigan por ti

¿Te imaginas no volver a buscar fuentes a mano?

Los agentes pueden encargarse de la investigacion previa.

Este parrafo sobrevive sin cambios en la version publicada.

Parrafo que la persona elimino al editar.
"""

PUBLICADO = """---
id: p1
titulo: "Agentes que investigan solos"
fecha: 2026-10-05
url: https://ejemplo.substack.com/p/agentes-que-investigan-solos
---
Los agentes pueden encargarse de la investigacion previa, y te explico como lo probe.

Este parrafo sobrevive sin cambios en la version publicada.

Parrafo nuevo que la persona anadio con un ejemplo real.
"""

ESTILO = """# Estilo de la publicacion

## Tono y voz

Cercano y directo, en segunda persona.

## Reglas aprendidas

- Regla previa de ejemplo. (2026-08-01, origen: 2026-07-01-tema)
  - Antes: «antes»
  - Después: «despues»
"""


def oportunidad_md(oid: str, estado: str, motivo: str = "", extra: str = "") -> str:
    return (
        "---\n"
        f"id: {oid}\n"
        f"estado: {estado}\n"
        f'motivo_estado: "{motivo}"\n'
        "interes: alto\n"
        "canales: 2\n"
        "cobertura: nuevo\n"
        f"{extra}"
        "---\n"
        "## La oportunidad\n\nTexto.\n"
    )


class BaseRegistrador(unittest.TestCase):
    def setUp(self):
        self.raiz = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.raiz, ignore_errors=True)
        escribir(self.raiz / "proyecto.config.json", json.dumps({
            "publicacion": {"substack": "https://ejemplo.substack.com"},
        }))

        inventario = {
            "p1": {
                "id": "p1",
                "titulo": "Agentes que investigan solos",
                "fecha": "2026-10-05",
                "url": "https://ejemplo.substack.com/p/agentes-que-investigan-solos",
                "archivo": "biblioteca/substack/articulos/2026-10-05-agentes.md",
                "estado": "completo",
                "metricas": {"reacciones": 12, "comentarios": 3, "restacks": 1,
                             "fecha_captura": "2026-10-12T10:00:00Z"},
            },
            "p2": {
                "id": "p2",
                "titulo": "Automatiza tu newsletter con n8n",
                "fecha": "2026-10-10",
                "url": "https://ejemplo.substack.com/p/automatiza-n8n",
                "archivo": "biblioteca/substack/articulos/2026-10-10-n8n.md",
                "estado": "completo",
                "metricas": {"reacciones": 5, "comentarios": 0, "restacks": 0,
                             "fecha_captura": "2026-10-12T10:00:00Z"},
            },
            "p0": {
                "id": "p0",
                "titulo": "Agentes que investigan por ti (antiguo)",
                "fecha": "2026-01-15",
                "url": "https://ejemplo.substack.com/p/antiguo",
                "archivo": "biblioteca/substack/articulos/2026-01-15-antiguo.md",
                "estado": "completo",
                "metricas": {"reacciones": 40, "comentarios": 9, "restacks": 4,
                             "fecha_captura": "2026-10-12T10:00:00Z"},
            },
        }
        escribir(self.raiz / "biblioteca/substack/control/inventario.json",
                 json.dumps(inventario, ensure_ascii=False, indent=2))
        escribir(self.raiz / "biblioteca/substack/articulos/2026-10-05-agentes.md",
                 PUBLICADO)

        self.oid = "2026-09-01-agentes-investigacion"
        escribir(self.raiz / f"biblioteca/oportunidades/{self.oid}.md",
                 oportunidad_md(self.oid, "aceptada"))
        escribir(self.raiz / "biblioteca/oportunidades/2026-09-02-propuesta.md",
                 oportunidad_md("2026-09-02-propuesta", "propuesta"))
        escribir(self.raiz / "biblioteca/oportunidades/2026-09-03-descartada.md",
                 oportunidad_md("2026-09-03-descartada", "descartada",
                                motivo="ya cubierto por otro canal"))
        escribir(self.raiz / "biblioteca/oportunidades/2026-09-04-sin-motivo.md",
                 oportunidad_md("2026-09-04-sin-motivo", "descartada"))

        escribir(self.raiz / f"biblioteca/contenidos/{self.oid}/principal.md", BORRADOR)
        escribir(self.raiz / f"biblioteca/contenidos/{self.oid}/principal.borrador.md",
                 BORRADOR)
        escribir(self.raiz / "biblioteca/estilo.md", ESTILO)

    def registrador(self) -> Registrador:
        return Registrador(self.raiz / "proyecto.config.json", hoy=HOY)

    def enlazar(self):
        return self.registrador().cmd_enlazar(self.oid, "p1")

    def leer(self, relativa: str) -> str:
        return (self.raiz / relativa).read_text(encoding="utf-8")

    def resultado_json(self) -> dict:
        return json.loads(self.leer(f"biblioteca/contenidos/{self.oid}/resultado.json"))


class TestDecisiones(BaseRegistrador):
    def test_agrupa_por_estado_y_senala_descartes_sin_motivo(self):
        codigo = self.registrador().cmd_decisiones()
        self.assertEqual(codigo, 1)  # hay un descarte sin motivo: aviso
        texto = self.leer("biblioteca/decisiones.md")
        self.assertIn("## Propuestas", texto)
        self.assertIn("## Aceptadas", texto)
        self.assertIn("## Publicadas", texto)
        self.assertIn("## Descartadas", texto)
        self.assertIn("2026-09-02-propuesta", texto)
        self.assertIn(self.oid, texto)
        self.assertIn("motivo: ya cubierto por otro canal", texto)
        self.assertIn("2026-09-04-sin-motivo — SIN MOTIVO", texto)

    def test_es_determinista(self):
        self.registrador().cmd_decisiones()
        primera = self.leer("biblioteca/decisiones.md")
        self.registrador().cmd_decisiones()
        self.assertEqual(primera, self.leer("biblioteca/decisiones.md"))

    def test_publicada_enlaza_al_articulo(self):
        self.enlazar()
        codigo = self.registrador().cmd_decisiones()
        texto = self.leer("biblioteca/decisiones.md")
        self.assertIn(
            f"- {self.oid} — [Agentes que investigan solos]"
            "(https://ejemplo.substack.com/p/agentes-que-investigan-solos)",
            texto,
        )
        self.assertEqual(codigo, 1)  # sigue el descarte sin motivo


class TestBuscarPublicado(BaseRegistrador):
    def test_propone_primero_el_titulo_mas_parecido(self):
        import io
        from contextlib import redirect_stdout
        salida = io.StringIO()
        with redirect_stdout(salida):
            codigo = self.registrador().cmd_buscar_publicado(self.oid)
        self.assertEqual(codigo, 0)
        datos = json.loads(salida.getvalue())
        self.assertEqual(datos["candidatos"][0]["post_id"], "p1")
        self.assertGreater(datos["candidatos"][0]["puntuacion"],
                           datos["candidatos"][1]["puntuacion"])
        # p0 es muy parecido pero anterior a la fecha del borrador: fuera
        self.assertNotIn("p0", [c["post_id"] for c in datos["candidatos"]])

    def test_no_enlaza_nada(self):
        import io
        from contextlib import redirect_stdout
        with redirect_stdout(io.StringIO()):
            self.registrador().cmd_buscar_publicado(self.oid)
        self.assertFalse(
            (self.raiz / f"biblioteca/contenidos/{self.oid}/resultado.json").exists()
        )
        encabezado, _ = parsear_frontmatter(
            self.leer(f"biblioteca/oportunidades/{self.oid}.md")
        )
        self.assertEqual(encabezado["estado"], "aceptada")


class TestEnlazar(BaseRegistrador):
    def test_rechaza_post_id_inexistente(self):
        codigo = self.registrador().cmd_enlazar(self.oid, "no-existe")
        self.assertEqual(codigo, 2)
        self.assertFalse(
            (self.raiz / f"biblioteca/contenidos/{self.oid}/resultado.json").exists()
        )

    def test_escribe_resultado_y_cambia_el_estado(self):
        codigo = self.enlazar()
        self.assertEqual(codigo, 0)
        resultado = self.resultado_json()
        self.assertEqual(resultado["articulo"]["id"], "p1")
        self.assertEqual(resultado["articulo"]["fecha_publicacion"], "2026-10-05")
        self.assertTrue(resultado["articulo"]["url"].startswith("https://"))
        encabezado, cuerpo = parsear_frontmatter(
            self.leer(f"biblioteca/oportunidades/{self.oid}.md")
        )
        self.assertEqual(encabezado["estado"], "publicada")
        self.assertEqual(encabezado["articulo"], "p1")
        self.assertIn("## La oportunidad", cuerpo)  # el cuerpo no se toca

    def test_conserva_lo_previo_de_resultado_json(self):
        escribir(self.raiz / f"biblioteca/contenidos/{self.oid}/resultado.json",
                 json.dumps({"reglas": [{"regla": "previa", "fecha": "2026-01-01"}]}))
        self.enlazar()
        self.assertEqual(self.resultado_json()["reglas"][0]["regla"], "previa")


class TestMetricas(BaseRegistrador):
    def test_acumula_capturas_sin_sobrescribir(self):
        self.enlazar()
        self.registrador().cmd_metricas()
        resultado = self.resultado_json()
        self.assertEqual(len(resultado["metricas"]["capturas"]), 1)
        self.assertEqual(resultado["metricas"]["capturas"][0]["reacciones"], 12)
        self.assertEqual(resultado["metricas"]["capturas"][0]["dias"], 7)
        self.assertEqual(resultado["metricas"]["capturas"][0]["hito"], "7d")

        # segunda captura con otra fecha: se añade sin borrar la primera
        inventario = json.loads(self.leer("biblioteca/substack/control/inventario.json"))
        inventario["p1"]["metricas"] = {"reacciones": 30, "comentarios": 6,
                                        "restacks": 2,
                                        "fecha_captura": "2026-11-04T10:00:00Z"}
        escribir(self.raiz / "biblioteca/substack/control/inventario.json",
                 json.dumps(inventario))
        self.registrador().cmd_metricas()
        capturas = self.resultado_json()["metricas"]["capturas"]
        self.assertEqual(len(capturas), 2)
        self.assertEqual(capturas[0]["reacciones"], 12)
        self.assertEqual(capturas[1]["reacciones"], 30)
        self.assertEqual(capturas[1]["hito"], "30d")

        # repetir con la misma fecha no duplica
        self.registrador().cmd_metricas()
        self.assertEqual(len(self.resultado_json()["metricas"]["capturas"]), 2)

    def test_funciona_sin_csv_y_con_csv(self):
        self.enlazar()
        codigo = self.registrador().cmd_metricas()
        self.assertEqual(codigo, 0)
        self.assertNotIn("estadisticas", self.resultado_json()["metricas"])

        escribir(self.raiz / "biblioteca/substack/control/estadisticas/export.csv",
                 "post_id,title,opens,clicks\n"
                 "p1,Agentes que investigan solos,420,37\n"
                 "p2,Automatiza tu newsletter con n8n,100,5\n")
        codigo = self.registrador().cmd_metricas()
        self.assertEqual(codigo, 0)
        estadisticas = self.resultado_json()["metricas"]["estadisticas"]
        self.assertEqual(estadisticas["aperturas"], 420)
        self.assertEqual(estadisticas["clics"], 37)
        self.assertEqual(estadisticas["archivo"], "export.csv")


class TestDiferencias(BaseRegistrador):
    def obtener(self) -> dict:
        import io
        from contextlib import redirect_stdout
        salida = io.StringIO()
        with redirect_stdout(salida):
            codigo = self.registrador().cmd_diferencias(self.oid)
        self.assertEqual(codigo, 0)
        return json.loads(salida.getvalue())

    def test_detecta_cambios_de_parrafos_y_de_titulo(self):
        self.enlazar()
        datos = self.obtener()
        self.assertTrue(datos["titulo"]["cambiado"])
        self.assertEqual(datos["titulo"]["antes"], "Agentes que investigan por ti")
        self.assertEqual(datos["titulo"]["despues"], "Agentes que investigan solos")
        self.assertIn("Parrafo que la persona elimino al editar.", datos["eliminados"])
        self.assertIn("Parrafo nuevo que la persona anadio con un ejemplo real.",
                      datos["anadidos"])
        modificados_antes = [m["antes"] for m in datos["modificados"]]
        self.assertIn("Los agentes pueden encargarse de la investigacion previa.",
                      modificados_antes)
        # la pregunta retorica de apertura desaparecio
        todos_eliminados = datos["eliminados"] + modificados_antes
        self.assertTrue(any("Te imaginas" in p for p in todos_eliminados))
        self.assertNotEqual(datos["longitud"]["diferencia"], 0)

    def test_sin_enlace_falla_con_claridad(self):
        codigo = self.registrador().cmd_diferencias(self.oid)
        self.assertEqual(codigo, 2)


class TestGuardarReglas(BaseRegistrador):
    def guardar(self, reglas) -> int:
        archivo = self.raiz / "reglas.json"
        escribir(archivo, json.dumps(reglas, ensure_ascii=False))
        return self.registrador().cmd_guardar_reglas(archivo)

    def regla(self, texto="No abrir con una pregunta retorica."):
        return {"regla": texto,
                "ejemplo_antes": "¿Te imaginas no volver a buscar fuentes a mano?",
                "ejemplo_despues": "Los agentes pueden encargarse de la investigacion.",
                "origen": self.oid}

    def test_anade_la_regla_con_fecha_y_origen(self):
        codigo = self.guardar([self.regla()])
        self.assertEqual(codigo, 0)
        texto = self.leer("biblioteca/estilo.md")
        self.assertIn(
            f"- No abrir con una pregunta retorica. ({HOY}, origen: {self.oid})", texto
        )
        self.assertIn("Antes: «¿Te imaginas", texto)
        # y queda registrada en resultado.json del contenido
        self.assertEqual(self.resultado_json()["reglas"][0]["regla"],
                         "No abrir con una pregunta retorica.")

    def test_no_duplica_una_regla_repetida(self):
        self.guardar([self.regla()])
        codigo = self.guardar([self.regla("no abrir con una pregunta retórica")])
        self.assertEqual(codigo, 1)  # repetida: aviso
        texto = self.leer("biblioteca/estilo.md")
        self.assertEqual(texto.lower().count("no abrir con una pregunta ret"), 1)

    def test_no_toca_el_resto_de_estilo(self):
        antes = self.leer("biblioteca/estilo.md")
        seccion_tono = antes.split("## Reglas aprendidas")[0]
        self.guardar([self.regla()])
        despues = self.leer("biblioteca/estilo.md")
        self.assertTrue(despues.startswith(seccion_tono))
        self.assertIn("- Regla previa de ejemplo.", despues)

    def test_rechaza_una_regla_incompleta(self):
        codigo = self.guardar([{"regla": "sin ejemplos", "origen": self.oid}])
        self.assertEqual(codigo, 2)
        self.assertNotIn("sin ejemplos", self.leer("biblioteca/estilo.md"))


if __name__ == "__main__":
    unittest.main()
