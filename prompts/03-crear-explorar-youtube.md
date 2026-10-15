Crea la skill `explorar-youtube`. Recorre una lista de canales de YouTube, mide qué vídeos destacan dentro de su propio canal, selecciona los relevantes para nuestra línea editorial, lee su contenido mediante los subtítulos y guarda una ficha de cada uno. Las fichas son la evidencia externa con la que después se detectan oportunidades.

Es la primera parte de la fase 2 de `ARQUITECTURA.md`. Léelo antes de empezar y respeta sus secciones 2, 4, 5, 6, 8.2 y 10. Lee también `.agents/skills/analizar-biblioteca/SKILL.md`: los temas y subtemas que use esta skill deben compartir vocabulario con las fichas propias. Si `ARQUITECTURA.md` o `proyecto.config.json` no existen, detente e indica que primero hay que ejecutar el prompt 00.

En este paso creas y validas la skill con respuestas simuladas. **No ejecutes `yt-dlp` de verdad ni descargues subtítulos reales.**

## 1. Reparto entre script y modelo

| Lo hace el script (Python sin IA) | Lo hace el modelo |
|---|---|
| Leer `canales.md` y listar los canales con `yt-dlp` | Clasificar la relevancia de los títulos, en un lote |
| Calcular las señales de cada vídeo | Leer cada transcripción y rellenar su ficha |
| Seleccionar los candidatos | |
| Descargar y limpiar los subtítulos | |
| Validar y guardar todo | |

El modelo nunca escribe en `biblioteca/` directamente. Entrega un JSON y el script lo valida y lo guarda.

## 2. Estructura

```text
.agents/skills/explorar-youtube/
├── SKILL.md
├── references/
│   ├── ficha-externa.schema.json
│   ├── formulas-titulo.json
│   ├── instrucciones-relevancia.md
│   └── instrucciones-ficha-video.md
└── scripts/
    ├── explorar_youtube.py
    └── test_explorar_youtube.py
```

Salidas, como fija `ARQUITECTURA.md`:

```text
biblioteca/youtube/
├── canales.md                         # Entrada; no se modifica
├── videos/<video_id>/
│   ├── meta.json                      # Datos, señales y relevancia
│   ├── subtitulos.<idioma>.vtt        # Original descargado
│   ├── transcripcion.md               # Texto limpio con marcas de tiempo
│   └── ficha.json                     # Ficha externa
├── mapa-videos.md                     # Vista humana de las fichas (comando `mapa`)
└── control/
    ├── metricas.jsonl                 # Una línea por vídeo y captura
    └── ejecuciones/<run_id>.json
```

Cada vídeo tiene una única carpeta, identificada por su ID, aunque aparezca en varias ejecuciones.

**`SKILL.md`:**
- Empieza con un frontmatter con `name` y `description`. Úsala para buscar qué se está publicando en el nicho o como paso previo a `detectar-oportunidades`.
- Describe el flujo de la sección 5, qué necesita (`yt-dlp` instalado y `youtube-transcript-api` como vía alternativa de subtítulos; sin claves de API) y cómo interpretar el informe.
- Es breve: los criterios del modelo están en `references/`.

## 3. Dependencias

- **No se necesita ninguna clave de API.** Toda la información de YouTube se obtiene con `yt-dlp` (con `youtube-transcript-api` como vía alternativa solo para subtítulos).
- Añade `yt-dlp` y `youtube-transcript-api` a `requirements.txt`. yt-dlp lista canales, obtiene metadatos y descarga subtítulos; `youtube-transcript-api` es la **vía alternativa de subtítulos**: usa otro endpoint y entra en juego automáticamente cuando yt-dlp falla (YouTube limita con HTTP 429 las descargas de subtítulos en ráfaga). Si tampoco está disponible por esa vía, el vídeo queda marcado sin subtítulos, nunca inventado.
- El script invoca `yt-dlp` como subproceso a través de una única función inyectable (para poder simularla en las pruebas).
- Si `yt-dlp` no está instalado, cualquier comando que lo necesite termina con código 2, sin tocar ningún dato, e indica la instrucción de instalación (`pip install yt-dlp`).

## 4. Comandos del script

