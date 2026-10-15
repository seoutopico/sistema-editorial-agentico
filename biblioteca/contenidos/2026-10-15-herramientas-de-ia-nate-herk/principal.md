---
oportunidad: 2026-10-15-herramientas-de-ia-nate-herk
estado: borrador
fecha: 2026-10-15
titulos_alternativos: [Cuánto esfuerzo conviene pagar a la IA: lo medí en mi propio sistema editorial, Más esfuerzo no compra mejor texto (y lo comprobé dos veces por nivel)]
---
# Pagué más razonamiento a la IA y no escribió mejor

*¿Cómo estás? Soy Aina y esto es Think&Hack.*

Llevaba meses con una pregunta rondándome: ¿cuánto razonamiento conviene pagar a la IA en cada tarea? Los modelos traen un parámetro de esfuerzo con varios niveles, y se repite mucho que subirlo mejora el resultado. Yo misma lo había subido alguna vez por intuición, sin medir nada.

Esta semana dejé de opinar y lo medí: el mismo encargo real de mi sistema editorial, ejecutado en cuatro niveles de esfuerzo de Claude Opus 5.5, con criterios de calidad escritos antes de ejecutar nada, dos repeticiones por nivel y puntuación a ciegas. Te cuento qué dice la documentación oficial de Anthropic, qué salió de mi tabla y la regla práctica que me llevo. Spoiler: pagar más esfuerzo no me compró mejor texto, y lo que sí me cobró te va a sorprender.

Si te gusta probar la IA y entender cómo puedes aprovecharla en tu trabajo, suscríbete a Think&Hack. Por aquí comparto lo que voy aprendiendo, mis experimentos y cómo puedes probarlos tú. :)

---

## Aclara los nombres antes de tocar nada

El *esfuerzo* (effort) es cuánto razonamiento interno le pides al modelo antes de responder. Más esfuerzo significa más tiempo pensando y, en principio, más tokens.

La documentación oficial de Anthropic lista cinco valores del parámetro: low, medium, high, xhigh y max [f2]. Cinco, no seis ni cuatro: si por ahí lees nombres como «Extra» o «UltraCode», no son niveles de la API. Si vas a tocar el parámetro, conviene saber cómo se llama de verdad cada cosa.

## Lee lo que Anthropic ya decidió por ti

Aquí viene lo que casi nadie mira y a mí me parece la pista principal. La guía oficial de prompting de Opus 5.5 dice literalmente que empieces en medium, que es el valor por defecto, y que pruebes varios niveles contra tus propias evaluaciones [f1]. Y reserva xhigh y max para casos donde hayas **medido** una mejora [f1].

