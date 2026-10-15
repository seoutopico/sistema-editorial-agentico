"""Pruebas de detectar_oportunidades.py.

Trabajan sobre una biblioteca ficticia en una carpeta temporal, con fichas
externas de dos fuentes (`youtube` y una inventada, `blog`) para comprobar que
el script no depende de YouTube. Nunca tocan `biblioteca/` real ni la red.
"""

from __future__ import annotations

import contextlib
import io
import json
import unittest
import tempfile
from pathlib import Path

from detectar_oportunidades import (
    CODIGO_FATAL,
    CODIGO_OK,
    CODIGO_PARCIAL,
    Detector,
    lunes_siguiente,
    normalizar_tema,
    parsear_frontmatter,
    validar_cuerpo_oportunidad,
)

HOY = "2026-10-14"


# ---------------------------------------------------------------------------
# Constructores de la biblioteca ficticia
# ---------------------------------------------------------------------------

def ficha_externa(fuente, vid, tema, autor, multiplo, entidades, tesis="", marca="01:00",
                  fecha="2026-10-01", huella=None):
    return {
        "id": vid,
        "fuente": fuente,
        "url": f"https://ejemplo.test/{fuente}/{vid}",
        "autor": autor,
        "fecha": fecha,
        "huella": huella or f"huella-{fuente}-{vid}",
        "tema": tema,
        "tesis": tesis or f"Tesis sobre {tema}",
        "afirmaciones": [
            {"texto": f"Afirmación de {vid}", "marca": marca, "tipo": "demostración"},
        ],
        "entidades": entidades,
        "demuestra": "Algo funcionando",
        "promete_sin_demostrar": "",
        "preguntas_abiertas": [],
        "senales": {"multiplo_mediana": multiplo, "interaccion": None, "dias": 13},
    }


def ficha_propia(pid, tema, titulo, tesis, entidades, huella=None):
    return {
        "id": pid,
        "url": f"https://ejemplo.test/p/{pid}",
        "fecha": "2026-01-10",
        "titulo": titulo,
        "huella": huella or f"huella-{pid}",
        "basada_en": "completo",
        "tema": tema,
        "subtemas": [tema],
        "enfoque": "tutorial con prueba propia",
        "tesis": tesis,
        "entidades": entidades,
        "nivel": "intermedio",
        "metricas_publicas": {"reacciones": 3, "comentarios": 1, "restacks": 0},
    }


def oportunidad_md(oid, estado, tema, motivo="", evidencias=(), cuerpo=None):
    cuerpo = cuerpo or CUERPO_VALIDO
    lista = f"[{', '.join(evidencias)}]"
    return (
        "---\n"
        f"id: {oid}\n"
        f"estado: {estado}\n"
        f'motivo_estado: "{motivo}"\n'
        f"tema: {tema}\n"
        "interes: medio\n"
        "canales: 1\n"
        "cobertura: nuevo\n"
        f"evidencias: {lista}\n"
        "relacionados: []\n"
        "---\n"
        f"{cuerpo}\n"
    )


