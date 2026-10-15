---
oportunidad: 2026-10-15-herramientas-de-ia-nate-herk
estado: aprobada
fecha: 2026-10-15
---
## Pregunta de investigación

¿Cuánto razonamiento conviene pagar en cada tarea? En concreto: ¿se sostiene fuera de la generación creativa 3D el hallazgo del vídeo de que más esfuerzo no garantiza mejor resultado y sí multiplica el coste, y qué regla práctica se puede dar para elegir nivel de esfuerzo en Opus 5.5 en tareas de trabajo normales?

## Resumen

El vídeo [f5] ejecuta el mismo prompt en varios niveles de esfuerzo de Opus 5.5 (n=1 por nivel, calidad a ojo) y concluye que el ganador fue "Extra", no Max, con 12,9x de diferencia de coste entre extremos. Anthropic confirma la recomendación que el vídeo cita: empezar en medium (el nivel por defecto de Opus 5.5) y escalar solo con mejora medida [f1][f2], aunque los niveles documentados son cinco, no seis [f2]. Nuestro experimento propio [f7] (4 niveles x 2 repeticiones, misma tarea editorial real, evaluación a ciegas con criterios previos) replica el patrón en tareas cortas: con nuestra rúbrica no se detectaron diferencias de medium hacia arriba, y el precio del esfuerzo alto se pagó en latencia (x4,2-5,6), no en tokens (alrededor de +12%). Con n=1, como el vídeo, el ranking fino entre niveles vecinos es ruido. Los precios de API que compara el vídeo hermano son exactos: Opus 5.5 cuesta el doble que GPT-6 Sol [f3][f4].

## Verificación de afirmaciones

