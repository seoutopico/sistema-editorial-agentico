---
id: 2026-10-15-herramientas-de-ia-nate-herk
estado: aceptada
motivo_estado: "Primera ejecución completa del pipeline; único experimento ejecutable sin manos de Aina (encargo: 'lanza el proceso completo')"
tema: Herramientas de IA
grupo_id: herramientas-de-ia-nate-herk
interes: alto
canales: 1
cobertura: ampliación
evidencias: [youtube:7jHXoPGnA4c@00:00, youtube:7jHXoPGnA4c@01:00, youtube:7jHXoPGnA4c@02:02, youtube:7jHXoPGnA4c@03:35, youtube:7jHXoPGnA4c@05:38, youtube:7jHXoPGnA4c@06:40, youtube:7jHXoPGnA4c@08:50, youtube:7jHXoPGnA4c@10:54, youtube:7jHXoPGnA4c@13:29, youtube:7jHXoPGnA4c@16:00, youtube:7jHXoPGnA4c@17:33, youtube:7jHXoPGnA4c@18:34, youtube:7jHXoPGnA4c@19:05, youtube:QCkHIyEPIYo@01:01, youtube:QCkHIyEPIYo@03:35, youtube:QCkHIyEPIYo@06:40, youtube:QCkHIyEPIYo@07:12, youtube:QCkHIyEPIYo@10:48, youtube:QCkHIyEPIYo@13:21, youtube:QCkHIyEPIYo@17:28, youtube:QCkHIyEPIYo@21:05, youtube:QCkHIyEPIYo@21:36, youtube:QCkHIyEPIYo@22:07, youtube:QCkHIyEPIYo@22:37, youtube:QCkHIyEPIYo@25:43, youtube:eF3yeJuifoQ@00:00, youtube:eF3yeJuifoQ@02:05, youtube:eF3yeJuifoQ@04:40, youtube:eF3yeJuifoQ@05:10, youtube:eF3yeJuifoQ@08:28, youtube:eF3yeJuifoQ@13:23, youtube:eF3yeJuifoQ@22:43, youtube:eF3yeJuifoQ@23:14, youtube:eF3yeJuifoQ@25:19, youtube:eF3yeJuifoQ@26:52, youtube:eF3yeJuifoQ@27:24, youtube:eF3yeJuifoQ@29:28, youtube:eF3yeJuifoQ@30:30, youtube:eF3yeJuifoQ@31:31, youtube:eF3yeJuifoQ@33:05, youtube:o3IEkKXXXvo@01:32, youtube:o3IEkKXXXvo@02:34, youtube:o3IEkKXXXvo@03:04, youtube:o3IEkKXXXvo@07:10, youtube:o3IEkKXXXvo@10:17, youtube:o3IEkKXXXvo@11:20, youtube:o3IEkKXXXvo@13:55, youtube:o3IEkKXXXvo@15:28, youtube:o3IEkKXXXvo@17:33, youtube:o3IEkKXXXvo@24:49, youtube:o3IEkKXXXvo@26:22, youtube:o3IEkKXXXvo@23:15]
relacionados: [substack:183130708, substack:195602355, substack:205019542, substack:216545004, substack:217631531]
---
## La oportunidad

Más esfuerzo de razonamiento no garantiza mejor resultado y sí multiplica el coste: con el mismo prompt, el nivel Extra de Opus 5.5 superó a Max costando la mitad, y la ejecución más cara costó 12,9 veces más que la más barata. Nadie está midiendo esto en tareas de trabajo de conocimiento normales: llevamos meses enseñando a montar flujos con agentes, pero nunca hemos respondido con cifras la pregunta que viene justo después, cuánto razonamiento conviene pagar para cada tarea. Es puro proceso, medible con nuestras herramientas y sin tocar los ángulos de vídeo del grupo.

## Por qué ahora (evidencias)

