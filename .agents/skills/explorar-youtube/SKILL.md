---
name: explorar-youtube
description: Recorre los canales de biblioteca/youtube/canales.md con yt-dlp, mide qué vídeos destacan dentro de su propio canal, clasifica su relevancia editorial, lee los subtítulos de los candidatos y guarda una ficha externa por vídeo. Úsala para saber qué se está publicando en el nicho o como paso previo a detectar-oportunidades.
---

# explorar-youtube

Primera parte de la fase 2 del sistema editorial (ver `ARQUITECTURA.md`,
secciones 2, 4, 5, 6, 8.2 y 10). El script hace lo repetible (listar canales,
calcular señales, seleccionar candidatos, descargar y limpiar subtítulos,
validar y guardar); el modelo solo el juicio (clasificar relevancia y rellenar
fichas). El modelo nunca escribe en `biblioteca/`: entrega un JSON y el script
lo valida y lo guarda.

Los criterios del modelo están en `references/instrucciones-relevancia.md` y
`references/instrucciones-ficha-video.md`; el esquema de la ficha, en
`references/ficha-externa.schema.json`; las fórmulas de título, en
`references/formulas-titulo.json` (~18 fórmulas con nombre en castellano y
patrones regex para títulos en español e inglés).

## Qué necesita

- `yt-dlp` instalado (`pip install yt-dlp`). **Sin claves de API**: toda la
  información de YouTube (listados, metadatos, subtítulos) sale de `yt-dlp`.
  Si falta, el script termina con código 2 sin tocar nada.
- `youtube-transcript-api` (opcional): vía alternativa de subtítulos que entra
  en juego automáticamente cuando `yt-dlp` falla (p. ej. límite HTTP 429).
- `proyecto.config.json` (bloques `linea_editorial`, `recursos` y `youtube`) y
  `biblioteca/youtube/canales.md` (un canal por línea; no se modifica).

## Qué escribe

- `biblioteca/youtube/videos/<video_id>/` — una única carpeta por vídeo:
  `meta.json` (datos, señales, relevancia), `subtitulos.<idioma>.vtt`,
  `transcripcion.md` y `ficha.json`.
- `biblioteca/youtube/mapa-videos.md` — vista legible por humanos de las
  fichas, por temas (comando `mapa`).
- `biblioteca/youtube/control/metricas.jsonl` — una línea por vídeo y captura.
- `biblioteca/youtube/control/ejecuciones/<run_id>.json` — informe de cada
  comando que cambia datos.

## Flujo

Todos los comandos se ejecutan desde la raíz del proyecto:

```bash
python .agents/skills/explorar-youtube/scripts/explorar_youtube.py <comando>
```

1. **`recoger`.** Lista cada canal, guarda `meta.json` y las métricas y
   calcula las señales y la `formula_titulo` de cada vídeo. Repetirlo solo
   actualiza estadísticas, señales y fórmula.
2. **Relevancia.** `relevancia-pendiente` devuelve los vídeos sin clasificar
   junto con la `linea_editorial`, los `recursos` de la configuración (con
   `fuera_de_alcance`, para descartar lo que la publicación no puede
   aprovechar) y los temas existentes; el modelo clasifica todos los vídeos
   en una sola respuesta siguiendo `instrucciones-relevancia.md`; después,
   `guardar-relevancia <archivo.json>`.
3. **`candidatos`.** Selección determinista; completa los metadatos de los
   elegidos con `yt-dlp` y muestra cada uno con sus señales, su fórmula de
   título y su motivo, más el recuento de fórmulas dominantes entre los
   vídeos con interés alto (`formulas_dominantes_interes_alto`).
4. **`subtitulos <video_id>…`** de los candidatos. Prefiere subtítulos
   manuales a automáticos, en el orden de idiomas configurado, y genera
   `transcripcion.md` limpio. Si `yt-dlp` falla (p. ej. HTTP 429), reintenta
   con pausa creciente y después prueba la vía alternativa con
   `youtube-transcript-api`. Si no hay subtítulos, lo marca con su motivo;
   nunca se inventa el contenido.
5. **Fichas.** `pendientes-ficha` lista los vídeos con transcripción y sin
   ficha al día, más `subtemas_existentes` (los subtemas de las fichas propias
   y de las fichas de vídeo guardadas, con frecuencias, para reutilizar el
   vocabulario de la biblioteca); el modelo lee cada transcripción completa y
   redacta su ficha siguiendo `instrucciones-ficha-video.md`; después,
   `guardar-ficha <video_id> <archivo.json>`. Con varios vídeos se puede usar
   un subagente por vídeo, en paralelo: cada subagente recibe la transcripción
   y las instrucciones y devuelve solo el JSON de la ficha.
6. **`mapa`.** Regenera `biblioteca/youtube/mapa-videos.md` a partir de las
   fichas al día y sus `meta.json`: cabecera con fecha y cobertura, un bloque
   por tema (vídeos con fecha, enlace, canal, señales, fórmula de título,
   tesis, qué demuestra, qué promete sin demostrar y preguntas abiertas), la
   sección "Fórmulas dominantes entre los vídeos de interés alto" y la lista
   de vídeos candidatos sin ficha todavía, para que el mapa no parezca
   completo. Es determinista y no llama a `yt-dlp`.
7. **Informar:** canales fallidos, candidatos, vídeos sin subtítulos y fichas
   creadas.

## Cómo interpretar el informe

Cada ejecución queda en `control/ejecuciones/<run_id>.json` con los canales
pedidos, correctos y fallidos (con motivo), los vídeos nuevos y actualizados,
los candidatos, los subtítulos obtenidos y no disponibles, las fichas
guardadas y las llamadas a `yt-dlp`. Señales por vídeo en `meta.json`:

- `multiplo_mediana`: visualizaciones / mediana de los vídeos largos del
  canal con 7 días o más. `interes`: alto ≥ 2, medio entre 1 y 2, bajo < 1.
- `senal_incompleta`: menos de 7 días (o sin fecha); interés `sin_datos`.
- `mediana_poco_fiable`: el canal tiene menos de 5 vídeos válidos.
- `interaccion`: (likes + comentarios) / visualizaciones; `null` hasta tener
  metadatos completos o si los likes están ocultos (ver
  `interaccion_motivo`).
- `formula_titulo`: fórmula de título según `references/formulas-titulo.json`
  (gana la de más patrones coincidentes; sin coincidencias, `sin clasificar`).
  **Honestidad por diseño**: clasifica las palabras del título, no el porqué
  real del éxito del vídeo; úsala como mapa del nicho, no como receta. El
  comando ligero `clasificar-titulos` (sin `yt-dlp`) reprocesa los
  `meta.json` existentes tras cambiar las fórmulas o para vídeos antiguos.

Códigos de salida: `0` correcto, `1` errores parciales (los datos válidos se
conservan y el informe dice qué falló), `2` no pudo ejecutarse. Un fallo nunca
se presenta como "sin vídeos nuevos".

## Pruebas

```bash
python -m unittest discover .agents/skills/explorar-youtube/scripts -v
```

Inyectan una función simulada en lugar de `yt-dlp` y trabajan en una carpeta
temporal; nunca tocan `biblioteca/` ni la red.
