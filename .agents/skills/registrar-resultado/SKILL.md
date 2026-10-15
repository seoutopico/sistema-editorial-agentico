---
name: registrar-resultado
description: Cierra el ciclo editorial. Enlaza cada contenido con su artículo publicado, acumula las métricas, regenera biblioteca/decisiones.md y convierte las correcciones de la persona en reglas de biblioteca/estilo.md. Úsala después de publicar un contenido, o cada semana para actualizar decisiones y métricas.
---

# registrar-resultado

Fase 5 del sistema editorial (ver `ARQUITECTURA.md`, secciones 2, 4, 7, 8.6,
9 y 10). El script hace lo repetible (enlazar el artículo, guardar métricas,
generar `decisiones.md`, calcular las diferencias y añadir reglas sin
duplicar); el modelo solo el juicio (convertir las diferencias en reglas de
estilo generales, siguiendo `references/instrucciones-reglas.md`).

## Qué lee

- `biblioteca/oportunidades/*.md` — el estado del encabezado es la fuente de verdad.
- `biblioteca/substack/control/inventario.json` y `biblioteca/substack/articulos/` — lo publicado y sus métricas públicas.
- `biblioteca/contenidos/<id>/principal.md` y `principal.borrador.md`.
- `biblioteca/substack/control/estadisticas/*.csv` — opcional, exportado por la persona desde Substack.

## Qué escribe

- `biblioteca/decisiones.md` — propuestas, aceptadas, publicadas y descartadas con motivo.
- `biblioteca/estilo.md` — solo la sección `## Reglas aprendidas`.
- `biblioteca/oportunidades/<id>.md` — solo `estado: publicada` y `articulo` al enlazar.
- `biblioteca/contenidos/<id>/resultado.json` — artículo publicado, serie de métricas y reglas derivadas.

## Flujo después de publicar

Todos los comandos se ejecutan desde la raíz del proyecto:

```bash
python .agents/skills/registrar-resultado/scripts/registrar_resultado.py <comando>
```

1. Ejecutar `recuperar-newsletters` y `analizar-biblioteca` para incorporar el
   artículo nuevo a la biblioteca.
2. **`buscar-publicado <oportunidad_id>`** propone los 3 artículos con el
   título más parecido; no enlaza nada. Confirmar con la persona y
   **`enlazar <oportunidad_id> <post_id>`**: escribe `resultado.json`, pasa la
   oportunidad a `publicada` y sustituye `{{enlace}}` en las piezas.
3. **`diferencias <oportunidad_id>`** devuelve en JSON los párrafos
   eliminados, añadidos y modificados entre el borrador del modelo y lo
   publicado, con el cambio de título y de longitud.
4. **Reglas.** El modelo convierte esas diferencias en reglas de estilo
   siguiendo `references/instrucciones-reglas.md` (máximo cinco, con su
   ejemplo antes y después). La persona las revisa y se guardan con
   **`guardar-reglas <archivo.json>`**, que las añade a `## Reglas
   aprendidas` sin duplicar y sin tocar el resto de `estilo.md`.
5. **`decisiones`** y **`metricas`** cierran la pasada.

## Cada semana

`decisiones` y `metricas`: actualizan `biblioteca/decisiones.md` y la serie
de capturas de cada contenido publicado (señalando las de ~7 y ~30 días).

Códigos de salida: `0` correcto, `1` avisos (p. ej. descartes sin motivo o
reglas repetidas), `2` no pudo ejecutarse o la validación falló. Las
escrituras son atómicas.

## Pruebas

```bash
python -m unittest discover .agents/skills/registrar-resultado/scripts -v
```

Usan inventario, artículos, oportunidades, contenidos y estilo ficticios en
una carpeta temporal; nunca tocan `biblioteca/` ni la red.
