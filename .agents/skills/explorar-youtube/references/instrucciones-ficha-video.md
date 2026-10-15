# Instrucciones: rellenar la ficha de un vídeo

Entrada: la transcripción completa (`transcripcion.md`, párrafos con marcas
`[mm:ss]`) de un vídeo listado por `pendientes-ficha`. Salida: un JSON solo
con los campos de juicio; los datos objetivos (`id`, `fuente`, `url`, `autor`,
`fecha`, `huella`, `senales`) los impone el script desde `meta.json` y no se
pueden modificar.

```json
{
  "tema": "…",
  "subtemas": ["…"],
  "tesis": "…",
  "afirmaciones": [
    { "texto": "…", "marca": "12:34", "tipo": "dato" }
  ],
  "entidades": ["…"],
  "demuestra": "…",
  "promete_sin_demostrar": "…",
  "preguntas_abiertas": ["…"],
  "avisos_transcripcion": ["…"]
}
```

## Criterios por campo

- **`tema`**: reutiliza el tema asignado en la relevancia o uno existente si
  encaja; mismo vocabulario que las fichas propias.
- **`subtemas`**: de 1 a 6 subtemas cortos y generales (2-4 palabras), los
  aspectos concretos que trata el vídeo dentro del tema (por ejemplo
  "rediseño de procesos antes de automatizar", no "IA" ni una frase entera).
  La salida de `pendientes-ficha` incluye `subtemas_existentes`, el
  vocabulario de la biblioteca (fichas propias y fichas de vídeo guardadas)
  con sus frecuencias: **reutiliza un subtema existente siempre que encaje**
  y crea uno nuevo solo si ninguno sirve. El cruce con los artículos propios
  de `detectar-oportunidades` compara subtemas de ambos lados, así que un
  sinónimo innecesario es una oportunidad perdida.
- **`tesis`**: lo que defiende el vídeo, no su título. Una frase.
- **`afirmaciones`**: las importantes, cada una con la marca de tiempo de la
  transcripción (`marca`, formato `mm:ss`) y su `tipo`:
  - `dato`: cifra o hecho comprobable que se cita.
  - `demostración`: algo que se enseña funcionando en pantalla.
  - `opinión`: juicio del autor sin dato ni demostración detrás.
- **`demuestra`**: solo lo que se enseña funcionando en el vídeo. Si no
  demuestra nada, una cadena vacía.
- **`promete_sin_demostrar`**: lo que afirma sin enseñarlo o sin fuente. Es
  materia prima para aportar algo distinto. Si no hay nada, cadena vacía.
- **`entidades`**: herramientas, productos, modelos y personas, con su nombre
  canónico, como en las fichas propias (por ejemplo "Claude Code", no
  "claude code CLI").
- **`preguntas_abiertas`**: lo que el vídeo no resuelve y un lector de la
  publicación se preguntaría.
- **`avisos_transcripcion`** (opcional): si la transcripción es automática y
  es confusa en un punto, indícalo aquí con su marca de tiempo en lugar de
  interpretarlo. Nunca inventes contenido que la transcripción no soporta.

Después, guarda el JSON en un archivo y ejecuta
`guardar-ficha <video_id> <archivo.json>`. Si la validación falla, el script
explica qué campo falla y no escribe nada: corrige y repite.
