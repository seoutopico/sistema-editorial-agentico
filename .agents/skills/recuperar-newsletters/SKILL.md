---
name: recuperar-newsletters
description: Descarga y mantiene actualizado el histórico publicado de la newsletter de Substack en biblioteca/substack/. Úsala cuando haya que actualizar o revisar lo publicado, antes de analizar la biblioteca o tras publicar un artículo nuevo.
---

# recuperar-newsletters

Fase 1 del sistema editorial (ver `ARQUITECTURA.md`, secciones 2, 4 y 8.1). Script Python sin IA, solo biblioteca estándar.

## Qué lee

- `proyecto.config.json` en la raíz: `publicacion.substack` y los parámetros de `red` (timeout, intentos, pausa). Nada de la publicación está escrito en el código.
- La API pública de Substack: `/api/v1/archive` (paginado) y `/api/v1/posts/<slug>`.

## Qué escribe

Todo bajo `biblioteca/substack/`:

- `articulos/<YYYY-MM-DD>-<slug>.md` — frontmatter (id, título, subtítulo, fecha, url, tipo, audiencia, estado, huella) + cuerpo en Markdown.
- `INDICE.md` — tabla de más reciente a más antiguo.
- `control/inventario.json` — un registro por `id`, con métricas y fechas de control. Es la entrada de `analizar-biblioteca`.
- `control/originales/<id>.json` — última respuesta de la API por artículo.
- `control/historial/<id>/<marca>.md` — versiones anteriores cuando el contenido cambia.
- `control/ejecuciones/<run_id>.json` — informe de cada ejecución.

Un artículo se identifica siempre por su `id`; un cambio de slug renombra, no duplica. Un extracto o un error nunca sustituye una copia completa. Las escrituras son atómicas (temporal + rename).

## Cómo se ejecuta

Desde la raíz del proyecto:

```bash
python .agents/skills/recuperar-newsletters/scripts/recuperar_newsletters.py            # descarga completa
python .agents/skills/recuperar-newsletters/scripts/recuperar_newsletters.py --limite 5 # prueba corta
python .agents/skills/recuperar-newsletters/scripts/recuperar_newsletters.py --config otra/ruta.json
```

## Cómo interpretar el informe

Al terminar imprime: artículos vistos, páginas leídas, contadores (nuevos, actualizados, sin cambios, extractos, errores) y la lista de errores e incidencias con su motivo. Si la paginación quedó incompleta lo avisa explícitamente: un fallo de consulta nunca se presenta como "sin novedades". El detalle queda en `control/ejecuciones/<run_id>.json`.

## Códigos de salida

- `0` — todo correcto.
- `1` — terminó, pero con errores parciales, incidencias o paginación incompleta.
- `2` — no pudo ejecutarse (configuración inválida o archivo de Substack inaccesible).

## Pruebas

```bash
python -m unittest discover .agents/skills/recuperar-newsletters/scripts -v
```

Usan respuestas simuladas inyectando la función de red; nunca acceden a internet.
