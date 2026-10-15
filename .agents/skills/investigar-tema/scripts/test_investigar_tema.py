"""Pruebas de investigar_tema.py con una biblioteca ficticia y la red simulada.

Nunca tocan biblioteca/ ni la red: todo ocurre en una carpeta temporal y
pedir_url se sustituye por una función falsa.
"""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import investigar_tema  # noqa: E402

OPORTUNIDAD_ID = "2026-10-10-agentes-que-redactan-notas"

OPORTUNIDAD_ACEPTADA = """---
id: 2026-10-10-agentes-que-redactan-notas
estado: aceptada
motivo_estado: ""
interes: alto
canales: 2
cobertura: nuevo
evidencias: [youtube:vid001@02:10, youtube:vid001@05:30]
relacionados: [substack:post1]
---
## La oportunidad

Agentes que redactan notas de reunión sin revisar.

## Por qué ahora (evidencias)

youtube:vid001@02:10 y youtube:vid001@05:30.

## Qué hemos publicado y qué falta

Publicamos un tutorial básico; falta la parte de verificación.

## Qué aportaríamos

Una prueba propia con actas reales.

## Qué hay que investigar o probar

- Si la herramienta Notaria admite castellano en su versión gratuita.
- Cuánto tarda en procesar una reunión de una hora.

## Riesgos

La herramienta es de pago a partir del plan básico.
"""

FICHA_VID001 = {
    "id": "vid001",
    "fuente": "youtube",
    "url": "https://ejemplo.invalid/watch?v=vid001",
    "autor": "Canal Ficticio",
    "fecha": "2026-09-30",
    "huella": "abc123",
    "tema": "agentes que redactan notas",
    "tesis": "Las notas de reunión se pueden delegar en un agente.",
    "afirmaciones": [
        {"texto": "Notaria transcribe una hora de audio en dos minutos.", "marca": "02:10", "tipo": "dato"},
        {"texto": "El agente publica las notas sin revisión humana.", "marca": "05:30", "tipo": "demostración"},
    ],
    "entidades": ["Notaria"],
    "demuestra": "El flujo completo con una reunión corta.",
    "promete_sin_demostrar": "Que escala a reuniones de una hora.",
    "preguntas_abiertas": [],
    "senales": {"multiplo_mediana": 2.5, "interaccion": 0.03, "dias": 10},
}

FUENTES_VALIDAS = [
    {
        "id": "f1",
        "url": "https://ejemplo.invalid/docs",
        "titulo": "Documentación de Notaria",
        "autor_o_entidad": "Notaria Inc.",
        "tipo": "oficial",
        "fecha": "2026-09-01",
        "consultada": "2026-10-14",
        "respalda": ["a1"],
        "contradice": [],
        "nota": "La documentación indica que una hora de audio se procesa en unos dos minutos.",
    },
    {
        "id": "f2",
        "url": "https://ejemplo.invalid/watch?v=vid001",
        "titulo": "Vídeo de origen",
        "autor_o_entidad": "Canal Ficticio",
        "tipo": "vídeo",
        "fecha": "2026-09-30",
        "consultada": "2026-10-14",
        "respalda": ["a2"],
        "contradice": [],
        "nota": "Muestra el flujo con una reunión corta.",
    },
]


def cuerpo_investigacion(filas: str) -> str:
    return f"""## Pregunta de investigación

¿Se pueden delegar las notas de reunión en un agente sin revisión humana?

## Resumen

La transcripción rápida está documentada; la publicación sin revisión solo
aparece en el vídeo de origen.

## Verificación de afirmaciones

| ID | Afirmación | Estado | Fuentes | Nota |
|---|---|---|---|---|
{filas}

## Hallazgos nuevos

La documentación [f1] añade un límite de 90 minutos por archivo.

## Contradicciones y límites

Nadie independiente ha medido el tiempo real de procesado.

## Prueba práctica

Procesar una reunión propia de una hora y cronometrar; confirma si tarda
menos de cinco minutos.

## Ángulo propuesto

Probar el flujo completo en castellano y contar qué revisa una persona.

## Fuentes

[f1] Documentación de Notaria, Notaria Inc., 2026-09-01, https://ejemplo.invalid/docs
[f2] Vídeo de origen, Canal Ficticio, 2026-09-30, https://ejemplo.invalid/watch?v=vid001
"""


