"""Pruebas de adaptar_contenido.py con un contenido ficticio en una carpeta
temporal: principal aprobado, configuración de prueba y una copia de las
plantillas reales de canal. Nunca tocan biblioteca/ ni la red."""

from __future__ import annotations

import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from adaptar_contenido import MARCADOR_ENLACE, main, parsear_frontmatter

CONTENIDO_ID = "2026-10-20-agentes-investigacion"
DIR_CANALES_REAL = Path(__file__).resolve().parent.parent / "references" / "canales"

PRINCIPAL = """\
---
oportunidad: 2026-10-20-agentes-investigacion
estado: aprobado
fecha: 2026-10-22
titulos_alternativos: [Agentes a prueba, Lo que los agentes no hacen solos]
---
# Probamos los agentes que investigan solos

Los agentes reducen el tiempo de documentación de tres horas a cuarenta
minutos. La promesa de publicar sin revisión humana quedó refutada: el
estudio documenta errores graves.

## Fuentes

[f1] Documentación de AgentesSA, AgentesSA, 2026-09-01, https://docs.ejemplo.dev/agentes
"""


def pieza_linkedin(hashtags: int = 2, con_enlace: bool = True,
                   relleno: int = 700) -> str:
    cuerpo = (
        "Un agente no te quita la revisión; te quita la parte aburrida de "
        "documentar.\n\n"
        + "x" * relleno
        + ("\n\nEl proceso completo, con lo que falló: " + MARCADOR_ENLACE
           if con_enlace else "")
        + ("\n\n" + " ".join(f"#tema{i}" for i in range(hashtags)) if hashtags else "")
    )
    return cuerpo


def pieza_notes(con_enlace: bool = True) -> str:
    return (
        "Documentar una investigación nos llevaba tres horas; con el agente, "
        "cuarenta minutos. Lo medimos con nuestra propia biblioteca."
        + (" " + MARCADOR_ENLACE if con_enlace else "")
    )


def pieza_substack(asunto: str = "Probamos los agentes que investigan solos") -> str:
    return f"""\
## asunto
{asunto}

## vista_previa
De tres horas a cuarenta minutos documentando, y por qué no publicaría sin revisar.

## subtitulo
Prueba real de agentes de investigación: lo que automatizan bien y lo que sigue necesitando a una persona.
"""


class PruebaBase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="adaptar-")
        self.raiz = Path(self._tmp)
        self.addCleanup(shutil.rmtree, self._tmp, True)

        self.canales_salida = ["substack", "linkedin", "notes"]
        self._escribir_config()
        self.dir_canales = self.raiz / "canales"
        shutil.copytree(DIR_CANALES_REAL, self.dir_canales)

        carpeta = self.raiz / "biblioteca" / "contenidos" / CONTENIDO_ID
        carpeta.mkdir(parents=True)
        self.ruta_principal = carpeta / "principal.md"
        self.ruta_principal.write_text(PRINCIPAL, encoding="utf-8")
        (self.raiz / "biblioteca" / "estilo.md").write_text(
            "# Voz\n\nTono directo.\n\n## Reglas aprendidas\n\n- Ninguna.\n",
            encoding="utf-8",
        )
        self.dir_piezas = carpeta / "piezas"

    def _escribir_config(self):
        (self.raiz / "proyecto.config.json").write_text(json.dumps({
            "publicacion": {"nombre": "Ejemplo", "substack": "https://ejemplo.substack.com"},
            "canales_salida": self.canales_salida,
        }, ensure_ascii=False, indent=2), encoding="utf-8")

    def ejecutar(self, *argumentos: str) -> tuple[int, str, str]:
        salida, errores = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(errores):
            codigo = main([
                "--config", str(self.raiz / "proyecto.config.json"),
                "--canales", str(self.dir_canales),
                "--hoy", "2026-10-23", *argumentos,
            ])
        return codigo, salida.getvalue(), errores.getvalue()

    def guardar(self, canal: str, contenido: str, *extra: str) -> tuple[int, str, str]:
        ruta = self.raiz / f"pieza-modelo-{canal}.md"
        ruta.write_text(contenido, encoding="utf-8")
        return self.ejecutar("guardar", CONTENIDO_ID, canal, str(ruta), *extra)