CUERPO_VALIDO = """## La oportunidad

Un tema con recorrido para nosotros.

## Por qué ahora (evidencias)

Varias señales recientes (youtube:v1@12:34).

## Qué hemos publicado y qué falta

Tratamos el tema en [el artículo](../substack/articulos/2026-01-10-agentes-investigacion.md), falta el caso práctico.

## Qué aportaríamos

Una prueba propia del flujo completo.

## Qué hay que investigar o probar

Verificar la afirmación youtube:v1@12:34 con una prueba.

## Riesgos

Tema posiblemente efímero.
"""


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.raiz = Path(self._tmp.name)
        self.config = self.raiz / "proyecto.config.json"
        self.config.write_text(json.dumps({
            "linea_editorial": {
                "nicho": "IA aplicada al trabajo",
                "audiencia": "Profesionales",
                "aportacion": "Probar las cosas y explicar el proceso real",
            }
        }, ensure_ascii=False), encoding="utf-8")
        self.biblioteca = self.raiz / "biblioteca"
        self.dir_oportunidades = self.biblioteca / "oportunidades"
        self.dir_oportunidades.mkdir(parents=True)
        self._montar_fixture()

    # -- fixture ------------------------------------------------------------

    def escribir_externa(self, ficha, subcarpeta="items"):
        carpeta = self.biblioteca / ficha["fuente"] / subcarpeta / ficha["id"]
        carpeta.mkdir(parents=True, exist_ok=True)
        (carpeta / "ficha.json").write_text(
            json.dumps(ficha, ensure_ascii=False, indent=2), encoding="utf-8")

    def escribir_propia(self, ficha):
        carpeta = self.biblioteca / "substack" / "fichas"
        carpeta.mkdir(parents=True, exist_ok=True)
        (carpeta / f"{ficha['id']}.json").write_text(
            json.dumps(ficha, ensure_ascii=False, indent=2), encoding="utf-8")

    def escribir_articulo(self, pid, nombre, texto):
        carpeta = self.biblioteca / "substack" / "articulos"
        carpeta.mkdir(parents=True, exist_ok=True)
        (carpeta / nombre).write_text(texto, encoding="utf-8")
        ruta_inv = self.biblioteca / "substack" / "control" / "inventario.json"
        ruta_inv.parent.mkdir(parents=True, exist_ok=True)
        inventario = json.loads(ruta_inv.read_text(encoding="utf-8")) if ruta_inv.is_file() else {}
        inventario[pid] = {"id": pid, "archivo": f"biblioteca/substack/articulos/{nombre}"}
        ruta_inv.write_text(json.dumps(inventario, ensure_ascii=False, indent=2), encoding="utf-8")

    def escribir_oportunidad(self, oid, estado, tema, motivo="", evidencias=(), cuerpo=None):
        (self.dir_oportunidades / f"{oid}.md").write_text(
            oportunidad_md(oid, estado, tema, motivo, evidencias, cuerpo), encoding="utf-8")

    def _montar_fixture(self):
        # Grupo "agentes": entidades muy coincidentes entre v1, v2 y b1 (fuente
        # blog). Compartir tema ya no basta: v2 comparte entidades con v1
        # (Jaccard 2/3) además del tema.
        self.escribir_externa(ficha_externa(
            "youtube", "v1", "Agentes que investigan solos", "Canal A", 2.5,
            ["Claude Code", "agentes"], tesis="Los agentes pueden investigar sin supervisión",
            marca="12:34"))
        self.escribir_externa(ficha_externa(
            "youtube", "v2", "agentes  que investigan SOLOS", "Canal B", 0.8,
            ["Claude Code", "agentes", "subagentes"], marca="03:10"))
        self.escribir_externa(ficha_externa(
            "blog", "b1", "Automatizar la investigación con agentes", "Blog X", None,
            ["Claude Code", "agentes"], tesis="Automatizar la investigación con agentes funciona",
            marca="parrafo-4"))
        # Grupo "edición de vídeo": interés bajo y un solo canal (sin interés real).
        self.escribir_externa(ficha_externa(
            "youtube", "v3", "Edición de vídeo con IA", "Canal A", 0.5,
            ["CapCut"], tesis="Editar vídeo con IA ahorra tiempo"))
        # Grupo "modelo nuevo": interés bajo pero 2 canales (interés real por canales).
        self.escribir_externa(ficha_externa(
            "youtube", "v4", "Nuevo modelo de OpenAI", "Canal A", 0.5, ["OpenAI", "GPT"]))
        self.escribir_externa(ficha_externa(
            "youtube", "v5", "Nuevo modelo de OpenAI", "Canal B", 0.4, ["OpenAI"]))
        # Fichas propias y artículos.
        self.escribir_propia(ficha_propia(
            "p1", "Agentes para automatizar la investigación",
            "Probé agentes que investigan por mí",
            "Los agentes de investigación funcionan con supervisión",
            ["Claude Code", "agentes"]))
        self.escribir_propia(ficha_propia(
            "p2", "Prompts para escribir mejor", "Prompts que uso cada semana",
            "Un buen prompt ahorra revisiones", ["ChatGPT"]))
        self.escribir_articulo("p1", "2026-01-10-agentes-investigacion.md",
                               "Texto completo del artículo sobre agentes de investigación.")
        self.escribir_articulo("p2", "2026-02-01-prompts.md",
                               "Texto completo del artículo sobre prompts.")
        # Decisiones anteriores.
        self.escribir_oportunidad(
            "2026-09-01-edicion-de-video-con-ia", "descartada", "edición de vídeo con IA",
            motivo="tema efímero y fuera de nicho")
        self.escribir_oportunidad(
            "2026-09-05-agentes-de-investigacion", "propuesta", "agentes de investigación",
            evidencias=["youtube:zz9@00:10"])
        self.escribir_oportunidad(
            "2026-09-10-flujos-con-n8n", "aceptada", "flujos con n8n", motivo="la probamos")

    # -- utilidades ----------------------------------------------------------

    def detector(self):
        return Detector(self.config, hoy=HOY)

    def ejecutar(self, metodo, *args):
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            codigo = metodo(*args)
        return codigo, salida.getvalue()

    def grupos(self):
        codigo, _ = self.ejecutar(self.detector().cmd_agrupar)
        datos = json.loads((self.dir_oportunidades / "control" / "grupos.json").read_text(encoding="utf-8"))
        return codigo, {g["grupo_id"]: g for g in datos["grupos"]}

    def pendientes(self):
        codigo, salida = self.ejecutar(self.detector().cmd_pendientes)
        return codigo, {p["grupo_id"]: p for p in json.loads(salida)}

    def evaluacion_valida(self, grupo_id, **cambios):
        base = {
            "grupo_id": grupo_id,
            "articulos_comparados": ["p1", "p2"],
            "cobertura": "ampliación",
            "que_hemos_publicado": "Un tutorial de agentes con supervisión",
            "diferencia": "No cubrimos el flujo sin supervisión",
            "aportacion": "Probar el flujo completo y contar lo que falla",
            "parecida_a": None,
            "razon_nueva": None,
            "encaje": True,
            "motivo": "Es el nicho y podemos probarlo",
        }
        base.update(cambios)
        return base

    def guardar_evaluacion(self, datos):
        archivo = self.raiz / "evaluacion.json"
        archivo.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
        return self.ejecutar(self.detector().cmd_guardar_evaluacion, archivo)

    def leer_evaluacion(self, grupo_id):
        ruta = self.dir_oportunidades / "control" / "evaluaciones" / f"{grupo_id}.json"
        return json.loads(ruta.read_text(encoding="utf-8"))

    def guardar_oportunidad(self, grupo_id, cuerpo=CUERPO_VALIDO, actualizar=None):
        archivo = None
        if cuerpo is not None:
            archivo = self.raiz / "cuerpo.md"
            archivo.write_text(cuerpo, encoding="utf-8")
        return self.ejecutar(self.detector().cmd_guardar_oportunidad, grupo_id, archivo, actualizar)


