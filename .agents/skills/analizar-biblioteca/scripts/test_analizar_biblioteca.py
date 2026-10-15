"""Pruebas de analizar_biblioteca.py sobre una biblioteca ficticia.

Se ejecutan con:
    python -m unittest discover .agents/skills/analizar-biblioteca/scripts -v

Nunca tocan biblioteca/ ni la red: todo ocurre en una carpeta temporal.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from analizar_biblioteca import Analizador, validar_contra_esquema

CUERPO_COMPLETO = """## Lo que probé

Monté el flujo entero con Claude Code. Tardé dos tardes. El resultado funciona.

- Primer paso: definir el objetivo.
- Segundo paso: limitar las herramientas.
- Tercer paso: medir el resultado.

> La automatización sin criterio solo acelera los errores.

![diagrama del flujo](https://example.com/diagrama.png)

## Lo que aprendí

Un agente mal acotado produce más trabajo del que ahorra. Lo comprobé con tres casos reales. Ninguno sobrevivió sin supervisión.
"""

CUERPO_EXTRACTO = "Este artículo es solo para suscriptores. Aquí va el primer párrafo de cortesía."


def crear_biblioteca_ficticia(raiz: Path) -> dict:
    """Crea inventario + 4 artículos: uno sin ficha, uno con ficha al día,
    uno con huella cambiada y uno que es un extracto (con ficha al día).
    Devuelve el inventario."""
    dir_articulos = raiz / "biblioteca" / "substack" / "articulos"
    dir_fichas = raiz / "biblioteca" / "substack" / "fichas"
    dir_control = raiz / "biblioteca" / "substack" / "control"
    for d in (dir_articulos, dir_fichas, dir_control):
        d.mkdir(parents=True, exist_ok=True)

    def registro(id_, fecha, titulo, slug, estado, huella):
        nombre = f"{fecha}-{slug}.md"
        return {
            "id": id_,
            "slug": slug,
            "titulo": titulo,
            "subtitulo": "",
            "fecha": fecha,
            "url": f"https://ejemplo.substack.com/p/{slug}",
            "tipo": "newsletter",
            "audiencia": "everyone",
            "estado": estado,
            "huella": huella,
            "archivo": f"biblioteca/substack/articulos/{nombre}",
            "metricas": {"reacciones": 12, "comentarios": 3, "restacks": 1,
                         "fecha_captura": "2026-10-01T00:00:00Z"},
        }

    inventario = {
        "101": registro("101", "2026-09-20", "Agentes que investigan solos", "agentes-investigan", "completo", "h101"),
        "102": registro("102", "2026-07-01", "Mi flujo real con n8n", "flujo-n8n", "completo", "h102"),
        "103": registro("103", "2025-12-10", "Prompts que no envejecen", "prompts-no-envejecen", "completo", "h103-nueva"),
        "104": registro("104", "2026-08-15", "Especial de pago", "especial-pago", "extracto", "h104"),
    }

    for reg in inventario.values():
        cuerpo = CUERPO_EXTRACTO if reg["estado"] == "extracto" else CUERPO_COMPLETO
        texto = f"---\nid: {reg['id']}\ntitulo: \"{reg['titulo']}\"\n---\n\n{cuerpo}\n"
        (raiz / reg["archivo"]).write_text(texto, encoding="utf-8")

    (dir_control / "inventario.json").write_text(
        json.dumps(inventario, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    def ficha(reg, tema, basada_en, huella=None):
        return {
            "id": reg["id"], "url": reg["url"], "fecha": reg["fecha"],
            "titulo": reg["titulo"], "huella": huella or reg["huella"],
            "basada_en": basada_en,
            "tema": tema,
            "subtemas": ["flujos de trabajo"],
            "enfoque": "caso",
            "tesis": "Automatizar sin criterio acelera los errores.",
            "entidades": ["n8n", "Claude Code"],
            "nivel": "intermedio",
            "metricas_publicas": {"reacciones": 12, "comentarios": 3, "restacks": 1},
        }

    # 102: ficha al día. 103: ficha con huella vieja. 104 (extracto): ficha al día.
    for reg, tema, huella in (
        (inventario["102"], "Automatización con n8n", None),
        (inventario["103"], "Prompts", "h103-vieja"),
        (inventario["104"], "Automatización con n8n", None),
    ):
        f = ficha(reg, tema, "extracto" if reg["estado"] == "extracto" else "completo", huella)
        (dir_fichas / f"{reg['id']}.json").write_text(
            json.dumps(f, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    return inventario


JUICIO_VALIDO = {
    "tema": "Agentes de IA",
    "subtemas": ["investigación automatizada", "límites de los agentes"],
    "enfoque": "tutorial con prueba propia",
    "tesis": "Un agente mal acotado produce más trabajo del que ahorra.",
    "entidades": ["Claude Code"],
    "nivel": "intermedio",
}


class BaseBiblioteca(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.inventario = crear_biblioteca_ficticia(self.raiz)
        self.analizador = Analizador(self.raiz, hoy=date(2026, 10, 14))
        self.dir_fichas = self.raiz / "biblioteca" / "substack" / "fichas"

    def escribir_juicio(self, datos) -> Path:
        ruta = self.raiz / "juicio.json"
        ruta.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
        return ruta


class TestPendientes(BaseBiblioteca):
    def test_detecta_sin_ficha_y_huella_cambiada_con_motivo(self):
        resultado = self.analizador.pendientes()
        por_id = {p["id"]: p for p in resultado["pendientes"]}
        self.assertEqual(set(por_id), {"101", "103"})
        self.assertEqual(por_id["101"]["motivo"], "sin ficha")
        self.assertIn("huella cambiada", por_id["103"]["motivo"])
        self.assertTrue(por_id["101"]["archivo"].endswith("2026-09-20-agentes-investigan.md"))

    def test_devuelve_temas_existentes_con_numero_de_articulos(self):
        resultado = self.analizador.pendientes()
        temas = {t["tema"]: t["articulos"] for t in resultado["temas_existentes"]}
        self.assertEqual(temas, {"Automatización con n8n": 2, "Prompts": 1})

    def test_sin_pendientes_lo_dice_expresamente(self):
        for id_ in ("101", "103"):
            exito, _ = self.analizador.guardar(id_, self.escribir_juicio(JUICIO_VALIDO))
            self.assertTrue(exito)
        resultado = self.analizador.pendientes()
        self.assertEqual(resultado["pendientes"], [])
        self.assertIn("mensaje", resultado)


class TestGuardar(BaseBiblioteca):
    def test_rechaza_campo_obligatorio_ausente_y_no_escribe(self):
        juicio = {k: v for k, v in JUICIO_VALIDO.items() if k != "tesis"}
        exito, mensaje = self.analizador.guardar("101", self.escribir_juicio(juicio))
        self.assertFalse(exito)
        self.assertIn("tesis", mensaje)
        self.assertFalse((self.dir_fichas / "101.json").exists())

    def test_rechaza_tipo_incorrecto_y_no_escribe(self):
        juicio = dict(JUICIO_VALIDO, subtemas="no es una lista")
        exito, mensaje = self.analizador.guardar("101", self.escribir_juicio(juicio))
        self.assertFalse(exito)
        self.assertIn("subtemas", mensaje)
        self.assertFalse((self.dir_fichas / "101.json").exists())

    def test_rechaza_enfoque_no_permitido_y_no_escribe(self):
        juicio = dict(JUICIO_VALIDO, enfoque="resumen")
        exito, mensaje = self.analizador.guardar("101", self.escribir_juicio(juicio))
        self.assertFalse(exito)
        self.assertIn("enfoque", mensaje)
        self.assertFalse((self.dir_fichas / "101.json").exists())

    def test_impone_los_datos_objetivos_del_inventario(self):
        juicio = dict(
            JUICIO_VALIDO,
            id="999", url="https://falso.example", huella="falsa",
            basada_en="extracto",
            metricas_publicas={"reacciones": 9999, "comentarios": 9999, "restacks": 9999},
        )
        exito, mensaje = self.analizador.guardar("101", self.escribir_juicio(juicio))
        self.assertTrue(exito, mensaje)
        ficha = json.loads((self.dir_fichas / "101.json").read_text(encoding="utf-8"))
        reg = self.inventario["101"]
        self.assertEqual(ficha["id"], "101")
        self.assertEqual(ficha["url"], reg["url"])
        self.assertEqual(ficha["huella"], "h101")
        self.assertEqual(ficha["basada_en"], "completo")
        self.assertEqual(ficha["metricas_publicas"],
                         {"reacciones": 12, "comentarios": 3, "restacks": 1})
        self.assertIn("ignorados", mensaje)

    def test_basada_en_refleja_si_el_articulo_es_un_extracto(self):
        exito, _ = self.analizador.guardar("104", self.escribir_juicio(JUICIO_VALIDO))
        self.assertTrue(exito)
        ficha = json.loads((self.dir_fichas / "104.json").read_text(encoding="utf-8"))
        self.assertEqual(ficha["basada_en"], "extracto")

        exito, _ = self.analizador.guardar("101", self.escribir_juicio(JUICIO_VALIDO))
        self.assertTrue(exito)
        ficha = json.loads((self.dir_fichas / "101.json").read_text(encoding="utf-8"))
        self.assertEqual(ficha["basada_en"], "completo")

    def test_id_inexistente_no_escribe(self):
        exito, mensaje = self.analizador.guardar("999", self.escribir_juicio(JUICIO_VALIDO))
        self.assertFalse(exito)
        self.assertIn("999", mensaje)
        self.assertFalse((self.dir_fichas / "999.json").exists())


class TestMapa(BaseBiblioteca):
    def test_agrupa_por_tema_con_fechas_y_frecuencias(self):
        contenido = self.analizador.mapa()
        self.assertIn("### Automatización con n8n", contenido)
        self.assertIn("- Articulos: 2", contenido)
        self.assertIn("Primera fecha: 2026-07-01 · Ultima fecha: 2026-08-15", contenido)
        self.assertIn("n8n (2)", contenido)
        self.assertIn("- n8n: 2 articulo(s)", contenido)  # entidades globales

    def test_senala_articulos_sin_ficha_al_dia(self):
        contenido = self.analizador.mapa()
        self.assertIn("## Articulos sin ficha", contenido)
        self.assertIn("Agentes que investigan solos", contenido)        # 101: sin ficha
        self.assertIn("Prompts que no envejecen", contenido)           # 103: ficha caducada
        # La ficha con huella vieja no cuenta como tema vigente
        self.assertNotIn("### Prompts\n", contenido)

    def test_salida_determinista(self):
        primera = self.analizador.mapa()
        segunda = self.analizador.mapa()
        self.assertEqual(primera, segunda)
        self.assertEqual(
            primera,
            (self.raiz / "biblioteca" / "mapa-temas.md").read_text(encoding="utf-8"),
        )

    def test_temas_sin_tocar_en_6_meses(self):
        # Ficha al día para 103 (fecha 2025-12-10, hace >6 meses) con tema propio
        juicio = dict(JUICIO_VALIDO, tema="Prompts")
        exito, _ = self.analizador.guardar("103", self.escribir_juicio(juicio))
        self.assertTrue(exito)
        contenido = self.analizador.mapa()
        seccion = contenido.split("## Temas sin tocar")[1].split("##")[0]
        self.assertIn("Prompts (ultimo articulo: 2025-12-10)", seccion)
        self.assertNotIn("Automatización con n8n", seccion)


class TestMetricasEstilo(BaseBiblioteca):
    def test_ignora_los_extractos(self):
        metricas = self.analizador.metricas_estilo()
        self.assertEqual(metricas["articulos_completos_analizados"], 3)
        self.assertEqual(metricas["extractos_ignorados"], 1)
        self.assertGreater(metricas["palabras"]["media"], 0)
        self.assertEqual(metricas["secciones"]["media"], 2.0)
        self.assertEqual(metricas["uso"]["articulos_con_listas"], 3)
        self.assertEqual(metricas["uso"]["articulos_con_citas"], 3)
        self.assertEqual(metricas["uso"]["articulos_con_imagenes"], 3)
        self.assertGreater(metricas["frases"]["longitud_media_palabras"], 0)


class TestGuardarEstilo(BaseBiblioteca):
    def test_conserva_la_seccion_reglas_aprendidas(self):
        estilo = self.raiz / "biblioteca" / "estilo.md"
        estilo.write_text(
            "# Estilo\n\n## Tono y voz\n\nVieja descripcion.\n\n"
            "## Reglas aprendidas\n\n- No abrir con una pregunta retorica.\n",
            encoding="utf-8",
        )
        nuevo = self.raiz / "nuevo-estilo.md"
        nuevo.write_text(
            "# Estilo\n\n## Tono y voz\n\nNueva descripcion.\n\n"
            "## Reglas aprendidas\n\n(pendiente)\n",
            encoding="utf-8",
        )
        exito, _ = self.analizador.guardar_estilo(nuevo)
        self.assertTrue(exito)
        resultado = estilo.read_text(encoding="utf-8")
        self.assertIn("Nueva descripcion.", resultado)
        self.assertIn("- No abrir con una pregunta retorica.", resultado)
        self.assertNotIn("(pendiente)", resultado)
        self.assertNotIn("Vieja descripcion.", resultado)

    def test_anade_las_reglas_si_el_nuevo_no_trae_la_seccion(self):
        estilo = self.raiz / "biblioteca" / "estilo.md"
        estilo.write_text(
            "# Estilo\n\n## Reglas aprendidas\n\n- Regla previa.\n", encoding="utf-8"
        )
        nuevo = self.raiz / "nuevo-estilo.md"
        nuevo.write_text("# Estilo\n\n## Tono y voz\n\nTexto.\n", encoding="utf-8")
        exito, _ = self.analizador.guardar_estilo(nuevo)
        self.assertTrue(exito)
        resultado = estilo.read_text(encoding="utf-8")
        self.assertIn("## Reglas aprendidas", resultado)
        self.assertIn("- Regla previa.", resultado)

    def test_sin_estilo_previo_escribe_el_nuevo_tal_cual(self):
        nuevo = self.raiz / "nuevo-estilo.md"
        nuevo.write_text("# Estilo\n\n## Reglas aprendidas\n", encoding="utf-8")
        exito, _ = self.analizador.guardar_estilo(nuevo)
        self.assertTrue(exito)
        self.assertEqual(
            (self.raiz / "biblioteca" / "estilo.md").read_text(encoding="utf-8"),
            "# Estilo\n\n## Reglas aprendidas\n",
        )


class TestControlVocabulario(BaseBiblioteca):
    """Control de vocabulario: fichas existentes (102, 103, 104) usan el
    subtema 'flujos de trabajo' y las entidades 'n8n' y 'Claude Code'."""

    def test_guardar_avisa_ante_subtema_casi_duplicado(self):
        juicio = dict(JUICIO_VALIDO, subtemas=["flujos de trabajos"])
        exito, mensaje = self.analizador.guardar("101", self.escribir_juicio(juicio))
        self.assertTrue(exito)  # avisa pero guarda igualmente
        self.assertIn("se parece a", mensaje)
        self.assertIn("'flujos de trabajos'", mensaje)
        self.assertIn("'flujos de trabajo'", mensaje)
        self.assertTrue((self.dir_fichas / "101.json").exists())

    def test_guardar_avisa_ante_entidad_casi_duplicada(self):
        juicio = dict(JUICIO_VALIDO, entidades=["Claude Codes"])
        exito, mensaje = self.analizador.guardar("101", self.escribir_juicio(juicio))
        self.assertTrue(exito)
        self.assertIn("entidad 'Claude Codes' se parece a 'Claude Code'", mensaje)

    def test_guardar_no_avisa_con_coincidencia_exacta_normalizada(self):
        # Mayusculas y tildes distintas, pero el mismo termino: reutilizacion.
        juicio = dict(JUICIO_VALIDO, subtemas=["Flujos de Trabajo"], entidades=["claude code"])
        exito, mensaje = self.analizador.guardar("101", self.escribir_juicio(juicio))
        self.assertTrue(exito)
        self.assertNotIn("se parece a", mensaje)

    def test_guardar_no_avisa_con_termino_distinto(self):
        juicio = dict(JUICIO_VALIDO, subtemas=["evaluación de modelos"], entidades=["OpenAI"])
        exito, mensaje = self.analizador.guardar("101", self.escribir_juicio(juicio))
        self.assertTrue(exito)
        self.assertNotIn("se parece a", mensaje)

    def test_reguardar_no_compara_contra_la_version_anterior_de_si_misma(self):
        juicio = dict(JUICIO_VALIDO, subtemas=["agentes con memoria"], entidades=["LangChain"])
        exito, _ = self.analizador.guardar("101", self.escribir_juicio(juicio))
        self.assertTrue(exito)
        exito, mensaje = self.analizador.guardar("101", self.escribir_juicio(juicio))
        self.assertTrue(exito)
        self.assertNotIn("se parece a", mensaje)

    def test_pendientes_devuelve_subtemas_y_entidades_con_frecuencias(self):
        resultado = self.analizador.pendientes()
        self.assertEqual(
            resultado["subtemas_existentes"],
            [{"subtema": "flujos de trabajo", "articulos": 3}],
        )
        entidades = {e["entidad"]: e["articulos"] for e in resultado["entidades_existentes"]}
        self.assertEqual(entidades, {"n8n": 3, "Claude Code": 3})

    def test_vocabulario_detecta_un_par_sembrado(self):
        juicio = dict(JUICIO_VALIDO, subtemas=["flujos de trabajos"])
        exito, _ = self.analizador.guardar("101", self.escribir_juicio(juicio))
        self.assertTrue(exito)
        resultado = self.analizador.vocabulario()
        pares = {
            (p["tipo"], p["termino_a"], p["termino_b"]) for p in resultado["sospechosos"]
        }
        self.assertIn(("subtema", "flujos de trabajo", "flujos de trabajos"), pares)
        subtemas = {s["termino"]: s["frecuencia"] for s in resultado["subtemas"]}
        self.assertEqual(subtemas["flujos de trabajo"], 3)
        self.assertEqual(subtemas["flujos de trabajos"], 1)

    def test_vocabulario_sin_casi_duplicados_devuelve_sospechosos_vacio(self):
        resultado = self.analizador.vocabulario()
        self.assertEqual(resultado["sospechosos"], [])
        self.assertEqual([t["termino"] for t in resultado["temas"]],
                         ["Automatización con n8n", "Prompts"])


class TestValidador(unittest.TestCase):
    def test_booleano_no_pasa_por_entero(self):
        errores = validar_contra_esquema(True, {"type": "integer"}, "campo")
        self.assertTrue(errores)


if __name__ == "__main__":
    unittest.main()