| ID | Afirmación | Estado | Fuentes | Nota |
|---|---|---|---|---|
| a1 | La intro del vídeo editada por Opus 5.5 con un solo prompt | sin_confirmar | — | No usada en el contenido |
| a2 | Hyperframes es gratis y se instala pasando la URL del repo a Claude Code | sin_confirmar | — | No usada en el contenido |
| a3 | Primer paso: transcribir con ElevenLabs o Whisper | sin_confirmar | — | No usada en el contenido |
| a4 | El modelo añadió decisiones de diseño no pedidas | sin_confirmar | — | No usada en el contenido |
| a5 | Convirtió el análisis de un reel ajeno en una skill | sin_confirmar | — | No usada en el contenido |
| a6 | El agente generó imágenes y las envió a Kling | sin_confirmar | — | No usada en el contenido |
| a7 | 105 GB de grabaciones convertidos en vídeo promocional con tres prompts | sin_confirmar | — | No usada en el contenido |
| a8 | Tres ediciones de estilos distintos del mismo clip, un prompt cada una | sin_confirmar | — | No usada en el contenido |
| a9 | Casi todos los ejemplos se ejecutaron con esfuerzo en alto | sin_confirmar | — | Relato del autor sobre su propio uso, sin registro externo; high sí es un nivel documentado del parámetro effort (f2) |
| a10 | Marco de cinco pasos: transcribir, cortar, planificar, skills, verificar | sin_confirmar | — | No usada en el contenido |
| a11 | Actualizar la skill con feedback construye un componente reutilizable | sin_confirmar | — | No usada en el contenido |
| a12 | El bucle de verificación entrega de facto la versión cinco o seis | sin_confirmar | — | No usada en el contenido |
| a13 | Ya no hace falta experiencia previa en edición de vídeo | sin_confirmar | — | No usada en el contenido |
| a14 | El mismo prompt ejecutado en los seis niveles de esfuerzo de Opus 5.5 | refutada | f2, f5 | El experimento existe tal y como lo muestra el vídeo (f5), pero el "seis niveles de esfuerzo" mezcla planos: la documentación oficial lista cinco valores del parámetro effort de la API (low, medium, high, xhigh, max); el que el vídeo llama "extra" es xhigh y "UltraCode" no es un valor de effort sino, como mucho, un modo del arnés (f2). Refutada en su formulación literal; es confusión de nomenclatura más que invención |
| a15 | Nivel bajo: 16m43s, 3,91$, 191K tokens, 22 comprobaciones | sin_confirmar | — | Cifras mostradas en pantalla por el autor; sin fuente externa que las respalde |
| a16 | Nivel medio: 1h13, 12,44$, 490K tokens, 23 comprobaciones | sin_confirmar | — | Relato del autor; sin fuente externa |
| a17 | Anthropic recomienda empezar en esfuerzo medio y escalar según necesidad | verificada | f1, f2 | La guía oficial de prompting de Opus 5.5 dice literalmente "Start at medium, the default on Claude Opus 5.5... and test several levels against your own evals" y reserva xhigh y max para mejoras medidas (f1); la página de effort confirma que medium es el por defecto en Opus 5.5 (f2) |
| a18 | Nivel alto: 1h07, 16,31$, 509K tokens; único que preguntó al usuario | sin_confirmar | — | Relato del autor; sin fuente externa |
| a19 | Nivel extra: 1h30, 25,92$, 733K tokens, 34 comprobaciones | sin_confirmar | — | Relato del autor; sin fuente externa. "Extra" corresponde a xhigh en la documentación (f2) |
| a20 | Nivel max: 2h28, 50,38$, 1,18M tokens, 51 comprobaciones, con fallos visibles | sin_confirmar | — | Relato del autor; sin fuente externa |
| a21 | UltraCode: 1h35, 18,69$, 606K tokens, 42 comprobaciones | sin_confirmar | — | Relato del autor; UltraCode no es un nivel de esfuerzo documentado (f2) |
| a22 | Ninguna de las seis ejecuciones usó subagentes | sin_confirmar | — | Relato del autor sobre sus logs; sin registro externo |
| a23 | Sospecha un bug del arnés con UltraCode | sin_confirmar | — | Opinión-sospecha del autor sin evidencia concluyente |
| a24 | La más cara costó 12,9 veces más que la más barata; total unos 127$ | sin_confirmar | — | Aritmética coherente con sus propias cifras (50,38/3,91 = 12,9), pero las cifras base son relato del autor. En nuestra tarea corta la brecha de tokens fue solo +12%, con la latencia como coste dominante (f7) |
| a25 | El ganador fue Extra; Max caro y lento; Medio basta para la mayoría del trabajo de conocimiento | sin_confirmar | — | Opinión del autor con n=1 y calidad juzgada a ojo. Nuestro experimento (f7) respalda la parte estructural (de medium hacia arriba la calidad fue plana; max no aportó nada) y la doc oficial respalda medium como punto de partida (f1), pero el ranking fino Extra sobre Max con n=1 es indistinguible del ruido (f7) |
| a26 | Opus 5.5 cuesta el doble que GPT-6 Sol: 4$/20$ frente a 2$/10$ | verificada | f3, f4 | Precios oficiales vigentes a 2026-10-15: Opus 5.5 a 4$ entrada y 20$ salida (f3); gpt-6-sol a 2$ entrada y 10$ salida en el tramo estándar de hasta 272K de contexto (f4). Exactamente el doble. Lo verificado son las cifras; la cláusula final de la afirmación ("la métrica relevante es qué calidad te da cada modelo por los mismos cien dólares") es opinión del autor, no verificable |
| a27 | Prueba previa con Fireflies: Sol devolvió una fecha incorrecta | sin_confirmar | — | No usada en el contenido |
| a28 | Caso 1, diseño web: Opus costó el triple y fue más premium | sin_confirmar | — | No usada en el contenido |
| a29 | Caso 2, vídeo promocional desde Frame.io: punto para Opus | sin_confirmar | — | No usada en el contenido |
| a30 | Caso 3, reel con Hyperframes: Opus mejor, el doble de lento, 4x el coste | sin_confirmar | — | No usada en el contenido |
| a31 | Casos 4 y 5 anulados: ambos agentes editaron archivos del otro | sin_confirmar | — | No usada en el contenido |
| a32 | Caso 6, mundo 3D: Opus mejor, 60$ frente a 8,55$ | sin_confirmar | — | No usada en el contenido |
| a33 | Sol pregunta más y en Codex la pregunta no bloquea | sin_confirmar | — | No usada en el contenido |
| a34 | Caso 7, globo 3D de viaje: Opus investigó mejor costando el triple | sin_confirmar | — | No usada en el contenido |
| a35 | Caso 8, código: Sol 100/100 por 1$; Opus 97/100 por unas 20 veces más | sin_confirmar | — | No usada en el contenido |
| a36 | Sol se detuvo por una salvaguarda de ciberseguridad; Opus no | sin_confirmar | — | No usada en el contenido |
| a37 | Caso 9, curso en School vía navegador: Opus más rápido y barato | sin_confirmar | — | No usada en el contenido |
| a38 | Caso 10, dibujo en Canva: Opus sorprendentemente bueno; Sol hizo trampa | sin_confirmar | — | No usada en el contenido |
| a39 | Totales: 7-1 para Opus; 213$ frente a 74,46$ | sin_confirmar | — | Relato del autor; se menciona solo como contexto del vídeo hermano |
| a40 | Opus para creatividad y juicio; Sol como trabajador barato orquestado | sin_confirmar | — | Opinión del autor; hipótesis que él mismo deja sin probar |
| a41 | Un vídeo de 14 minutos se redujo a 9 con dos grabaciones | sin_confirmar | — | No usada en el contenido |
| a42 | Skills para decidir encuadre según contexto | sin_confirmar | — | No usada en el contenido |
| a43 | Dos reels de formato corto generados con el flujo | sin_confirmar | — | No usada en el contenido |
| a44 | El agente recolectó B-roll real y buscó el logo en Google Drive | sin_confirmar | — | No usada en el contenido |
| a45 | Configuración: proyecto local en Codex más la URL del repo de Hyperframes | sin_confirmar | — | No usada en el contenido |
| a46 | Flujo conceptual de cuatro fases | sin_confirmar | — | No usada en el contenido |
| a47 | Para transcribir prefiere ElevenLabs frente a Whisper | sin_confirmar | — | No usada en el contenido |
| a48 | El agents.md acumula preferencias de edición | sin_confirmar | — | No usada en el contenido |
| a49 | Construye la intro en directo con /goal y un prompt enorme | sin_confirmar | — | No usada en el contenido |
| a50 | Primera versión en 18 minutos; segunda iteración en 10 | sin_confirmar | — | No usada en el contenido |
| a51 | Hyperframes genera un estudio local en localhost | sin_confirmar | — | No usada en el contenido |
| a52 | "Convierte eso en una skill" y reutilizar con feedback | sin_confirmar | — | No usada en el contenido |
| a53 | Variabilidad entre repeticiones, generalización a tareas de texto, calidad con criterios objetivos | verificada | f7 | Comprobado con experimento propio: 4 niveles x 2 repeticiones sobre una tarea editorial real, criterios de calidad fijados antes de ejecutar y evaluación a ciegas. La variabilidad intra-nivel resultó del orden de la diferencia entre niveles contiguos (con n=1 el ranking fino es ruido); el patrón "más esfuerzo no implica mejor" se sostuvo también en una tarea corta de texto (sin diferencias detectables de medium hacia arriba con nuestra rúbrica, con posible efecto techo del instrumento); el contraste con un modelo barato queda pendiente como extensión opcional. Evidencia cruda en experimento/ciegas/ y experimento/mapeo-oculto.json |