# El grupo_id lleva el slug del tema dominante + la entidad/eje dominante.
# "openai" ya está contenida en el slug del tema, así que no se repite.
GRUPO_AGENTES = "agentes-que-investigan-solos-claude-code"
GRUPO_VIDEO = "edicion-de-video-con-ia-capcut"
GRUPO_MODELO = "nuevo-modelo-de-openai"


class PruebasAgrupar(Base):
    def test_agrupa_por_entidades_y_separa_lo_distinto(self):
        codigo, grupos = self.grupos()
        self.assertEqual(codigo, CODIGO_OK)
        self.assertEqual(set(grupos), {GRUPO_AGENTES, GRUPO_VIDEO, GRUPO_MODELO})
        agentes = grupos[GRUPO_AGENTES]
        # v1, v2 y b1 comparten entidades (Jaccard >= 0.5), aunque b1 tenga otro tema.
        self.assertEqual(agentes["fichas"], ["blog:b1", "youtube:v1", "youtube:v2"])
        self.assertEqual(agentes["senales"]["fichas"], 3)
        self.assertEqual(grupos[GRUPO_VIDEO]["fichas"], ["youtube:v3"])

    def test_mismo_tema_sin_entidades_comunes_separa(self):
        # Grano fino: la etiqueta "Herramientas de IA" no junta historias sin relación.
        self.escribir_externa(ficha_externa(
            "youtube", "w1", "Herramientas de IA", "Canal A", 0.5,
            ["Gemini Live", "Google"]))
        self.escribir_externa(ficha_externa(
            "youtube", "w2", "Herramientas de IA", "Canal B", 0.4,
            ["Qwen", "LM Studio"]))
        _, grupos = self.grupos()
        self.assertIn("herramientas-de-ia-gemini-live", grupos)
        self.assertIn("herramientas-de-ia-qwen", grupos)
        self.assertEqual(grupos["herramientas-de-ia-gemini-live"]["fichas"], ["youtube:w1"])
        self.assertEqual(grupos["herramientas-de-ia-qwen"]["fichas"], ["youtube:w2"])

    def test_mismo_tema_con_jaccard_alto_junta(self):
        _, grupos = self.grupos()
        # v4 ["OpenAI", "GPT"] y v5 ["OpenAI"]: Jaccard = 1/2 >= 0.5.
        self.assertEqual(grupos[GRUPO_MODELO]["fichas"], ["youtube:v4", "youtube:v5"])

    def test_colision_de_grupo_id_se_desambigua_con_ordinal(self):
        # Mismo tema y misma entidad dominante, pero sin afinidad suficiente.
        self.escribir_externa(ficha_externa(
            "youtube", "w1", "Herramientas de IA", "Canal A", 0.5,
            ["Qwen", "Gemini Live", "Google"]))
        self.escribir_externa(ficha_externa(
            "youtube", "w2", "Herramientas de IA", "Canal B", 0.4,
            ["Qwen", "LM Studio", "llama.cpp"]))
        _, grupos = self.grupos()
        self.assertIn("herramientas-de-ia-qwen", grupos)
        self.assertIn("herramientas-de-ia-qwen-2", grupos)

    def test_cuenta_autores_distintos(self):
        _, grupos = self.grupos()
        self.assertEqual(grupos[GRUPO_AGENTES]["senales"]["canales"], 3)
        self.assertEqual(grupos[GRUPO_VIDEO]["senales"]["canales"], 1)
        self.assertEqual(grupos[GRUPO_MODELO]["senales"]["canales"], 2)

    def test_grupo_id_estable_entre_ejecuciones(self):
        _, primera = self.grupos()
        _, segunda = self.grupos()
        self.assertEqual(sorted(primera), sorted(segunda))
        self.assertEqual(primera[GRUPO_AGENTES]["huella_fichas"],
                         segunda[GRUPO_AGENTES]["huella_fichas"])

    def test_ficha_invalida_se_omite_y_se_informa(self):
        carpeta = self.biblioteca / "blog" / "items" / "rota"
        carpeta.mkdir(parents=True)
        (carpeta / "ficha.json").write_text('{"id": "rota"}', encoding="utf-8")
        codigo, grupos = self.grupos()
        self.assertEqual(codigo, CODIGO_PARCIAL)
        self.assertEqual(set(grupos), {GRUPO_AGENTES, GRUPO_VIDEO, GRUPO_MODELO})


