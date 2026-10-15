---
id: 201948710
titulo: "Cómo convertí mi inbox en un sistema verificable de agentes"
subtitulo: "Esta semana di una ponencia sobre cómo pasé de un pipeline lineal a un arnés agentic con cola, memoria, delegación, revisión y cierre verificable."
fecha: 2026-06-14
url: https://ainalluna.substack.com/p/como-converti-mi-inbox-en-un-sistema
tipo: newsletter
audiencia: everyone
estado: completo
huella: f15fef545a57773f6c4bff48b45f0ebe2cdcfe69bd71268f03ff44d1472dc115
---

[

![imagen](https://substackcdn.com/image/fetch/$s_!TFLL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e262513-3f92-474e-881a-91a493ffba59_892x417.png)

](https://substackcdn.com/image/fetch/$s_!TFLL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e262513-3f92-474e-881a-91a493ffba59_892x417.png)

¿Cómo estás?

Soy Aina y esto es Think&Hack.

Esta semana di una ponencia de 20 minutos sobre algo que me lleva obsesionando bastante tiempo: **qué pasa cuando dejamos de usar la IA como una conversación y empezamos a rodearla de un sistema.**

No hablé de prompts mágicos.

No hablé de una herramienta nueva que lo hace todo.

Hablé de una cosa mucho menos vistosa, pero mucho más importante si quieres trabajar con agentes de verdad: **cómo diseñar un arnés alrededor de la IA para que pueda operar, fallar, revisar y cerrar bien.**

La charla se titulaba: *Cómo convertí mi inbox en un sistema verificable de agentes*.

Y la tesis era esta:

**No rehice carpetas. Cambié el contrato de trabajo con la IA.**

Antes tenía un sistema potente: inbox, proyectos, memoria, comandos, agentes, hooks, skills y automatización. Funcionaba. Me ayudaba a convertir entradas sueltas en trabajo organizado.

Pero había un problema de fondo.

El sistema dependía demasiado de que el modelo recordara qué estaba haciendo, qué faltaba, qué criterio tenía que cumplir y cuándo podía decir “he terminado”.

Y ahí aparece una de las frases centrales de la charla:

**Un agente no termina cuando responde. Termina cuando verifica.**

Si quieres aprender a convertir la IA en sistemas útiles, suscríbete a Think&Hack.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)

---

## El problema: confundimos respuesta con cierre.

Cuando trabajas con IA en tareas pequeñas, una respuesta puede parecer suficiente.

Le pides que resuma algo, que reescriba un texto, que proponga una estructura o que te ayude a pensar una idea. La conversación empieza, la conversación termina y tú decides si te sirve.

Pero cuando empiezas a usar agentes para operar sobre sistemas reales, esa lógica se rompe.

Un agente puede tocar archivos, mover documentos, actualizar estados, clasificar una bandeja de entrada, crear proyectos, lanzar comandos, dejar trazas en una memoria y coordinar subagentes.

Y entonces la pregunta ya no es: “¿Me ha dado una buena respuesta?”.

La pregunta es otra:

**¿El sistema puede demostrar que la tarea está hecha?**

Ese matiz lo cambia todo.

Porque el agente puede sonar seguro y estar equivocado. Puede decir que ha actualizado un README y haber olvidado una parte. Puede procesar una entrada y dejar un adjunto huérfano. Puede cambiar el estado de un proyecto y no dejar log. Puede cerrar una tarea porque su resumen parece coherente, no porque haya verificado la evidencia.

Ese era el fallo de diseño de mi sistema anterior.

No le faltaban piezas. Tenía muchas.

Tenía comandos para procesar inbox, crear proyectos, refrescar estado, hacer lint del sistema y mantener memoria.

Tenía subagentes para clasificar entradas, actualizar proyectos, refrescar estado y mantener la wiki.

Tenía hooks para enganchar comportamiento al arranque, validar el sistema y evitar cierres falsos.

**Era potente.**

Pero no formaba un ciclo cerrado de trabajo.

[

![imagen](https://substackcdn.com/image/fetch/$s_!NWeO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F22ddb439-a960-4970-baf6-ae85bba8ecaa_992x314.png)

](https://substackcdn.com/image/fetch/$s_!NWeO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F22ddb439-a960-4970-baf6-ae85bba8ecaa_992x314.png)

Había acción, automatización y memoria. Pero el cierre seguía siendo débil.

## La solución: default-FAIL

La nueva versión parte de una regla muy sencilla:

**Por defecto, nada está hecho.**

No porque desconfiemos de la IA de forma abstracta. Sino porque, si el sistema puede cambiar cosas importantes, el cierre no puede depender del tono de seguridad del modelo.

La unidad de trabajo entra en una cola; el líder la lee, los workers ejecutan, el revisor contrasta, el check valida y solo entonces se puede marcar como hecho.

**El flujo ya no es: **“Haz esto y dime cuando termines”.

**Es:** “Esta unidad tiene criterios de aceptación. Trabaja sobre ella, deja evidencia, permite revisión y no cierres hasta que el sistema lo demuestre”.

**Ahí aparece el arnés.**

No como una metáfora bonita, sino como una arquitectura concreta:

```
`_cola/` para convertir peticiones en unidades verificables.
`_progress/` para sacar memoria operativa del contexto.
`_projects/` para mantener el dominio.
`_memory/` para dejar aprendizaje y trazabilidad.
`bin/check.ps1` para validar invariantes.
agentes `.md` para definir roles.
playbooks para describir procesos.
revisor para juzgar evidencia.
```

[

![imagen](https://substackcdn.com/image/fetch/$s_!-OBK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e204ee5-d2e8-448d-9e7b-06809378efd1_979x384.png)

](https://substackcdn.com/image/fetch/$s_!-OBK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e204ee5-d2e8-448d-9e7b-06809378efd1_979x384.png)

---

## La cola cambia todo.

Uno de los cambios más importantes fue convertir las peticiones en unidades de trabajo explícitas.

Antes, una petición podía vivir como una frase: “Procesa esto”, “actualiza este proyecto”, “archiva esta comunicación” o “crea una nueva ficha”.

El problema es que una frase deja demasiado espacio a la interpretación. Y cuando una sesión se alarga, se compacta, se interrumpe o cambia de agente, esa interpretación empieza a degradarse.

**Ahora una unidad vive en `_cola/trabajo.json`.**

Tiene un `id`, un tipo, un título, criterios, estado y, sobre todo, una definición externa a la conversación.

Por ejemplo, una unidad no se cierra porque el agente diga “he terminado”.

Se cierra si se cumplen criterios como:

-

el README se ha actualizado;

-

el log ha recibido una entrada append-only;

-

`STATUS.md` queda coherente si cambia el estado;

-

`bin/check` sale en verde;

-

el revisor devuelve `PASS`.

Esto parece más complejo.

Lo es.

Pero esa complejidad compra algo que la conversación sola no puede darte: **continuidad**.

Si la sesión se corta, la cola sigue ahí. Si el contexto se compacta, `_progress/` sigue ahí. Si otro agente retoma la tarea, los criterios siguen ahí.

Una unidad pendiente sigue pendiente aunque el agente anterior se sintiera terminado.

[

![imagen](https://substackcdn.com/image/fetch/$s_!peix!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F398db976-67b3-4a97-81c4-2b61f5a2c85a_1110x456.png)

](https://substackcdn.com/image/fetch/$s_!peix!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F398db976-67b3-4a97-81c4-2b61f5a2c85a_1110x456.png)

---

## Sacar la memoria del modelo

Hay una idea que atraviesa toda la charla:

**Memoria útil no es más contexto. Es estado legible y verificable.**

Durante mucho tiempo hemos tratado la ventana de contexto como si fuera el lugar natural donde debía vivir el trabajo.

Añades más instrucciones, más historial, más ejemplos, más documentos y más conversación.

Y durante un rato funciona.

Hasta que deja de funcionar.

El contexto se vuelve pesado. El agente empieza a mezclar pasos. Recuerda unas cosas y pierde otras. Arrastra decisiones antiguas. Resume demasiado. O peor: mantiene una sensación de continuidad que ya no está respaldada por el estado real del sistema.

Por eso en el arnés la memoria operativa sale del modelo.

**Los subagentes no tienen que devolverlo todo en la conversación principal: escriben en `_progress/`, el líder puede leer lo necesario y el revisor puede contrastar lo que se hizo.**

El sistema puede continuar sin exigir que el modelo cargue todo en la cabeza.

Esto no elimina el contexto.

Lo vuelve más limpio.

El agente usa la conversación para coordinar y razonar, no para sostener todo el estado del mundo.

El arnés, en ese sentido, es un patrón de navegación.

Le dice al agente dónde mirar, qué dejar escrito, qué comprobar y cuándo no puede cerrar.

[

![imagen](https://substackcdn.com/image/fetch/$s_!T3lc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F207be2ca-80cf-44f6-9f3e-040de06a5608_1818x872.png)

](https://substackcdn.com/image/fetch/$s_!T3lc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F207be2ca-80cf-44f6-9f3e-040de06a5608_1818x872.png)

---

## El revisor no evalúa intenciones.

La **pieza **más **importante **no es el líder ni son los workers. Es el **revisor**.

Porque el revisor cambia la pregunta.

**No pregunta:** “¿El agente dice que lo ha hecho?”.

**Pregunta:** “¿Dónde está la evidencia?”.

**El protocolo del revisor es muy concreto:**

1.

Lee los criterios de aceptación.

2.

Lee `_`rogress/<run-id>/`.`

3.

Contrasta con el `git diff`.

4.

Verifica las escrituras esperadas.

5.

Ejecuta `bin/check`.

6.

Devuelve `PASS` o `NEEDS_WORK`.

Esa última parte importa.

Ante la duda, `NEEDS_WORK`.

No porque queramos ponerle trabas al agente, sino porque la autonomía sin revisión produce deuda.

[

![imagen](https://substackcdn.com/image/fetch/$s_!uaxX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6362b779-806f-48ba-b3ec-b3838961a8af_1035x606.png)

](https://substackcdn.com/image/fetch/$s_!uaxX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6362b779-806f-48ba-b3ec-b3838961a8af_1035x606.png)

Un sistema agentic que puede hacer cosas por ti necesita una forma de decir: “Todavía no”.

Y esa forma no puede depender de una intuición. Tiene que depender de criterios.

---

## El arquitecto cambia el sistema

La otra pieza que enseñé en la ponencia es el arquitecto.

Si el líder opera el sistema y el revisor valida el trabajo, el arquitecto cambia el propio arnés. Es el **agente **que **entra **cuando no **quieres **procesar una unidad más, sino **extender el sistema:** añadir una regla, crear un comando, modificar una skill, documentar una convención o sumar una nueva comprobación.

Esto también cambia el tipo de confianza que puedes tener en el sistema.

Porque una mejora no se queda solo como “a partir de ahora acuérdate de esto”. Si aparece una regla nueva, el arquitecto la documenta y añade la forma de verificarla en `bin/check`.

El sistema no mejora porque el modelo prometa portarse mejor la próxima vez.

Mejora porque una parte del arnés cambia.

[

![imagen](https://substackcdn.com/image/fetch/$s_!ywqq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c2192c7-c822-4565-914d-1b08e37ee735_1077x805.png)

](https://substackcdn.com/image/fetch/$s_!ywqq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c2192c7-c822-4565-914d-1b08e37ee735_1077x805.png)

---

## El repo que enseñé en el QR

Al final de la ponencia puse un QR al repo porque no quería que esto quedara como una idea abstracta.

**El ejemplo está aquí: **[https://github.com/seoutopico/pm_claude_code/tree/v3](https://github.com/seoutopico/pm_claude_code/tree/v3)

Es un sistema de gestión de proyectos en Claude Code, hecho con Markdown, memoria persistente, agentes, cola de trabajo y checks. La gracia está en comparar la V1 con la V3: el dominio es parecido, pero la V3 añade el arnés que convierte una petición en una unidad trazable y revisable.

Ahí se ve mucho mejor el cambio: no es pedirle a la IA que “sea más cuidadosa”, sino construir un entorno donde no pueda cerrar sin evidencia.

Para mí, esa es la parte importante: **la respuesta ya no es el final del trabajo. El final del trabajo es la evidencia.**

En la ponencia cerré con una frase que resume muy bien el punto:

**Que la IA gestione sistemas no la convierte en responsable. La responsabilidad sigue siendo tuya.**

Por eso me interesa tanto esta forma de trabajar. No quita responsabilidad: la vuelve más visible.

**Un agente no termina cuando responde. Termina cuando verifica.**

Si al leer esto has pensado “esto es justo lo que me pasa cuando intento usar agentes para trabajo real”, probablemente conoces a alguien que también debería leerlo.

[Compartir](https://ainalluna.substack.com/p/como-converti-mi-inbox-en-un-sistema?utm_source=substack&utm_medium=email&utm_content=share&action=share)

## Recursos:

**El repo para trastear: **[https://github.com/seoutopico/pm_claude_code/tree/v3](https://github.com/seoutopico/pm_claude_code/tree/v3)

**La presentación: **[https://docs.google.com/presentation/d/1K8syMHbtw_TaLoB57Z7HIHKXc7MiGUpav6cYLfdYhVc/edit?usp=sharing](https://docs.google.com/presentation/d/1K8syMHbtw_TaLoB57Z7HIHKXc7MiGUpav6cYLfdYhVc/edit?usp=sharing)

***Cuéntamelo. Siempre leo todo.***

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

# **Suscríbete a Think&Hack**

Casos reales, flujos que funcionan y formas concretas de usar la IA sin perder el control del proceso.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
