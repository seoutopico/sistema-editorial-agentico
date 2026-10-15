---
id: 217023771
titulo: "He probado un nuevo modelo de IA y he acabado definiendo qué es un sándwich."
subtitulo: "Jev promete clasificar información más rápido y más barato. Lo pongo a prueba para comprobar si estamos pagando de más por tareas que no necesitan una conversación con ChatGPT. "
fecha: 2026-09-27
url: https://ainalluna.substack.com/p/jev-typesafe-que-es-como-funciona
tipo: newsletter
audiencia: everyone
estado: completo
huella: a138fbe9861a4e2acde4f8b195c538d0167dbaae77c0390ed4a5c8560b206af8
---

[

![imagen](https://substackcdn.com/image/fetch/$s_!kYsN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84885397-747c-4cdb-9ce4-30f74cf54318_1672x941.png)

](https://substackcdn.com/image/fetch/$s_!kYsN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84885397-747c-4cdb-9ce4-30f74cf54318_1672x941.png)

*¿Cómo estás?*

*Soy Aina y esto es Think&Hack.*

Ayer me tiré de cabeza a probar un modelo de IA y acabé pensando qué características tiene que tener una comida para considerarse un sándwich.

Sí, ese fue mi rato de investigación del día. :)

Este nuevo modelo es [Jev, de TypeSafe](https://typesafe.ai/blog/introducing-system-one-models-and-jev), y está pensado para* clasificar y evaluar información*. Curioso, ¿no?, pero, *¿qué tiene esto de interesante si ya lo puedes hacer con cualquier modelo?*

Básicamente, porque lo presentan como un **LLM con el cual NO puedes chatear, es muy rápido y muy, muy barato. **

[

![imagen](https://substackcdn.com/image/fetch/$s_!tPpF!,w_1456,c_limit,f_auto,q_auto:good,fl_lossy/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e708fe6-1aa7-403f-81e5-9afd00a588a4_500x281.gif)

](https://substackcdn.com/image/fetch/$s_!tPpF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e708fe6-1aa7-403f-81e5-9afd00a588a4_500x281.gif)

*Con esa promesa de ahorrar tiempo y dinero*, me puse a leer su documentación y a trastear con su playground. Uno de los ejercicios era decidir si algo es un sándwich o no. Parece fácil, pero ¿tú considerarías un perrito caliente un sándwich?

---

## Vale, pero ¿qué estamos llamando sándwich?

En el playground de Jev, la página donde puedes probar el modelo, hay un ejercicio que consiste en decidir si una comida es un sándwich. Parece fácil, ¿no? Pan, algo de relleno… Pero entonces aparece un perrito caliente. ¿Lo consideramos como sándwich? ¿O el pan tiene que estar separado en dos piezas para ser un sándwich? 😥

Aquí es donde el trabajo se complica si queremos tener buenos resultados a la hora de clasificar: si al definir qué es un sándwich decimos que tiene que llevar un relleno entre dos trozos de pan separados, el hot dog quedaría fuera. En cambio, si aceptamos que el pan siga unido por un lado, entonces sí lo consideraríamos un sándwich.

Con la documentación leída y el ejemplo elegido, quise ir un poco más allá:** ¿merece la pena pararse a pensar qué consideramos un sándwich y describir los alimentos que le damos al modelo? **

### ¿Notará Jev que me he currado el contexto?

Elegí cuatro alimentos para poner a prueba a Jev: un perrito caliente, un taco, un burrito y un calzone.

De cada uno preparé dos versiones:

-

**Solo el nombre:** «hot dog».

-

**El nombre y una descripción:** «hot dog: una salchicha dentro de un pan parcialmente cortado, cuyos lados siguen unidos».

Quiero comprobar si Jev responde lo mismo cuando le pongo «hot dog» que cuando le cuento cómo está hecho.

En ambos casos le doy la misma definición de sándwich. Así comparo las respuestas sin cambiar también las reglas a mitad de la prueba.

[

![imagen](https://substackcdn.com/image/fetch/$s_!xG0b!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb66f5daf-d298-4a6f-8a61-6c6123c52a81_1908x1023.png)

](https://substackcdn.com/image/fetch/$s_!xG0b!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb66f5daf-d298-4a6f-8a61-6c6123c52a81_1908x1023.png)Ejemplo de cómo Jev clasifica alimento en base a definiciones previas.

Cuando solo le pongo “hot dog”, Jev da un 55 % de probabilidad de que sea un sándwich, lo que viene siendo un: *puede que sí, puede que no*. Pero cuando le defino qué es un perrito caliente, esa probabilidad sube al 84 %: con esa información, el modelo se inclina mucho más por decir que sí, que es un sándwich.

Con el perrito caliente y el calzone hay más dudas: uno lleva el relleno dentro de un pan abierto por un lado y el otro dentro de una masa cerrada. Según cómo definamos un sándwich, podemos considerarlos sándwiches o no. Al describir cómo están hechos, además de explicarle qué entendemos por sándwich, *le damos más información para aplicar ese criterio sin depender tanto de lo que el modelo interprete solo por el nombre.*

Y esto me lleva a algo de lo que hemos hablado varias veces: **le pedimos a la IA que haga un trabajo dando por hecho que entiende lo mismo que nosotros.** Pero una cosa es que conozca la palabra y otra que sepa qué queremos decir con ella en nuestro caso, en qué detalles nos fijamos y por qué tomamos una decisión y no otra.

Todo eso lo tenemos en la cabeza, pero ¿se lo hemos explicado?

Y por eso me he acordado de [Juan](https://ainalluna.substack.com/p/implementar-ia-empresa-empezar) y de todo lo que sabía después de quince años en la empresa, pero nunca había escrito. Lo que para él era obvio por experiencia, había que documentarlo para que otros pudieran utilizarlo. Con la IA nos toca hacer ese mismo esfuerzo, aunque empecemos por algo tan sencillo como explicar qué entendemos por sándwich.

Si queremos que la IA clasifique algo según nuestro criterio, tenemos que explicárselo, aunque a nosotros nos parezca obvio.

## Y todo esto, ¿es tan rápido y barato como prometen?

Que me haya puesto a pensar en sándwiches no significa que me haya olvidado de por qué entré a probarlo. Jev promete hacer estas tareas rápido y barato.

Para comprobarlo, he pasado el mismo ejercicio a Jev y a GPT-5.5, con las mismas preguntas y criterios. Vamos a ver qué pasa con nuestro ejemplo.

La diferencia se ve enseguida:

![imagen](https://substackcdn.com/image/fetch/$s_!ds5K!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc20ea7d8-20cf-46fc-9474-9eef19d38625_541x146.png)

Jev frente a GPT-5.5 con razonamiento medio: tiempo de respuesta y coste estimado para los mismos ocho casos de clasificación en esta prueba.

En esta ejecución, GPT-5.5 ha tardado casi **19 veces más** y el coste estimado ha sido unas **354 veces mayor**. Lo he utilizado con razonamiento medio, así que estos números corresponden a esa configuración y a esta prueba.

Para hacernos una idea del coste: repetir mil veces esta misma consulta, con el mismo consumo, supondría unos **0,06 dólares con Jev frente a 22,68 dólares con GPT-5.5**.

**Cuando una tarea se repite constantemente dentro de un proceso, la diferencia de coste entre modelos de IA se acumula. Merece la pena comprobar si un modelo más barato puede hacer ese trabajo con la calidad que necesitamos.**

Pero para aprovecharlo tenemos que hacer el trabajo que hemos visto antes: **tener claro qué queremos clasificar, definir las categorías y describir los elementos que le vamos a pasar**. Qué significa cada categoría, qué condiciones debe cumplir algo para pertenecer a ella y qué información necesita el modelo para distinguir unas de otras.

Pero además del tiempo y el coste, fíjate en cómo cambia la respuesta según lo que le contamos. Solo con el nombre, Jev da un 54 % de probabilidad de que el perrito caliente sea un sándwich; cuando le explicamos cómo está hecho, sube al 81 %. No significa que haya acertado más, pero sí que un detalle que nosotros damos por supuesto puede cambiar su valoración.

[

![imagen](https://substackcdn.com/image/fetch/$s_!QcVe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F80957750-4ebd-4568-87e0-098b2dc5cce0_707x715.png)

](https://substackcdn.com/image/fetch/$s_!QcVe!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F80957750-4ebd-4568-87e0-098b2dc5cce0_707x715.png)Jev ante el mismo alimento: con solo «hot dog» devuelve un 54 % de probabilidad de “sí, es un sándwich”; con una descripción, un 81 %. La definición de sándwich es la misma en ambos casos.

Si queremos que clasifique según nuestro criterio, tenemos que explicar tanto las categorías como lo que le estamos pidiendo que clasifique. Aunque a nosotros nos parezca obvio.

---

## ¿Y para qué utilizaría algo así?

No solo he estado probando cómo clasifica Jev en diferentes casos de uso, sino que también he recorrido medio YouTube y Reddit para ver qué está haciendo la gente con él. *Lleva apenas una semana en el mercado*, así que lo que he encontrado son *experimentos y primeras pruebas como estas:*

-

**Ponerlo a comprar y vender.** Hay quien ha conectado Jev a datos de precios para que decida si comprar o vender. Y yo ya estoy pensando en llevarlo a la segunda mano… Wallapop, calienta que sales. :) 💵💵

-

**Que elija dónde hacer clic en una web.** Le dan información sobre la página y una lista de elementos con los que puede interactuar. Jev elige el botón o el campo y el programa hace el clic o escribe. Si la respuesta no es suficientemente clara, le pasan el trabajo a otro modelo. ¿Útil?

-

**Revisar lo que otro agente quiere ejecutar en la terminal.** Antes de ejecutar un comando, Jev comprueba si podría hacer algo peligroso o necesitar autorización. Me interesa esta prueba porque, cuando un agente encadena muchas acciones, también importa cuánto tarda en revisar cada una. ¡Todo es probar!

-

**Recurrir al modelo caro solo cuando haga falta.** Primero responde Jev y, cuando su nivel de confianza es bajo, se utiliza la respuesta de un modelo más potente. Hay que hacer algún test para ver si funciona y así reducir costes. Interesante.

-

**Ponerlo a jugar a Doom.** Le pasan el estado del juego convertido a datos y Jev elige qué hacer unas diez veces por segundo. No está viendo la pantalla: alguien ha preparado la información que recibe para que pueda decidir su siguiente movimiento. El otro día, mi compi de trabajo me comentó que hay gente que paga para que sigan jugando en sus cuentas mientras ellos curran .. Esto da para otro post).

Yo, de momento, ya tengo unas cuantas ideas para seguir probando. Quiero ver si puedo aprovechar Jev en alguno de los procesos que ya tengo montados y si lo que ahorro en tiempo y coste compensa lo que tenga que revisar después. Ya te contaré.

¿Qué tarea de tu día a día te gustaría que hiciera la IA, pero todavía no le has explicado cómo la haces tú?

#### ***Cuéntamelo. Siempre leo todo.***

[Deja un comentario](https://ainalluna.substack.com/p/jev-typesafe-que-es-como-funciona/comments)

**P.D.** En noviembre vuelvo a dar clase en **The Bridge**, esta vez dentro del Máster de IA Generativa Avanzada.

Y me apetecía contarlo porque no es una colaboración que haya aceptado “porque sí”.

Antes de verano di con ellos dos sesiones sobre Claude Code y salí bastante sorprendida. Dar clase online muchas veces tiene una barrera rara: tú hablas, ves cámaras apagadas y cuesta saber si al otro lado realmente está pasando algo.

Aquí fue distinto.

La propia dinámica de la escuela hacía que la gente participara, preguntara y se metiera de verdad en la clase. Y, sobre todo, noté que los alumnos ya tenían suficiente base como para que no sonara a chino hablar de cosas como agentes, memoria, contexto, verificación o cómo llevar IA a procesos reales.

Eso, como profesora, se agradece muchísimo.

Así que cuando me propusieron volver para esta nueva edición, me hizo bastante ilusión.

Esta vez voy a trabajar precisamente en la parte que más me interesa: **cómo pasar de usar herramientas de IA a diseñar sistemas de trabajo con criterio, control y capacidad real de llevarlos a producción.**

Si te apetece profundizar por ahí, te dejo el programa:

👉 [https://hubs.la/Q04sVMh10](https://hubs.la/Q04sVMh10)

---

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

# **Suscríbete a Think&Hack**

**Tools are great. Systems are better.**

Casos reales, flujos que funcionan y formas concretas de usar la IA sin perder el control del proceso.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