```text
python .agents/skills/explorar-youtube/scripts/explorar_youtube.py <comando>
```

### `recoger`

1. **Leer `biblioteca/youtube/canales.md`.** Acepta líneas con `https://www.youtube.com/@handle` o con `https://www.youtube.com/channel/UC…` e ignora el resto del texto. Una URL que no se reconoce es un error de ese canal y no detiene a los demás.
2. **Listar cada canal con `yt-dlp`**, como fija la sección 8.2 de `ARQUITECTURA.md`:
   - `yt-dlp --flat-playlist -J --extractor-args "youtubetab:approximate_date" --playlist-end <N> <url-del-canal>/videos`, donde N es `youtube.videos_por_canal`. Devuelve un JSON con las entradas del canal: id, título, visualizaciones, duración en segundos y fecha aproximada. Según la versión de yt-dlp, la fecha aproximada llega en `upload_date` (AAAAMMDD) o en `timestamp` (epoch): acepta ambas.
   - La descripción, los likes, los comentarios y la fecha exacta **no** vienen en el listado plano; se completan después, solo para los candidatos (comando `candidatos`).
3. **Guardar `meta.json`** por vídeo:
   - Datos: id, url, canal, título, duración en segundos y fecha (aproximada hasta que se completen los metadatos; el campo indica su precisión).
   - Estadísticas con fecha de captura (visualizaciones; likes y comentarios cuando estén disponibles).
   - Si un vídeo ya existe, solo se actualizan sus estadísticas y señales. Su relevancia, transcripción y ficha no se tocan.
4. **Añadir una línea a `metricas.jsonl`** por vídeo: id, fecha de captura, visualizaciones y, si están disponibles, likes y comentarios. Es el histórico para ver cómo evoluciona un vídeo.
5. **Calcular las señales** de cada canal, según la sección 8.2 de `ARQUITECTURA.md`:
   - **Formato largo:** duración ≥ `youtube.duracion_minima_segundos`.
   - **`dias`:** días desde la publicación.
   - **Mediana del canal:** visualizaciones de sus vídeos de formato largo con 7 días o más.
   - **`multiplo_mediana`** = visualizaciones / mediana.
   - **`interaccion`** = (likes + comentarios) / visualizaciones, cuando hay metadatos completos. Si aún no los hay, o los likes están ocultos o los comentarios desactivados, el dato es `null` y se indica.
   - **`interes`:** `alto` si el múltiplo es ≥ 2, `medio` entre 1 y 2, `bajo` si es < 1.
   - Un vídeo con menos de 7 días tiene `senal_incompleta: true` e interés `sin_datos`.
   - Si el canal tiene menos de 5 vídeos válidos para la mediana, sus vídeos se marcan con `mediana_poco_fiable`.
   - **`formula_titulo`:** fórmula de título del vídeo según `references/formulas-titulo.json` (~18 fórmulas con nombre en castellano y patrones regex sin acentos que valen para títulos en español e inglés). Gana la fórmula con más patrones coincidentes; sin coincidencias, `sin clasificar`. **Honestidad por diseño:** el archivo y el script dejan claro que la fórmula clasifica las palabras del título, no el porqué real del éxito del vídeo.
6. **Errores:** si un canal falla (no existe, bloqueo, red), se registra con su motivo, se conservan sus datos anteriores y se sigue con los demás.

### `relevancia-pendiente`

Devuelve en JSON los vídeos de formato largo dentro de `youtube.ventana_dias` que todavía no tienen relevancia. De cada uno: id, canal, título y, si está disponible, los primeros 500 caracteres de la descripción.

Incluye también:
- La `linea_editorial` de la configuración.
- Los `recursos` de la configuración (herramientas, hardware, formatos que domina y `fuera_de_alcance`), para que el modelo descarte lo que la publicación no puede aprovechar antes de gastar subtítulos y fichas.
- La **lista de temas existentes**, reunida de las fichas propias, las fichas externas y las relevancias anteriores, para que el modelo los reutilice.

### `guardar-relevancia <archivo.json>`

Recibe una lista de `{id, relevante, tema, motivo}`. Valida que los IDs existen y los campos están completos, y guarda el resultado en el `meta.json` de cada vídeo con la fecha. **Un vídeo ya clasificado no se vuelve a pedir.**