class PruebaPreparar(PruebaBase):
    def test_rechaza_un_principal_no_aprobado(self):
        self.ruta_principal.write_text(
            PRINCIPAL.replace("estado: aprobado", "estado: borrador"), encoding="utf-8"
        )
        codigo, _, errores = self.ejecutar("preparar", CONTENIDO_ID)
        self.assertEqual(codigo, 2)
        self.assertIn("borrador", errores)
        self.assertIn("aprobado", errores)

    def test_senala_un_canal_configurado_sin_plantilla(self):
        self.canales_salida = ["substack", "fantasma"]
        self._escribir_config()
        codigo, _, errores = self.ejecutar("preparar", CONTENIDO_ID)
        self.assertEqual(codigo, 2)
        self.assertIn("fantasma", errores)
        self.assertIn("fantasma.md", errores)

    def test_devuelve_canales_limites_y_pendientes(self):
        codigo, salida, _ = self.ejecutar("preparar", CONTENIDO_ID)
        self.assertEqual(codigo, 0)
        paquete = json.loads(salida)
        self.assertTrue(paquete["principal"].endswith("principal.md"))
        self.assertEqual(sorted(paquete["canales"]), ["linkedin", "notes", "substack"])
        linkedin = paquete["canales"]["linkedin"]
        self.assertEqual(linkedin["limites"]["max_caracteres"], 3000)
        self.assertTrue(linkedin["limites"]["enlace_obligatorio"])
        self.assertFalse(linkedin["tiene_pieza"])
        self.assertEqual(
            sorted(paquete["pendientes"]), ["linkedin", "notes", "substack"]
        )

    def test_indica_que_canales_ya_tienen_pieza(self):
        self.guardar("notes", pieza_notes())
        codigo, salida, _ = self.ejecutar("preparar", CONTENIDO_ID)
        self.assertEqual(codigo, 0)
        paquete = json.loads(salida)
        self.assertTrue(paquete["canales"]["notes"]["tiene_pieza"])
        self.assertEqual(paquete["canales"]["notes"]["estado_pieza"], "borrador")
        self.assertNotIn("notes", paquete["pendientes"])


