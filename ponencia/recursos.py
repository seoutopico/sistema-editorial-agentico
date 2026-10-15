# -*- coding: utf-8 -*-
"""Recursos visuales para la ponencia: capturas de archivos reales del
repositorio (estilo editor oscuro, con recuadro rojo).

Uso: python ponencia/recursos.py   → escribe en ponencia/capturas/ y ponencia/gifs/
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
AQUI = Path(__file__).resolve().parent
CAP = AQUI / "capturas"
CAP.mkdir(exist_ok=True)

FONTS = Path("C:/Windows/Fonts")
MONO = str(FONTS / "consola.ttf")
MONO_B = str(FONTS / "consolab.ttf")
SANS = str(FONTS / "segoeui.ttf")
SANS_B = str(FONTS / "segoeuib.ttf")

# Paleta Think&Hack (medida sobre la presentación) y del editor
CREMA = (234, 231, 220)
TINTA = (31, 41, 55)
CORAL = (253, 101, 52)
GRIS = (85, 91, 97)
ROJO = (229, 57, 53)
ED_BG = (30, 30, 30)
ED_BAR = (37, 37, 38)
ED_TAB = (30, 30, 30)
ED_TXT = (212, 212, 212)
ED_NUM = (110, 110, 110)
ED_KEY = (156, 220, 254)
ED_STR = (206, 145, 120)
ED_NUMV = (181, 206, 168)
ED_HEAD = (86, 156, 214)
ED_COM = (106, 153, 85)
ED_KW = (197, 134, 192)


def f(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- coloreado
def _trozos(linea, modo):
    """Devuelve [(texto, color)] con un coloreado sencillo por tipo de archivo."""
    if modo == "json":
        out, i = [], 0
        for m in re.finditer(r'"(?:[^"\\]|\\.)*"\s*:|"(?:[^"\\]|\\.)*"|\b-?\d+(?:\.\d+)?\b|\btrue\b|\bfalse\b|\bnull\b', linea):
            if m.start() > i:
                out.append((linea[i:m.start()], ED_TXT))
            t = m.group(0)
            if t.endswith(":"):
                out.append((t[:-1].rstrip(), ED_KEY)); out.append((":", ED_TXT))
            elif t.startswith('"'):
                out.append((t, ED_STR))
            else:
                out.append((t, ED_NUMV))
            i = m.end()
        if i < len(linea):
            out.append((linea[i:], ED_TXT))
        return out or [("", ED_TXT)]
    if modo == "md":
        s = linea.lstrip()
        if s.startswith("#"):
            return [(linea, ED_HEAD)]
        if s.startswith("---"):
            return [(linea, ED_COM)]
        m = re.match(r"^(\s*)([\w-]+):(.*)$", linea)
        if m and len(m.group(2)) < 20:
            return [(m.group(1) + m.group(2), ED_KEY), (":", ED_TXT), (m.group(3), ED_STR)]
        if s.startswith(("- ", "* ", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
            k = len(linea) - len(s)
            return [(linea[:k], ED_TXT), (s[:2], ED_KW), (s[2:], ED_TXT)]
        if s.startswith("|"):
            return [(linea, ED_TXT)]
        if s.startswith(">"):
            return [(linea, ED_COM)]
        return [(linea, ED_TXT)]
    if modo == "py":
        out, i = [], 0
        for m in re.finditer(r'#.*$|"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|\b(def|class|return|if|else|elif|for|in|not|and|or|import|from|raise|with|as|None|True|False)\b', linea):
            if m.start() > i:
                out.append((linea[i:m.start()], ED_TXT))
            t = m.group(0)
            col = ED_COM if t.startswith("#") else ED_STR if t[0] in "\"'" else ED_KW
            out.append((t, col)); i = m.end()
        if i < len(linea):
            out.append((linea[i:], ED_TXT))
        return out or [("", ED_TXT)]
    if modo == "term":
        if linea.startswith("$ "):
            return [("$ ", ED_COM), (linea[2:], (255, 255, 255))]
        if "OK" in linea and linea.startswith(("Ran", "OK")):
            return [(linea, ED_NUMV)]
        if "ok" in linea and "..." in linea:
            k = linea.rfind("ok")
            return [(linea[:k], ED_TXT), ("ok", ED_NUMV)]
        if "ERRORES" in linea or "incidencia" in linea:
            return [(linea, CORAL)]
        return [(linea, ED_TXT)]
    return [(linea, ED_TXT)]


def captura(nombre, lineas, archivo, modo="md", resaltar=(), ancho=1500, tam=22, numeros=True,
            ruta_visible=None, max_lineas=None, etiqueta=None):
    """Imagen tipo editor oscuro con pestaña, números de línea y recuadros rojos.
    resaltar: lista de (linea_inicio, linea_fin) 1-based inclusivos."""
    if max_lineas:
        lineas = lineas[:max_lineas]
    fm = f(MONO, tam)
    fb = f(MONO_B, tam)
    fs = f(SANS, 19)
    lh = int(tam * 1.5)
    barra = 54
    margen_x = 28
    alto = barra + lh * len(lineas) + 40
    im = Image.new("RGB", (ancho, alto), ED_BG)
    d = ImageDraw.Draw(im)
    # barra con pestaña
    d.rectangle([0, 0, ancho, barra], fill=ED_BAR)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([18 + i * 26, 18, 36 + i * 26, 36], fill=c)
    tab_x = 110
    tw = d.textlength(ruta_visible or archivo, font=fs) + 48
    d.rectangle([tab_x, 10, tab_x + tw, barra], fill=ED_TAB)
    d.rectangle([tab_x, 10, tab_x + tw, 13], fill=CORAL)
    d.text((tab_x + 24, 20), ruta_visible or archivo, font=fs, fill=(230, 230, 230))
    # líneas
    num_w = 64 if numeros else 0
    y = barra + 20
    for i, ln in enumerate(lineas, 1):
        if numeros:
            d.text((margen_x, y), f"{i:>3}", font=fm, fill=ED_NUM)
        x = margen_x + num_w
        for tx, col in _trozos(ln.rstrip("\n"), modo):
            d.text((x, y), tx, font=fm, fill=col)
            x += d.textlength(tx, font=fm)
        y += lh
    # recuadros rojos
    for (a, b) in resaltar:
        y0 = barra + 20 + (a - 1) * lh - 6
        y1 = barra + 20 + b * lh + 2
        d.rounded_rectangle([margen_x + num_w - 12, y0, ancho - 24, y1], radius=6, outline=ROJO, width=4)
    if etiqueta:
        # chip claro con el nombre del archivo, como en la presentación de MujeresEnSEO
        fe = f(SANS, 22)
        ew = d.textlength(etiqueta, font=fe) + 40
        d.rounded_rectangle([ancho - ew - 30, barra + 14, ancho - 30, barra + 58], radius=4, fill=CREMA)
        d.text((ancho - ew - 10, barra + 22), etiqueta, font=fe, fill=TINTA)
    im.save(CAP / f"{nombre}.png")
    return CAP / f"{nombre}.png"


def leer(rel, a=1, b=None):
    lineas = (RAIZ / rel).read_text(encoding="utf-8").splitlines()
    return lineas[a - 1: b]


def _cortar(lineas, ancho_max=92):
    out = []
    for ln in lineas:
        while len(ln) > ancho_max:
            k = ln.rfind(" ", 0, ancho_max)
            k = ancho_max if k < 20 else k
            out.append(ln[:k]); ln = "  " + ln[k:].lstrip()
        out.append(ln)
    return out


# ---------------------------------------------------------------- capturas reales
def capturas():
    # 1. SKILL.md real de recuperar-newsletters
    ln = _cortar(leer(".agents/skills/recuperar-newsletters/SKILL.md", 1, 28), 88)
    # localizar la description y la regla
    i_desc = next(i for i, l in enumerate(ln, 1) if l.startswith("description"))
    j_desc = i_desc
    while j_desc < len(ln) and ln[j_desc].startswith("  "):
        j_desc += 1
    captura("skill_md", ln, ".agents/skills/recuperar-newsletters/SKILL.md", "md",
            resaltar=[(i_desc, j_desc)], etiqueta="SKILL.md")

    # 2. Árbol real de la skill con references y scripts
    arbol = [
        ".agents/skills/",
        "├── recuperar-newsletters/",
        "│   ├── SKILL.md                     ← cuándo se usa, qué lee, qué escribe",
        "│   └── scripts/",
        "│       ├── recuperar_newsletters.py   (603 líneas, sin IA)",
        "│       └── test_recuperar_newsletters.py   (11 pruebas)",
        "└── analizar-biblioteca/",
        "    ├── SKILL.md",
        "    ├── references/",
        "    │   ├── ficha-articulo.schema.json  ← el contrato de la ficha",
        "    │   └── instrucciones-ficha.md      ← criterios para el modelo",
        "    └── scripts/",
        "        ├── analizar_biblioteca.py",
        "        └── test_analizar_biblioteca.py",
    ]
    captura("arbol_skills", arbol, "explorador", "txt", resaltar=[(2, 3), (9, 11)], numeros=False, etiqueta=".agents/skills/")

    # 3. Descripción mala vs buena (del artículo de Aina, 2026-07-05)
    mala = ["---", "name: meeting-helper", "description: Ayuda con reuniones.", "---", "",
            "# Meeting helper", "", "Resume reuniones de forma clara.", "Extrae acuerdos.", "Sé conciso.",
            "Organiza la información.", "Incluye próximos pasos."]
    captura("desc_mala", mala, "SKILL.md  (versión mala)", "md", resaltar=[(3, 3)], ancho=1100, etiqueta="antes")
    buena = _cortar(["---", "name: decision-brief",
             "description: Usa esta skill cuando el usuario necesite convertir notas de reunión, conversaciones, hilos de chat o apuntes técnicos desordenados en un brief de decisión con contexto, opciones, decisión, riesgos y siguiente acción. No la uses para actas completas, registros legales, planes de proyecto, creación de tickets ni resúmenes genéricos.",
             "---", "", "## Procedimiento", "1. Lee el material con mirada orientada a decisión.",
             "2. Clasifica la decisión: explícita, implícita o no sostenida por las notas.",
             "3. Escribe la decisión o declara que no hay evidencia suficiente.",
             "4. No inventes responsables, fechas ni compromisos.",
             "5. Valida el brief antes de cerrarlo."], 70)
    i_end = next(i for i, l in enumerate(buena, 1) if l == "---" and i > 1)
    captura("desc_buena", buena, "SKILL.md  (versión buena)", "md", resaltar=[(3, i_end - 1)], ancho=1100, etiqueta="después")

    # 4. Informe real de ejecución del script (descarga completa de hoy)
    ej = json.loads((RAIZ / "biblioteca/substack/control/ejecuciones/20261014T184051Z.json").read_text(encoding="utf-8"))
    ln = json.dumps({k: ej[k] for k in ("run_id", "inicio", "fin", "paginas_leidas", "paginacion_completa", "contadores")},
                    ensure_ascii=False, indent=2).splitlines()
    ln += ['  "cambios": [', '    {"tipo": "nuevo", "id": "219821904", "slug": "crear-sistema-diseno-codex-agentes-ia"},',
           '    {"tipo": "nuevo", "id": "217631531", "slug": "como-crear-skill-chatgpt-work"},',
           '    … 48 más', '  ],', '  "errores": []', '}']
    i_c = next(i for i, l in enumerate(ln, 1) if '"contadores"' in l)
    captura("ejecucion", ln, "biblioteca/substack/control/ejecuciones/20261014T184051Z.json", "json",
            resaltar=[(i_c, i_c + 6)], etiqueta="informe de ejecución")

    # 5. Inventario real: una entrada
    inv = json.loads((RAIZ / "biblioteca/substack/control/inventario.json").read_text(encoding="utf-8"))
    e = inv["217631531"]
    e = {k: e[k] for k in ("id", "slug", "titulo", "fecha", "estado", "huella", "metricas", "ultima_comprobacion", "archivo")}
    ln = json.dumps({"217631531": e}, ensure_ascii=False, indent=2).splitlines()
    ln = [l if len(l) < 95 else l[:92] + "…" for l in ln]
    i_h = next(i for i, l in enumerate(ln, 1) if '"huella"' in l)
    captura("inventario", ln, "biblioteca/substack/control/inventario.json  (1 de 55)", "json",
            resaltar=[(i_h, i_h)], etiqueta="inventario.json")

    # 6. Salida real de las pruebas
    r = subprocess.run([sys.executable, "-m", "unittest", "discover",
                        ".agents/skills/recuperar-newsletters/scripts", "-v"], cwd=RAIZ, capture_output=True, text=True)
    salida = (r.stderr or r.stdout).splitlines()
    salida = [l for l in salida if l.strip()]
    ln = ["$ python -m unittest discover .agents/skills/recuperar-newsletters/scripts -v"] + salida
    ln = [re.sub(r"\s\(test_recuperar_newsletters\.[\w.]+\)", "", l) for l in ln]
    captura("tests", ln, "terminal", "term", numeros=False, etiqueta="11 pruebas con datos simulados")

    # 7. Ficha real de un artículo
    ficha = json.loads((RAIZ / "biblioteca/substack/fichas/217631531.json").read_text(encoding="utf-8"))
    ln = _cortar(json.dumps(ficha, ensure_ascii=False, indent=2).splitlines(), 88)
    i_t = next(i for i, l in enumerate(ln, 1) if '"tema"' in l)
    i_s = next(i for i, l in enumerate(ln, 1) if '"tesis"' in l)
    j_s = i_s
    while j_s < len(ln) and not ln[j_s].lstrip().startswith('"'):
        j_s += 1
    captura("ficha", ln, "biblioteca/substack/fichas/217631531.json", "json",
            resaltar=[(i_t, i_t), (i_s, j_s)], etiqueta="ficha de un artículo")

    # 8. Esquema real de la ficha (el contrato)
    ln = leer(".agents/skills/analizar-biblioteca/references/ficha-articulo.schema.json")
    ln = _cortar(ln, 88)
    i_req = next((i for i, l in enumerate(ln, 1) if '"required"' in l), 1)
    j_req = i_req
    while j_req < len(ln) and "]" not in ln[j_req - 1]:
        j_req += 1
    captura("schema", ln[:min(len(ln), 34)], ".agents/skills/analizar-biblioteca/references/ficha-articulo.schema.json", "json",
            resaltar=[(i_req, min(j_req, 34))], etiqueta="el contrato")

    # 9. Mapa de temas real (resultado de hoy)
    ln = leer("biblioteca/mapa-temas.md", 1, 26)
    ln = [l if len(l) < 100 else l[:97] + "…" for l in ln]
    captura("mapa_temas", ln, "biblioteca/mapa-temas.md", "md", resaltar=[(3, 3)], etiqueta="generado hoy: 55 fichas")

    # 10. Las cuatro condiciones (ARQUITECTURA.md 8.4, texto real)
    todo = leer("ARQUITECTURA.md")
    a = next(i for i, l in enumerate(todo, 1) if l.startswith("### 8.4"))
    b = next(i for i, l in enumerate(todo, 1) if l.startswith("**Orden de prioridad"))
    ln = _cortar(todo[a - 1: b], 96)
    i_tab = next(i for i, l in enumerate(ln, 1) if l.startswith("| **Interés"))
    captura("condiciones", ln, "ARQUITECTURA.md  §8.4", "md", resaltar=[(i_tab, i_tab + 3)], etiqueta="qué es una oportunidad")

    # 11. Arnés: reglas reales del prompt 05 (investigar-tema)
    p5 = leer("prompts/05-crear-investigar-tema.md")
    a = next(i for i, l in enumerate(p5, 1) if l.startswith("### `guardar-investigacion"))
    b = next(i for i, l in enumerate(p5, 1) if l.startswith("### `guardar-revision"))
    ln = _cortar([l for l in p5[a - 1: b - 1] if l.strip()], 92)
    i_v = next(i for i, l in enumerate(ln, 1) if "verificarse" in l or "no basta" in l)
    i_v0 = next(i for i, l in enumerate(ln, 1) if "verificada" in l and "refutada" in l)
    i_n = next(i for i, l in enumerate(ln, 1) if l.startswith("**Nunca sobrescribe"))
    captura("arnes_reglas", ln, "prompts/05-crear-investigar-tema.md", "md",
            resaltar=[(i_v0, i_v), (i_n, i_n)], etiqueta="lo que el script no deja pasar")

    # 12. Aprender: diferencias y reglas (prompt 08, texto real)
    p8 = leer("prompts/08-crear-registrar-resultado.md")
    a = next(i for i, l in enumerate(p8, 1) if l.startswith("### `diferencias"))
    b = next(i for i, l in enumerate(p8, 1) if l.startswith("### Códigos de salida") and i > a)
    ln = _cortar([l for l in p8[a - 1: b - 1] if l.strip()], 92)
    i_r = next(i for i, l in enumerate(ln, 1) if l.startswith("### `guardar-reglas"))
    captura("aprender", ln, "prompts/08-crear-registrar-resultado.md", "md",
            resaltar=[(i_r, i_r + 7)], etiqueta="correcciones → reglas")

    # 13. Estado real del sistema (README)
    rd = leer("README.md")
    a = next(i for i, l in enumerate(rd, 1) if l.startswith("| Prompt"))
    ln = rd[a - 1: a + 10]
    ln = [re.sub(r" — `python[^|]*", " — construida y probada", l) for l in ln]
    captura("estado", ln, "README.md", "md", resaltar=[(3, 5)], etiqueta="estado del sistema")

    # 14. Señales reales de un vídeo de YouTube (explorar-youtube, hoy)
    m = json.loads((RAIZ / "biblioteca/youtube/videos/AYQtRqW1xX4/meta.json").read_text(encoding="utf-8"))
    m = {k: m[k] for k in ("id", "canal", "titulo", "fecha", "duracion_segundos", "estadisticas", "senales")}
    m["senales"] = {k: m["senales"][k] for k in ("multiplo_mediana", "mediana_canal", "interes", "dias", "formato_largo")}
    ln = _cortar(json.dumps(m, ensure_ascii=False, indent=2).splitlines(), 88)
    i_s = next(i for i, l in enumerate(ln, 1) if '"senales"' in l)
    captura("youtube", ln, "biblioteca/youtube/videos/AYQtRqW1xX4/meta.json  (1 de 150)", "json",
            resaltar=[(i_s, i_s + 3)], etiqueta="señales calculadas por el script")

    # 15. Guía de estilo real, generada hoy a partir de 55 artículos
    ln = leer("biblioteca/estilo.md")
    ln = _cortar(ln[:5] + ["…"] + ln[66:70], 96)
    i_r = next(i for i, l in enumerate(ln, 1) if l.startswith("## Reglas aprendidas"))
    captura("estilo", ln, "biblioteca/estilo.md", "md", resaltar=[(i_r, len(ln))], etiqueta="generada hoy de 55 artículos")


if __name__ == "__main__":
    capturas()
    print("capturas:", sorted(p.name for p in CAP.glob("*.png")))
