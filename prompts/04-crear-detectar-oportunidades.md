Crea la skill `detectar-oportunidades`. Cruza la evidencia externa (fichas de vídeos u otras fuentes) con lo que ya hemos publicado y con las decisiones anteriores, y propone oportunidades justificadas. Una oportunidad es un tema con interés real, que encaja con la línea editorial, que no hemos cubierto y al que podemos aportar algo concreto.

Es la segunda parte de la fase 2 de `ARQUITECTURA.md`. Léelo antes de empezar y respeta sus secciones 2, 4, 6, 8.3, 8.4 y 10. Lee también los `SKILL.md` de `analizar-biblioteca` y `explorar-youtube` para conocer las fichas que consume. Si alguna de esas skills no existe, detente e indica qué prompt falta.

En este paso creas y validas la skill con fichas ficticias. **No analices la biblioteca real.**

## 1. Reparto entre script y modelo

| Lo hace el script (Python sin IA) | Lo hace el modelo |
|---|---|
| Reunir las fichas externas y agruparlas por tema | Leer los artículos parecidos completos |
| Calcular las señales de cada grupo | Decidir la cobertura y la aportación |
| Buscar artículos y oportunidades parecidas (BM25) | Redactar la propuesta |
| Aplicar las cuatro condiciones | |
| Validar y guardar | |

**La decisión final de si algo es oportunidad la toma el script** aplicando las cuatro condiciones a datos calculados y al juicio del modelo. Así el criterio es siempre el mismo y cada condición queda visible.

## 2. Estructura

```text
.agents/skills/detectar-oportunidades/
├── SKILL.md
├── references/
│   ├── evaluacion.schema.json
│   ├── plantilla-oportunidad.md
│   └── instrucciones-evaluacion.md
└── scripts/
    ├── detectar_oportunidades.py
    └── test_detectar_oportunidades.py
```

Salidas:

```text
biblioteca/oportunidades/
├── <YYYY-MM-DD>-<slug>.md          # Una por oportunidad, con la plantilla de ARQUITECTURA.md
├── INDICE.md                       # Generado: oportunidades ordenadas por prioridad y estado
└── control/
    ├── grupos.json                 # Último agrupamiento calculado
    └── evaluaciones/<grupo_id>.json
```

**`SKILL.md`:**
- Empieza con un frontmatter con `name` y `description`. Úsala después de `explorar-youtube`, o de cualquier `explorar-<fuente>`, para obtener propuestas de contenido.
- Describe el flujo de la sección 5.
- Es breve: los criterios están en `references/`.

## 3. Entradas

- **Fichas externas:** todos los archivos `biblioteca/<fuente>/**/ficha.json`, con el esquema de ficha externa de `ARQUITECTURA.md`. **No hay rutas de YouTube escritas en el código.** Una fuente nueva que produzca fichas con ese esquema se incorpora sin cambiar el script.
- **Fichas propias:** `biblioteca/substack/fichas/*.json`, con la ruta de cada artículo según el inventario.
- **Oportunidades existentes:** su encabezado (estado, motivo y tema). Son las decisiones anteriores: un descarte con su motivo se tiene en cuenta en el siguiente cruce.
- **Configuración:** `linea_editorial` de `proyecto.config.json`.

## 4. Comandos del script

```text
python .agents/skills/detectar-oportunidades/scripts/detectar_oportunidades.py <comando>
```

### `agrupar`

Agrupa las fichas externas que tratan el mismo asunto:

1. Normaliza el tema: minúsculas, sin tildes y sin espacios sobrantes.
2. Pertenecen al mismo grupo las fichas con igual tema normalizado, o con temas distintos pero entidades muy coincidentes (índice de Jaccard ≥ 0,5 sobre las entidades normalizadas).
3. El `grupo_id` es estable entre ejecuciones: es un slug del tema más frecuente del grupo.

Señales de cada grupo:
- Número de fichas.
- **Número de autores distintos** (`canales`).
- **Mejor interés** del grupo, con el orden `alto > medio > bajo > sin_datos`.
- Mayor múltiplo de la mediana.
- Fecha más reciente.

**Interés real** si el mejor interés es `medio` o `alto`, o si `canales` ≥ 2. Escribe `control/grupos.json`.

### `pendientes`

Devuelve en JSON un **paquete** por cada grupo que necesita evaluación. Un grupo la necesita en estos casos:
- No tiene evaluación.
- Tiene fichas nuevas o cambiadas desde la última.
- Han cambiado los artículos o decisiones con los que se comparó.

