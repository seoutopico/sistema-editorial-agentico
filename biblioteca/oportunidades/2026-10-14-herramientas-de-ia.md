---
id: 2026-10-14-herramientas-de-ia
estado: descartada
motivo_estado: "Exige GPU/hardware que la autora no tiene; aportación no ejecutable con sus recursos (decisión de Aina, 2026-10-14)"
tema: Herramientas de IA
grupo_id: herramientas-de-ia
interes: alto
canales: 2
cobertura: ampliación
evidencias: [youtube:4_fM3Nv8BB0@02:04, youtube:4_fM3Nv8BB0@02:35, youtube:4_fM3Nv8BB0@03:38, youtube:4_fM3Nv8BB0@05:13, youtube:4_fM3Nv8BB0@08:20, youtube:4_fM3Nv8BB0@10:25, youtube:4_fM3Nv8BB0@11:29, youtube:4_fM3Nv8BB0@13:02, youtube:4_fM3Nv8BB0@15:39, youtube:AwYYpXfFM9k@03:07, youtube:AwYYpXfFM9k@04:09, youtube:AwYYpXfFM9k@05:42, youtube:AwYYpXfFM9k@06:43, youtube:AwYYpXfFM9k@07:15, youtube:AwYYpXfFM9k@08:48, youtube:AwYYpXfFM9k@11:56, youtube:AwYYpXfFM9k@15:34, youtube:AwYYpXfFM9k@16:36, youtube:AwYYpXfFM9k@19:11, youtube:AwYYpXfFM9k@20:44, youtube:AwYYpXfFM9k@12:57, youtube:AwYYpXfFM9k@21:47, youtube:ZqkljdI1HT0@00:02, youtube:ZqkljdI1HT0@01:04, youtube:ZqkljdI1HT0@01:35, youtube:ZqkljdI1HT0@02:37, youtube:ZqkljdI1HT0@03:51, youtube:ZqkljdI1HT0@09:37, youtube:ZqkljdI1HT0@13:13, youtube:ZqkljdI1HT0@14:15, youtube:ZqkljdI1HT0@15:16, youtube:ZqkljdI1HT0@15:47, youtube:ZqkljdI1HT0@16:50, youtube:ZqkljdI1HT0@17:50, youtube:ZqkljdI1HT0@18:23, youtube:ZqkljdI1HT0@18:54]
relacionados: [substack:177779518, substack:179631597, substack:183914023, substack:184848409, substack:217023771]
---
## La oportunidad

Un modelo abierto gratuito (Qwen 3.8) ejecutado 100% en local en una GPU de consumo ya compite en trabajo agéntico real con modelos de pago, pero la demostración pública se hizo en una RTX 5090 de gama altísima y la promesa de que vale "desde 8 GB de VRAM" quedó sin probar. Verificar esa promesa en un equipo que la audiencia sí tiene, contando el proceso completo con lo que funciona y lo que no, es justo nuestro terreno. Ojo: el grupo mezcla tres vídeos de temas distintos (tutor por voz de Gemini 3.8 Live, modelo de decisión Jev y modelo local); esta propuesta se ciñe al ángulo del modelo local, que es el no cubierto con aportación más clara. El tutor de Gemini 3.8 Live podría ser una pieza aparte; Jev ya lo publicamos.

## Por qué ahora (evidencias)

Interés alto en el grupo (3 fichas, 2 canales, múltiplo de mediana hasta 3,82, última fecha 2026-09-21). Qwen 3.8 ocupa 17 GB, es gratuito y puntúa por delante de modelos de pago según Artificial Analysis (youtube:ZqkljdI1HT0@00:02). En las pruebas del vídeo, ejecutado en local (RTX 5090, LM Studio + Hermes), entrega una web funcional donde Gemini 3.7 Flash solo entrega un mockup (youtube:ZqkljdI1HT0@09:37) y su Excel recalcula bien al cambiar la fecha de referencia mientras el de Gemini se queda congelado (youtube:ZqkljdI1HT0@15:16). Se afirma que con una GPU desde 8 GB de VRAM ya se puede probar (youtube:ZqkljdI1HT0@02:37) y que viene mal configurado de fábrica: con razonamiento al máximo, 21 minutos para un encargo que apagándolo lleva 2 (youtube:ZqkljdI1HT0@16:50).

## Qué hemos publicado y qué falta

Ya cubrimos Jev con prueba propia y comparativa de coste (biblioteca/substack/articulos/2026-09-27-jev-typesafe-que-es-como-funciona.md), herramientas de Google con pruebas propias —Nano Banana (biblioteca/substack/articulos/2025-11-02-4-y-la-maquina-dibujo-exactamente.md), Nano Banana Pro (biblioteca/substack/articulos/2026-01-21-nano-banana-pro-prompts.md), RAG con NotebookLM+Gemini (biblioteca/substack/articulos/2026-01-18-rag-notebooklm-gemini.md)— y la idea de elegir modelo según la tarea (biblioteca/substack/articulos/2025-11-23-7-se-infiel-a-chatgpt.md). Falta todo lo relativo a ejecutar un modelo abierto en local para trabajo real: qué hardware hace falta de verdad, cómo se configura y hasta dónde llega frente a la nube. Tampoco hemos tratado el tutor por voz con pantalla compartida de Gemini 3.8 Live (youtube:4_fM3Nv8BB0), que queda fuera de esta propuesta como posible pieza aparte.

## Qué aportaríamos

Una prueba propia de Qwen 3.8 en hardware modesto (GPU de 8-16 GB de VRAM, no una RTX 5090) con una tarea real nuestra, documentando el proceso completo: instalación y configuración de LM Studio, el ajuste del razonamiento que el vídeo dice que viene mal de fábrica (youtube:ZqkljdI1HT0@16:50), qué cuantización cabe en esa VRAM, velocidad real en tokens por segundo y comparación del resultado con el mismo encargo en un modelo de pago. El resultado contrasta una promesa concreta que el vídeo no demuestra (usable desde 8 GB, youtube:ZqkljdI1HT0@02:37) y responde la pregunta útil para la audiencia: ¿el modelo que puedes ejecutar en el PC que ya tienes resuelve tu problema?

## Qué hay que investigar o probar

- Verificar que Qwen 3.8 arranca y es usable en una GPU de 8-16 GB: el vídeo lo afirma (youtube:ZqkljdI1HT0@02:37) pero todas sus pruebas son en una RTX 5090.
- Medir velocidad real: el vídeo cita 15-30 tokens/s por defecto y hasta 70 optimizado en una 4090 (youtube:ZqkljdI1HT0@17:50), cifras citadas y no mostradas.
- Reproducir el problema de configuración del razonamiento referido de Simon Willison (youtube:ZqkljdI1HT0@16:50) y documentar el ajuste correcto.
- Contrastar las posiciones de los índices de Artificial Analysis y Gerganov (youtube:ZqkljdI1HT0@00:02, youtube:ZqkljdI1HT0@01:04), mostradas como tablas sin verificar.
- Calcular el coste real del montaje local frente a una suscripción, pregunta que el propio vídeo deja abierta.

## Riesgos

La promesa central (usable desde 8 GB) puede resultar falsa o quedarse en algo inusable en la práctica; sería igualmente publicable como "lo que no funciona", pero cambia el enfoque. Las pruebas del vídeo son una sola ejecución por modelo y auditadas por Opus 5, un modelo de la competencia, así que las comparativas de partida son frágiles. El tema caduca rápido: los modelos locales se suceden cada pocas semanas y la ventana para que la prueba sea relevante es corta. Requiere disponer de una GPU de la gama objetivo para que la prueba sea honesta.