Fíjate en el detalle: medium no es solo una recomendación, es el valor por defecto del modelo [f2]. **Anthropic no te sugiere empezar abajo: te coloca abajo de serie.** Eso es una decisión de producto, no una nota al pie. Ya vimos un movimiento parecido cuando OpenAI cambió sus reglas de prompting: te lo conté en la [guía de prompting de GPT-5.2](https://ainalluna.substack.com/p/14-guia-prompting-gpt-52-lo-que-cambio).

## Monta el experimento antes de opinar

Yo misma tengo una espinita con esto: cuando probé Codex dentro de mi sistema de escritura, [elegí razonamiento alto para una tarea sin medirlo](https://ainalluna.substack.com/p/codex-chatgpt-plus-incluido). Pura intuición. Esta vez lo hice al revés:

- **Criterios primero.** Escribí la rúbrica de calidad antes de ver ningún resultado, para no puntuar a favor de mi hipótesis.
- **Tarea real.** Redactar la misma Substack Note desde un artículo propio, con mi guía de estilo y mi plantilla. Nada de mundos 3D: texto de trabajo normal.
- **Cuatro niveles, dos repeticiones.** El mismo prompt literal en low, medium, high y max. Dos ejecuciones por nivel, para poder ver la variabilidad.
- **Evaluación a ciegas.** Puntué las ocho notas de 0 a 10 sin saber de qué nivel salía cada una; el mapeo se reveló después [f7].

Antes de seguir, comprueba conmigo que el método se sostiene: criterios previos, repetición y ceguera. Con n=2 sigue siendo un experimento pequeño, pero ya no es una impresión.

## Mira la tabla y saca tus cuentas

Estos son los resultados completos [f7]:

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

Tres cosas me llaman la atención:

- **La calidad fue plana de medium hacia arriba.** Seis de las ocho ejecuciones puntuaron 9,5. Las dos únicas notas con pegas salieron de low [f7].
- **Los tokens casi no se movieron.** Entre max y low, la diferencia fue de un +11-13 % según el par que compares [f7]. Yo esperaba un salto de coste grande y no apareció.
- **La duración sí se disparó:** max tardó entre 4,2 y 5,6 veces más que low [f7].

Una honestidad necesaria: que seis ejecuciones empaten en 9,5 con una rúbrica de granularidad 0,5 puede ser un efecto techo de mi instrumento. Lo defendible no es «la calidad es igual», sino «con esta rúbrica y esta tarea no detecté diferencias de medium hacia arriba» [f7].

## Entiende dónde duele cada factura

Aquí está el giro que no me esperaba. Yo daba por hecho que el esfuerzo alto se pagaría en tokens, es decir, en dinero. En mi tarea corta no fue así: el esfuerzo alto se pagó en **espera**. Casi los mismos tokens, pero cuatro o cinco veces más tiempo mirando la pantalla [f7].

Mi hipótesis para tareas largas (construir una aplicación, procesar horas de material) es que ahí el exceso sí dolerá en la cartera, porque el razonamiento extra se acumula durante horas. Pero eso es el siguiente experimento, no un dato: de momento solo puedo afirmar lo que midió mi tabla.

## Repite antes de creerte un ranking

La parte que más me ha servido no es la tabla: es lo que pasa al repetir. Mis dos ejecuciones de low difirieron entre sí (9,0 frente a 8,5) tanto como dos niveles contiguos. Y las dos de high tardaron 28,4 y 22,2 segundos, una brecha parecida a la que separa niveles vecinos [f7].

Traducción: **con una sola ejecución por nivel, cualquier ranking fino entre niveles es ruido.** La variabilidad dentro de un mismo nivel es del orden de la diferencia entre niveles [f7]. Que una ejecución gane a otra no confirma que ese nivel sea mejor. Solo se ve repitiendo. La próxima vez que veas una comparativa espectacular con una sola pasada por opción, ya sabes qué preguntarle.

## Quédate con la regla, no con las cifras

Los precios y los niveles cambiarán con la siguiente versión del modelo. Lo que no caduca es el método. Mi regla práctica, con todos los límites de un experimento pequeño:

- **Medium por defecto.** Es donde Anthropic te coloca de serie, y en mi tarea no encontré motivo para moverme [f1][f2][f7].
- **High como tope en piezas cortas.** Por encima, en mi prueba, solo compré espera [f7].
- **Xhigh y max, solo con mejora medida.** Que es exactamente lo que pide la documentación oficial [f1]. Para tareas largas de construcción pueden tener sentido, pero midiendo, no por fe.

Y la meta-regla: antes de pagar más esfuerzo, escribe tus criterios, ejecuta al menos dos veces por nivel y puntúa a ciegas. Es menos épico que una demo espectacular, pero es lo que convierte una impresión en un dato.

---

**¿Tú en qué nivel de esfuerzo trabajas? ¿Lo elegiste midiendo algo o, como yo hasta ahora, por intuición?**

***Cuéntamelo. Siempre leo todo.***

[Deja un comentario]

**Tools are great. Systems are better.**

Casos reales, flujos que funcionan y formas concretas de usar la IA sin perder el control del proceso.

## Fuentes

[f1] Prompting Claude Opus 5.5, Anthropic, s. f. (consultada 2026-10-15), https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5
[f2] Effort — Claude Docs, Anthropic, s. f. (consultada 2026-10-15), https://platform.claude.com/docs/en/build-with-claude/effort
[f7] Experimento propio: 4 niveles x 2 repeticiones sobre una Substack Note real, Aina Lluna, 2026-10-15, biblioteca/contenidos/2026-10-15-herramientas-de-ia-nate-herk/experimento/resultados.md (archivo local del repositorio)