class PruebasInteresReal(Base):
    def test_por_nivel_de_interes(self):
        _, grupos = self.grupos()
        agentes = grupos[GRUPO_AGENTES]["senales"]
        self.assertEqual(agentes["mejor_interes"], "alto")  # multiplo 2.5
        self.assertTrue(agentes["interes_real"])
        video = grupos[GRUPO_VIDEO]["senales"]
        self.assertEqual(video["mejor_interes"], "bajo")
        self.assertFalse(video["interes_real"])

    def test_por_numero_de_canales(self):
        _, grupos = self.grupos()
        modelo = grupos[GRUPO_MODELO]["senales"]
        self.assertEqual(modelo["mejor_interes"], "bajo")
        self.assertTrue(modelo["interes_real"])  # 2 canales

    def test_regla_dos_canales_se_calcula_a_nivel_de_tema(self):
        # Dos canales hablan del tema, pero sin entidades comunes: los grupos
        # quedan separados y aun así ambos tienen interés real por el TEMA.
        self.escribir_externa(ficha_externa(
            "youtube", "w1", "Herramientas de IA", "Canal A", 0.5,
            ["Gemini Live", "Google"]))
        self.escribir_externa(ficha_externa(
            "youtube", "w2", "Herramientas de IA", "Canal B", 0.4,
            ["Qwen", "LM Studio"]))
        _, grupos = self.grupos()
        for gid in ("herramientas-de-ia-gemini-live", "herramientas-de-ia-qwen"):
            senales = grupos[gid]["senales"]
            self.assertEqual(senales["mejor_interes"], "bajo")
            self.assertEqual(senales["canales"], 1)
            self.assertEqual(senales["canales_tema"], 2)
            self.assertTrue(senales["interes_real"])


class PruebasBM25(Base):
    def test_situa_primero_el_articulo_del_mismo_tema_con_su_ruta(self):
        _, paquetes = self.pendientes()
        articulos = paquetes[GRUPO_AGENTES]["articulos_parecidos"]
        self.assertEqual(articulos[0]["post_id"], "p1")
        self.assertGreater(articulos[0]["puntuacion"], 0)
        self.assertEqual(articulos[0]["ruta_texto"],
                         "biblioteca/substack/articulos/2026-01-10-agentes-investigacion.md")
        self.assertTrue((self.raiz / articulos[0]["ruta_texto"]).is_file())

    def test_encuentra_la_oportunidad_descartada_parecida(self):
        _, paquetes = self.pendientes()
        parecidas = paquetes[GRUPO_VIDEO]["oportunidades_parecidas"]
        ids = [p["id"] for p in parecidas]
        self.assertIn("2026-09-01-edicion-de-video-con-ia", ids)
        descartada = next(p for p in parecidas if p["estado"] == "descartada")
        self.assertEqual(descartada["motivo"], "tema efímero y fuera de nicho")


