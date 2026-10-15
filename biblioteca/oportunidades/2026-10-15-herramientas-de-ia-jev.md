---
id: 2026-10-15-herramientas-de-ia-jev
estado: propuesta
motivo_estado: ""
tema: Herramientas de IA
grupo_id: herramientas-de-ia-jev
interes: alto
canales: 3
cobertura: ampliación
evidencias: [youtube:AwYYpXfFM9k@03:07, youtube:AwYYpXfFM9k@04:09, youtube:AwYYpXfFM9k@05:42, youtube:AwYYpXfFM9k@06:43, youtube:AwYYpXfFM9k@07:15, youtube:AwYYpXfFM9k@08:48, youtube:AwYYpXfFM9k@11:56, youtube:AwYYpXfFM9k@15:34, youtube:AwYYpXfFM9k@16:36, youtube:AwYYpXfFM9k@19:11, youtube:AwYYpXfFM9k@20:44, youtube:AwYYpXfFM9k@12:57, youtube:AwYYpXfFM9k@21:47, youtube:tYugqJ9YytQ@00:00, youtube:tYugqJ9YytQ@00:30, youtube:tYugqJ9YytQ@01:33, youtube:tYugqJ9YytQ@02:37, youtube:tYugqJ9YytQ@06:13, youtube:tYugqJ9YytQ@05:43, youtube:tYugqJ9YytQ@12:31, youtube:tYugqJ9YytQ@13:34, youtube:tYugqJ9YytQ@08:22, youtube:tYugqJ9YytQ@16:10, youtube:tYugqJ9YytQ@16:42, youtube:tYugqJ9YytQ@17:44, youtube:tYugqJ9YytQ@25:01, youtube:tYugqJ9YytQ@27:07, youtube:tYugqJ9YytQ@27:37, youtube:tYugqJ9YytQ@23:58, youtube:ymgH8jS6Wb8@01:32, youtube:ymgH8jS6Wb8@01:02, youtube:ymgH8jS6Wb8@02:34, youtube:ymgH8jS6Wb8@03:35, youtube:ymgH8jS6Wb8@06:09, youtube:ymgH8jS6Wb8@06:40, youtube:ymgH8jS6Wb8@10:15, youtube:ymgH8jS6Wb8@08:42, youtube:ymgH8jS6Wb8@14:53, youtube:ymgH8jS6Wb8@12:48, youtube:ymgH8jS6Wb8@04:06, youtube:ymgH8jS6Wb8@15:23]
relacionados: [substack:179631597, substack:188057916, substack:189540705, substack:214284185, substack:217023771]
---
## La oportunidad

Jev, el clasificador de propósito general de TypeSafe, ha pasado en un mes de curiosidad a patrón de arquitectura: tres canales distintos lo tratan como pieza nueva de la caja de herramientas, desde el enrutado a modelos baratos hasta la tesis del "tercer primitivo del software". Nosotros ya lo probamos y publicamos, pero con una prueba de juguete; el artículo cerró anunciando llevarlo a nuestros procesos y esa continuación sigue pendiente. La oportunidad es entregarla: Jev a escala real dentro de nuestro propio sistema editorial, midiendo lo que nadie muestra, la precisión.

## Por qué ahora (evidencias)

Interés alto en el grupo: 3 fichas de 3 canales, múltiplo de mediana hasta 3,82, fichas de 2026-09-19 y 2026-09-21. Jev conserva la comprensión de contexto de un LLM pero salta directo a la clasificación sin generar tokens (youtube:AwYYpXfFM9k@03:07) y cobra solo la entrada, con salida gratis (youtube:AwYYpXfFM9k@07:15). Demostraciones en directo: clasifica los vídeos de un canal más rápido y con menos errores que GPT-5.6 Luna por 0,00046 frente a 0,015 de coste (youtube:AwYYpXfFM9k@15:34) y 1.000 correos con siete reglas en ~70 segundos por 9 centavos frente a 5 minutos y 62 centavos (youtube:ymgH8jS6Wb8@06:09), bajando a 6 segundos tras paralelizar (youtube:ymgH8jS6Wb8@06:40). Fue el modelo de adopción más rápida en la historia de Vercel AI Gateway (youtube:tYugqJ9YytQ@00:30) y los patrones propuestos (triaje de entrada, filtro previo al LLM caro, verificación de acciones de agentes, columnas que juzgan) están formulados en youtube:tYugqJ9YytQ@13:34 y youtube:ymgH8jS6Wb8@04:06.

