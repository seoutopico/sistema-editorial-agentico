---
id: 199565877
titulo: "Cuando la IA se pierde en la conversación (y por qué insistir puede empeorarlo)"
subtitulo: "4 formas de recuperar el control del contexto."
fecha: 2026-05-31
url: https://ainalluna.substack.com/p/ia-se-pierde-conversacion-control-contexto
tipo: newsletter
audiencia: everyone
estado: completo
huella: 4b93f3ad25a28e981f4dc323d5152c263bd61d80cdd1037b49007c6910d4ab9e
---

¿Cómo estás?

Soy Aina y esto es Think&Hack.

Esta semana te cuento por qué algunas de tus mejores conversaciones con la IA se tuercen a mitad de camino y qué puedes hacer para recuperar el control del contexto.

Si te interesa entender no solo qué hace la IA, sino cómo trabajar mejor con ella, suscríbete a Think&Hack y empieza a sacarle más partido desde hoy.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)

[

![imagen](https://substackcdn.com/image/fetch/$s_!ww4o!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59abb384-a3b1-44ab-a2b3-81c9c677195e_1254x1254.png)

](https://substackcdn.com/image/fetch/$s_!ww4o!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59abb384-a3b1-44ab-a2b3-81c9c677195e_1254x1254.png)

## No todos los fallos de contexto son iguales.

Un caso es cuando empiezas con una tarea incompleta y vas añadiendo requisitos. Ahí el modelo puede precipitarse, asumir demasiado pronto qué quieres y luego parchear la respuesta sobre una primera solución equivocada. Ese fenómeno está descrito en investigaciones sobre conversaciones multivuelta: los modelos rinden peor cuando la tarea se revela poco a poco que cuando se entrega completa desde el inicio.

**Pero hay un caso más interesante: **cuando no solo añades requisitos, sino que cambias de marco.

Empiezas explorando una idea. La primera respuesta te sirve para pensar. Aprendes algo, descartas la dirección inicial y abres otra rama. Para ti, la conversación ha cambiado de nivel. Para el modelo, muchas veces no. El modelo interpreta tu nuevo mensaje como una continuación de la trayectoria anterior, no como una reescritura de la intención.

A veces la IA no falla porque olvide el contexto, sino porque recuerda demasiado bien el contexto equivocado.

Esta idea aparece muy bien explicada en un paper reciente sobre conversaciones multivuelta y **desajuste de intención** (*intent mismatch*). La tesis es sencilla: muchas veces el problema no es que el modelo ignore lo que dices, sino que coloca tu nueva instrucción en el sitio equivocado. ***La interpreta como una continuación de su respuesta anterior, no como una actualización de tu intención original.***

Por eso corregir dentro del mismo hilo puede fallar: la corrección no llega a una página en blanco, llega a una conversación que ya arrastra una interpretación previa.

[

![imagen](https://substackcdn.com/image/fetch/$s_!hlID!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff9ca1afd-0f68-42a9-82a1-f2c623c2508f_1183x484.png)

](https://substackcdn.com/image/fetch/$s_!hlID!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff9ca1afd-0f68-42a9-82a1-f2c623c2508f_1183x484.png)[Fuente del paper: https://arxiv.org/pdf/2602.07338](https://arxiv.org/pdf/2602.07338)

---

## 4 formas de recuperar el control del contexto

Antes de seguir corrigiendo al modelo, hazte una pregunta: *¿El problema está en la respuesta o en el contexto desde el que está respondiendo?*

Si el contexto ya arrastra una interpretación vieja, añadir más instrucciones al final puede no arreglar nada. No necesitas insistir más: necesitas cambiar el punto desde el que el modelo está pensando.

**Editar, ramificar, rebobinar o reiniciar.**

### 1. Editar el mensaje anterior.

![imagen](https://substackcdn.com/image/fetch/$s_!Rz3r!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b170392-c213-479a-9607-fc6edb6b4c55_713x130.png)

Esta técnica consiste en modificar un mensaje previo, normalmente con el lápiz de edición, para que el modelo responda desde esa versión corregida.

**Cuándo usarlo:** cuando sabes dónde nació el malentendido: una instrucción ambigua, una hipótesis mal formulada o una petición incompleta.

**Por qué funciona:** en vez de añadir una corrección al final del hilo, cambias el punto de origen del contexto. No le dices al modelo “corrige lo que entendiste mal”; haces que vuelva a partir de una instrucción mejor.

### 2. Crear una nueva rama

![imagen](https://substackcdn.com/image/fetch/$s_!ajkG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fff5e28b3-f0a7-4166-a1d6-604aa9a09760_758x216.png)

En ChatGPT, esta opción aparece como “Hilo nuevo desde este chat”: crea una conversación nueva desde un punto concreto sin borrar la original.

**Cuándo usarlo:** cuando quieres explorar otra dirección sin perder la conversación original.

**Por qué funciona:** separa caminos. Si una idea nueva no debería mezclarse con la trayectoria anterior, la conviertes en una rama independiente. Así evitas que el modelo intente reconciliar hipótesis incompatibles dentro del mismo hilo.

### 3. Usar `/rewind` en Claude Code

[

![imagen](https://substackcdn.com/image/fetch/$s_!BIgs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F87053f3f-a359-4607-ad90-586be5a17a6e_1108x562.png)

](https://substackcdn.com/image/fetch/$s_!BIgs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F87053f3f-a359-4607-ad90-586be5a17a6e_1108x562.png)

Si usas **Claude Code**, `/rewind` sirve para volver a un punto anterior de la conversación y eliminar los turnos posteriores al desvío.

**Cuándo usarlo:** cuando Claude Code ha tomado un mal camino hace pocos turnos y quieres continuar desde antes del error.

**Por qué funciona:** no intentas corregir encima de la trayectoria equivocada. La borras del contexto y sigues desde el último punto sano.

### 4. Reiniciar en un chat nuevo.

A veces la mejor solución no es seguir afinando el hilo, sino cerrarlo. Toma distancia y empieza una conversación desde cero, sin arrastrar todo el historial anterior.

**Cuándo usarlo:** cuando el objetivo ha cambiado demasiado o la conversación ya está contaminada por pruebas fallidas, correcciones, contradicciones o ruido.

**Por qué funciona:** corta el arrastre contextual. Pero no conviene copiar todo el historial: lo útil es llevar solo un resumen limpio con el objetivo actual, las restricciones importantes, las decisiones válidas y lo que ya no quieres que el modelo asuma.

---

La próxima vez que una conversación con la IA empiece brillante y se tuerza a mitad de camino, no asumas automáticamente que el modelo “se ha vuelto tonto”.

Puede que simplemente esté atrapado en una interpretación vieja.

Y cuando eso pasa, insistir más no siempre ayuda. A veces solo añade otra capa de ruido sobre un contexto que ya iba torcido.

La habilidad no está solo en escribir mejores prompts. Está en saber cuándo continuar, cuándo editar, cuándo abrir una rama y cuándo empezar de cero.

Porque trabajar bien con IA no consiste en tener una conversación infinita.

Consiste en conservar vivo solo el contexto que todavía sirve.

**Ahora te pregunto: **cuando una conversación con la IA se tuerce, *¿qué haces: insistes en el mismo hilo, editas el punto de partida, abres una rama o empiezas de cero?*

***Cuéntamelo. Siempre leo todo.***

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

# **Suscríbete a Think&Hack**

Casos reales, flujos que funcionan y formas concretas de usar la IA sin perder el control del proceso.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
