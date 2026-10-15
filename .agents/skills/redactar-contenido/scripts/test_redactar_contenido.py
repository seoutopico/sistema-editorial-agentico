"""Pruebas de redactar_contenido.py con un contenido ficticio en una carpeta
temporal: oportunidad, investigación aprobada, fuentes, estilo.md e inventario.
Nunca tocan biblioteca/ ni la red."""

from __future__ import annotations

import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import redactar_contenido
from redactar_contenido import main

OPORTUNIDAD_ID = "2026-10-20-agentes-investigacion"

INVESTIGACION = """\
---
oportunidad: 2026-10-20-agentes-investigacion
estado: aprobada
fecha: 2026-10-21
---
## Pregunta de investigación

¿Sirven los agentes para automatizar la investigación editorial?

## Resumen

Los agentes preparan material útil, pero la promesa de publicar sin revisar
quedó refutada.

## Verificación de afirmaciones

| ID | Afirmación | Estado | Fuentes | Nota |
|---|---|---|---|---|
| a1 | Los agentes reducen el tiempo de documentación | verificada | f1 | La documentación oficial lo mide |
| a2 | Se puede publicar sin revisión humana | refutada | f2 | El estudio muestra errores graves |
| a3 | Funciona igual en castellano | sin_confirmar | — | Sin fuente independiente |

## Hallazgos nuevos

La documentación oficial detalla los límites del modo autónomo [f1].

## Contradicciones y límites

Lo que promete el vídeo no coincide con el estudio [f2].

## Prueba práctica

Probamos el flujo con nuestra propia biblioteca y medimos el tiempo.

## Ángulo propuesto

Prueba propia con el proceso real, con lo que funcionó y lo que no.

## Fuentes

[f1] Documentación de Agentes SA, AgentesSA, 2026-09-01, https://docs.ejemplo.dev/agentes
[f2] Estudio de errores, Universidad Ejemplo, 2026-08-15, https://uni.ejemplo.edu/estudio
"""

FUENTES = [
    {
        "id": "f1", "url": "https://docs.ejemplo.dev/agentes",
        "titulo": "Documentación de AgentesSA", "autor_o_entidad": "AgentesSA",
        "tipo": "oficial", "fecha": "2026-09-01", "consultada": "2026-10-21",
        "respalda": ["a1"], "contradice": [],
        "nota": "Mide la reducción de tiempo de documentación.",
    },
    {
        "id": "f2", "url": "https://uni.ejemplo.edu/estudio",
        "titulo": "Estudio de errores", "autor_o_entidad": "Universidad Ejemplo",
        "tipo": "paper", "fecha": "2026-08-15", "consultada": "2026-10-21",
        "respalda": [], "contradice": ["a2"],
        "nota": "Documenta errores graves al publicar sin revisión.",
    },
    {
        "id": "f3", "url": "https://blog.ejemplo.net/promesa",
        "titulo": "Publica sin revisar", "autor_o_entidad": "Blog Ejemplo",
        "tipo": "blog", "fecha": "2026-07-01", "consultada": "2026-10-21",
        "respalda": ["a2"], "contradice": [],
        "nota": "Solo respalda la afirmación refutada a2.",
    },
]

OPORTUNIDAD = """\
---
id: 2026-10-20-agentes-investigacion
estado: aceptada
relacionados: [substack:101]
---
## La oportunidad

Agentes que investigan solos.
"""

ESTILO = """\
# Voz de la publicación

Tono directo, primera persona, ejemplos propios.

## Reglas aprendidas

- No abrir con una pregunta retórica.
"""


