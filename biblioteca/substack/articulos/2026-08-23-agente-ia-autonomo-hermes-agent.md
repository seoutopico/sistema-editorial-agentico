---
id: 212107861
titulo: "He construido un agente autónomo y te explico cómo."
subtitulo: "Le he dado un objetivo real: hacer crecer Think&Hack. Ahora toca ver si aprende a conseguirlo sin que yo tenga que acordarme de ponerlo a trabajar."
fecha: 2026-08-23
url: https://ainalluna.substack.com/p/agente-ia-autonomo-hermes-agent
tipo: newsletter
audiencia: everyone
estado: completo
huella: 1e4344b097e8e1782c55204e36a4392ae8efed7bd642b1e79cb0a621501fac10
---

[

![imagen](https://substackcdn.com/image/fetch/$s_!kvLy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83cffd74-507c-4625-8b29-1d6bd06888c1_1672x941.png)

](https://substackcdn.com/image/fetch/$s_!kvLy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83cffd74-507c-4625-8b29-1d6bd06888c1_1672x941.png)

*¿Cómo estás?*

*Soy Aina y esto es Think&Hack. *

Llevo semanas hablando de agentes, skills, memoria y sistemas verificables.

Todos los sistemas tenían el mismo problema, que seguían dependiendo de mí: abrir el ordenador, acordarme del prompt y darle al botón.

Y cada sistema que montaba añadía otra cosa que tenía que recordar: qué lanzar, qué había cambiado, qué había quitado, qué era nuevo… vamos, un `Diógenes mental de información. `

Es absurdo haber automatizado muchas formas de trabajar y seguir necesitando acordarme de cómo lanzar el proceso, así que la pregunta más evidente que me he estado haciendo estas últimas semanas es: **¿hasta qué punto he construido realmente un agente autónomo?**

[

![imagen](https://substackcdn.com/image/fetch/$s_!-QQA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6854ac4e-2bc6-4dcf-b519-6d1df47ca70e_1672x941.png)

](https://substackcdn.com/image/fetch/$s_!-QQA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6854ac4e-2bc6-4dcf-b519-6d1df47ca70e_1672x941.png)Esto delata mi edad. :p

Para llevar adelante el reto, quiero un reto real, un objetivo medible y un proceso útil y automatizado de los muchos que tengo “agentizados”.

Así que voy a darle a un agente de IA un objetivo bastante concreto:

###  **hacer crecer Think&Hack.**

Te presento a **Hacki** mi agente autónomo de IA conectado a Hermes.

---

## ¿Quién es Hacki y qué va a hacer?

[

![imagen](https://substackcdn.com/image/fetch/$s_!5Pic!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F155ad7eb-e1d2-4add-a73f-59009d9d0c54_2172x724.png)

](https://substackcdn.com/image/fetch/$s_!5Pic!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F155ad7eb-e1d2-4add-a73f-59009d9d0c54_2172x724.png)

[

![imagen](https://substackcdn.com/image/fetch/$s_!4sVz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8301261e-c333-4c5e-963a-dc7c22c83bcc_780x770.png)

](https://substackcdn.com/image/fetch/$s_!4sVz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8301261e-c333-4c5e-963a-dc7c22c83bcc_780x770.png)Hacki te saluda.

Hacki es el nombre que le he puesto al agente que tendrá una única misión: intentar hacer crecer** la visibilidad y las suscripciones de Think&Hack a través de *****Substack Notes.***

Y digo *intentar* porque esa es precisamente la gracia del experimento.

No sé si va a funcionar.

No sé si dentro de unas semanas descubriré que he montado un sistema muy sofisticado para conseguir exactamente los mismos resultados que ya tenía 😅.

Lo que quiero probar es si Hacki puede recibir un objetivo relativamente abierto, trabajar sobre él cada semana, mirar qué ha ocurrido y utilizar esa información para decidir qué hacer después.

En este caso tendrá dos métricas bastante fáciles de entender: **visibilidad y suscriptores**.

Para conseguirlo, Hacki deberá revisar las Notes que ya he publicado y sus resultados, detectar temas, formatos y hooks que parecen funcionar, preparar el calendario de la siguiente semana, escribir las Notes completas, publicarlas, buscar conversaciones en las que tenga sentido participar y analizar después qué ha pasado.

Pero para mí hay una parte todavía más importante: **no quiero que cada semana empiece desde cero**.

Si una estrategia funciona, quiero saberlo.

Si una Note no consigue absolutamente nada, también.

La lógica será bastante sencilla:

**publicar → medir → aprender → decidir → repetir.**

Al menos sobre el papel.

---

## El sistema que hay detrás

**Hacki es un agente de IA autónomo construido sobre Hermes Agent: **recibe un objetivo, ejecuta tareas programadas y, en este experimento, utilizará los resultados de cada semana para decidir qué hacer después.

Hermes Agent es un agente open source desarrollado por Nous Research.

Lo elegí por una razón bastante práctica: puedo tenerlo ejecutándose en mi servidor y *programar tareas para que trabaje sin que yo tenga que acordarme de lanzarlas* cada vez. Además, queda aislado de mi ordenador y de mis archivos personales. **Seguridad ante todo.**

Es decir, justo el problema con el que empezaba esta newsletter.

Además, puede conservar memoria, utilizar skills y trabajar con herramientas, así que encaja bastante bien con muchas de las piezas que hemos ido viendo estos meses en Think&Hack. Hermes está diseñado precisamente para mantener memoria persistente, ejecutar tareas programadas y trabajar de forma desatendida.

**No** voy a convertir las próximas newsletters en un tutorial de instalación de Hermes.

Primero porque probablemente perderíamos a media newsletter por el camino.

Y segundo porque ahora mismo me interesa bastante más saber **si el sistema sirve para algo** que enseñarte a montarlo.

Así que voy a hacer dos cosas distintas:

En Think&Hack iremos viendo el experimento real: qué decide Hacki, qué publica, qué funciona, qué falla y qué voy cambiando; al final de cada news tendremos un apartado llamado Hacki en acción.

Y en el curso de septiembre ordenaré toda la parte de construcción: agente, skills, memoria, tareas programadas, permisos, verificaciones y supervisión.

Si quieres que te avise cuando abra las inscripciones:

👉 **[[Apúntate a la lista de espera]](https://ainalluna.com/curso-agentes-autonomos/index.html)**

---

## Hay cosas que Hacki no va a hacer.

Aquí tuve que decidir dónde terminaba la autonomía del agente y dónde quería seguir estando yo.

Porque técnicamente podría dejar que hiciera bastante más.

Pero que algo se pueda automatizar no significa necesariamente que deba o quiera automatizarlo.

Hacki va a escribir las Notes completas y decidir cuáles cree que merece la pena publicar. Yo las revisaré antes y podré aprobarlas, cambiarlas o descartarlas.

Y hay otra cosa que tengo bastante clara: **Hacki no va a hacerse pasar por mí para hablar contigo nunca.**

Puede encontrar Notes interesantes, conversaciones en las que tenga sentido entrar o creadores con los que podría ser interesante hablar.

*Pero **no va** a dar likes por mí, ni comentar por mí, ni enviar un mensaje privado haciéndose pasar por Aina.*

No sé a ti, pero a mí me parecería bastante feo descubrir que llevo tres semanas hablando con alguien y que en realidad estaba construyendo una relación con su agente.

Así que la división será esta:

**Hacki encuentra dónde merece la pena participar. Yo participo.**

Para empezar voy a probar una regla 10-5-1 por cada Note que publique:

-

10 likes en Notes relevantes.

-

5 comentarios donde realmente tenga algo que aportar.

-

1 creador con el que tenga sentido empezar una conversación.

Todo eso lo haré yo.

¿10-5-1 es la proporción correcta?

Ni idea.

Me la he inventado como punto de partida.

La probamos, medimos y, si no aporta nada, fuera.

---

## Pero antes de dejarle hacer nada, necesitamos una línea de salida.

Aquí empieza la parte que más ganas tenía de mirar.

Si dentro de unas semanas digo que Hacki ha hecho crecer Think&Hack, necesito poder demostrarlo de alguna manera.

Así que antes de ponerlo a trabajar he sacado los datos disponibles de las Notes que he publicado hasta ahora.

La situación de partida es esta (datos a 15 de agosto de 2026). Sí, llevo una semana preparando todo el sistema. Por eso la semana pasada no hubo news.

![imagen](https://substackcdn.com/image/fetch/$s_!1Uiw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F979b7bdb-3a24-48e3-8afa-20007e99bfd3_1047x177.png)

-

**301 Notes publicadas.**

-

**78 suscripciones atribuidas directamente a Notes.**

Y mi primera reacción fue pensar algo bastante obvio:

*si publico más Notes, debería conseguir más suscriptores.*

Pues parece que no.

---

## Mi intuición decía una cosa. Los datos, otra.

![imagen](https://substackcdn.com/image/fetch/$s_!YGuG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9359d8f0-3876-4e56-a180-80ae18ee75d7_1305x313.png)

He comparado cuántas Notes publico cada semana con cuántos suscriptores consigo. **La correlación es de -0,08: prácticamente cero.** Es decir, con los datos que tengo, **publicar más Notes no parece estar relacionado con conseguir más suscriptores.**

Y aquí apareció mi maldito *sesgo de confirmación*, porque mi cabeza seguía pensando: *¿cómo puede ser que publicar más no sea mejor?* Así que me hice otra pregunta: quizá el efecto no se ve en la misma semana. Una Note puede hacer que alguien me descubra hoy, lea varias cosas, me siga y termine suscribiéndose unos días más tarde, así que repetí el análisis mirando qué ocurría **la semana siguiente**.

Así que repetí el análisis mirando si las Notes publicadas una semana antes estaban relacionadas con las **suscripciones atribuidas a Notes durante la semana siguiente**. Ahí la correlación sube a **+0,25**. Hay algo más de señal que en el -0,08 anterior, pero sigue siendo una relación débil, así que tampoco me sirve para concluir que publicar más sea la respuesta.

Así que mi sesgo de confirmación no consiguió salirse con la suya. Con los datos que tengo ahora mismo, **no puedo decir que publicar más Notes haga crecer más Think&Hack**.

Y, en realidad, casi prefiero que haya salido así, porque hace que el experimento sea bastante más interesante. Si hubiese encontrado una relación clarísima entre volumen y crecimiento, el trabajo de Hacki sería bastante aburrido: publicar más Notes y listo.

Pero si producir más contenido no parece ser suficiente, entonces el problema que tiene que resolver es otro.

La pregunta ya no es **“¿cómo conseguimos publicar más?”**, sino **“¿qué hace que una Note consiga suscriptores y podemos aprender a repetirlo?”**.

Y esa pregunta me interesa bastante más.

---

## Tenemos un problema con los datos

Substack me dice **qué Notes han generado suscripciones**, pero no me da las impresiones de cada Note. Así que sé cuáles consiguen suscriptores, pero no puedo saber si es porque convierten mejor o simplemente porque más gente las ha visto.

Eso limita bastante lo que puedo concluir por ahora. Puedo detectar qué Notes están asociadas a más suscripciones, comparar temas, formatos o hooks y buscar patrones, no puedo medir una tasa de conversión real. Para eso necesitaría saber también cuánta gente ha visto cada una.

Así que Hacki tendrá que empezar trabajando con lo que sí tenemos disponible y, a partir de ahí, intentar encontrar señales útiles en los datos.

-

cuántos suscriptores consigue cada Note;

-

qué porcentaje de Notes consigue al menos uno;

-

qué temas aparecen más entre las que funcionan;

-

qué hooks y formatos se repiten;

-

si funcionan mejor las educativas, las personales, las promocionales, las de feedback o las de colaboración;

-

y qué interacciones parecen estar relacionadas con nuevas suscripciones.

Cada semana recogerá los nuevos datos, actualizará el estado del experimento y utilizará lo aprendido para preparar la siguiente.

Y ahí veremos si realmente empieza a encontrar algún patrón.

👉 **Consulta el dashboard completo de Hacki:**
[https://seoutopico.github.io/thinkandhack-performance/](https://seoutopico.github.io/thinkandhack-performance/)

---

## Tú también puedes poner a prueba a Hacki

Todo esto empezó, porque hace unos días publiqué una Note diciendo que no sabía sobre qué escribir y os pedí ideas.

** **me respondió proponiéndome hacer algo con un agente autónomo, o eso quise entender. Pásate por su news, y no dudes en mirar qué son los “Miquelets”.

Y una cosa llevó a la otra.

Así que me parece bastante justo que el experimento siga abierto a ideas externas.

Si se te ocurre una estrategia que debería probar Hacki, una métrica que debería mirar o ves algo en el planteamiento que crees que estoy haciendo mal, **déjamelo en el chat de Substack**.

No prometo hacerle caso a todo, pero sí iré incorporando las propuestas que tengan sentido y contando qué ocurre.

Además, entre las ideas que acabemos incorporando al experimento, sortearé **una plaza para el curso de septiembre**.

👉 **Abriré un chat común para todos :)**

---

[

![imagen](https://substackcdn.com/image/fetch/$s_!a4zT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85a1a880-e624-45ad-8b14-17d37f89f69e_2172x724.png)

](https://substackcdn.com/image/fetch/$s_!a4zT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85a1a880-e624-45ad-8b14-17d37f89f69e_2172x724.png)

#### 📅 Hacki en acción — Semana 0: la línea de salida

Arrancamos, Hacki tiene un objetivo definido y tenemos los datos de partida.

A partir de ahora, cada semana volveré a este mismo bloque para ver **qué ha hecho Hacki, qué ha pasado y qué ha aprendido de ello**.

### Los números

-

**301 Notes publicadas**

-

**78 suscripciones atribuidas a Notes**

-

**43 semanas de datos**

[

![imagen](https://substackcdn.com/image/fetch/$s_!f4uw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F42b33182-f3b8-40c5-baa5-cd23f41a7393_1316x350.png)

](https://substackcdn.com/image/fetch/$s_!f4uw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F42b33182-f3b8-40c5-baa5-cd23f41a7393_1316x350.png)

Esta semana todavía no hay un “antes y después” porque Hacki no ha empezado a tomar decisiones. Estos son los números contra los que compararemos todo lo que ocurra a partir de ahora.

### ¿Qué estamos intentando aprender?

Hay seis cosas que quiero que Hacki, mi agente de IA autónomo, empiece a responder semana a semana:

**1. ¿Cuántos suscriptores consigue cada Note?**

No quiero medir solo cuántas Notes publicamos. Quiero saber cuáles consiguen realmente que alguien decida suscribirse.

**2. ¿Qué porcentaje de Notes consigue al menos un suscriptor?**

Porque quizá no necesitamos publicar más. Quizá necesitamos aumentar la proporción de Notes que hacen algo.

**3. ¿Qué temas aparecen más entre las Notes que funcionan?**

IA, agentes, opinión, experimentos, productividad, algo más personal... veremos si aparece algún patrón.

**4. ¿Qué hooks y formatos se repiten?**

Aquí quiero ver si determinadas formas de abrir una Note o estructurarla funcionan mejor que otras.

**5. ¿Qué tipo de Note funciona mejor?**

Voy a clasificarlas entre educativas, personales, promocionales, feedback, colaboración y las categorías que vayan apareciendo.

**6. ¿Qué ocurre alrededor de las Notes que funcionan?**

Likes, comentarios, conversaciones con otros creadores, restacks... quiero ver si hay señales que ayuden a explicar por qué unas llegan más lejos que otras.

### Lo que ya sabemos en la Semana 0

La primera hipótesis era bastante sencilla:

**publicar más Notes debería conseguir más suscriptores.**

De momento, los datos no la sostienen.

En las 43 semanas completas que tengo disponibles, la correlación entre el número de Notes publicadas y las suscripciones conseguidas esa misma semana es de **-0,08**.

Al mirar la semana siguiente aparece una señal positiva de **+0,25**, pero sigue siendo demasiado débil como para concluir que publicar más provoque más crecimiento.

Así que Hacki empieza con una pregunta bastante más interesante que *“¿cómo publico más?”*:

>
>
> **¿Qué hace que una Note consiga suscriptores y podemos aprender a repetirlo?**
>
>

Consulta el dash para más info: [https://seoutopico.github.io/thinkandhack-performance/](https://seoutopico.github.io/thinkandhack-performance/)

---

**¿Crees que Hacki conseguirá aumentar la media de suscripciones de Think&Hack?**

Esta newsletter ha sido un poco diferente, pero creo que eso es precisamente lo interesante del experimento.

Quiero poner un agente autónomo de verdad delante de un objetivo real, medir lo que ocurre y ver si realmente podemos construir sistemas de IA que no solo ejecuten tareas, sino que **aprendan de los resultados y nos ayuden a acercarnos a un objetivo**.

A partir de la próxima semana empezaremos a tener datos.

P.D Gracias a ** **por recomendar Think&Hack en una de sus Notes. Esa Note es, hasta ahora, la que más suscripciones me ha generado. Si no conoces su news, acércate a leerla; seguro que te engancha :)

![imagen](https://substackcdn.com/image/fetch/$s_!JJqh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6a720b64-fc36-4aad-9283-414b33daeb17_1355x203.png)

Y eso deja otra pequeña pista para Hacki: **quizá no todo dependa de lo que publicas, sino también de quién ayuda a que llegue más lejos.**

Habrá que medirlo.

**👀 Te leo** ¿Tú qué apuestas? ¿Conseguirá aumentar la media de suscripciones de Think&Hack?

[Deja un comentario](https://ainalluna.substack.com/p/agente-ia-autonomo-hermes-agent/comments)

---

## Recursos

-

[Hermes Agent: documentación oficial](https://hermes-agent.nousresearch.com/docs/)

* **Cuéntamelo. Siempre leo todo.***

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

# **Suscríbete a Think&Hack**

**Tools are great. Systems are better.**

Casos reales, flujos que funcionan y formas concretas de usar la IA sin perder el control del proceso.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