class PruebasPendientes(Base):
    def test_no_repite_un_grupo_evaluado_sin_cambios(self):
        codigo, _ = self.guardar_evaluacion(self.evaluacion_valida(GRUPO_AGENTES))
        self.assertEqual(codigo, CODIGO_OK)
        _, paquetes = self.pendientes()
        self.assertNotIn(GRUPO_AGENTES, paquetes)
        self.assertIn(GRUPO_VIDEO, paquetes)  # sin evaluación: sigue pendiente

    def test_vuelve_a_pedirlo_si_cambia_una_ficha(self):
        self.guardar_evaluacion(self.evaluacion_valida(GRUPO_AGENTES))
        ficha = ficha_externa("youtube", "v1", "Agentes que investigan solos", "Canal A", 2.5,
                              ["Claude Code", "agentes"], huella="huella-cambiada")
        self.escribir_externa(ficha)
        _, paquetes = self.pendientes()
        self.assertIn(GRUPO_AGENTES, paquetes)
        self.assertEqual(paquetes[GRUPO_AGENTES]["motivo_pendiente"], "fichas_cambiadas")

    def test_vuelve_a_pedirlo_si_cambia_un_articulo_comparado(self):
        self.guardar_evaluacion(self.evaluacion_valida(GRUPO_AGENTES))
        self.escribir_propia(ficha_propia(
            "p1", "Agentes para automatizar la investigación",
            "Probé agentes que investigan por mí",
            "Los agentes de investigación funcionan con supervisión",
            ["Claude Code", "agentes"], huella="huella-articulo-cambiada"))
        _, paquetes = self.pendientes()
        self.assertIn(GRUPO_AGENTES, paquetes)
        self.assertEqual(paquetes[GRUPO_AGENTES]["motivo_pendiente"], "articulos_cambiados")

    def test_crear_la_propuesta_no_deja_el_grupo_pendiente_otra_vez(self):
        self.guardar_evaluacion(self.evaluacion_valida(GRUPO_AGENTES))
        codigo, _ = self.guardar_oportunidad(GRUPO_AGENTES)
        self.assertEqual(codigo, CODIGO_OK)
        _, paquetes = self.pendientes()
        self.assertNotIn(GRUPO_AGENTES, paquetes)
        # Cuando la persona decide (descarta la propuesta), el grupo sí vuelve.
        self.escribir_oportunidad(f"{HOY}-{GRUPO_AGENTES}", "descartada",
                                  "Agentes que investigan solos", motivo="no era el momento")
        ruta = self.dir_oportunidades / f"{HOY}-{GRUPO_AGENTES}.md"
        texto = ruta.read_text(encoding="utf-8").replace("cobertura: nuevo",
                                                         f"cobertura: nuevo\ngrupo_id: {GRUPO_AGENTES}")
        ruta.write_text(texto, encoding="utf-8")
        _, paquetes = self.pendientes()
        self.assertIn(GRUPO_AGENTES, paquetes)
        self.assertEqual(paquetes[GRUPO_AGENTES]["motivo_pendiente"], "decisiones_cambiadas")

    def test_vuelve_a_pedirlo_si_cambia_una_decision_parecida(self):
        self.guardar_evaluacion(self.evaluacion_valida(GRUPO_AGENTES))
        # La propuesta parecida cambia de estado: la decisión con la que se comparó ya no es la misma.
        self.escribir_oportunidad(
            "2026-09-05-agentes-de-investigacion", "descartada", "agentes de investigación",
            motivo="al final no era el momento", evidencias=["youtube:zz9@00:10"])
        _, paquetes = self.pendientes()
        self.assertIn(GRUPO_AGENTES, paquetes)
        self.assertEqual(paquetes[GRUPO_AGENTES]["motivo_pendiente"], "decisiones_cambiadas")


