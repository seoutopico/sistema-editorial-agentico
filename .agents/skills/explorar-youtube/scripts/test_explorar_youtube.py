"""Pruebas de explorar_youtube.py.

Inyectan una funcion simulada en lugar de yt-dlp (JSON de listado plano, JSON
de video individual y archivos VTT de ejemplo) y trabajan en una carpeta
temporal. Nunca acceden a internet ni tocan biblioteca/.
"""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import explorar_youtube as ey  # noqa: E402

HOY = date(2026, 10, 14)
CANAL_A = "https://www.youtube.com/@canala"
CANAL_B = "https://www.youtube.com/@canalb"

VTT_EJEMPLO = """WEBVTT
Kind: captions
Language: es

00:00:00.000 --> 00:00:02.000
hola a todos

00:00:02.000 --> 00:00:04.000
hola a todos

00:00:04.000 --> 00:00:06.000
bienvenidos al <c>canal</c>

00:00:06.000 --> 00:00:08.000
bienvenidos al canal
hoy probamos agentes

00:00:35.000 --> 00:00:38.000
aqui empieza otra parte
"""


def entrada(video_id, vis, dur=600, fecha="20260901", titulo=None):
    return {
        "id": video_id,
        "title": titulo or f"Video {video_id}",
        "view_count": vis,
        "duration": dur,
        "upload_date": fecha,
    }


def listado(nombre_canal, entradas):
    return {"channel": nombre_canal, "entries": entradas}


def crear_fake(canales=None, videos=None, subs=None):
    """Simula yt-dlp. canales: {url_canal: listado | None (error)};
    videos: {id: metadatos | None (error)};
    subs: {id: [{"auto": bool, "idioma": str, "vtt": str}]}."""
    canales = canales or {}
    videos = videos or {}
    subs = subs or {}
    llamadas = []

    def ejecutar(args):
        llamadas.append(list(args))
        url = args[-1]
        if "--flat-playlist" in args:
            clave = url[: -len("/videos")]
            respuesta = canales.get(clave)
            if respuesta is None:
                return 1, "", "ERROR: [youtube:tab] el canal no esta disponible"
            return 0, json.dumps(respuesta), ""
        if "--skip-download" in args:
            video_id = url.rsplit("v=", 1)[-1]
            destino = Path(args[args.index("--paths") + 1])
            quiere_auto = "--write-auto-subs" in args
            for info in subs.get(video_id, []):
                if info.get("auto", False) == quiere_auto:
                    (destino / f"subtitulos.{info['idioma']}.vtt").write_text(
                        info["vtt"], encoding="utf-8"
                    )
            return 0, "", ""
        video_id = url.rsplit("v=", 1)[-1]
        respuesta = videos.get(video_id)
        if respuesta is None:
            return 1, "", "ERROR: el video no esta disponible"
        return 0, json.dumps(respuesta), ""

    ejecutar.llamadas = llamadas
    return ejecutar