Para detectarlo, cada evaluación guarda la huella de su contexto: IDs y huellas de las fichas del grupo, de los artículos comparados y el estado de las oportunidades parecidas.

Contenido de cada paquete:
- El grupo, con sus señales y sus fichas externas completas.
- Los **5 artículos propios más parecidos**, calculados con BM25. Cada uno con su puntuación, su ficha y **la ruta del texto completo**.
  - Documento: título, tema, subtemas, tesis y entidades de cada ficha propia.
  - Consulta: tema, tesis y entidades de las fichas del grupo.
  - Tokenización: minúsculas, sin tildes, sin signos y sin una lista corta de palabras vacías en español e inglés.
  - Implementación en Python puro, sin dependencias.
- Las **oportunidades existentes parecidas**, por BM25 sobre su tema y título, con su estado y motivo.
- La `linea_editorial`.

### `guardar-evaluacion <archivo.json>`

Valida el JSON del modelo con `evaluacion.schema.json`:

```json
{
  "grupo_id": "…",
  "articulos_comparados": ["<post_id>"],
  "cobertura": "nuevo | ampliación | cubierto",
  "que_hemos_publicado": "Qué cubren ya nuestros artículos",
  "diferencia": "Qué no cubren",
  "aportacion": "Lo que podemos añadir nosotros, o null",
  "parecida_a": "<id de una oportunidad existente>, o null",
  "razon_nueva": "Por qué volver a proponerla, o null",
  "encaje": true,
  "motivo": "Una frase"
}
```

Después aplica **las cuatro condiciones** de la sección 8.4 de `ARQUITECTURA.md` y guarda el resultado en `control/evaluaciones/<grupo_id>.json`, con cada condición y su valor:

1. **Interés real:** calculado en `agrupar`.
2. **Encaje:** `encaje` es `true`.
3. **No cubierto:** `cobertura` es `nuevo` o `ampliación`.
4. **Aportación:** `aportacion` no está vacía.

Además:
- Si `parecida_a` apunta a una oportunidad **descartada**, hace falta `razon_nueva`; sin ella no es oportunidad.
- Si apunta a una oportunidad en estado `propuesta`, `aceptada` o `publicada`, no se crea otra. Se informa para añadir las evidencias nuevas a la existente.
- `articulos_comparados` debe incluir los artículos del paquete que el modelo leyó; si faltan, la evaluación se rechaza.

### `guardar-oportunidad <grupo_id> <archivo.md>`

Solo se acepta si la evaluación del grupo cumple las cuatro condiciones.

1. **El script escribe el encabezado** con datos calculados: `id`, `estado: propuesta`, `motivo_estado: ""`, `tema`, `grupo_id`, `interes`, `canales`, `cobertura`, `evidencias` (con el formato `<fuente>:<id>@<marca>`, tomado de las afirmaciones de las fichas) y `relacionados`.
2. **El modelo aporta el cuerpo,** con las secciones de `references/plantilla-oportunidad.md`, que son las de la sección 8.4 de `ARQUITECTURA.md`. El script comprueba que estén todas y no estén vacías.

Para añadir evidencias a una oportunidad existente, `guardar-oportunidad --actualizar <oportunidad_id>` añade las nuevas evidencias al encabezado sin tocar el cuerpo ni el estado.

**Nunca se sobrescribe una oportunidad cuyo estado no sea `propuesta`.** El estado lo cambia la persona.

### `indice`

Regenera `biblioteca/oportunidades/INDICE.md`.
- Las propuestas aparecen primero, ordenadas por interés, después por `canales` y después por cobertura (`nuevo` antes que `ampliación`).
- Debajo, las aceptadas, publicadas y descartadas, con su motivo.
- La salida es determinista.

### Códigos de salida y errores

- `0`: correcto.
- `1`: errores parciales, como una ficha no válida que se omite y se informa.
- `2`: no pudo ejecutarse.

Las escrituras son atómicas.

## 5. Flujo que describe SKILL.md

1. `agrupar` y `pendientes`.
2. Por cada paquete, el modelo **lee el texto completo de los artículos parecidos**, no solo sus fichas, y redacta la evaluación siguiendo `instrucciones-evaluacion.md`. Después, `guardar-evaluacion`.
3. Por cada grupo que cumple las condiciones, el modelo redacta la propuesta con la plantilla y ejecuta `guardar-oportunidad`.
4. `indice`.
5. **Informar:**
   - Grupos evaluados.
   - Oportunidades nuevas.
   - Oportunidades existentes con evidencias nuevas.
   - Grupos descartados por cada condición.