## Hallazgos nuevos

- **Los niveles son cinco, no seis.** La documentación oficial del parámetro effort lista low, medium, high, xhigh y max; el "Extra" del vídeo es xhigh y "UltraCode" no es un nivel de esfuerzo de la API [f2]. Cualquier pieza que cite el vídeo debe traducir su nomenclatura.
- **Anthropic no solo recomienda empezar en medium: lo hizo el valor por defecto.** Opus 5.5 es, junto a Haiku 5.5, el único modelo actual cuyo esfuerzo por defecto es medium en vez de high, y la guía pide explícitamente barrer niveles contra evals propios y reservar xhigh y max para mejoras medidas [f1][f2]. La recomendación que el vídeo cita de pasada es en realidad una decisión de producto.
- **En tareas cortas, el coste del esfuerzo alto fue latencia, no dinero.** En nuestro experimento la diferencia de tokens entre max y low fue de solo +11-13% según el par comparado, pero la duración se multiplicó por 4,2-5,6 [f7]. Como hipótesis derivada (una tarea larga frente a una corta, no una ley): el 12,9x de coste del vídeo [f5] apunta a que en tareas de horas el esfuerzo se paga en dólares, mientras que en nuestra pieza corta se pagó en espera.
- **La variabilidad intra-nivel invalida rankings con n=1.** Dos ejecuciones del mismo nivel difirieron entre sí tanto como dos niveles contiguos (low: 9,0 frente a 8,5; high: 28,4 s frente a 22,2 s) [f7]. El "ganador Extra" del vídeo es indistinguible del azar con una sola ejecución por nivel.
- **Los precios que ancla el vídeo hermano son exactos.** Opus 5.5 a 4$/20$ [f3] y GPT-6 Sol a 2$/10$ [f4]: el doble, como afirma a26, con el matiz de que Sol sube a 4$/15$ en contexto largo [f4].

## Contradicciones y límites

- El vídeo presenta seis "niveles de esfuerzo"; la documentación oficial define cinco y no reconoce UltraCode como nivel [f2] frente a [f5]. No es un error de datos sino de nomenclatura, pero obliga a traducir.
- Las cifras del vídeo (3,91$ a 50,38$, tiempos, tokens, comprobaciones) solo existen en la pantalla del autor: coherentes entre sí, pero sin registro externo posible. Quedan como relato del autor.
- Nuestro experimento no contradice el del vídeo: lo acota. Él midió una tarea creativa de horas; nosotros, una tarea editorial de segundos. En nuestras dos muestras el patrón común es que max no compró calidad; dónde duele (coste o latencia) es hipótesis, no ley, porque hay una sola tarea de cada tipo [f5][f7].
- Posible efecto techo del instrumento: 6 de 8 ejecuciones puntuaron 9,5 sobre 10 con una rúbrica de granularidad 0,5. Lo defendible no es "la calidad es igual" sino "no se detectaron diferencias con este instrumento en esta tarea" [f7].
- Límites propios: una sola tarea corta, evaluador único (aunque a ciegas y con criterios previos), y tokens del arnés que incluyen el contexto fijo, lo que comprime las diferencias relativas [f7].
- La comparación con un modelo barato muy instruido (pregunta abierta del vídeo hermano, a40) queda sin probar por ambas partes.