### `candidatos`

Selección determinista, según la sección 8.2 de `ARQUITECTURA.md`.

**Entra un vídeo** si cumple a la vez:
- Es relevante.
- Es de formato largo.
- Está dentro de la ventana.
- Todavía no tiene ficha.
- Tiene interés `medio` o `alto`, **o** su tema aparece en vídeos relevantes de 2 o más canales.

**Orden:**
1. Interés.
2. Número de canales con ese tema.
3. Múltiplo de la mediana.

Se toman `youtube.candidatos_por_ejecucion` vídeos. Para cada candidato se completan los metadatos con `yt-dlp -J <url-del-vídeo>` (fecha exacta, descripción, likes, comentarios) y se recalculan `dias` e `interaccion`. La lista se guarda en el informe de la ejecución y se muestra junto a sus señales, su `formula_titulo` y el motivo por el que entra cada uno. El informe incluye además `formulas_dominantes_interes_alto`: el recuento de fórmulas de título entre todos los vídeos con interés alto de la ejecución (qué patrón domina en el nicho), ordenado de más a menos vídeos.

### `clasificar-titulos`

Comando ligero, sin `yt-dlp`: reprocesa los `meta.json` existentes y guarda la `formula_titulo` de cada vídeo (útil para vídeos recogidos antes de que existiera el clasificador o tras cambiar `references/formulas-titulo.json`). No toca estadísticas, señales, relevancia, transcripciones ni fichas, e imprime el recuento de fórmulas dominantes entre los vídeos de interés alto.

### `subtitulos <video_id>…`

- Descarga los subtítulos con `yt-dlp` sin descargar el vídeo. Orden de preferencia: manuales en cada idioma de `youtube.idiomas_subtitulos` y después automáticos en el mismo orden.
- Si `yt-dlp` falla con HTTP 429, reintenta con pausa creciente según la configuración de `red`; si sigue fallando, prueba la vía alternativa con `youtube-transcript-api` (misma preferencia: manuales antes que automáticos, en el orden de idiomas) y guarda su resultado como VTT en la carpeta del vídeo, para que la limpieza sea la misma.
- Guarda el VTT original.
- Genera `transcripcion.md` limpio:
  - Quita etiquetas y estilos.
  - Elimina las líneas repetidas que producen los subtítulos automáticos.
  - Agrupa el texto en párrafos con su marca de tiempo `[mm:ss]` aproximadamente cada 30 segundos.
- Un vídeo que ya tiene transcripción no se vuelve a descargar.
- Si no hay subtítulos, lo marca en `meta.json` con su motivo. **Nunca inventes el contenido.**

### `pendientes-ficha`

Lista los vídeos que tienen transcripción y no tienen ficha, o cuya ficha no coincide con la huella de la transcripción.

Incluye también `subtemas_existentes`: los subtemas de las fichas propias (`biblioteca/substack/fichas/*.json`) y de las fichas de vídeo ya guardadas, con su frecuencia, ordenados de más a menos usados. Es el vocabulario que quien redacta la ficha debe reutilizar.

### `guardar-ficha <video_id> <archivo.json>`

1. Combina los campos de juicio del modelo con los datos objetivos de `meta.json`: `id`, `fuente`, `url`, `autor`, `fecha`, `huella` y `senales`. El modelo no puede modificar esos datos.
2. Valida la ficha con `ficha-externa.schema.json`, usando la biblioteca estándar.
3. La escribe de forma atómica.

Si la validación falla, no escribe nada y explica qué campo falla.

### `mapa`

Regenera `biblioteca/youtube/mapa-videos.md` a partir de todas las fichas de vídeo (`biblioteca/youtube/videos/*/ficha.json`) y sus `meta.json`. Es la vista legible por humanos de lo que las fichas han capturado, sin navegar JSONs. Una ficha solo cuenta si su huella coincide con la transcripción actual; si no, el vídeo aparece como pendiente.