class PruebasGuardarEvaluacion(Base):
    def test_grupo_cubierto_no_es_oportunidad(self):
        codigo, salida = self.guardar_evaluacion(self.evaluacion_valida(
            GRUPO_AGENTES, cobertura="cubierto"))
        self.assertEqual(codigo, CODIGO_OK)
        guardada = self.leer_evaluacion(GRUPO_AGENTES)
        self.assertFalse(guardada["es_oportunidad"])
        self.assertFalse(guardada["condiciones"]["no_cubierto"]["cumple"])
        self.assertIn("no_cubierto", guardada["motivo_descarte"])

    def test_sin_aportacion_no_es_oportunidad(self):
        self.guardar_evaluacion(self.evaluacion_valida(GRUPO_AGENTES, aportacion=None))
        guardada = self.leer_evaluacion(GRUPO_AGENTES)
        self.assertFalse(guardada["es_oportunidad"])
        self.assertFalse(guardada["condiciones"]["aportacion"]["cumple"])

    def test_sin_encaje_no_es_oportunidad(self):
        self.guardar_evaluacion(self.evaluacion_valida(
            GRUPO_AGENTES, encaje=False, motivo="Fuera de nicho"))
        guardada = self.leer_evaluacion(GRUPO_AGENTES)
        self.assertFalse(guardada["es_oportunidad"])
        self.assertFalse(guardada["condiciones"]["encaje"]["cumple"])

    def test_sin_interes_real_no_es_oportunidad(self):
        self.guardar_evaluacion(self.evaluacion_valida(GRUPO_VIDEO, cobertura="nuevo"))
        guardada = self.leer_evaluacion(GRUPO_VIDEO)
        self.assertFalse(guardada["es_oportunidad"])
        self.assertFalse(guardada["condiciones"]["interes_real"]["cumple"])
        # Las otras tres sí se cumplen: la condición fallida queda señalada.
        self.assertTrue(guardada["condiciones"]["encaje"]["cumple"])
        self.assertTrue(guardada["condiciones"]["no_cubierto"]["cumple"])
        self.assertTrue(guardada["condiciones"]["aportacion"]["cumple"])

    def test_rechaza_si_faltan_articulos_comparados(self):
        codigo, _ = self.guardar_evaluacion(self.evaluacion_valida(
            GRUPO_AGENTES, articulos_comparados=["p1"]))
        self.assertEqual(codigo, CODIGO_FATAL)
        ruta = self.dir_oportunidades / "control" / "evaluaciones" / f"{GRUPO_AGENTES}.json"
        self.assertFalse(ruta.is_file())

    def test_rechaza_si_no_cumple_el_esquema(self):
        evaluacion = self.evaluacion_valida(GRUPO_AGENTES)
        del evaluacion["motivo"]
        codigo, _ = self.guardar_evaluacion(evaluacion)
        self.assertEqual(codigo, CODIGO_FATAL)


class PruebasParecidas(Base):
    def test_parecida_a_un_descarte_exige_razon_nueva(self):
        self.guardar_evaluacion(self.evaluacion_valida(
            GRUPO_AGENTES, parecida_a="2026-09-01-edicion-de-video-con-ia"))
        guardada = self.leer_evaluacion(GRUPO_AGENTES)
        self.assertFalse(guardada["es_oportunidad"])
        self.assertIn("razon_nueva", guardada["motivo_descarte"])

    def test_con_razon_nueva_si_es_oportunidad(self):
        self.guardar_evaluacion(self.evaluacion_valida(
            GRUPO_AGENTES, parecida_a="2026-09-01-edicion-de-video-con-ia",
            razon_nueva="Ha salido una versión nueva que cambia el coste"))
        guardada = self.leer_evaluacion(GRUPO_AGENTES)
        self.assertTrue(guardada["es_oportunidad"])

    def test_parecida_a_una_propuesta_no_crea_duplicado(self):
        self.guardar_evaluacion(self.evaluacion_valida(
            GRUPO_AGENTES, parecida_a="2026-09-05-agentes-de-investigacion"))
        guardada = self.leer_evaluacion(GRUPO_AGENTES)
        self.assertFalse(guardada["es_oportunidad"])
        self.assertEqual(guardada["accion"], "actualizar:2026-09-05-agentes-de-investigacion")
        # guardar-oportunidad con esa evaluación se rechaza.
        codigo, _ = self.guardar_oportunidad(GRUPO_AGENTES)
        self.assertEqual(codigo, CODIGO_FATAL)