## Prueba práctica

Ya ejecutada, con criterios escritos antes de ver ningún resultado (biblioteca/contenidos/2026-10-15-herramientas-de-ia-nate-herk/experimento/criterios.md): redactar la misma Substack Note desde un artículo propio, con estilo.md y plantilla, en low, medium, high y max, dos repeticiones por nivel, mismo prompt literal, evaluación a ciegas 0-10 y mapeo revelado después [f7].

| Nivel | Rep | Tokens | Duración | Calidad (0-10, a ciegas) |
|---|---|---|---|---|
| low | 1 | 58.113 | 17,5 s | 9,0 |
| low | 2 | 58.156 | 19,1 s | 8,5 |
| medium | 1 | 58.409 | 21,9 s | 9,5 |
| medium | 2 | 58.398 | 21,5 s | 9,5 |
| high | 1 | 58.950 | 28,4 s | 9,5 |
| high | 2 | 58.528 | 22,2 s | 9,5 |
| max | 1 | 65.432 | 97,8 s | 9,5 |
| max | 2 | 63.416 | 79,5 s | 9,5 |

Resultado: H1 sostenida con reservas (con esta rúbrica y esta tarea no se detectaron diferencias de medium hacia arriba; 6 de 8 ejecuciones en 9,5/10, posible efecto techo), H2 matizada (tokens +11-13% pero latencia x4,2-5,6: en esta tarea corta el esfuerzo se pagó en espera), H3 parcialmente confirmada (variabilidad intra-nivel del orden de la diferencia entre niveles contiguos). Las dos únicas notas con pegas salieron de low. Regla práctica derivada: con buen contexto, medium basta y high es el tope útil en piezas cortas. La evidencia cruda es auditable en el repositorio: las 8 notas puntuadas a ciegas en experimento/ciegas/ y el mapeo revelado en experimento/mapeo-oculto.json.

## Ángulo propuesto

"Probé lo que el vídeo cuenta, en mi terreno y con n=2: esto es lo que cambia." El vídeo de Nate Herk responde a la pregunta correcta (cuánto razonamiento conviene pagar) con un método frágil: una ejecución por nivel, calidad a ojo, una tarea creativa espectacular pero ajena al trabajo de la audiencia. La pieza replica su experimento sobre una tarea editorial real con lo que a él le faltó: criterios de calidad escritos antes de ejecutar, dos repeticiones por nivel y evaluación a ciegas. Tres giros propios sobre su tesis: (1) su conclusión central aguanta, más esfuerzo no compra calidad y la doc oficial de Anthropic ya lo asume al poner medium por defecto [f1][f2]; (2) en nuestra tarea corta la factura no fueron dólares sino segundos, x4,2-5,6 de latencia por un +12% escaso de tokens [f7], la cara de la moneda que el vídeo no ve; (3) su ranking fino entre niveles es ruido, porque la variabilidad entre repeticiones del mismo nivel es igual de grande, y eso solo se ve repitiendo [f7]. Cierre accionable: la regla de tres niveles (medium por defecto, high como tope en piezas cortas, max solo para tareas largas de construcción, y aun así midiendo), anclada en el método, no en las cifras, porque los precios y niveles cambiarán.

## Fuentes

[f1] Prompting Claude Opus 5.5, Anthropic, s. f. (consultada 2026-10-15), https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5
[f2] Effort — Claude Docs, Anthropic, s. f. (consultada 2026-10-15), https://platform.claude.com/docs/en/build-with-claude/effort
[f3] Pricing — Claude Docs, Anthropic, s. f. (consultada 2026-10-15), https://platform.claude.com/docs/en/about-claude/pricing
[f4] API Pricing — OpenAI, OpenAI, s. f. (consultada 2026-10-15), https://developers.openai.com/api/docs/pricing
[f5] Experimento de niveles de esfuerzo de Opus 5.5, Nate Herk (AI Automation), 2026-09-24, https://www.youtube.com/watch?v=QCkHIyEPIYo
[f6] Opus 5.5 vs GPT-6 Sol: 10 casos reales, Nate Herk (AI Automation), 2026-09-23, https://www.youtube.com/watch?v=eF3yeJuifoQ
[f7] Experimento propio: 4 niveles x 2 repeticiones sobre una Substack Note real, Aina Lluna, 2026-10-15, biblioteca/contenidos/2026-10-15-herramientas-de-ia-nate-herk/experimento/resultados.md (archivo local del repositorio)
