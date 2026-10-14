Crea la skill `registrar-resultado`. Cierra el ciclo:
- Enlaza cada contenido con el artículo publicado.
- Guarda sus métricas.
- Recopila las decisiones sobre oportunidades.
- Convierte las correcciones de la persona en reglas de estilo.

Así, la siguiente búsqueda y la siguiente redacción aprovechan lo aprendido.

Es la fase 5 de `ARQUITECTURA.md`. Léelo antes de empezar y respeta sus secciones 2, 4, 7, 8.6, 9 y 10. Lee también los `SKILL.md` de `recuperar-newsletters`, `analizar-biblioteca`, `detectar-oportunidades`, `redactar-contenido` y `adaptar-contenido`, porque esta skill lee sus salidas. Si alguna no existe, detente e indica qué prompt falta.

En este paso creas y validas la skill con datos ficticios. **No modifiques la biblioteca real.**

## 1. Reparto entre script y modelo

| Lo hace el script (Python sin IA) | Lo hace el modelo |
|---|---|
| Encontrar y enlazar el artículo publicado | Convertir las diferencias en reglas de estilo generales |
| Guardar las métricas | |
| Generar `decisiones.md` | |
| Calcular las diferencias entre borrador y publicado | |
| Añadir reglas sin duplicar | |

## 2. Estructura

```text
.agents/skills/registrar-resultado/
├── SKILL.md
├── references/
│   └── instrucciones-reglas.md
└── scripts/
    ├── registrar_resultado.py
    └── test_registrar_resultado.py
```

Salidas:

```text
biblioteca/
├── decisiones.md                      # Generado a partir de las oportunidades
├── estilo.md                          # Solo cambia la sección "## Reglas aprendidas"
├── oportunidades/<id>.md              # El estado pasa a "publicada" al enlazar
└── contenidos/<id>/resultado.json     # Artículo publicado, métricas y reglas derivadas
```

**`SKILL.md`:**
- Empieza con un frontmatter con `name` y `description`. Úsala después de publicar un contenido, o cada semana para actualizar decisiones y métricas.
- Describe el flujo de la sección 4.
- Es breve.

## 3. Comandos del script

```text
python .agents/skills/registrar-resultado/scripts/registrar_resultado.py <comando>
```

### `decisiones`

Regenera `biblioteca/decisiones.md` a partir del encabezado de todas las oportunidades. Tiene cuatro secciones: propuestas, aceptadas, publicadas (con enlace al artículo) y descartadas (con su motivo).

- Una oportunidad descartada sin `motivo_estado` aparece señalada. **Un descarte sin motivo no enseña nada al siguiente cruce.**
- La salida es determinista.

### `buscar-publicado <oportunidad_id>`

Propone el artículo publicado que corresponde al contenido: compara el título de `principal.md` y sus alternativos con los títulos del inventario de Substack posteriores a la fecha del borrador. Devuelve los 3 más parecidos con su puntuación.

**No enlaza nada por sí solo.**

### `enlazar <oportunidad_id> <post_id>`

Lo ejecuta la persona, o el modelo cuando la persona confirma la propuesta.

1. Comprueba que el `post_id` existe en el inventario.
2. Escribe `contenidos/<id>/resultado.json` con el artículo, su URL y la fecha de publicación.
3. Cambia la oportunidad a `estado: publicada`, con `articulo: <post_id>`.
4. Ejecuta `enlazar` de `adaptar-contenido` con la URL, si hay piezas.

### `metricas`

Por cada contenido publicado, copia en `resultado.json` las métricas públicas del inventario (reacciones, comentarios y restacks) con su fecha de captura.
- Conserva todas las capturas: es una serie, no un valor que se sobrescribe.
- Señala las capturas que corresponden aproximadamente a los 7 y 30 días de la publicación.
- Si el usuario coloca un CSV de estadísticas exportado de Substack en `biblioteca/substack/control/estadisticas/`, añade las aperturas y los clics de cada artículo que encuentre. Si no hay CSV, lo indica sin fallar.