- **Cabecera:** fecha de generación, número de fichas y número de vídeos recogidos sin ficha.
- **Por cada tema**, en orden alfabético: número de vídeos, canales, y por cada vídeo (ordenados por fecha y después por id): fecha, título con enlace, canal, señales (múltiplo de la mediana, interés, días, fórmula de título), su **tesis**, qué **demuestra**, qué **promete sin demostrar** y sus **preguntas abiertas**.
- **Sección "Fórmulas dominantes entre los vídeos de interés alto"**: recuento breve de `formula_titulo` entre los vídeos con interés alto, con la advertencia de que la fórmula clasifica las palabras del título, no el porqué real del éxito. La fórmula se calcula al vuelo desde el título, así que el mapa funciona también con vídeos recogidos antes de que existiera el clasificador.
- **Sección final:** vídeos candidatos sin ficha todavía —con transcripción pendiente de ficha (o con la ficha desactualizada) o marcados sin subtítulos—, con su motivo, para que el mapa no parezca completo.
- La salida es determinista: los mismos datos producen el mismo archivo, byte a byte. Se escribe de forma atómica y el comando no llama a `yt-dlp`.

### Informe de ejecución

Cada comando que cambia datos lo registra en `control/ejecuciones/<run_id>.json`:
- `run_id` en UTC con formato `YYYYMMDDTHHMMSSZ`.
- Canales pedidos, correctos y fallidos, con motivo.
- Vídeos nuevos y actualizados.
- Candidatos.
- Subtítulos obtenidos y no disponibles.
- Fichas guardadas.
- Llamadas a `yt-dlp` realizadas.

**Códigos de salida:**
- `0`: correcto.
- `1`: errores parciales.
- `2`: no pudo ejecutarse.

Un fallo nunca se presenta como "sin vídeos nuevos".

## 5. Flujo que describe SKILL.md

1. `recoger`.
2. **Relevancia.** `relevancia-pendiente`; el modelo clasifica todos los vídeos en una sola respuesta siguiendo `instrucciones-relevancia.md`; después, `guardar-relevancia`.
3. `candidatos`.
4. `subtitulos` de los candidatos.
5. **Fichas.** `pendientes-ficha`; el modelo lee cada transcripción completa y redacta su ficha siguiendo `instrucciones-ficha-video.md`; después, `guardar-ficha`.
   - Con varios vídeos se puede usar un subagente por vídeo, en paralelo. Cada subagente recibe la transcripción y las instrucciones, y devuelve solo el JSON de la ficha.
6. **`mapa`.** Regenera `biblioteca/youtube/mapa-videos.md` con las fichas nuevas, para que la vista humana quede al día.
7. **Informar:** canales fallidos, candidatos, vídeos sin subtítulos y fichas creadas.

## 6. Criterios del modelo

**`instrucciones-relevancia.md`:**
- **Relevante** es lo que encaja con `linea_editorial.nicho` y tiene utilidad para `linea_editorial.audiencia`. El número de visualizaciones no cuenta en esta decisión.
- **Fuera de alcance:** un vídeo cuyo único ángulo cae de lleno en `recursos.fuera_de_alcance` se marca `relevante: false` con el motivo "fuera de alcance: <qué>"; si además tiene un ángulo aprovechable en texto o proceso, sigue siendo relevante por ese ángulo.
- `tema`: reutiliza uno existente si encaja; crea uno nuevo solo si ninguno sirve.
- `motivo`: una frase.
- Con título y descripción ambiguos, se marca `relevante: true` con el motivo "requiere ver contenido". Es preferible revisar de más a perder una oportunidad; la regla de fuera de alcance solo se aplica cuando el único ángulo es claro.

**`instrucciones-ficha-video.md`:** criterios para cada campo de la ficha externa de la sección 6 de `ARQUITECTURA.md`.
- `subtemas`: de 1 a 6 subtemas cortos y generales (2-4 palabras), reutilizando el vocabulario de `subtemas_existentes` que devuelve `pendientes-ficha`; un subtema nuevo solo si ninguno sirve. Las fichas propias tienen `subtemas` y el cruce de `detectar-oportunidades` compara los dos lados, así que el campo es obligatorio en el esquema.
- `tesis`: lo que defiende el vídeo, no su título.
- `afirmaciones`: las importantes, cada una con la marca de tiempo de la transcripción y su tipo (`dato`, `demostración` u `opinión`).
- `demuestra`: solo lo que se enseña funcionando en el vídeo.
- `promete_sin_demostrar`: lo que afirma sin enseñarlo o sin fuente. Es materia prima para aportar algo distinto.
- `entidades`: con nombre canónico, como en las fichas propias.
- `preguntas_abiertas`: lo que el vídeo no resuelve y un lector se preguntaría.
- Si la transcripción es automática y confusa en un punto, se indica en lugar de interpretarlo.