## 6. Criterios del modelo

**`instrucciones-evaluacion.md`:**
- **`cobertura`** se decide leyendo nuestros artículos, no por el parecido BM25:
  - `cubierto`: ya defendimos lo mismo con un enfoque equivalente.
  - `ampliación`: tratamos el tema, pero falta un ángulo, un caso o una actualización relevante.
  - `nuevo`: no lo hemos tratado.
- **`aportacion`** es concreta y comprobable, por ejemplo una prueba propia del flujo, el caso en español, contrastar lo que el vídeo promete sin demostrar o el proceso paso a paso. Si no hay ninguna, es `null`: repetir lo que dice el vídeo no es aportar.
- **`encaje`**: frente a `linea_editorial.nicho` y `linea_editorial.aportacion`.
- **Descartes:** si hay una oportunidad descartada parecida, se lee su motivo. Solo se vuelve a proponer si algo ha cambiado, y se explica en `razon_nueva`.
- **Fuentes:** las afirmaciones se citan con su evidencia (`fuente:id@marca`). No se añade información que no esté en las fichas o en los artículos.

**`plantilla-oportunidad.md`:**
- **La oportunidad:** dos o tres frases.
- **Por qué ahora:** señales y evidencias citadas.
- **Qué hemos publicado y qué falta:** con enlaces a los artículos.
- **Qué aportaríamos.**
- **Qué hay que investigar o probar:** afirmaciones a verificar y pruebas posibles.
- **Riesgos:** por ejemplo, una promesa sin demostrar, un tema efímero o una herramienta de pago.

## 7. Pruebas

Escríbelas con `unittest`, sobre una biblioteca ficticia en una carpeta temporal. Prepara fichas externas de dos fuentes distintas: `youtube` y una inventada, `blog`, para comprobar que no depende de YouTube. Incluye también fichas propias, artículos y oportunidades en distintos estados.

Deben comprobar que:
1. `agrupar` junta fichas con el mismo tema y con entidades coincidentes, separa las distintas, cuenta autores distintos y mantiene el `grupo_id` entre ejecuciones.
2. La regla de interés real funciona tanto por nivel de interés como por número de canales.
3. BM25 sitúa primero el artículo propio que trata el mismo tema y devuelve la ruta de su texto.
4. `pendientes` no repite un grupo evaluado sin cambios, y lo vuelve a pedir si cambia una ficha, un artículo comparado o una decisión parecida.
5. `guardar-evaluacion` aplica cada condición: un grupo `cubierto`, uno sin aportación, uno sin encaje y uno sin interés real no son oportunidad, y la evaluación indica qué condición falló.
6. Una oportunidad parecida a un descarte exige `razon_nueva`; una parecida a una propuesta existente no crea un duplicado.
7. `guardar-oportunidad` rechaza grupos que no cumplen las condiciones o cuerpos con secciones vacías, escribe el encabezado con los datos calculados y nunca sobrescribe una oportunidad aceptada o descartada.
8. `--actualizar` añade evidencias sin tocar el cuerpo ni el estado.
9. `indice` ordena por prioridad y es determinista.

Ejecuta las pruebas y muestra el resultado.

Para comprobar las instrucciones del modelo, toma un paquete ficticio, redacta tú mismo la evaluación y la oportunidad siguiendo `references/`, guárdalas con los comandos y muestra el resultado. Usa un caso ya cubierto y un caso de ampliación: el primero debe quedar descartado y el segundo aceptado como propuesta, con su diferencia y evidencias. Todo ocurre en la carpeta temporal de pruebas.

## 8. Documentación

- Actualiza en `README.md` la fila del prompt 04 a `hecho`.
- No modifiques `ARQUITECTURA.md`. Si algo obliga a cambiar el diseño, indícalo al final como propuesta.

## 9. Entrega

Muestra:
- El árbol de la skill.
- `SKILL.md` y las instrucciones.
- El resultado de las pruebas.
- La evaluación y la oportunidad de ejemplo.
- Cómo ejecutarla sobre la biblioteca real.

Separa lo comprobado con datos ficticios de lo que solo se verá con datos reales, como la calidad del agrupamiento.