class CasoBase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.raiz = Path(self._tmp.name)

    def crear_proyecto(self, canales_md=None, **youtube):
        config = {
            "linea_editorial": {
                "nicho": "IA aplicada al trabajo",
                "audiencia": "Profesionales",
                "aportacion": "Probar las cosas",
            },
            "recursos": {
                "herramientas": ["Claude Code", "n8n"],
                "hardware": "PC de consumo, sin GPU grande",
                "formatos_que_domina": ["texto y capturas"],
                "fuera_de_alcance": ["edición y producción de vídeo"],
            },
            "youtube": {
                "videos_por_canal": 30,
                "ventana_dias": 60,
                "duracion_minima_segundos": 180,
                "candidatos_por_ejecucion": 10,
                "idiomas_subtitulos": ["es", "en"],
            },
            "red": {"timeout_segundos": 30, "intentos": 3, "pausa_segundos": 0.5},
        }
        config["youtube"].update(youtube)
        (self.raiz / "proyecto.config.json").write_text(
            json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        dir_youtube = self.raiz / "biblioteca" / "youtube"
        dir_youtube.mkdir(parents=True, exist_ok=True)
        if canales_md is None:
            canales_md = f"# Canales\n\n- {CANAL_A}\n- {CANAL_B}\n"
        (dir_youtube / "canales.md").write_text(canales_md, encoding="utf-8")

    def explorador(self, fake):
        return ey.Explorador(self.raiz, hoy=HOY, ejecutar_ytdlp=fake)

    def ejecutar(self, explorador, metodo, *args):
        salida = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(error):
            codigo = getattr(explorador, metodo)(*args)
        return codigo, salida.getvalue(), error.getvalue()

    def meta(self, video_id):
        ruta = self.raiz / "biblioteca" / "youtube" / "videos" / video_id / "meta.json"
        return json.loads(ruta.read_text(encoding="utf-8"))

    def lineas_metricas(self):
        ruta = self.raiz / "biblioteca" / "youtube" / "control" / "metricas.jsonl"
        if not ruta.is_file():
            return []
        return [json.loads(l) for l in ruta.read_text(encoding="utf-8").splitlines() if l]

    def informes(self, comando=None):
        carpeta = self.raiz / "biblioteca" / "youtube" / "control" / "ejecuciones"
        if not carpeta.is_dir():
            return []

        def orden(ruta):
            # <run_id>.json y, si hay colision, <run_id>-N.json (posterior).
            base, separador, sufijo = ruta.stem.partition("Z-")
            return (base + "Z" if separador else base, int(sufijo) if sufijo else 0)

        datos = [
            json.loads(r.read_text(encoding="utf-8"))
            for r in sorted(carpeta.glob("*.json"), key=orden)
        ]
        if comando:
            datos = [d for d in datos if d["comando"] == comando]
        return datos

    def escribir_json(self, nombre, datos):
        ruta = self.raiz / nombre
        ruta.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
        return ruta


class TestCanalesMd(CasoBase):
    def test_interpreta_handles_ids_y_urls_no_validas(self):
        texto = (
            "# Canales\n"
            "Texto explicativo que se ignora.\n"
            f"- {CANAL_A}\n"
            "- https://www.youtube.com/channel/UCabc123XYZ_-\n"
            "- https://www.youtube.com/watch?v=noesuncanal\n"
        )
        canales, errores = ey.leer_canales(texto)
        self.assertEqual(
            canales,
            [CANAL_A, "https://www.youtube.com/channel/UCabc123XYZ_-"],
        )
        self.assertEqual(len(errores), 1)
        self.assertIn("watch?v=noesuncanal", errores[0]["url"])

    def test_url_no_valida_falla_solo_para_ese_canal(self):
        self.crear_proyecto(
            canales_md=(
                f"- {CANAL_A}\n"
                "- https://example.com/otracosa\n"
                "- https://www.youtube.com/channel/UCzzz999\n"
            )
        )
        fake = crear_fake(canales={
            CANAL_A: listado("Canal A", [entrada("v1", 1000)]),
            "https://www.youtube.com/channel/UCzzz999": listado("Canal C", [entrada("v2", 2000)]),
        })
        codigo, _, _ = self.ejecutar(self.explorador(fake), "cmd_recoger")
        self.assertEqual(codigo, 1)  # error parcial por la URL no valida
        self.assertEqual(self.meta("v1")["canal"], "Canal A")
        self.assertEqual(self.meta("v2")["canal"], "Canal C")
        informe = self.informes()[-1]
        self.assertEqual(len(informe["canales"]["fallidos"]), 1)
        self.assertIn("example.com", informe["canales"]["fallidos"][0]["url"])


class TestRecoger(CasoBase):
    def test_guarda_meta_y_metricas_sin_duplicar(self):
        self.crear_proyecto(canales_md=f"- {CANAL_A}\n")
        fake1 = crear_fake(canales={
            CANAL_A: listado("Canal A", [entrada("v1", 1000), entrada("v2", 2000)]),
        })
        explorador = self.explorador(fake1)
        codigo, _, _ = self.ejecutar(explorador, "cmd_recoger")
        self.assertEqual(codigo, 0)
        self.assertEqual(self.meta("v1")["estadisticas"]["visualizaciones"], 1000)
        self.assertEqual(len(self.lineas_metricas()), 2)

        # Entre ejecuciones: relevancia, transcripcion y ficha existentes.
        clasificacion = self.escribir_json(
            "rel.json",
            [{"id": "v1", "relevante": True, "tema": "Agentes", "motivo": "encaja"}],
        )
        self.ejecutar(explorador, "cmd_guardar_relevancia", clasificacion)
        dir_v1 = self.raiz / "biblioteca" / "youtube" / "videos" / "v1"
        (dir_v1 / "transcripcion.md").write_text("[00:00] hola\n", encoding="utf-8")
        (dir_v1 / "ficha.json").write_text('{"huella": "x"}', encoding="utf-8")

        fake2 = crear_fake(canales={
            CANAL_A: listado("Canal A", [entrada("v1", 1500), entrada("v2", 2500)]),
        })
        codigo, _, _ = self.ejecutar(self.explorador(fake2), "cmd_recoger")
        self.assertEqual(codigo, 0)

        carpetas = sorted(
            p.name for p in (self.raiz / "biblioteca" / "youtube" / "videos").iterdir()
        )
        self.assertEqual(carpetas, ["v1", "v2"])  # no duplica videos
        self.assertEqual(len(self.lineas_metricas()), 4)  # nueva captura por video
        meta_v1 = self.meta("v1")
        self.assertEqual(meta_v1["estadisticas"]["visualizaciones"], 1500)
        self.assertEqual(meta_v1["relevancia"]["tema"], "Agentes")  # no se toca
        self.assertEqual(
            (dir_v1 / "transcripcion.md").read_text(encoding="utf-8"), "[00:00] hola\n"
        )
        self.assertEqual(
            (dir_v1 / "ficha.json").read_text(encoding="utf-8"), '{"huella": "x"}'
        )
        informe = self.informes()[-1]
        self.assertEqual(informe["videos_nuevos"], [])
        self.assertEqual(sorted(informe["videos_actualizados"]), ["v1", "v2"])

    def test_canal_con_error_conserva_datos_y_sale_con_1(self):
        self.crear_proyecto()
        fake_ok = crear_fake(canales={
            CANAL_A: listado("Canal A", [entrada("a1", 1000)]),
            CANAL_B: listado("Canal B", [entrada("b1", 5000)]),
        })
        self.ejecutar(self.explorador(fake_ok), "cmd_recoger")

        fake_fallo = crear_fake(canales={
            CANAL_A: listado("Canal A", [entrada("a1", 1100)]),
            # CANAL_B no responde: error de red o canal inexistente.
        })
        codigo, _, error = self.ejecutar(self.explorador(fake_fallo), "cmd_recoger")
        self.assertEqual(codigo, 1)
        self.assertIn("conservan", error)
        # Los datos anteriores del canal fallido siguen intactos.
        self.assertEqual(self.meta("b1")["estadisticas"]["visualizaciones"], 5000)
        self.assertEqual(self.meta("a1")["estadisticas"]["visualizaciones"], 1100)
        informe = self.informes()[-1]
        fallidos = informe["canales"]["fallidos"]
        self.assertEqual(len(fallidos), 1)
        self.assertEqual(fallidos[0]["url"], CANAL_B)
        self.assertIn("no esta disponible", fallidos[0]["motivo"])


class TestSenales(CasoBase):
    def test_mediana_multiplo_interes_y_marcas(self):
        self.crear_proyecto()
        fake = crear_fake(canales={
            CANAL_A: listado("Canal A", [
                entrada("s1", 600),
                entrada("s2", 1200),
                entrada("s3", 3000),
                entrada("s4", 6000),
                entrada("s5", 9000),
                entrada("s6", 50000, dur=60),            # corto: fuera de la mediana
                entrada("s7", 10, fecha="20261012"),     # 2 dias: senal incompleta
                entrada("s8", 100, dur=None),            # duracion null (directo)
            ]),
            CANAL_B: listado("Canal B", [
                entrada("t1", 1000),
                entrada("t2", 2000),
            ]),
        })
        codigo, _, _ = self.ejecutar(self.explorador(fake), "cmd_recoger")
        self.assertEqual(codigo, 0)

        s3 = self.meta("s3")["senales"]
        self.assertEqual(s3["mediana_canal"], 3000)  # excluye s6 (corto), s7 (<7d), s8 (sin duracion)
        self.assertEqual(s3["multiplo_mediana"], 1.0)
        self.assertEqual(s3["interes"], "medio")
        self.assertFalse(s3["mediana_poco_fiable"])

        self.assertEqual(self.meta("s1")["senales"]["interes"], "bajo")
        self.assertEqual(self.meta("s4")["senales"]["multiplo_mediana"], 2.0)
        self.assertEqual(self.meta("s4")["senales"]["interes"], "alto")
        self.assertEqual(self.meta("s5")["senales"]["interes"], "alto")

        s7 = self.meta("s7")["senales"]
        self.assertTrue(s7["senal_incompleta"])
        self.assertEqual(s7["interes"], "sin_datos")

        s8 = self.meta("s8")["senales"]
        self.assertFalse(s8["formato_largo"])  # duracion null no rompe los filtros
        self.assertIsNone(self.meta("s8")["duracion_segundos"])

        self.assertFalse(self.meta("s6")["senales"]["formato_largo"])

        # La interaccion es null hasta tener metadatos completos, y se indica.
        self.assertIsNone(s3["interaccion"])
        self.assertIn("incompletos", s3["interaccion_motivo"])

        # Canal con menos de 5 videos validos para la mediana.
        self.assertTrue(self.meta("t1")["senales"]["mediana_poco_fiable"])
        self.assertTrue(self.meta("t2")["senales"]["mediana_poco_fiable"])


class TestRelevanciaYCandidatos(CasoBase):
    def preparar(self, **youtube):
        self.crear_proyecto(**youtube)
        self.fake = crear_fake(
            canales={
                CANAL_A: listado("Canal A", [
                    entrada("a1", 600),
                    entrada("a2", 1200),
                    entrada("a3", 3000),
                    entrada("a4", 6000),
                    entrada("a5", 9000),
                    entrada("a6", 3000, fecha="20260701"),  # fuera de la ventana
                    entrada("a7", 99999, dur=60),            # corto
                    entrada("a8", 7000),                     # tendra ficha
                ]),
                CANAL_B: listado("Canal B", [
                    entrada("b1", 1000),
                    entrada("b2", 1000),
                    entrada("b3", 1000),
                    entrada("b4", 1000),
                    entrada("b5", 1000),
                    entrada("b6", 500),
                ]),
            },
            videos={
                "a5": {"upload_date": "20260901", "description": "desc a5",
                       "view_count": 9000, "like_count": None, "comment_count": 10},
                "a3": {"upload_date": "20260902", "description": "desc a3",
                       "view_count": 3000, "like_count": 100, "comment_count": 20},
                "b1": {"upload_date": "20260901", "description": "desc b1",
                       "view_count": 1000, "like_count": 10, "comment_count": 0},
                "b6": {"upload_date": "20260901", "description": "desc b6",
                       "view_count": 500, "like_count": 5, "comment_count": 1},
                "a1": {"upload_date": "20260901", "description": "desc a1",
                       "view_count": 600, "like_count": 6, "comment_count": 0},
            },
        )
        explorador = self.explorador(self.fake)
        self.ejecutar(explorador, "cmd_recoger")
        # a8 ya tiene ficha.
        dir_a8 = self.raiz / "biblioteca" / "youtube" / "videos" / "a8"
        (dir_a8 / "ficha.json").write_text('{"huella": "x"}', encoding="utf-8")
        return explorador

    def clasificar(self, explorador):
        ruta = self.escribir_json("rel.json", [
            {"id": "a1", "relevante": True, "tema": "Tema compartido", "motivo": "x"},
            {"id": "a2", "relevante": True, "tema": "Solo A", "motivo": "x"},
            {"id": "a3", "relevante": True, "tema": "Solo A", "motivo": "x"},
            {"id": "a4", "relevante": False, "tema": None, "motivo": "no encaja"},
            {"id": "a5", "relevante": True, "tema": "Solo A", "motivo": "x"},
            {"id": "a6", "relevante": True, "tema": "Tema compartido", "motivo": "x"},
            {"id": "a8", "relevante": True, "tema": "Solo A", "motivo": "x"},
            {"id": "b1", "relevante": True, "tema": "Tema B", "motivo": "x"},
            {"id": "b6", "relevante": True, "tema": "Tema compartido", "motivo": "x"},
        ])
        codigo, _, _ = self.ejecutar(explorador, "cmd_guardar_relevancia", ruta)
        self.assertEqual(codigo, 0)

    def test_relevancia_pendiente_filtra_y_lista_temas(self):
        explorador = self.preparar()
        # Un tema propio de Substack debe aparecer en los temas existentes.
        dir_fichas = self.raiz / "biblioteca" / "substack" / "fichas"
        dir_fichas.mkdir(parents=True)
        (dir_fichas / "1.json").write_text(
            '{"id": "1", "tema": "Tema propio"}', encoding="utf-8"
        )
        codigo, salida, _ = self.ejecutar(explorador, "cmd_relevancia_pendiente")
        self.assertEqual(codigo, 0)
        datos = json.loads(salida)
        ids = {v["id"] for v in datos["videos"]}
        self.assertIn("a1", ids)
        self.assertNotIn("a6", ids)  # fuera de la ventana
        self.assertNotIn("a7", ids)  # corto
        self.assertIn("Tema propio", datos["temas_existentes"])
        self.assertEqual(datos["linea_editorial"]["nicho"], "IA aplicada al trabajo")
        # Los recursos de la configuracion acompañan a la linea editorial,
        # para que el modelo aplique la regla de fuera de alcance.
        self.assertEqual(
            datos["recursos"]["fuera_de_alcance"], ["edición y producción de vídeo"]
        )
        self.assertIn("herramientas", datos["recursos"])

        self.clasificar(explorador)
        _, salida, _ = self.ejecutar(explorador, "cmd_relevancia_pendiente")
        ids = {v["id"] for v in json.loads(salida)["videos"]}
        self.assertNotIn("a1", ids)  # un video clasificado no se vuelve a pedir
        self.assertIn("b2", ids)     # los no clasificados siguen pendientes

    def test_candidatos_filtros_orden_y_limite(self):
        explorador = self.preparar()
        self.clasificar(explorador)
        codigo, salida, _ = self.ejecutar(explorador, "cmd_candidatos")
        self.assertEqual(codigo, 0)
        datos = json.loads(salida)
        ids = [c["id"] for c in datos["candidatos"]]
        # a5 alto; a3 y b1 medios (desempate por id); b6 y a1 bajos con tema en
        # 2 canales (desempate por multiplo). Excluidos: a2 (bajo, 1 canal),
        # a4 (no relevante), a6 (fuera de ventana), a7 (corto), a8 (con ficha).
        self.assertEqual(ids, ["a5", "a3", "b1", "b6", "a1"])
        self.assertEqual(datos["elegibles_totales"], 5)

        # Metadatos completados solo para los candidatos.
        meta_a3 = self.meta("a3")
        self.assertEqual(meta_a3["fecha_precision"], "exacta")
        self.assertEqual(meta_a3["fecha"], "2026-09-02")
        self.assertEqual(meta_a3["descripcion"], "desc a3")
        self.assertEqual(meta_a3["senales"]["interaccion"], 0.04)  # (100+20)/3000
        # Likes ocultos: interaccion null sin romper el calculo, con motivo.
        meta_a5 = self.meta("a5")
        self.assertIsNone(meta_a5["senales"]["interaccion"])
        self.assertIn("ocultos", meta_a5["senales"]["interaccion_motivo"])
        # a2 no es candidato: sigue sin metadatos completos.
        self.assertFalse(self.meta("a2")["metadatos_completos"])

        informe = self.informes()[-1]
        self.assertEqual([c["id"] for c in informe["candidatos"]], ids)
        self.assertTrue(all(c["motivo"] for c in informe["candidatos"]))

    def test_candidatos_respeta_el_limite(self):
        explorador = self.preparar(candidatos_por_ejecucion=2)
        self.clasificar(explorador)
        _, salida, _ = self.ejecutar(explorador, "cmd_candidatos")
        ids = [c["id"] for c in json.loads(salida)["candidatos"]]
        self.assertEqual(ids, ["a5", "a3"])


class TestSubtitulos(CasoBase):
    def preparar_video(self, explorador, video_id):
        explorador.guardar_meta({
            "id": video_id,
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "canal": "Canal A",
            "canal_url": CANAL_A,
            "titulo": f"Video {video_id}",
            "estadisticas": {},
        })

    def test_limpieza_del_vtt(self):
        texto = ey.limpiar_vtt(VTT_EJEMPLO)
        # Elimina repeticiones de los subtitulos automaticos...
        self.assertEqual(texto.count("hola a todos"), 1)
        self.assertEqual(texto.count("bienvenidos al canal"), 1)
        # ...conserva todo el texto, sin etiquetas...
        self.assertIn("hoy probamos agentes", texto)
        self.assertIn("aqui empieza otra parte", texto)
        self.assertNotIn("<c>", texto)
        # ...y agrupa con marcas de tiempo cada ~30 segundos.
        self.assertIn("[00:00]", texto)
        self.assertIn("[00:35]", texto)

    def test_descarga_preferencias_y_sin_subtitulos(self):
        self.crear_proyecto()
        fake = crear_fake(subs={
            "auto1": [{"auto": True, "idioma": "es", "vtt": VTT_EJEMPLO}],
            "manu1": [
                {"auto": False, "idioma": "en", "vtt": VTT_EJEMPLO},
                {"auto": True, "idioma": "es", "vtt": VTT_EJEMPLO},
            ],
            # "nada1" no tiene subtitulos.
        })
        explorador = self.explorador(fake)
        for video_id in ("auto1", "manu1", "nada1"):
            self.preparar_video(explorador, video_id)

        codigo, salida, _ = self.ejecutar(
            explorador, "cmd_subtitulos", ["auto1", "manu1", "nada1"]
        )
        self.assertEqual(codigo, 0)
        datos = json.loads(salida)

        # Solo automaticos: se usan, y queda registrado el origen.
        self.assertEqual(self.meta("auto1")["subtitulos"]["origen"], "automaticos")
        self.assertTrue(
            (self.raiz / "biblioteca/youtube/videos/auto1/transcripcion.md").is_file()
        )
        # Manuales (aunque sea en otro idioma) antes que automaticos.
        self.assertEqual(self.meta("manu1")["subtitulos"]["origen"], "manuales")
        self.assertEqual(self.meta("manu1")["subtitulos"]["idioma"], "en")
        # Sin subtitulos: marcado con motivo y sin transcripcion.
        sub_nada = self.meta("nada1")["subtitulos"]
        self.assertFalse(sub_nada["disponibles"])
        self.assertIn("sin subtitulos", sub_nada["motivo"])
        self.assertFalse(
            (self.raiz / "biblioteca/youtube/videos/nada1/transcripcion.md").exists()
        )
        self.assertEqual(len(datos["subtitulos_no_disponibles"]), 1)

        # Un video con transcripcion no se vuelve a descargar.
        llamadas_antes = len(fake.llamadas)
        codigo, salida, _ = self.ejecutar(explorador, "cmd_subtitulos", ["auto1"])
        self.assertEqual(codigo, 0)
        self.assertEqual(json.loads(salida)["omitidos_con_transcripcion"], ["auto1"])
        self.assertEqual(len(fake.llamadas), llamadas_antes)


class TestGuardar(CasoBase):
    def preparar_video_con_transcripcion(self, explorador, video_id="v1"):
        explorador.guardar_meta({
            "id": video_id,
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "canal": "Canal A",
            "canal_url": CANAL_A,
            "titulo": "Video v1",
            "fecha": "2026-09-01",
            "estadisticas": {"visualizaciones": 1000},
            "senales": {"multiplo_mediana": 2.5, "interaccion": 0.04, "dias": 43},
        })
        ruta = self.raiz / "biblioteca" / "youtube" / "videos" / video_id / "transcripcion.md"
        ruta.write_text("[00:00] hola, hoy probamos agentes\n", encoding="utf-8")

    def juicio_valido(self):
        return {
            "tema": "Agentes",
            "subtemas": ["agentes en flujos de trabajo", "coste de los agentes"],
            "tesis": "Los agentes ahorran tiempo si se acotan bien.",
            "afirmaciones": [
                {"texto": "El flujo tarda 3 minutos", "marca": "00:00", "tipo": "dato"}
            ],
            "entidades": ["Claude Code"],
            "demuestra": "Un flujo funcionando de principio a fin",
            "promete_sin_demostrar": "Que escala a equipos grandes",
            "preguntas_abiertas": ["¿Cuanto cuesta en tokens?"],
        }

    def test_guardar_relevancia_rechaza_sin_escribir(self):
        self.crear_proyecto(canales_md=f"- {CANAL_A}\n")
        fake = crear_fake(canales={CANAL_A: listado("Canal A", [entrada("v1", 1000)])})
        explorador = self.explorador(fake)
        self.ejecutar(explorador, "cmd_recoger")

        casos = [
            [{"id": "inexistente", "relevante": True, "tema": "T", "motivo": "m"}],
            [{"id": "v1", "relevante": "si", "tema": "T", "motivo": "m"}],
            [{"id": "v1", "relevante": True, "tema": "", "motivo": "m"}],
            [{"id": "v1", "relevante": True, "tema": "T", "motivo": ""}],
            # Una entrada valida junto a una invalida: no se escribe ninguna.
            [
                {"id": "v1", "relevante": True, "tema": "T", "motivo": "m"},
                {"id": "otro", "relevante": True, "tema": "T", "motivo": "m"},
            ],
        ]
        for caso in casos:
            ruta = self.escribir_json("rel.json", caso)
            codigo, _, error = self.ejecutar(explorador, "cmd_guardar_relevancia", ruta)
            self.assertEqual(codigo, 1, caso)
            self.assertNotIn("relevancia", self.meta("v1"), caso)
            self.assertIn("no se escribe nada", error)

    def test_guardar_ficha_rechaza_e_impone_datos_objetivos(self):
        self.crear_proyecto()
        explorador = self.explorador(crear_fake())
        self.preparar_video_con_transcripcion(explorador)
        dir_v1 = self.raiz / "biblioteca" / "youtube" / "videos" / "v1"

        # Invalida: falta la tesis.
        juicio = self.juicio_valido()
        del juicio["tesis"]
        ruta = self.escribir_json("ficha.json", juicio)
        codigo, _, error = self.ejecutar(explorador, "cmd_guardar_ficha", "v1", ruta)
        self.assertEqual(codigo, 1)
        self.assertIn("tesis", error)
        self.assertFalse((dir_v1 / "ficha.json").exists())

        # Invalida: tipo de afirmacion fuera del enum.
        juicio = self.juicio_valido()
        juicio["afirmaciones"][0]["tipo"] = "rumor"
        ruta = self.escribir_json("ficha.json", juicio)
        codigo, _, _ = self.ejecutar(explorador, "cmd_guardar_ficha", "v1", ruta)
        self.assertEqual(codigo, 1)
        self.assertFalse((dir_v1 / "ficha.json").exists())

        # Valida, con datos objetivos falsificados: el script los impone.
        juicio = self.juicio_valido()
        juicio.update({"id": "FALSO", "url": "http://mal", "huella": "0",
                       "senales": {"multiplo_mediana": 999}})
        ruta = self.escribir_json("ficha.json", juicio)
        codigo, salida, _ = self.ejecutar(explorador, "cmd_guardar_ficha", "v1", ruta)
        self.assertEqual(codigo, 0)
        self.assertIn("ignorados", salida)
        ficha = json.loads((dir_v1 / "ficha.json").read_text(encoding="utf-8"))
        self.assertEqual(ficha["id"], "v1")
        self.assertEqual(ficha["url"], "https://www.youtube.com/watch?v=v1")
        self.assertEqual(ficha["autor"], "Canal A")
        self.assertEqual(ficha["fuente"], "youtube")
        self.assertEqual(ficha["senales"]["multiplo_mediana"], 2.5)
        self.assertEqual(ficha["huella"], explorador.huella_transcripcion("v1"))

        # pendientes-ficha: al dia tras guardar; pendiente si cambia la huella.
        _, salida, _ = self.ejecutar(explorador, "cmd_pendientes_ficha")
        self.assertEqual(json.loads(salida)["pendientes"], [])
        (dir_v1 / "transcripcion.md").write_text("[00:00] otro texto\n", encoding="utf-8")
        _, salida, _ = self.ejecutar(explorador, "cmd_pendientes_ficha")
        pendientes = json.loads(salida)["pendientes"]
        self.assertEqual(pendientes[0]["id"], "v1")
        self.assertIn("huella distinta", pendientes[0]["motivo"])

    def test_guardar_ficha_valida_subtemas(self):
        self.crear_proyecto()
        explorador = self.explorador(crear_fake())
        self.preparar_video_con_transcripcion(explorador)
        dir_v1 = self.raiz / "biblioteca" / "youtube" / "videos" / "v1"

        # Sin subtemas: se rechaza sin escribir.
        juicio = self.juicio_valido()
        del juicio["subtemas"]
        ruta = self.escribir_json("ficha.json", juicio)
        codigo, _, error = self.ejecutar(explorador, "cmd_guardar_ficha", "v1", ruta)
        self.assertEqual(codigo, 1)
        self.assertIn("subtemas", error)
        self.assertFalse((dir_v1 / "ficha.json").exists())

        # Mas de 6 subtemas: se rechaza.
        juicio = self.juicio_valido()
        juicio["subtemas"] = [f"subtema {i}" for i in range(7)]
        ruta = self.escribir_json("ficha.json", juicio)
        codigo, _, error = self.ejecutar(explorador, "cmd_guardar_ficha", "v1", ruta)
        self.assertEqual(codigo, 1)
        self.assertIn("subtemas", error)
        self.assertFalse((dir_v1 / "ficha.json").exists())

        # Lista vacia: se rechaza.
        juicio = self.juicio_valido()
        juicio["subtemas"] = []
        ruta = self.escribir_json("ficha.json", juicio)
        codigo, _, _ = self.ejecutar(explorador, "cmd_guardar_ficha", "v1", ruta)
        self.assertEqual(codigo, 1)
        self.assertFalse((dir_v1 / "ficha.json").exists())

        # Valida: los subtemas quedan en la ficha guardada.
        ruta = self.escribir_json("ficha.json", self.juicio_valido())
        codigo, _, _ = self.ejecutar(explorador, "cmd_guardar_ficha", "v1", ruta)
        self.assertEqual(codigo, 0)
        ficha = json.loads((dir_v1 / "ficha.json").read_text(encoding="utf-8"))
        self.assertEqual(
            ficha["subtemas"],
            ["agentes en flujos de trabajo", "coste de los agentes"],
        )

    def test_pendientes_ficha_devuelve_subtemas_existentes(self):
        self.crear_proyecto()
        explorador = self.explorador(crear_fake())

        # Fichas propias de Substack con subtemas (uno repetido).
        dir_fichas = self.raiz / "biblioteca" / "substack" / "fichas"
        dir_fichas.mkdir(parents=True)
        (dir_fichas / "1.json").write_text(
            json.dumps({"id": "1", "subtemas": ["coste de los agentes", "evaluación de modelos"]}),
            encoding="utf-8",
        )
        (dir_fichas / "2.json").write_text(
            json.dumps({"id": "2", "subtemas": ["coste de los agentes"]}),
            encoding="utf-8",
        )

        # Una ficha de video guardada aporta tambien sus subtemas.
        self.preparar_video_con_transcripcion(explorador, "v1")
        ruta = self.escribir_json("ficha.json", self.juicio_valido())
        codigo, _, _ = self.ejecutar(explorador, "cmd_guardar_ficha", "v1", ruta)
        self.assertEqual(codigo, 0)
        # Y otro video con transcripcion queda pendiente de ficha.
        self.preparar_video_con_transcripcion(explorador, "v2")

        codigo, salida, _ = self.ejecutar(explorador, "cmd_pendientes_ficha")
        self.assertEqual(codigo, 0)
        datos = json.loads(salida)
        self.assertEqual([p["id"] for p in datos["pendientes"]], ["v2"])
        # Frecuencias: propias (2+1) + ficha de video (1+1), de mas a menos.
        self.assertEqual(
            datos["subtemas_existentes"],
            {
                "coste de los agentes": 3,
                "agentes en flujos de trabajo": 1,
                "evaluación de modelos": 1,
            },
        )
        # El orden tambien cuenta: primero el mas frecuente.
        self.assertEqual(
            list(datos["subtemas_existentes"]),
            ["coste de los agentes", "agentes en flujos de trabajo", "evaluación de modelos"],
        )

    def test_guardar_ficha_sin_transcripcion(self):
        self.crear_proyecto()
        explorador = self.explorador(crear_fake())
        explorador.guardar_meta({
            "id": "v9", "url": "https://www.youtube.com/watch?v=v9",
            "canal": "Canal A", "canal_url": CANAL_A, "estadisticas": {},
        })
        ruta = self.escribir_json("ficha.json", self.juicio_valido())
        codigo, _, error = self.ejecutar(explorador, "cmd_guardar_ficha", "v9", ruta)
        self.assertEqual(codigo, 1)
        self.assertIn("transcripcion", error)


class TestMapa(CasoBase):
    def preparar_mapa(self):
        self.crear_proyecto()
        explorador = self.explorador(crear_fake())
        base = self.raiz / "biblioteca" / "youtube" / "videos"

        def video(video_id, titulo, fecha, canal, senales):
            explorador.guardar_meta({
                "id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "canal": canal,
                "canal_url": CANAL_A,
                "titulo": titulo,
                "fecha": fecha,
                "estadisticas": {"visualizaciones": 1000},
                "senales": senales,
            })

        senales = {"multiplo_mediana": 2.5, "interes": "alto", "dias": 40,
                   "interaccion": 0.04}
        # Dos videos con ficha al dia, en dos temas.
        for video_id, titulo, fecha, tema in (
            ("m1", "Agentes en produccion", "2026-09-01", "Agentes"),
            ("m2", "Benchmarks que enganan", "2026-09-05", "Evaluacion"),
        ):
            video(video_id, titulo, fecha, "Canal A", senales)
            (base / video_id / "transcripcion.md").write_text(
                f"[00:00] contenido de {video_id}\n", encoding="utf-8"
            )
            ficha = {
                "id": video_id,
                "tema": tema,
                "tesis": f"Tesis de {video_id}.",
                "demuestra": f"Demo de {video_id} funcionando.",
                "promete_sin_demostrar": f"Promesa de {video_id}.",
                "preguntas_abiertas": [f"¿Pregunta de {video_id}?"],
                "huella": explorador.huella_transcripcion(video_id),
            }
            (base / video_id / "ficha.json").write_text(
                json.dumps(ficha, ensure_ascii=False), encoding="utf-8"
            )
        # Con transcripcion y sin ficha.
        video("m3", "Pendiente de ficha", "2026-09-10", "Canal B", senales)
        (base / "m3" / "transcripcion.md").write_text("[00:00] hola\n", encoding="utf-8")
        # Marcado sin subtitulos.
        video("m4", "Sin subtitulos", "2026-09-12", "Canal B", senales)
        meta4 = explorador.cargar_meta("m4")
        meta4["subtitulos"] = {"disponibles": False, "motivo": "sin subtitulos manuales ni automaticos en es, en"}
        explorador.guardar_meta(meta4)
        return explorador

    def test_mapa_determinista_con_contenido_y_pendientes(self):
        explorador = self.preparar_mapa()
        ruta_mapa = self.raiz / "biblioteca" / "youtube" / "mapa-videos.md"

        codigo, salida, _ = self.ejecutar(explorador, "cmd_mapa")
        self.assertEqual(codigo, 0)
        self.assertIn("mapa-videos.md", salida)
        bytes1 = ruta_mapa.read_bytes()
        codigo, _, _ = self.ejecutar(explorador, "cmd_mapa")
        self.assertEqual(codigo, 0)
        self.assertEqual(bytes1, ruta_mapa.read_bytes())  # determinista

        texto = bytes1.decode("utf-8")
        # Cabecera: fecha, fichas y videos sin ficha.
        self.assertIn("Generado el 2026-10-14 a partir de 2 ficha(s)", texto)
        self.assertIn("Videos recogidos sin ficha: 2", texto)
        # Temas en orden alfabetico, con canales y señales.
        self.assertLess(texto.index("### Agentes"), texto.index("### Evaluacion"))
        self.assertIn("- Canales: Canal A", texto)
        self.assertIn("x2.5 de la mediana · interes alto · 40 dias", texto)
        # Enlace, tesis, demuestra, promete y preguntas de cada ficha.
        self.assertIn("[Agentes en produccion](https://www.youtube.com/watch?v=m1)", texto)
        self.assertIn("Tesis: Tesis de m1.", texto)
        self.assertIn("Demuestra: Demo de m2 funcionando.", texto)
        self.assertIn("Promete sin demostrar: Promesa de m2.", texto)
        self.assertIn("- ¿Pregunta de m1?", texto)
        # Videos candidatos sin ficha todavia, con su motivo.
        self.assertIn("sin ficha todavia", texto)
        self.assertIn("[Pendiente de ficha](https://www.youtube.com/watch?v=m3)", texto)
        self.assertIn("con transcripcion, ficha pendiente", texto)
        self.assertIn("[Sin subtitulos](https://www.youtube.com/watch?v=m4)", texto)
        self.assertIn("sin subtitulos manuales ni automaticos", texto)

    def test_mapa_ignora_ficha_con_huella_desactualizada(self):
        explorador = self.preparar_mapa()
        ruta = self.raiz / "biblioteca" / "youtube" / "videos" / "m1" / "transcripcion.md"
        ruta.write_text("[00:00] la transcripcion cambio\n", encoding="utf-8")
        codigo, _, _ = self.ejecutar(explorador, "cmd_mapa")
        self.assertEqual(codigo, 0)
        texto = (self.raiz / "biblioteca" / "youtube" / "mapa-videos.md").read_text(encoding="utf-8")
        self.assertIn("a partir de 1 ficha(s)", texto)
        self.assertNotIn("Tesis: Tesis de m1.", texto)
        self.assertIn("la transcripcion cambio despues de la ficha", texto)


class TestFormulasTitulo(CasoBase):
    def test_clasifica_titulos_de_ejemplo(self):
        casos = {
            # Una formula distinta por titulo, en español e ingles.
            "El 97% de los que empiezan con IA lo dejan antes de un mes": "La estadística",
            "7 errores que cometes con ChatGPT (y como evitarlos)": "La lista",
            "You don't need ChatGPT Plus: forget the hype": "El giro contrario",
            "Claude vs ChatGPT: cual es mejor para programar": "La comparativa",
            # Sin ningun patron coincidente.
            "Charlamos con Marta sobre su huerto": "sin clasificar",
        }
        for titulo, esperada in casos.items():
            self.assertEqual(ey.clasificar_titulo(titulo), esperada, titulo)
        self.assertEqual(ey.clasificar_titulo(""), "sin clasificar")

    def test_recoger_guarda_formula_en_meta(self):
        self.crear_proyecto(canales_md=f"- {CANAL_A}\n")
        fake = crear_fake(canales={
            CANAL_A: listado("Canal A", [
                entrada("f1", 1000, titulo="5 herramientas de IA que uso cada dia"),
                entrada("f2", 2000, titulo="Charlamos con Marta sobre su huerto"),
            ]),
        })
        codigo, _, _ = self.ejecutar(self.explorador(fake), "cmd_recoger")
        self.assertEqual(codigo, 0)
        self.assertEqual(self.meta("f1")["formula_titulo"], "La lista")
        self.assertEqual(self.meta("f2")["formula_titulo"], "sin clasificar")

    def test_candidatos_muestra_formula_y_recuento_dominantes(self):
        self.crear_proyecto()
        fake = crear_fake(
            canales={
                CANAL_A: listado("Canal A", [
                    entrada("c1", 1000, titulo="Video c1"),
                    entrada("c2", 1000, titulo="Video c2"),
                    entrada("c3", 1000, titulo="Video c3"),
                    # Interes alto (multiplo >= 2 sobre mediana 1000):
                    entrada("c4", 4000, titulo="El 80% de las empresas usa mal la IA"),
                    entrada("c5", 6000, titulo="9 trucos de Claude que nadie cuenta"),
                ]),
            },
            videos={
                "c4": {"upload_date": "20260901", "description": "d",
                       "view_count": 4000, "like_count": 10, "comment_count": 1},
                "c5": {"upload_date": "20260901", "description": "d",
                       "view_count": 6000, "like_count": 10, "comment_count": 1},
            },
        )
        explorador = self.explorador(fake)
        self.ejecutar(explorador, "cmd_recoger")
        ruta = self.escribir_json("rel.json", [
            {"id": "c4", "relevante": True, "tema": "Adopcion", "motivo": "x"},
            {"id": "c5", "relevante": True, "tema": "Trucos", "motivo": "x"},
        ])
        self.ejecutar(explorador, "cmd_guardar_relevancia", ruta)

        codigo, salida, _ = self.ejecutar(explorador, "cmd_candidatos")
        self.assertEqual(codigo, 0)
        datos = json.loads(salida)
        formulas = {c["id"]: c["formula_titulo"] for c in datos["candidatos"]}
        self.assertEqual(formulas["c4"], "La estadística")
        self.assertEqual(formulas["c5"], "La lista")
        # Recuento de formulas dominantes entre los videos con interes alto.
        self.assertEqual(
            datos["formulas_dominantes_interes_alto"],
            {"La estadística": 1, "La lista": 1},
        )

    def test_mapa_incluye_formula_y_seccion_dominantes(self):
        explorador = TestMapa.preparar_mapa(self)
        meta = explorador.cargar_meta("m1")
        meta["titulo"] = "Probe 5 agentes en produccion durante 30 dias"
        explorador.guardar_meta(meta)
        codigo, _, _ = self.ejecutar(explorador, "cmd_mapa")
        self.assertEqual(codigo, 0)
        texto = (self.raiz / "biblioteca" / "youtube" / "mapa-videos.md").read_text(encoding="utf-8")
        self.assertIn("formula: El experimento", texto)
        self.assertIn("## Formulas dominantes entre los videos de interes alto", texto)
        self.assertIn("- El experimento: 1", texto)
        # Honestidad por diseño: el mapa lo dice en la propia seccion.
        self.assertIn("no el porque real del exito", texto)


class TestYtDlpNoDisponible(CasoBase):
    def test_sale_con_2_sin_modificar_nada(self):
        self.crear_proyecto()
        error = io.StringIO()
        with mock.patch.object(
            ey,
            "resolver_comando_ytdlp",
            side_effect=ey.YtDlpNoDisponible(ey.INSTRUCCION_INSTALACION),
        ):
            with contextlib.redirect_stderr(error), contextlib.redirect_stdout(io.StringIO()):
                codigo = ey.main(["recoger", "--raiz", str(self.raiz), "--hoy", "2026-10-14"])
        self.assertEqual(codigo, 2)
        self.assertIn("pip install yt-dlp", error.getvalue())
        base = self.raiz / "biblioteca" / "youtube"
        self.assertFalse((base / "videos").exists())
        self.assertFalse((base / "control").exists())


if __name__ == "__main__":
    unittest.main()
