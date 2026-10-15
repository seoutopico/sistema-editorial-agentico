---
id: 2026-10-14-agentes-de-ia
estado: propuesta
motivo_estado: ""
tema: Agentes de IA
grupo_id: agentes-de-ia
interes: alto
canales: 2
cobertura: ampliación
evidencias: [youtube:1qGH6NwTj3o@01:33, youtube:1qGH6NwTj3o@00:32, youtube:1qGH6NwTj3o@03:35, youtube:1qGH6NwTj3o@04:35, youtube:1qGH6NwTj3o@08:39, youtube:1qGH6NwTj3o@09:10, youtube:1qGH6NwTj3o@10:11, youtube:1qGH6NwTj3o@10:42, youtube:1qGH6NwTj3o@15:18, youtube:1qGH6NwTj3o@18:52, youtube:1qGH6NwTj3o@19:23, youtube:1qGH6NwTj3o@22:27, youtube:1qGH6NwTj3o@25:30, youtube:1qGH6NwTj3o@26:01, youtube:ZnlLfKR-vDQ@00:03, youtube:ZnlLfKR-vDQ@02:08, youtube:ZnlLfKR-vDQ@02:40, youtube:ZnlLfKR-vDQ@06:21, youtube:ZnlLfKR-vDQ@07:55, youtube:ZnlLfKR-vDQ@08:58, youtube:ZnlLfKR-vDQ@10:32, youtube:ZnlLfKR-vDQ@11:34, youtube:ZnlLfKR-vDQ@11:04, youtube:ZnlLfKR-vDQ@13:08, youtube:ZnlLfKR-vDQ@14:40, youtube:ZnlLfKR-vDQ@14:09, youtube:ZnlLfKR-vDQ@15:43, youtube:ZnlLfKR-vDQ@17:17]
relacionados: [substack:178260057, substack:183644091, substack:195602355, substack:206663634, substack:219821904]
---
## La oportunidad

La "carpeta de agente" portable (AGENTS.md + contexto + skills + memoria + proyectos) ha saltado de la terminal a las herramientas de consumo: Mitjana la demuestra cargándola como proyecto en ChatGPT y repitiendo el trabajo con la misma carpeta en Claude Cowork, y Nate B Jones defiende que el siguiente paso es delegar áreas permanentes de responsabilidad. Nosotros llevamos meses defendiendo exactamente esa idea (el criterio en archivos aguanta el cambio de herramienta), pero siempre en terminal: podemos probar el flujo sin terminal y verificar lo que ninguno de los dos vídeos demuestra.

## Por qué ahora (evidencias)

Dos canales distintos con interés alto (múltiplo 6.24 el mejor) y fichas de 2026-09-06 y 2026-09-20. Mitjana demuestra el flujo completo: carga la carpeta como proyecto en ChatGPT y el modelo pregunta en vez de inventar (youtube:ZnlLfKR-vDQ@06:21), el agente rellena solo el archivo de memoria con los criterios de la conversación (youtube:ZnlLfKR-vDQ@10:32), crea una skill a petición con el formato correcto (youtube:ZnlLfKR-vDQ@11:34) y la misma carpeta en Claude Cowork resuelve un segundo proyecto con una sola instrucción (youtube:ZnlLfKR-vDQ@15:43). Jones sostiene que pasamos de encargar tareas a delegar trabajo permanente en los próximos 6 meses (youtube:1qGH6NwTj3o@25:30) y que antes de dar sitio a un superagente hay que decidir qué puede leer, iniciar y quién lo vigila (youtube:1qGH6NwTj3o@26:01).

## Qué hemos publicado y qué falta

Ya cubrimos el núcleo: que lo que aguanta el cambio de agente es el criterio escrito en archivos, con prueba propia de Codex sobre un sistema montado para Claude Code (biblioteca/substack/articulos/2026-04-27-codex-chatgpt-plus-incluido.md); el arnés con estado fuera de la conversación, permisos y condiciones de cierre (biblioteca/substack/articulos/2026-07-19-harness-engineering-agentes-ia.md); un arnés con skills y dos agentes, constructor y revisor (biblioteca/substack/articulos/2026-10-11-crear-sistema-diseno-codex-agentes-ia.md); y la arquitectura real de memoria por plataforma (biblioteca/substack/articulos/2026-01-07-gestion-memorias-llm.md). También el uso crítico de la investigación delegada (biblioteca/substack/articulos/2025-11-09-5-deep-research-acelera-tu-mente.md). Falta el flujo sin terminal (ChatGPT Proyectos y Claude Cowork), la memoria y skills que el propio agente escribe durante la conversación, y la interoperabilidad real cuando un segundo modelo trabaja sobre lo que escribió el primero.

## Qué aportaríamos

Una prueba propia del flujo completo sin terminal con nuestro propio caso: montar la carpeta de agente, cargarla como proyecto en ChatGPT, dejar que escriba memoria y skills, y después pasar la misma carpeta a Claude Cowork. Contrastar lo que el vídeo promete sin demostrar: si las skills y la memoria escritas por ChatGPT las lee y respeta de verdad otro modelo o son texto que cada uno interpreta a su manera, qué pasa cuando los criterios acumulados se contradicen, y si el método sirve fuera del caso de presupuestos. Publicar el proceso real, con lo que funciona, lo que se rompe y la revisión manual que exige el resultado.

## Qué hay que investigar o probar

Verificar la portabilidad real: la misma carpeta en Claude Cowork completa el proyecto con una sola instrucción (youtube:ZnlLfKR-vDQ@15:43), pero el vídeo no enseña qué hace Claude con la memoria y las skills escritas por ChatGPT. Probar la promesa de que sirve "para cualquier tarea" (youtube:ZnlLfKR-vDQ@00:03), demostrada solo con presupuestos de reformas. Comprobar qué planes de pago exige cada herramienta para reproducir el flujo. De la ficha de Jones, casi todo es relato sin demostración en pantalla (youtube:1qGH6NwTj3o@01:33 el experimento de Mollick, @08:39 los 41 documentos de Logora): si tocamos la delegación permanente, habría que contrastar esos casos con fuentes primarias, no repetirlos.

## Riesgos

La ficha de Jones es íntegramente promesa sin demostrar y con transcripción degradada: no sirve como evidencia, solo como señal de interés. El flujo de Mitjana depende de funciones recientes (pestaña Work de ChatGPT, Claude Cowork) que pueden cambiar o requerir planes de pago concretos. Riesgo de solapamiento con nuestra pieza de abril (Codex sobre sistema de Claude Code): la prueba debe centrarse en lo que aquella no tocó, el flujo sin terminal y la memoria/skills escritas por el agente, para no repetirnos.