def crear_biblioteca_ficticia(raiz: Path):
    """Config, oportunidad, investigación aprobada, fuentes, estilo e inventario."""
    (raiz / "proyecto.config.json").write_text(json.dumps({
        "publicacion": {
            "nombre": "Ejemplo", "substack": "https://ejemplo.substack.com", "idioma": "es",
        },
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    dir_oportunidades = raiz / "biblioteca" / "oportunidades"
    dir_oportunidades.mkdir(parents=True)
    (dir_oportunidades / f"{OPORTUNIDAD_ID}.md").write_text(OPORTUNIDAD, encoding="utf-8")

    carpeta = raiz / "biblioteca" / "contenidos" / OPORTUNIDAD_ID
    carpeta.mkdir(parents=True)
    (carpeta / "investigacion.md").write_text(INVESTIGACION, encoding="utf-8")
    (carpeta / "fuentes.json").write_text(
        json.dumps(FUENTES, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    (raiz / "biblioteca" / "estilo.md").write_text(ESTILO, encoding="utf-8")

    # Inventario con artículos completos de 80, 100 y 120 palabras: mediana 100.
    dir_control = raiz / "biblioteca" / "substack" / "control"
    dir_control.mkdir(parents=True)
    dir_articulos = raiz / "biblioteca" / "substack" / "articulos"
    dir_articulos.mkdir(parents=True)
    inventario = {}
    for post_id, palabras in (("101", 80), ("102", 100), ("103", 120)):
        nombre = f"2026-09-0{int(post_id) - 100}-articulo-{post_id}.md"
        inventario[post_id] = {
            "id": post_id,
            "url": f"https://ejemplo.substack.com/p/articulo-{post_id}",
            "titulo": f"Artículo {post_id}",
            "fecha": f"2026-09-0{int(post_id) - 100}",
            "estado": "completo",
            "huella": f"h{post_id}",
            "archivo": f"biblioteca/substack/articulos/{nombre}",
        }
        cuerpo = " ".join(["palabra"] * palabras)
        (dir_articulos / nombre).write_text(
            f"---\nid: {post_id}\n---\n{cuerpo}\n", encoding="utf-8"
        )
    (dir_control / "inventario.json").write_text(
        json.dumps(inventario, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def texto_modelo(extra: str = "", palabras_relleno: int = 60) -> str:
    """Un texto válido de unas 100 palabras, con citas, enlace interno y fuentes."""
    relleno = " ".join(["palabra"] * palabras_relleno)
    return f"""\
---
titulo: Probamos los agentes que investigan solos
titulos_alternativos: [Agentes a prueba, Lo que los agentes no hacen solos]
---
Los agentes reducen el tiempo de documentación [f1]. La promesa de publicar
sin revisión humana quedó refutada por el estudio [f2]. Ya contamos algo
parecido en [nuestro artículo](https://ejemplo.substack.com/p/articulo-101).
{extra}

{relleno}

## Fuentes

[f1] Documentación de AgentesSA, AgentesSA, 2026-09-01, https://docs.ejemplo.dev/agentes
[f2] Estudio de errores, Universidad Ejemplo, 2026-08-15, https://uni.ejemplo.edu/estudio
"""


class PruebaBase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="redactar-")
        self.raiz = Path(self._tmp)
        self.addCleanup(shutil.rmtree, self._tmp, True)
        crear_biblioteca_ficticia(self.raiz)
        self.carpeta = self.raiz / "biblioteca" / "contenidos" / OPORTUNIDAD_ID
        self.ruta_principal = self.carpeta / "principal.md"
        self.ruta_borrador = self.carpeta / "principal.borrador.md"

    def ejecutar(self, *argumentos: str) -> tuple[int, str, str]:
        salida, errores = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(errores):
            codigo = main([
                "--config", str(self.raiz / "proyecto.config.json"),
                "--hoy", "2026-10-22", *argumentos,
            ])
        return codigo, salida.getvalue(), errores.getvalue()

    def escribir_borrador_modelo(self, contenido: str) -> Path:
        ruta = self.raiz / "borrador-modelo.md"
        ruta.write_text(contenido, encoding="utf-8")
        return ruta

    def guardar_valido(self, *extra: str) -> tuple[int, str, str]:
        ruta = self.escribir_borrador_modelo(texto_modelo())
        return self.ejecutar("guardar", OPORTUNIDAD_ID, str(ruta), *extra)


class PruebaPreparar(PruebaBase):
    def test_rechaza_una_investigacion_no_aprobada(self):
        ruta = self.carpeta / "investigacion.md"
        ruta.write_text(
            ruta.read_text(encoding="utf-8").replace(
                "estado: aprobada", "estado: pendiente_aprobacion"
            ),
            encoding="utf-8",
        )
        codigo, _, errores = self.ejecutar("preparar", OPORTUNIDAD_ID)
        self.assertEqual(codigo, 2)
        self.assertIn("pendiente_aprobacion", errores)
        self.assertIn("aprobada", errores)

    def test_devuelve_rutas_metricas_y_relacionados(self):
        codigo, salida, _ = self.ejecutar("preparar", OPORTUNIDAD_ID)
        self.assertEqual(codigo, 0)
        paquete = json.loads(salida)
        self.assertTrue(paquete["rutas"]["investigacion"].endswith("investigacion.md"))
        self.assertTrue(paquete["estilo_existe"])
        self.assertEqual(paquete["metricas_estilo"]["palabras"]["mediana"], 100)
        self.assertEqual(
            paquete["articulos_relacionados"],
            [{
                "referencia": "substack:101",
                "titulo": "Artículo 101",
                "url": "https://ejemplo.substack.com/p/articulo-101",
            }],
        )

    def test_avisa_si_no_existe_estilo(self):
        (self.raiz / "biblioteca" / "estilo.md").unlink()
        codigo, _, errores = self.ejecutar("preparar", OPORTUNIDAD_ID)
        self.assertEqual(codigo, 1)
        self.assertIn("estilo.md", errores)
        self.assertIn("analizar-biblioteca", errores)


class PruebaGuardar(PruebaBase):
    def test_rechaza_cita_inexistente_y_enlace_fuera_del_inventario(self):
        ruta = self.escribir_borrador_modelo(texto_modelo(
            extra="Un dato inventado [f9] y [otro artículo]"
                  "(https://ejemplo.substack.com/p/no-existe)."
        ))
        codigo, _, errores = self.ejecutar("guardar", OPORTUNIDAD_ID, str(ruta))
        self.assertEqual(codigo, 2)
        self.assertIn("[f9]", errores)
        self.assertIn("no-existe", errores)
        self.assertFalse(self.ruta_principal.exists())
        self.assertFalse(self.ruta_borrador.exists())

    def test_rechaza_fuente_que_solo_respalda_refutadas(self):
        ruta = self.escribir_borrador_modelo(texto_modelo(
            extra="Según el blog, se puede publicar sin revisar [f3]."
        ))
        codigo, _, errores = self.ejecutar("guardar", OPORTUNIDAD_ID, str(ruta))
        self.assertEqual(codigo, 2)
        self.assertIn("[f3]", errores)
        self.assertIn("refutadas", errores)
        self.assertFalse(self.ruta_principal.exists())

    def test_avisa_de_longitud_fuera_de_rango_sin_rechazar(self):
        ruta = self.escribir_borrador_modelo(texto_modelo(palabras_relleno=0))
        codigo, salida, errores = self.ejecutar("guardar", OPORTUNIDAD_ID, str(ruta))
        self.assertEqual(codigo, 1)
        self.assertIn("60-140", errores.replace(" ", " "))
        self.assertTrue(self.ruta_principal.is_file())
        avisos = json.loads(salida)["avisos"]
        self.assertTrue(any("fuera del rango" in a for a in avisos))

    def test_crea_principal_y_borrador_identicos_con_encabezado_del_script(self):
        codigo, _, _ = self.guardar_valido()
        self.assertEqual(codigo, 0)
        principal = self.ruta_principal.read_text(encoding="utf-8")
        self.assertEqual(principal, self.ruta_borrador.read_text(encoding="utf-8"))
        encabezado, cuerpo = redactar_contenido.parsear_frontmatter(principal)
        self.assertEqual(encabezado["oportunidad"], OPORTUNIDAD_ID)
        self.assertEqual(encabezado["estado"], "borrador")
        self.assertEqual(encabezado["fecha"], "2026-10-22")
        self.assertEqual(
            encabezado["titulos_alternativos"],
            ["Agentes a prueba", "Lo que los agentes no hacen solos"],
        )
        self.assertTrue(cuerpo.startswith("# Probamos los agentes que investigan solos"))

    def test_no_toca_un_principal_aprobado(self):
        self.guardar_valido()
        aprobado = self.ruta_principal.read_text(encoding="utf-8").replace(
            "estado: borrador", "estado: aprobado"
        )
        self.ruta_principal.write_text(aprobado, encoding="utf-8")
        codigo, _, errores = self.guardar_valido("--reemplazar")
        self.assertEqual(codigo, 2)
        self.assertIn("aprobado", errores)
        self.assertEqual(self.ruta_principal.read_text(encoding="utf-8"), aprobado)

    def test_no_sustituye_un_borrador_sin_reemplazar_y_si_con_el(self):
        self.guardar_valido()
        original = self.ruta_principal.read_text(encoding="utf-8")

        codigo, _, errores = self.guardar_valido()
        self.assertEqual(codigo, 2)
        self.assertIn("--reemplazar", errores)
        self.assertEqual(self.ruta_principal.read_text(encoding="utf-8"), original)

        ruta = self.escribir_borrador_modelo(texto_modelo(extra="Versión nueva."))
        codigo, _, _ = self.ejecutar("guardar", OPORTUNIDAD_ID, str(ruta), "--reemplazar")
        self.assertEqual(codigo, 0)
        nuevo = self.ruta_principal.read_text(encoding="utf-8")
        self.assertNotEqual(nuevo, original)
        self.assertIn("Versión nueva.", nuevo)
        self.assertEqual(nuevo, self.ruta_borrador.read_text(encoding="utf-8"))


class PruebaComprobar(PruebaBase):
    def test_detecta_un_error_introducido_a_mano_y_no_modifica_nada(self):
        self.guardar_valido()
        editado = self.ruta_principal.read_text(encoding="utf-8").replace(
            "[f1]", "[f1] y un dato nuevo sin fuente [f9]"
        )
        self.ruta_principal.write_text(editado, encoding="utf-8")
        borrador = self.ruta_borrador.read_text(encoding="utf-8")

        codigo, salida, _ = self.ejecutar("comprobar", OPORTUNIDAD_ID)
        self.assertEqual(codigo, 2)
        informe = json.loads(salida)
        self.assertTrue(any("[f9]" in e for e in informe["errores"]))
        # No modifica nada: ni el texto editado ni el borrador original.
        self.assertEqual(self.ruta_principal.read_text(encoding="utf-8"), editado)
        self.assertEqual(self.ruta_borrador.read_text(encoding="utf-8"), borrador)

    def test_un_principal_correcto_pasa_sin_errores(self):
        self.guardar_valido()
        codigo, salida, _ = self.ejecutar("comprobar", OPORTUNIDAD_ID)
        self.assertEqual(codigo, 0)
        informe = json.loads(salida)
        self.assertEqual(informe["errores"], [])
        self.assertEqual(informe["avisos"], [])


if __name__ == "__main__":
    unittest.main()
