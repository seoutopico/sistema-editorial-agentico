# Handoff: sistema editorial Think&Hack

Fecha: 2026-10-15. Proyecto: `D:\pc-yoga\Ponencias\conia`. Repositorio: **https://github.com/seoutopico/sistema-editorial-agentico** (privado).

## 1. Qué es

Un proceso agéntico para crear contenido de Think&Hack (https://ainalluna.substack.com) a partir de **oportunidades reales**, en 5 fases: revisar lo publicado, encontrar oportunidades, investigar y desarrollar, adaptar y aprender. El plano completo y fuente de verdad es **`ARQUITECTURA.md`**; el estado por prompt está en la tabla del `README.md`.

## 2. Estado: SISTEMA COMPLETO Y EJECUTADO

- **Las 8 skills construidas** (prompts 00–08 ejecutados, cada uno en un subagente limpio) y **165 tests en verde** (`python -m unittest discover .agents/skills/<skill>/scripts`).
- **Fase 1 ejecutada con datos reales:** 55 artículos descargados, 55 fichas, `biblioteca/mapa-temas.md` (temas + subtemas + tesis por artículo) y `biblioteca/estilo.md`.
- **Fase 2 ejecutada con datos reales:** 150 vídeos de 5 canales (yt-dlp, sin API key), 100 clasificados por relevancia, 16 fichas de vídeo con subtemas, `biblioteca/youtube/mapa-videos.md`, y oportunidades en `biblioteca/oportunidades/` con `INDICE.md` + calendario sugerido.
- **Carpeta de agente portable** en `carpeta-agente/` (+ `carpeta-agente.zip`, fuera de Git): el sistema empaquetado con AGENTS.md para subirlo a Claude Cowork o ChatGPT Work (`COMO-SUBIRLA.md`).

## 3. Decisiones importantes tomadas en la sesión de 2026-10-14/15

1. **YouTube sin API**: todo con `yt-dlp` (listado plano con fecha en `upload_date` o `timestamp` según versión) y `youtube-transcript-api` como **vía alternativa de subtítulos** cuando YouTube devuelve HTTP 429 (frecuente en ráfagas). Sin claves en `.env`.
2. **`recursos` en `proyecto.config.json`**: herramientas, hardware y `fuera_de_alcance` (edición de vídeo; hardware caro/GPU). La relevancia y la evaluación de oportunidades filtran con ello: una aportación no ejecutable por Aina no es oportunidad.
3. **Grano fino en oportunidades**: una oportunidad por historia coherente. Agrupación por entidades **discriminantes** (se excluyen las ubicuas del nicho): Jaccard ≥ 0,5 o 2+ comunes. La regla de interés "2+ canales" se calcula a nivel de tema.
4. **Control de vocabulario** en `analizar-biblioteca`: `guardar` avisa de subtemas/entidades casi-duplicados; comando `vocabulario` para limpiezas; `pendientes` y `pendientes-ficha` devuelven el vocabulario existente para reutilizar.
5. **Clasificador de fórmulas de título** (`references/formulas-titulo.json` en explorar-youtube, 18 fórmulas propias en castellano): etiqueta el "porqué aparente" del título y cuenta fórmulas dominantes del nicho. Nota de honestidad: describe palabras, no explica el éxito.
6. **Mapas para humanos**: `mapa-temas.md` incluye subtemas y la tesis de cada artículo; `mapa-videos.md` es su espejo (tesis, demuestra, promete sin demostrar, preguntas abiertas). Los JSON son para los scripts; los mapas, para la persona.
7. **Los descartes son memoria**: dos oportunidades descartadas por Aina (vídeo; GPU) frenan automáticamente re-proponer esos ángulos salvo `razon_nueva` genuina.
8. **Regla de trabajo**: de skills/repos externos, inspiración, nunca copia literal y **nunca citar la fuente** en los artefactos del proyecto.

## 4. Cómo se usa cada semana

Ver sección "Uso cada semana" del `README.md` (comandos reales por fase). Puntos de control humanos: elegir oportunidad (cambiar `estado:` en su frontmatter), aprobar investigación, aprobar texto.

## 5. Pendiente / siguiente

- Aina debe revisar: la sección `recursos` de `proyecto.config.json` (deducida de sus artículos), `biblioteca/oportunidades/INDICE.md` (propuestas y calendario) y `biblioteca/youtube/informe-canales.md` (recomendación sobre `canales.md`).
- Fase 3 en adelante (`investigar-tema` → `redactar-contenido` → `adaptar-contenido`) se lanza cuando Aina marque una oportunidad como `aceptada`.
- `registrar-resultado` se ejecuta tras publicar.

## 6. Cómo continuar en otro PC

```text
gh auth login                      # cuenta seoutopico
gh repo clone seoutopico/sistema-editorial-agentico
cd sistema-editorial-agentico
pip install -r requirements.txt
claude
```

En Claude Code: "Lee HANDOFF.md y ARQUITECTURA.md y continúa desde el punto 5 del handoff."