class PruebaGuardarLimites(PruebaBase):
    def test_rechaza_una_pieza_demasiado_corta(self):
        codigo, _, errores = self.guardar("linkedin", pieza_linkedin(relleno=0))
        self.assertEqual(codigo, 2)
        self.assertIn("mínimo es 600", errores)
        self.assertFalse((self.dir_piezas / "linkedin.md").exists())

    def test_rechaza_una_pieza_demasiado_larga(self):
        codigo, _, errores = self.guardar("linkedin", pieza_linkedin(relleno=3200))
        self.assertEqual(codigo, 2)
        self.assertIn("máximo es 3000", errores)

    def test_rechaza_una_pieza_sin_enlace_obligatorio(self):
        codigo, _, errores = self.guardar("linkedin", pieza_linkedin(con_enlace=False))
        self.assertEqual(codigo, 2)
        self.assertIn("enlace", errores)
        self.assertIn(MARCADOR_ENLACE, errores)

    def test_rechaza_demasiados_hashtags(self):
        codigo, _, errores = self.guardar("linkedin", pieza_linkedin(hashtags=4))
        self.assertEqual(codigo, 2)
        self.assertIn("4 hashtags", errores)
        self.assertIn("máximo es 3", errores)

    def test_en_substack_los_limites_se_aplican_a_cada_campo(self):
        codigo, _, errores = self.guardar("substack", pieza_substack(asunto="x" * 70))
        self.assertEqual(codigo, 2)
        self.assertIn("asunto", errores)
        self.assertIn("máximo es 60", errores)

    def test_en_substack_falta_un_campo(self):
        sin_subtitulo = pieza_substack().split("## subtitulo")[0]
        codigo, _, errores = self.guardar("substack", sin_subtitulo)
        self.assertEqual(codigo, 2)
        self.assertIn("## subtitulo", errores)

    def test_guarda_una_pieza_valida_con_encabezado_del_script(self):
        codigo, salida, _ = self.guardar("linkedin", pieza_linkedin())
        self.assertEqual(codigo, 0)
        informe = json.loads(salida)
        self.assertTrue(informe["enlace_pendiente"])
        texto = (self.dir_piezas / "linkedin.md").read_text(encoding="utf-8")
        encabezado, cuerpo = parsear_frontmatter(texto)
        self.assertEqual(encabezado["canal"], "linkedin")
        self.assertEqual(encabezado["contenido"], CONTENIDO_ID)
        self.assertEqual(encabezado["estado"], "borrador")
        self.assertEqual(encabezado["fecha"], "2026-10-23")
        self.assertIn(MARCADOR_ENLACE, cuerpo)

    def test_rechaza_un_principal_no_aprobado(self):
        self.ruta_principal.write_text(
            PRINCIPAL.replace("estado: aprobado", "estado: borrador"), encoding="utf-8"
        )
        codigo, _, errores = self.guardar("notes", pieza_notes())
        self.assertEqual(codigo, 2)
        self.assertIn("aprobado", errores)


class PruebaCanalNuevo(PruebaBase):
    """Un canal nuevo con su plantilla funciona sin cambiar el código."""

    def setUp(self):
        super().setUp()
        (self.dir_canales / "x.md").write_text(
            "---\n"
            "canal: x\n"
            "max_caracteres: 200\n"
            "min_caracteres: 20\n"
            "enlace_obligatorio: true\n"
            "max_hashtags: 1\n"
            "---\n"
            "# Pieza de X\n\nUna frase y el enlace.\n",
            encoding="utf-8",
        )
        self.canales_salida = ["substack", "linkedin", "notes", "x"]
        self._escribir_config()

    def test_preparar_lo_lista_con_sus_limites(self):
        codigo, salida, _ = self.ejecutar("preparar", CONTENIDO_ID)
        self.assertEqual(codigo, 0)
        canal = json.loads(salida)["canales"]["x"]
        self.assertEqual(canal["limites"]["max_caracteres"], 200)
        self.assertTrue(canal["limites"]["enlace_obligatorio"])

    def test_guardar_aplica_sus_limites(self):
        codigo, _, errores = self.guardar("x", "Corta sin enlace pero con texto suficiente.")
        self.assertEqual(codigo, 2)
        self.assertIn("enlace", errores)

        codigo, _, _ = self.guardar("x", f"De tres horas a cuarenta minutos. {MARCADOR_ENLACE}")
        self.assertEqual(codigo, 0)
        self.assertTrue((self.dir_piezas / "x.md").is_file())


class PruebaNoSobrescribir(PruebaBase):
    def test_no_sobrescribe_una_pieza_aprobada_ni_con_reemplazar(self):
        self.guardar("notes", pieza_notes())
        ruta = self.dir_piezas / "notes.md"
        aprobada = ruta.read_text(encoding="utf-8").replace(
            "estado: borrador", "estado: aprobado"
        )
        ruta.write_text(aprobada, encoding="utf-8")

        codigo, _, errores = self.guardar("notes", pieza_notes(), "--reemplazar")
        self.assertEqual(codigo, 2)
        self.assertIn("aprobado", errores)
        self.assertEqual(ruta.read_text(encoding="utf-8"), aprobada)

    def test_no_sustituye_un_borrador_sin_reemplazar_y_si_con_el(self):
        self.guardar("notes", pieza_notes())
        ruta = self.dir_piezas / "notes.md"
        original = ruta.read_text(encoding="utf-8")

        codigo, _, errores = self.guardar("notes", pieza_notes())
        self.assertEqual(codigo, 2)
        self.assertIn("--reemplazar", errores)
        self.assertEqual(ruta.read_text(encoding="utf-8"), original)

        nueva = pieza_notes().replace("cuarenta", "cuarenta y cinco")
        codigo, _, _ = self.guardar("notes", nueva, "--reemplazar")
        self.assertEqual(codigo, 0)
        self.assertIn("cuarenta y cinco", ruta.read_text(encoding="utf-8"))