## Qué hemos publicado y qué falta

Ya publicamos Jev con prueba propia (biblioteca/substack/articulos/2026-09-27-jev-typesafe-que-es-como-funciona.md): qué es, por qué hay que explicitar criterios y definiciones, y una comparativa de coste y velocidad contra GPT-5.5 sobre 8 casos. También defendimos elegir modelo por tarea (biblioteca/substack/articulos/2025-11-23-7-se-infiel-a-chatgpt.md). Falta todo lo que va de la demo al proceso: clasificación a escala (cientos o miles de elementos, no 8), el patrón de enrutado donde Jev filtra y el modelo caro solo procesa lo que pasa el corte, y sobre todo la evaluación de precisión con un conjunto de referencia etiquetado, que ningún vídeo ni nuestro artículo midió. Nuestro propio cierre ("quiero ver si puedo aprovechar Jev en alguno de los procesos que ya tengo montados... ya te contaré") quedó sin entregar.

## Qué aportaríamos

La prueba que falta en todas las fuentes: Jev dentro de un sistema editorial real. Clasificar las fichas y artículos de nuestra biblioteca según nuestros criterios editoriales (tema, nivel, interés), con un conjunto de referencia de ~100 casos etiquetados a mano para medir precisión además de coste y velocidad, comparando contra el LLM que usamos hoy. Y montar el patrón de enrutado (Jev decide qué merece pasar al modelo caro) midiendo cuánto baja la factura del proceso completo y qué errores de clasificación cuesta. Texto, proceso y cifras propias, ejecutable vía API sin hardware, en una semana.

## Qué hay que investigar o probar

- La precisión real frente a un LLM sobre los mismos datos etiquetados: todas las demos muestran coste y velocidad, ninguna calidad (youtube:ymgH8jS6Wb8@12:48 lo recomienda pero no lo hace).
- Los multiplicadores anunciados (20-200x velocidad, 40-400x coste, youtube:ymgH8jS6Wb8@02:34; ~100x del lanzamiento, youtube:tYugqJ9YytQ@27:07) salen del fabricante: contrastarlos con nuestras mediciones.
- El límite de 64.000 tokens de entrada (youtube:ymgH8jS6Wb8@03:35): si obliga a trocear fichas largas y con qué efecto.
- Dónde está el umbral en que la clasificación ambigua exige razonamiento de LLM (pregunta abierta en las tres fichas).
- El precio publicado de 4,2 céntimos por millón de tokens de entrada (youtube:tYugqJ9YytQ@25:01).

## Riesgos

Las cifras espectaculares de terceros (34x más barato en documentos fiscales, 20.000 correos por 1 dólar, youtube:tYugqJ9YytQ@16:10 y @16:42) son reportes sin verificación independiente y no deben repetirse como hechos. Jev es un proveedor único y pequeño (TypeSafe): la pieza no debe recomendar construir sobre él sin señalar esa dependencia, aunque ya aparecen alternativas open source (youtube:AwYYpXfFM9k@21:47). Riesgo de autoplagio: la pieza solo vale si entrega lo que la de septiembre no tenía (escala, precisión, enrutado); si la precisión resulta mala, el resultado sigue siendo publicable como "lo que no funciona". Un error de clasificación en decisiones con riesgo puede costar más que el ahorro (el bot de trading que perdió 30.000 dólares, youtube:AwYYpXfFM9k@20:44).