FILAS_VALIDAS = """| a1 | Transcribe una hora en dos minutos | verificada | f1, f2 | La documentación lo confirma |
| a2 | Publica sin revisión humana | sin_confirmar | — | Solo el vídeo lo muestra |
| a3 | Admite castellano en el plan gratuito | sin_confirmar | — | La documentación no lo dice |
| a4 | Tiempo para una reunión de una hora | sin_confirmar | — | Pendiente de prueba propia |"""


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.raiz = Path(self._tmp.name)
        self.config = self.raiz / "proyecto.config.json"
        self.config.write_text(json.dumps({
            "linea_editorial": {"nicho": "IA aplicada", "audiencia": "pro", "aportacion": "probar"},
            "red": {"timeout_segundos": 1, "intentos": 2, "pausa_segundos": 0},
        }), encoding="utf-8")
        biblioteca = self.raiz / "biblioteca"
        (biblioteca / "oportunidades").mkdir(parents=True)
        (biblioteca / "oportunidades" / f"{OPORTUNIDAD_ID}.md").write_text(
            OPORTUNIDAD_ACEPTADA, encoding="utf-8"
        )
        (biblioteca / "oportunidades" / "2026-10-11-otra.md").write_text(
            OPORTUNIDAD_ACEPTADA.replace("estado: aceptada", "estado: propuesta")
            .replace(OPORTUNIDAD_ID, "2026-10-11-otra"),
            encoding="utf-8",
        )
        carpeta_video = biblioteca / "youtube" / "videos" / "vid001"
        carpeta_video.mkdir(parents=True)
        (carpeta_video / "ficha.json").write_text(
            json.dumps(FICHA_VID001, ensure_ascii=False), encoding="utf-8"
        )
        (biblioteca / "substack" / "control").mkdir(parents=True)
        (biblioteca / "substack" / "articulos").mkdir(parents=True)
        articulo = biblioteca / "substack" / "articulos" / "2026-01-01-tutorial.md"
        articulo.write_text("# Tutorial básico\n", encoding="utf-8")
        (biblioteca / "substack" / "control" / "inventario.json").write_text(
            json.dumps({"post1": {"archivo": str(articulo)}}), encoding="utf-8"
        )
        self.contenido = biblioteca / "contenidos" / OPORTUNIDAD_ID

    def correr(self, *args) -> tuple[int, str, str]:
        salida, errores = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(errores):
            codigo = investigar_tema.main(
                ["--config", str(self.config), "--hoy", "2026-10-14", *args]
            )
        return codigo, salida.getvalue(), errores.getvalue()

    def escribir_archivo(self, nombre: str, contenido) -> Path:
        ruta = self.raiz / nombre
        if isinstance(contenido, str):
            ruta.write_text(contenido, encoding="utf-8")
        else:
            ruta.write_text(json.dumps(contenido, ensure_ascii=False), encoding="utf-8")
        return ruta

    def preparar_hasta_fuentes(self):
        self.correr("preparar", OPORTUNIDAD_ID)
        archivo = self.escribir_archivo("fuentes.json", FUENTES_VALIDAS)
        codigo, _, errores = self.correr("guardar-fuentes", OPORTUNIDAD_ID, str(archivo))
        self.assertEqual(codigo, 0, errores)