### `diferencias <oportunidad_id>`

Compara `principal.borrador.md`, lo que escribió el modelo, con el artículo publicado en `biblioteca/substack/articulos/`.
- Usa `difflib` por párrafos.
- Devuelve en JSON los párrafos eliminados, añadidos y modificados, con su texto antes y después.
- Indica también el cambio de título y de longitud.

### `guardar-reglas <archivo.json>`

Recibe una lista de reglas:

```json
[{
  "regla": "…",
  "ejemplo_antes": "…",
  "ejemplo_despues": "…",
  "origen": "<oportunidad_id>"
}]
```

- Las añade a la sección `## Reglas aprendidas` de `biblioteca/estilo.md`, con su fecha y origen.
- No añade una regla que ya exista con el mismo texto normalizado; la informa como repetida.
- No toca el resto de `estilo.md`.
- Guarda en `resultado.json` qué reglas salieron de ese contenido.

### Códigos de salida

- `0`: correcto.
- `1`: avisos.
- `2`: no pudo ejecutarse o la validación falló.

Las escrituras son atómicas.

## 4. Flujo que describe SKILL.md

**Después de publicar:**
1. Ejecutar `recuperar-newsletters` y `analizar-biblioteca` para incorporar el artículo nuevo.
2. `buscar-publicado`, confirmar con la persona y `enlazar`.
3. `diferencias`.
4. **Reglas.** El modelo convierte las diferencias en reglas siguiendo `instrucciones-reglas.md`, la persona las revisa y se guardan con `guardar-reglas`.
5. `decisiones` y `metricas`.

**Cada semana:** `decisiones` y `metricas`.

## 5. Criterios del modelo

**`instrucciones-reglas.md`:**
- **Qué es una regla:** algo que se aplicaría a cualquier texto futuro, como "no abrir con una pregunta retórica" o "explicar el porqué antes del cómo". No lo es una corrección puntual de este texto, como un dato actualizado o una errata.
- **Cada regla:** se apoya en uno o varios cambios reales, con su ejemplo antes y después.
- **Cuántas:** como máximo cinco por contenido. Es mejor pocas y claras.
- **Contradicciones:** si una regla nueva contradice una existente, se señala para que decida la persona; no se añaden las dos.

## 6. Pruebas

Escríbelas con `unittest`, con datos ficticios en una carpeta temporal: inventario, artículos, oportunidades en distintos estados, contenidos con borrador y `estilo.md`.

Deben comprobar que:
1. `decisiones` agrupa por estado, señala los descartes sin motivo y es determinista.
2. `buscar-publicado` propone primero el artículo con el título más parecido y no enlaza nada.
3. `enlazar` rechaza un `post_id` inexistente; con uno válido, escribe `resultado.json` y cambia el estado de la oportunidad a `publicada`.
4. `metricas` acumula capturas sin sobrescribir las anteriores, y funciona con y sin CSV de estadísticas.
5. `diferencias` detecta párrafos añadidos, eliminados y modificados, además del cambio de título.
6. `guardar-reglas` añade reglas a `## Reglas aprendidas`, no duplica una regla repetida y no modifica el resto de `estilo.md`.

Ejecuta las pruebas y muestra el resultado.

Para comprobar las instrucciones, con un borrador y un publicado ficticios, obtén las diferencias, redacta tú mismo las reglas siguiendo `instrucciones-reglas.md` y guárdalas con el comando.

## 7. Documentación

- Actualiza en `README.md` la fila del prompt 08 a `hecho`.
- Añade al README la sección **"Uso cada semana"**, con los comandos reales de cada skill en el orden de la sección 9 de `ARQUITECTURA.md`.
- No modifiques `ARQUITECTURA.md`. Si algo obliga a cambiar el diseño, indícalo al final como propuesta.

## 8. Entrega

Muestra:
- El árbol de la skill.
- `SKILL.md` y las instrucciones.
- El resultado de las pruebas.
- Las reglas de ejemplo.
- La sección "Uso cada semana" del README.