class PruebasGuardarOportunidad(Base):
    def test_rechaza_grupos_que_no_cumplen_las_condiciones(self):
        self.guardar_evaluacion(self.evaluacion_valida(GRUPO_AGENTES, cobertura="cubierto"))
        codigo, _ = self.guardar_oportunidad(GRUPO_AGENTES)
        self.assertEqual(codigo, CODIGO_FATAL)
        self.assertFalse((self.dir_oportunidades / f"{HOY}-{GRUPO_AGENTES}.md").is_file())

    def test_rechaza_sin_evaluacion(self):
        codigo, _ = self.guardar_oportunidad(GRUPO_AGENTES)
        self.assertEqual(codigo, CODIGO_FATAL)

    def test_rechaza_cuerpo_con_secciones_que_faltan_o_vacias(self):
        self.guardar_evaluacion(self.evaluacion_valida(GRUPO_AGENTES))
        sin_riesgos = CUERPO_VALIDO.split("## Riesgos")[0]
        codigo, _ = self.guardar_oportunidad(GRUPO_AGENTES, cuerpo=sin_riesgos)
        self.assertEqual(codigo, CODIGO_FATAL)
        vacia = CUERPO_VALIDO.replace("Tema posiblemente efímero.", "")
        codigo, _ = self.guardar_oportunidad(GRUPO_AGENTES, cuerpo=vacia)
        self.assertEqual(codigo, CODIGO_FATAL)
        self.assertFalse((self.dir_oportunidades / f"{HOY}-{GRUPO_AGENTES}.md").is_file())

    def test_escribe_el_encabezado_con_los_datos_calculados(self):
        self.guardar_evaluacion(self.evaluacion_valida(GRUPO_AGENTES))
        codigo, _ = self.guardar_oportunidad(GRUPO_AGENTES)
        self.assertEqual(codigo, CODIGO_OK)
        ruta = self.dir_oportunidades / f"{HOY}-{GRUPO_AGENTES}.md"
        encabezado, cuerpo = parsear_frontmatter(ruta.read_text(encoding="utf-8"))
        self.assertEqual(encabezado["id"], f"{HOY}-{GRUPO_AGENTES}")
        self.assertEqual(encabezado["estado"], "propuesta")
        self.assertEqual(encabezado["motivo_estado"], "")
        self.assertEqual(encabezado["grupo_id"], GRUPO_AGENTES)
        self.assertEqual(encabezado["interes"], "alto")
        self.assertEqual(encabezado["canales"], 3)
        self.assertEqual(encabezado["cobertura"], "ampliación")
        self.assertEqual(encabezado["evidencias"],
                         ["blog:b1@parrafo-4", "youtube:v1@12:34", "youtube:v2@03:10"])
        self.assertEqual(encabezado["relacionados"], ["substack:p1", "substack:p2"])
        self.assertEqual(validar_cuerpo_oportunidad(cuerpo), [])

    def test_nunca_sobrescribe_una_oportunidad_aceptada_o_descartada(self):
        self.guardar_evaluacion(self.evaluacion_valida(GRUPO_AGENTES))
        oid = f"{HOY}-{GRUPO_AGENTES}"
        self.escribir_oportunidad(oid, "aceptada", "Agentes que investigan solos",
                                  motivo="ya en marcha")
        antes = (self.dir_oportunidades / f"{oid}.md").read_text(encoding="utf-8")
        codigo, _ = self.guardar_oportunidad(GRUPO_AGENTES)
        self.assertEqual(codigo, CODIGO_FATAL)
        self.assertEqual((self.dir_oportunidades / f"{oid}.md").read_text(encoding="utf-8"), antes)
        # Con estado descartada, igual.
        self.escribir_oportunidad(oid, "descartada", "Agentes que investigan solos", motivo="no")
        codigo, _ = self.guardar_oportunidad(GRUPO_AGENTES)
        self.assertEqual(codigo, CODIGO_FATAL)


class PruebasActualizar(Base):
    def test_anade_evidencias_sin_tocar_cuerpo_ni_estado(self):
        oid = "2026-09-05-agentes-de-investigacion"
        ruta = self.dir_oportunidades / f"{oid}.md"
        _, cuerpo_antes = parsear_frontmatter(ruta.read_text(encoding="utf-8"))
        codigo, salida = self.guardar_oportunidad(GRUPO_AGENTES, cuerpo=None, actualizar=oid)
        self.assertEqual(codigo, CODIGO_OK)
        encabezado, cuerpo = parsear_frontmatter(ruta.read_text(encoding="utf-8"))
        self.assertEqual(encabezado["estado"], "propuesta")
        self.assertEqual(cuerpo.strip(), cuerpo_antes.strip())
        self.assertEqual(encabezado["evidencias"],
                         ["youtube:zz9@00:10", "blog:b1@parrafo-4",
                          "youtube:v1@12:34", "youtube:v2@03:10"])
        # Repetir no duplica evidencias.
        self.guardar_oportunidad(GRUPO_AGENTES, cuerpo=None, actualizar=oid)
        encabezado, _ = parsear_frontmatter(ruta.read_text(encoding="utf-8"))
        self.assertEqual(len(encabezado["evidencias"]), 4)

    def test_rechaza_actualizar_una_descartada(self):
        codigo, _ = self.guardar_oportunidad(
            GRUPO_AGENTES, cuerpo=None, actualizar="2026-09-01-edicion-de-video-con-ia")
        self.assertEqual(codigo, CODIGO_FATAL)