class TestPreparar(Base):
    def test_rechaza_oportunidad_no_aceptada(self):
        codigo, _, errores = self.correr("preparar", "2026-10-11-otra")
        self.assertEqual(codigo, 2)
        self.assertIn("propuesta", errores)
        self.assertFalse((self.raiz / "biblioteca" / "contenidos" / "2026-10-11-otra").exists())

    def test_rechaza_oportunidad_inexistente(self):
        codigo, _, errores = self.correr("preparar", "no-existe")
        self.assertEqual(codigo, 2)
        self.assertIn("no existe", errores)

    def test_extrae_afirmaciones_con_ids_estables(self):
        codigo, salida, _ = self.correr("preparar", OPORTUNIDAD_ID)
        self.assertEqual(codigo, 0)
        paquete = json.loads(salida)
        afirmaciones = paquete["afirmaciones"]
        self.assertEqual([a["id"] for a in afirmaciones], ["a1", "a2", "a3", "a4"])
        self.assertEqual(afirmaciones[0]["origen"], "youtube:vid001@02:10")
        self.assertEqual(afirmaciones[0]["texto"], "Notaria transcribe una hora de audio en dos minutos.")
        self.assertEqual(afirmaciones[1]["tipo"], "demostración")
        self.assertEqual(afirmaciones[2]["origen"], f"oportunidad:{OPORTUNIDAD_ID}")
        self.assertEqual(afirmaciones[2]["tipo"], "a_comprobar")
        self.assertEqual(paquete["fichas_citadas"][0]["id"], "vid001")
        self.assertTrue(paquete["articulos_relacionados"][0]["ruta_texto"].endswith("2026-01-01-tutorial.md"))
        # Repetir produce los mismos IDs.
        guardadas = json.loads((self.contenido / "afirmaciones.json").read_text(encoding="utf-8"))
        codigo, salida, _ = self.correr("preparar", OPORTUNIDAD_ID)
        self.assertEqual(codigo, 0)
        self.assertEqual(json.loads(salida)["afirmaciones"], guardadas)

    def test_no_sobrescribe_investigacion_existente(self):
        self.correr("preparar", OPORTUNIDAD_ID)
        ruta = self.contenido / "investigacion.md"
        ruta.write_text("---\nestado: pendiente_aprobacion\n---\nTexto previo\n", encoding="utf-8")
        afirmaciones_previas = (self.contenido / "afirmaciones.json").read_text(encoding="utf-8")
        codigo, salida, errores = self.correr("preparar", OPORTUNIDAD_ID)
        self.assertEqual(codigo, 1)
        self.assertIn("ya existe una investigación", errores)
        self.assertTrue(json.loads(salida)["investigacion_existente"])
        self.assertIn("Texto previo", ruta.read_text(encoding="utf-8"))
        self.assertEqual((self.contenido / "afirmaciones.json").read_text(encoding="utf-8"),
                         afirmaciones_previas)


class TestGuardarFuentes(Base):
    def test_guarda_fuentes_validas(self):
        self.preparar_hasta_fuentes()
        fuentes = json.loads((self.contenido / "fuentes.json").read_text(encoding="utf-8"))
        self.assertEqual([f["id"] for f in fuentes], ["f1", "f2"])

    def test_rechaza_ids_duplicados_en_el_archivo(self):
        self.correr("preparar", OPORTUNIDAD_ID)
        repetidas = [FUENTES_VALIDAS[0], dict(FUENTES_VALIDAS[1], id="f1")]
        archivo = self.escribir_archivo("fuentes.json", repetidas)
        codigo, _, errores = self.correr("guardar-fuentes", OPORTUNIDAD_ID, str(archivo))
        self.assertEqual(codigo, 2)
        self.assertIn("duplicado", errores)
        self.assertFalse((self.contenido / "fuentes.json").exists())

    def test_rechaza_afirmacion_inexistente(self):
        self.correr("preparar", OPORTUNIDAD_ID)
        malas = [dict(FUENTES_VALIDAS[0], respalda=["a99"])]
        archivo = self.escribir_archivo("fuentes.json", malas)
        codigo, _, errores = self.correr("guardar-fuentes", OPORTUNIDAD_ID, str(archivo))
        self.assertEqual(codigo, 2)
        self.assertIn("a99", errores)

    def test_conserva_las_fuentes_anteriores_al_anadir(self):
        self.preparar_hasta_fuentes()
        nueva = [dict(FUENTES_VALIDAS[0], id="f3", url="https://ejemplo.invalid/otro",
                      titulo="Otra fuente")]
        archivo = self.escribir_archivo("mas-fuentes.json", nueva)
        codigo, _, errores = self.correr("guardar-fuentes", OPORTUNIDAD_ID, str(archivo))
        self.assertEqual(codigo, 0, errores)
        fuentes = json.loads((self.contenido / "fuentes.json").read_text(encoding="utf-8"))
        self.assertEqual([f["id"] for f in fuentes], ["f1", "f2", "f3"])
        # Y rechaza un id que ya estaba guardado.
        archivo = self.escribir_archivo("repetida.json", [dict(FUENTES_VALIDAS[0])])
        codigo, _, errores = self.correr("guardar-fuentes", OPORTUNIDAD_ID, str(archivo))
        self.assertEqual(codigo, 2)
        self.assertIn("ya existe", errores)


