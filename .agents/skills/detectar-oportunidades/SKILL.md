---
name: detectar-oportunidades
description: Cruza las fichas externas (YouTube u otra fuente con el mismo esquema) con los artículos propios y las decisiones anteriores, y propone oportunidades de contenido justificadas. Úsala después de explorar-youtube, o de cualquier explorar-<fuente>, para obtener propuestas de contenido.
---

# detectar-oportunidades

Segunda parte de la fase 2 del sistema editorial (ver `ARQUITECTURA.md`,
secciones 2, 4, 6, 8.3, 8.4 y 10). El script hace lo repetible (reunir y
agrupar fichas, calcular señales, buscar parecidos con BM25, aplicar las
cuatro condiciones, validar y guardar); el modelo solo el juicio (leer los
artículos parecidos completos, decidir cobertura y aportación, redactar la
propuesta). **La decisión final la toma el script** aplicando las cuatro
condiciones de la sección 8.4 a datos calculados y al juicio del modelo.

Los criterios del modelo están en `references/instrucciones-evaluacion.md` y
`references/plantilla-oportunidad.md`; el esquema de la evaluación, en
`references/evaluacion.schema.json`.

## Qué lee

- `biblioteca/<fuente>/**/ficha.json` — fichas externas de cualquier fuente
  con el esquema de la sección 6 (no hay rutas de YouTube en el código).
- `biblioteca/substack/fichas/*.json` y el texto completo de los artículos,
  localizados por `biblioteca/substack/control/inventario.json`.
- `biblioteca/oportunidades/*.md` — las decisiones anteriores (estado, motivo
  y tema de cada oportunidad).
- `linea_editorial` de `proyecto.config.json`.

## Qué escribe

- `biblioteca/oportunidades/<YYYY-MM-DD>-<slug>.md` — una por oportunidad.
- `biblioteca/oportunidades/INDICE.md` — generado, por prioridad y estado.
- `biblioteca/oportunidades/control/grupos.json` y
  `control/evaluaciones/<grupo_id>.json`.

## Flujo

Todos los comandos se ejecutan desde la raíz del proyecto:

```bash
python .agents/skills/detectar-oportunidades/scripts/detectar_oportunidades.py <comando>
```

1. **`agrupar`** y **`pendientes`.** El primero agrupa las fichas externas por
   tema y entidades y calcula las señales; el segundo devuelve un paquete JSON
   por cada grupo sin evaluación vigente (nuevo, con fichas cambiadas o con
   artículos o decisiones comparados que cambiaron).
2. **Evaluación por paquete.** El modelo **lee el texto completo de los
   artículos parecidos** (campo `ruta_texto`), no solo sus fichas, y redacta
   el JSON siguiendo `instrucciones-evaluacion.md`. Después,
   **`guardar-evaluacion <archivo.json>`**: el script valida el esquema,
   aplica las cuatro condiciones y guarda el resultado con cada condición y su
   valor. Si la evaluación se rechaza, explica por qué: corregir y repetir.
3. **Propuesta por grupo que cumple.** El modelo redacta el cuerpo con
   `plantilla-oportunidad.md` y ejecuta
   **`guardar-oportunidad <grupo_id> <archivo.md>`**: el script escribe el
   encabezado con los datos calculados y comprueba las secciones. Si la
   evaluación indica `accion: actualizar:<id>`, en su lugar
   **`guardar-oportunidad <grupo_id> --actualizar <oportunidad_id>`** añade
   las evidencias nuevas sin tocar el cuerpo ni el estado.
4. **`indice`.** Regenera `INDICE.md`.
5. **Informar:** grupos evaluados, oportunidades nuevas, oportunidades
   existentes con evidencias nuevas y grupos descartados por cada condición.

Códigos de salida: `0` correcto, `1` errores parciales (una ficha no válida se
omite y se informa), `2` no pudo ejecutarse. Las escrituras son atómicas y
nunca se sobrescribe una oportunidad cuyo estado no sea `propuesta`: el estado
lo cambia la persona.

## Pruebas

```bash
python -m unittest discover .agents/skills/detectar-oportunidades/scripts -v
```

Usan una biblioteca ficticia (fuentes `youtube` y `blog`) en una carpeta
temporal; nunca tocan `biblioteca/` ni la red.