Grupo con interés alto (4 fichas de un canal, múltiplo hasta 3,18, última fecha 2026-09-25). El experimento ejecuta el mismo prompt en los seis niveles de esfuerzo de Opus 5.5 (youtube:QCkHIyEPIYo@01:01) y publica métricas reales por nivel: bajo, 16 min 43 s, 3,91 $ y 191.000 tokens (youtube:QCkHIyEPIYo@03:35); medio, 1 h 13 min y 12,44 $ (youtube:QCkHIyEPIYo@06:40); max, 2 h 28 min, 50,38 $, 1,18 millones de tokens y aun así con fallos visibles (youtube:QCkHIyEPIYo@17:28). El ganador fue Extra, no Max (youtube:QCkHIyEPIYo@25:43), la diferencia de coste entre extremos fue de 12,9x (youtube:QCkHIyEPIYo@22:37) y Anthropic recomienda empezar en medio y escalar según necesidad (youtube:QCkHIyEPIYo@07:12). El vídeo hermano del mismo canal añade la versión entre modelos: Opus 5.5 gana 7-1 a GPT-6 Sol costando unas tres veces más (youtube:eF3yeJuifoQ@31:31), con la hipótesis sin probar de usar Opus como orquestador y Sol como trabajador barato (youtube:eF3yeJuifoQ@33:05).

## Qué hemos publicado y qué falta

Hemos publicado cómo montar un flujo agéntico con skills y revisarlo (biblioteca/substack/articulos/2026-09-20-como-usar-chatgpt-work.md), que el criterio escrito aguanta el cambio de agente, eligiendo razonamiento alto para una tarea concreta pero sin medirlo (biblioteca/substack/articulos/2026-04-27-codex-chatgpt-plus-incluido.md), la anatomía de una skill verificable (biblioteca/substack/articulos/2026-07-05-crear-skills-agentes-ia-verificables.md), convertir un tutorial ajeno en skill (biblioteca/substack/articulos/2026-10-04-como-crear-skill-chatgpt-work.md) y los modos de razonamiento como consejo de prompting (biblioteca/substack/articulos/2026-01-11-14-guia-prompting-gpt-52-lo-que-cambio.md). Falta lo que ninguno toca: cifras reales de coste, tiempo y calidad por nivel de esfuerzo en una tarea de trabajo normal, y un criterio práctico para elegir nivel.

## Qué aportaríamos

Replicar el experimento sobre una tarea real de nuestro sistema editorial (texto, procesos, hojas de cálculo, no mundos 3D): el mismo encargo en varios niveles de esfuerzo de Opus 5.5 en Claude Code, con más de una ejecución por nivel donde el vídeo solo hizo una (youtube:QCkHIyEPIYo@25:43 reconoce n=1 y juicio subjetivo), midiendo coste, tiempo y tokens, y evaluando la calidad contra criterios escritos antes de ejecutar. Responde si el patrón «Extra gana a Max» se sostiene fuera de la generación creativa (pregunta abierta de la ficha) y traduce la recomendación de Anthropic (youtube:QCkHIyEPIYo@07:12) a una regla práctica para nuestra audiencia. En tareas de texto el coste por ejecución es una fracción de los 127 $ del vídeo: cabe en una semana con un PC de consumo, sin vídeo ni GPU.

## Qué hay que investigar o probar

La variabilidad entre ejecuciones repetidas del mismo nivel, que el vídeo no mide (una sola ejecución por nivel, youtube:QCkHIyEPIYo@25:43). Si la relación esfuerzo-calidad observada en una tarea creativa 3D generaliza a tareas de texto y proceso (youtube:QCkHIyEPIYo@21:36 señala además que ningún nivel delegó en subagentes). Cómo medir calidad con criterios objetivos en lugar del paseo subjetivo del autor. Y, como contraste opcional, si el mismo encargo en un modelo barato con instrucciones muy específicas se acerca al resultado del caro, la pregunta que el vídeo hermano deja abierta (youtube:eF3yeJuifoQ@31:31, youtube:eF3yeJuifoQ@33:05).

## Riesgos

El hallazgo central del vídeo es n=1 con calidad juzgada a ojo por el autor, así que partimos de una señal frágil: nuestra prueba puede contradecirlo y la pieza debe estar preparada para ello. El experimento consume presupuesto de API real y varias horas de ejecuciones. Los niveles de esfuerzo y sus precios pueden cambiar con la siguiente versión del modelo, así que la pieza debe anclarse en el método de medir (criterios, n>1, coste por resultado útil) más que en las cifras concretas. Dos de las cuatro fichas del grupo son edición de vídeo y caen en el descarte vigente de la autora (2026-10-14-contenido-y-curacion-con-ia): esta propuesta no las toca y debe mantenerse en tareas de texto y proceso para no recaer en aquel motivo.