class PruebasIndice(Base):
    def test_ordena_por_prioridad_y_es_determinista(self):
        # Tres propuestas con prioridades distintas.
        self.escribir_oportunidad("2026-10-02-propuesta-media", "propuesta", "tema b")
        (self.dir_oportunidades / "2026-10-03-propuesta-alta.md").write_text(
            oportunidad_md("2026-10-03-propuesta-alta", "propuesta", "tema a")
            .replace("interes: medio", "interes: alto"), encoding="utf-8")
        (self.dir_oportunidades / "2026-10-04-propuesta-ampliacion.md").write_text(
            oportunidad_md("2026-10-04-propuesta-ampliacion", "propuesta", "tema c")
            .replace("cobertura: nuevo", "cobertura: ampliación")
            .replace("canales: 1", "canales: 5"), encoding="utf-8")
        codigo, _ = self.ejecutar(self.detector().cmd_indice)
        self.assertEqual(codigo, CODIGO_OK)
        indice = (self.dir_oportunidades / "INDICE.md").read_text(encoding="utf-8")
        pos = {oid: indice.index(oid) for oid in (
            "2026-10-03-propuesta-alta",        # interés alto primero
            "2026-10-04-propuesta-ampliacion",  # medio con 5 canales
            "2026-10-02-propuesta-media",       # medio, 1 canal, nuevo
            "2026-09-05-agentes-de-investigacion",
        )}
        self.assertLess(pos["2026-10-03-propuesta-alta"], pos["2026-10-04-propuesta-ampliacion"])
        self.assertLess(pos["2026-10-04-propuesta-ampliacion"], pos["2026-10-02-propuesta-media"])
        # Estados no propuestos, con su motivo.
        self.assertIn("## Aceptadas", indice)
        self.assertIn("la probamos", indice)
        self.assertIn("## Descartadas", indice)
        self.assertIn("tema efímero y fuera de nicho", indice)
        # Determinista: regenerar produce el mismo contenido byte a byte.
        self.ejecutar(self.detector().cmd_indice)
        self.assertEqual(indice, (self.dir_oportunidades / "INDICE.md").read_text(encoding="utf-8"))


class PruebasCalendario(Base):
    # HOY (2026-10-14) es miércoles: el lunes de la semana siguiente es 2026-10-19.

    def indice(self):
        codigo, _ = self.ejecutar(self.detector().cmd_indice)
        self.assertEqual(codigo, CODIGO_OK)
        return (self.dir_oportunidades / "INDICE.md").read_text(encoding="utf-8")

    def test_lunes_siguiente(self):
        self.assertEqual(lunes_siguiente("2026-10-14").isoformat(), "2026-10-19")  # miércoles
        self.assertEqual(lunes_siguiente("2026-10-19").isoformat(), "2026-10-26")  # lunes
        self.assertEqual(lunes_siguiente("2026-10-18").isoformat(), "2026-10-19")  # domingo

    def test_aceptadas_antes_que_propuestas_en_lunes_consecutivos(self):
        # Una propuesta de interés alto, que aun así va detrás de la aceptada.
        (self.dir_oportunidades / "2026-10-03-propuesta-alta.md").write_text(
            oportunidad_md("2026-10-03-propuesta-alta", "propuesta", "tema a")
            .replace("interes: medio", "interes: alto"), encoding="utf-8")
        indice = self.indice()
        self.assertIn("## Calendario sugerido", indice)
        self.assertIn("la persona decide", indice)
        calendario = indice.split("## Calendario sugerido")[1]
        filas = [l for l in calendario.splitlines() if l.startswith("| 2026-")]
        self.assertEqual(len(filas), 3)
        # La aceptada primero; después las propuestas por prioridad (alta antes que media).
        self.assertIn("2026-09-10-flujos-con-n8n", filas[0])
        self.assertIn("| aceptada |", filas[0])
        self.assertIn("2026-10-03-propuesta-alta", filas[1])
        self.assertIn("2026-09-05-agentes-de-investigacion", filas[2])
        # Semanas consecutivas a partir del lunes que viene, todas en lunes.
        fechas = [f.split("|")[1].strip() for f in filas]
        self.assertEqual(fechas, ["2026-10-19", "2026-10-26", "2026-11-02"])
        import datetime
        for f in fechas:
            self.assertEqual(datetime.date.fromisoformat(f).weekday(), 0)

    def test_determinista_y_respeta_hoy(self):
        indice = self.indice()
        self.assertEqual(indice, self.indice())
        # Con otra fecha, el calendario empieza en otro lunes.
        codigo, _ = self.ejecutar(Detector(self.config, hoy="2026-10-20").cmd_indice)
        self.assertEqual(codigo, CODIGO_OK)
        otro = (self.dir_oportunidades / "INDICE.md").read_text(encoding="utf-8")
        self.assertIn("| 2026-10-26 |", otro)

    def test_sin_programables_lo_dice(self):
        for ruta in self.dir_oportunidades.glob("*.md"):
            if ruta.name != "INDICE.md":
                ruta.unlink()
        indice = self.indice()
        self.assertIn("## Calendario sugerido", indice)
        self.assertIn("Nada que programar", indice)


class PruebasNormalizacion(unittest.TestCase):
    def test_normalizar_tema(self):
        self.assertEqual(normalizar_tema("  Edición   de VÍDEO  "), "edicion de video")


if __name__ == "__main__":
    unittest.main()