class PruebaEnlazar(PruebaBase):
    def test_sustituye_el_marcador_en_todas_las_piezas(self):
        self.guardar("linkedin", pieza_linkedin())
        self.guardar("notes", pieza_notes())
        self.guardar("substack", pieza_substack())

        url = "https://ejemplo.substack.com/p/agentes-investigacion"
        codigo, salida, _ = self.ejecutar("enlazar", CONTENIDO_ID, url)
        self.assertEqual(codigo, 0)
        informe = json.loads(salida)
        self.assertEqual(informe["total"], 2)
        self.assertEqual(informe["sustituciones"]["linkedin.md"], 1)
        self.assertEqual(informe["sustituciones"]["notes.md"], 1)
        self.assertEqual(informe["sustituciones"]["substack.md"], 0)
        for nombre in ("linkedin.md", "notes.md"):
            texto = (self.dir_piezas / nombre).read_text(encoding="utf-8")
            self.assertIn(url, texto)
            self.assertNotIn(MARCADOR_ENLACE, texto)

    def test_avisa_si_ninguna_pieza_tenia_marcador(self):
        self.guardar("substack", pieza_substack())
        codigo, _, errores = self.ejecutar(
            "enlazar", CONTENIDO_ID, "https://ejemplo.substack.com/p/x"
        )
        self.assertEqual(codigo, 1)
        self.assertIn(MARCADOR_ENLACE, errores)

    def test_rechaza_una_url_que_no_lo_es(self):
        self.guardar("notes", pieza_notes())
        codigo, _, errores = self.ejecutar("enlazar", CONTENIDO_ID, "pegar-aqui-la-url")
        self.assertEqual(codigo, 2)
        self.assertIn("http", errores)


class PruebaComprobar(PruebaBase):
    def test_detecta_una_pieza_editada_a_mano_que_supera_el_limite(self):
        self.guardar("notes", pieza_notes())
        ruta = self.dir_piezas / "notes.md"
        editada = ruta.read_text(encoding="utf-8").replace(
            "Lo medimos", "y" * 700 + " Lo medimos"
        )
        ruta.write_text(editada, encoding="utf-8")

        codigo, salida, _ = self.ejecutar("comprobar", CONTENIDO_ID)
        self.assertEqual(codigo, 2)
        informe = json.loads(salida)
        errores_pieza = informe["piezas"]["notes.md"]["errores"]
        self.assertTrue(any("máximo es 600" in e for e in errores_pieza))
        # No modifica nada.
        self.assertEqual(ruta.read_text(encoding="utf-8"), editada)

    def test_unas_piezas_correctas_pasan_y_lista_los_canales_sin_pieza(self):
        self.guardar("linkedin", pieza_linkedin())
        self.guardar("notes", pieza_notes())
        codigo, salida, _ = self.ejecutar("comprobar", CONTENIDO_ID)
        informe = json.loads(salida)
        self.assertEqual(informe["piezas"]["linkedin.md"]["errores"], [])
        self.assertEqual(informe["piezas"]["notes.md"]["errores"], [])
        self.assertEqual(informe["canales_sin_pieza"], ["substack"])
        self.assertEqual(codigo, 1)  # aviso: falta una pieza y hay {{enlace}} pendientes


if __name__ == "__main__":
    unittest.main()