class TestComprobarEnlaces(Base):
    def test_registra_codigo_y_conserva_la_fuente_rota(self):
        self.preparar_hasta_fuentes()
        respuestas = {"https://ejemplo.invalid/docs": (200, None),
                      "https://ejemplo.invalid/watch?v=vid001": (404, None)}
        original = investigar_tema.pedir_url
        investigar_tema.pedir_url = lambda url, timeout: respuestas[url]
        try:
            codigo, salida, errores = self.correr("comprobar-enlaces", OPORTUNIDAD_ID)
        finally:
            investigar_tema.pedir_url = original
        self.assertEqual(codigo, 1)
        self.assertIn("enlace roto", errores)
        fuentes = json.loads((self.contenido / "fuentes.json").read_text(encoding="utf-8"))
        self.assertEqual(len(fuentes), 2)  # no se borra ninguna
        self.assertEqual(fuentes[0]["comprobacion"], {"codigo": 200, "fecha": "2026-10-14"})
        self.assertEqual(fuentes[1]["comprobacion"]["codigo"], 404)
        self.assertEqual(json.loads(salida)["enlaces_rotos"], 1)

    def test_reintenta_ante_errores_de_red(self):
        self.preparar_hasta_fuentes()
        intentos = []
        def falsa(url, timeout):
            intentos.append(url)
            return (None, "timeout") if len(intentos) == 1 else (200, None)
        original = investigar_tema.pedir_url
        investigar_tema.pedir_url = falsa
        try:
            codigo, _, _ = self.correr("comprobar-enlaces", OPORTUNIDAD_ID)
        finally:
            investigar_tema.pedir_url = original
        self.assertEqual(codigo, 0)
        self.assertEqual(len(intentos), 3)  # 2 para la primera URL, 1 para la segunda