## 7. Pruebas

Escríbelas con `unittest`. Inyecta la función que invoca `yt-dlp` para usar respuestas simuladas (JSON de listado plano, JSON de vídeo individual) y archivos VTT de ejemplo en una carpeta temporal. Nunca accedas a internet.

Deben comprobar que:
1. `canales.md` se interpreta con handles y con IDs de canal, ignora el texto y una URL no válida falla solo para ese canal.
2. `recoger` guarda `meta.json` y `metricas.jsonl`. Repetirlo no duplica vídeos y añade una nueva captura de métricas sin tocar la relevancia, la transcripción ni la ficha.
3. Un canal con error, sea inexistente o con fallo de red, queda registrado; los demás continúan, se conservan sus datos anteriores y el código de salida es 1.
4. Las señales son correctas:
   - La mediana excluye vídeos cortos y de menos de 7 días.
   - El múltiplo y el nivel de interés se calculan bien.
   - Los likes ocultos no rompen el cálculo.
   - Un canal con pocos vídeos se marca como poco fiable.
5. La duración se interpreta bien tanto si llega en segundos como si llega como `null` (vídeo en directo o sin dato), sin romper los filtros.
6. `candidatos` respeta los filtros, la regla de 2 o más canales, el orden, el límite y excluye vídeos con ficha.
7. La limpieza del VTT elimina repeticiones de subtítulos automáticos y conserva todo el texto y las marcas de tiempo.
8. Un vídeo sin subtítulos queda marcado y no genera transcripción.
9. `guardar-relevancia` y `guardar-ficha` rechazan datos no válidos sin escribir, y `guardar-ficha` impone los datos objetivos.
10. Si `yt-dlp` no está disponible, el script termina con código 2 y no modifica nada, indicando cómo instalarlo.
11. `mapa` es determinista (dos ejecuciones con los mismos datos producen bytes idénticos), incluye la tesis, lo que demuestra y lo que promete sin demostrar de cada ficha, y lista los vídeos candidatos sin ficha todavía.
12. El clasificador de fórmulas de título: títulos de ejemplo que caen en fórmulas distintas (y uno sin clasificar), `formula_titulo` presente en `meta.json` tras `recoger`, el recuento de fórmulas dominantes en `candidatos` y la fórmula con su sección de dominantes en `mapa`.
13. `relevancia-pendiente` incluye la `linea_editorial`, los `recursos` (con `fuera_de_alcance`) y los temas existentes.
14. Una ficha con `subtemas` válidos se guarda; sin `subtemas` o con más de 6 se rechaza sin escribir. `pendientes-ficha` devuelve `subtemas_existentes` con las frecuencias de las fichas propias y de las fichas de vídeo guardadas.

Ejecuta las pruebas y muestra el resultado.

Para comprobar las instrucciones del modelo, usa una transcripción ficticia: rellena tú mismo su ficha siguiendo `instrucciones-ficha-video.md`, guárdala con `guardar-ficha` y muestra el resultado. Todo ocurre en la carpeta temporal de pruebas, nunca en `biblioteca/`.

## 8. Documentación

- Actualiza en `README.md` la fila del prompt 03 a `hecho` y explica que solo hace falta `yt-dlp` instalado (sin claves de API).
- No modifiques `ARQUITECTURA.md`. Si algo obliga a cambiar el diseño, indícalo al final como propuesta.

## 9. Entrega

Muestra:
- El árbol de la skill.
- `SKILL.md` y las dos instrucciones.
- El resultado de las pruebas y la ficha de ejemplo.
- Los comandos para la primera ejecución real.

Separa lo comprobado con datos simulados de lo que solo se sabrá con la ejecución real; por ejemplo, la disponibilidad de subtítulos o qué campos devuelve exactamente el listado plano de `yt-dlp` según el canal.