class TestGuardarInvestigacion(Base):
    def guardar(self, cuerpo: str) -> tuple[int, str, str]:
        archivo = self.escribir_archivo("investigacion.md", cuerpo)
        return self.correr("guardar-investigacion", OPORTUNIDAD_ID, str(archivo))

    def test_guarda_una_investigacion_valida(self):
        self.preparar_hasta_fuentes()
        codigo, salida, errores = self.guardar(cuerpo_investigacion(FILAS_VALIDAS))
        self.assertEqual(codigo, 0, errores)
        texto = (self.contenido / "investigacion.md").read_text(encoding="utf-8")
        self.assertTrue(texto.startswith(
            f"---\noportunidad: {OPORTUNIDAD_ID}\nestado: pendiente_aprobacion\nfecha: 2026-10-14\n---"
        ))
        resumen = json.loads(salida)
        self.assertEqual(resumen["afirmaciones"],
                         {"verificada": 1, "refutada": 0, "sin_confirmar": 3})

    def test_rechaza_seccion_ausente(self):
        self.preparar_hasta_fuentes()
        cuerpo = cuerpo_investigacion(FILAS_VALIDAS).replace("## Prueba práctica", "## Otra cosa")
        codigo, _, errores = self.guardar(cuerpo)
        self.assertEqual(codigo, 2)
        self.assertIn("falta la sección '## Prueba práctica'", errores)
        self.assertFalse((self.contenido / "investigacion.md").exists())

    def test_rechaza_afirmacion_sin_estado(self):
        self.preparar_hasta_fuentes()
        filas = "\n".join(FILAS_VALIDAS.splitlines()[:-1])  # quita la fila de a4
        codigo, _, errores = self.guardar(cuerpo_investigacion(filas))
        self.assertEqual(codigo, 2)
        self.assertIn("'a4' no aparece", errores)
        filas_mal = FILAS_VALIDAS.replace("| verificada |", "| casi segura |")
        codigo, _, errores = self.guardar(cuerpo_investigacion(filas_mal))
        self.assertEqual(codigo, 2)
        self.assertIn("casi segura", errores)

    def test_rechaza_verificada_solo_con_el_video_de_origen(self):
        self.preparar_hasta_fuentes()
        filas = FILAS_VALIDAS.replace("| verificada | f1, f2 |", "| verificada | f2 |")
        codigo, _, errores = self.guardar(cuerpo_investigacion(filas))
        self.assertEqual(codigo, 2)
        self.assertIn("tipo vídeo", errores)
        self.assertFalse((self.contenido / "investigacion.md").exists())

    def test_rechaza_referencia_inexistente(self):
        self.preparar_hasta_fuentes()
        cuerpo = cuerpo_investigacion(FILAS_VALIDAS).replace(
            "La documentación [f1]", "La documentación [f9]"
        )
        codigo, _, errores = self.guardar(cuerpo)
        self.assertEqual(codigo, 2)
        self.assertIn("[f9]", errores)

    def test_nunca_sobrescribe_una_investigacion_aprobada(self):
        self.preparar_hasta_fuentes()
        codigo, _, _ = self.guardar(cuerpo_investigacion(FILAS_VALIDAS))
        self.assertEqual(codigo, 0)
        ruta = self.contenido / "investigacion.md"
        aprobada = ruta.read_text(encoding="utf-8").replace(
            "estado: pendiente_aprobacion", "estado: aprobada"
        )
        ruta.write_text(aprobada, encoding="utf-8")
        codigo, _, errores = self.guardar(cuerpo_investigacion(FILAS_VALIDAS))
        self.assertEqual(codigo, 2)
        self.assertIn("aprobada", errores)
        self.assertEqual(ruta.read_text(encoding="utf-8"), aprobada)

    def test_permite_corregir_una_pendiente(self):
        self.preparar_hasta_fuentes()
        self.guardar(cuerpo_investigacion(FILAS_VALIDAS))
        cuerpo = cuerpo_investigacion(FILAS_VALIDAS).replace(
            "90 minutos", "120 minutos"
        )
        codigo, _, errores = self.guardar(cuerpo)
        self.assertEqual(codigo, 0, errores)
        self.assertIn("120 minutos", (self.contenido / "investigacion.md").read_text(encoding="utf-8"))


class TestGuardarRevision(Base):
    def test_guarda_el_informe(self):
        self.preparar_hasta_fuentes()
        archivo = self.escribir_archivo("revision.md", "# Revisión\n\n## Veredicto\n\nsin objeciones\n")
        codigo, _, errores = self.correr("guardar-revision", OPORTUNIDAD_ID, str(archivo))
        self.assertEqual(codigo, 0, errores)
        self.assertIn("sin objeciones", (self.contenido / "revision.md").read_text(encoding="utf-8"))

    def test_rechaza_informe_vacio(self):
        self.preparar_hasta_fuentes()
        archivo = self.escribir_archivo("revision.md", "   \n")
        codigo, _, errores = self.correr("guardar-revision", OPORTUNIDAD_ID, str(archivo))
        self.assertEqual(codigo, 2)
        self.assertIn("vacío", errores)


if __name__ == "__main__":
    unittest.main()
