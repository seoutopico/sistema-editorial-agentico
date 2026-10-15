---
id: 209140975
titulo: "Cinco agentes no son una estrategia de IA"
subtitulo: "Cómo diseñar y medir un piloto de IA para comprobar si un agente mejora el proceso antes de escalarlo."
fecha: 2026-08-02
url: https://ainalluna.substack.com/p/piloto-ia-disenar-medir-escalar
tipo: newsletter
audiencia: everyone
estado: completo
huella: 8fcdec01ba08b3db278630e2d74cf293ef9275f21fa4fc2b13137b36717fad7d
---

[

![imagen](https://substackcdn.com/image/fetch/$s_!Ko-t!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26524585-bbe3-4fc0-8f75-327ea15d65ec_1254x1254.png)

](https://substackcdn.com/image/fetch/$s_!Ko-t!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26524585-bbe3-4fc0-8f75-327ea15d65ec_1254x1254.png)

¿Cómo estás?

Soy Aina y esto es Think&Hack.

Acabo de terminar el **Programa en Resolución de Problemas Complejos de UNIR**. Durante seis meses hemos trabajado metodologías de diagnóstico, análisis, estrategia y comunicación y, en paralelo, hemos desarrollado y defendido un caso práctico en un equipo de cinco personas.

La formación ha coincidido con una serie de newsletters en la que hemos construido varias piezas de un sistema con IA: una skill para conservar el método, un agente para recibir el trabajo y un arnés para limitarlo y comprobarlo.

Podríamos seguir añadiendo componentes. Sin embargo, esta formación me ha devuelto a una pregunta anterior a todos ellos:

**¿Qué problema justifica construir el sistema?**

Puedes tener una skill bien definida, un agente que respeta sus límites y un arnés que verifica cada salida. Todo puede funcionar exactamente como lo diseñaste y, aun así, no mejorar el trabajo que querías mejorar.

Una herramienta puede cumplir exactamente su función y, aun así, fracasar en su propósito: la eficacia técnica no compensa una estrategia que ha elegido la solución antes de comprender el problema.

Esta semana no quiero enseñarte otra pieza técnica. Quiero llevar una idea de la resolución de problemas complejos a la implantación de IA: dejar de aprobar soluciones acompañadas de una cifra y empezar a formular hipótesis que podamos poner a prueba.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)

---

## El error de empezar por los agentes

Imagina que una organización aprueba este plan:

>
>
> `Implantaremos cinco agentes y reduciremos costes un 20 %.`
>
>

La frase parece concreta. Tiene una tecnología, una cantidad y un resultado. También esconde casi todo lo que necesitamos saber.

¿Dónde está hoy el problema? ¿Qué parte del proceso genera el coste? ¿Por qué pensamos que un agente puede cambiarla? ¿De dónde sale el 20 %? ¿Qué ocurre si la herramienta acelera una tarea, pero añade revisión en la siguiente? ¿Qué calidad no estamos dispuestos a perder? ¿Cuándo sabremos que conviene corregir el sistema en lugar de ampliarlo?

«Implantar cinco agentes» describe una **actividad**. «Reducir costes un 20 %» promete un **impacto**. Entre ambas cosas falta el argumento que las conecta.

La organización ha elegido la solución antes de terminar el diagnóstico y ha convertido dos suposiciones en certezas: que los agentes atacan la causa relevante y que hacerlo producirá ese ahorro. A partir de ahí, el piloto corre el riesgo de convertirse en una demostración: ya no se diseña para averiguar si la idea funciona, sino para justificar una decisión tomada.

Este orden resulta especialmente tentador con la IA. La solución es visible, nueva y fácil de enseñar. El problema, en cambio, suele ser más incómodo: información dispersa, responsabilidades mal repartidas, aprobaciones innecesarias, datos que llegan tarde o procesos que nadie ha observado de principio a fin.

Cuando una organización empieza por la tecnología, termina buscando una dificultad que la justifique; el diagnóstico deja de orientar la decisión y pasa a servir de coartada.

[Compartir](https://ainalluna.substack.com/p/piloto-ia-disenar-medir-escalar?utm_source=substack&utm_medium=email&utm_content=share&action=share)

## Antes del piloto: diagnosticar el problema correcto

Una de las ideas centrales que hemos trabajado venía de Richard Rumelt: la estrategia es, en esencia, resolución de problemas. Su núcleo encadena **diagnóstico, política guía y acciones coherentes**. No empieza con un roadmap ni con una cifra aspiracional, sino con una explicación de qué desafío importa y qué lo está sosteniendo.

Esto no convierte cualquier caso de uso de IA en un problema complejo. **La gestión de tickets, tal como la hemos planteado, es un proceso operativo acotado:** tiene entradas observables, etapas identificables y resultados que podemos medir. Puede ser complicado, pero no es complejo en el sentido de CPS que hemos estudiado durante el programa.

Lo que traslado de este aprendizaje no es la etiqueta, sino una forma de razonar que también resulta útil aquí: separar el problema de la solución, tratar el diagnóstico como una explicación que debe comprobarse y decidir de antemano qué evidencia nos hará continuar, corregir o parar.

Supongamos que las solicitudes de clientes tardan demasiado. Podemos observar que el equipo dedica muchas horas a clasificar correos, buscar información y preparar una primera respuesta. Aun así, todavía no sabemos si esa es la causa principal del retraso.

Quizá el cuello de botella esté en la aprobación posterior. Quizá la información necesaria no está actualizada. Quizá las solicitudes llegan mal categorizadas. O quizá la redacción sí consume tiempo, pero el proceso completo tarda lo mismo porque las respuestas generadas necesitan más revisiones.

No necesitamos presentar esa causa como cierta antes de actuar. Necesitamos **hacer explícita la hipótesis** y diseñar una intervención que nos permita comprobarla.

En este caso no estamos intentando navegar un escenario complejo. Estamos acotando una mejora operativa y probando si nuestra explicación del retraso es correcta antes de extender la solución.

---

## Cómo diseñar un piloto de IA que permita decidir

El mismo plan podría formularse así:

>
>
> `Las solicitudes de clientes tardan demasiado porque el equipo dedica muchas horas a clasificar correos, buscar información y preparar una primera respuesta. Creemos que automatizar la clasificación y el borrador inicial puede reducir ese tiempo sin empeorar la calidad del servicio.`
>
>
>
> `Durante seis semanas lo probaremos con un solo equipo y un tipo concreto de solicitud. Antes de empezar, mediremos cuánto tarda hoy el proceso y cuántos errores, reclamaciones y revisiones genera.`
>
>
>
> `Consideraremos que la prueba funciona si reduce al menos un 15 % el tiempo total sin aumentar los errores, las reclamaciones ni la carga de revisión humana. Si solo acelera la redacción, pero no el proceso completo, revisaremos nuestro diagnóstico. Si empeora la calidad o desplaza trabajo a otras personas, detendremos la prueba.`
>
>
>
> `Solo ampliaremos el sistema cuando tengamos evidencia de que mejora el proceso completo, no simplemente de que el agente funciona.`
>
>

Esta formulación es menos espectacular y mucho más útil.

El 15 % ya no aparece como una predicción que la organización promete cumplir. Funciona como un **umbral de decisión elegido antes de ver los resultados**. Sirve para distinguir una mejora que justifica continuar de una variación pequeña que no compensa el coste, el riesgo o el mantenimiento del sistema.

También obliga a decir qué haríamos si la prueba contradice nuestra explicación. Si el agente redacta más rápido, pero el tiempo total apenas cambia, no basta con ajustar el prompt y repetir la demo. Puede que el cuello de botella estuviera en otro lugar.

**El primer planteamiento** contiene una solución y una promesa:

-

cinco agentes;

-

un 20 % de ahorro.

**El segundo **contiene una hipótesis comprobable:

-

dónde creemos que está el problema;

-

qué intervención acotada probaremos;

-

durante cuánto tiempo;

-

contra qué situación inicial la compararemos;

-

qué resultado esperamos;

-

qué efectos adversos vigilaremos;

-

qué observación nos obligaría a corregir el diagnóstico;

-

qué evidencia exigiremos antes de escalar.

**No garantiza que acertemos. Hace posible aprender sin confundir actividad con avance.**

---

## Un agente puede funcionar y no mejorar el proceso

En las newsletters anteriores he insistido en que [un agente no termina cuando afirma que ha terminado](https://substack.com/@ainalluna/p-202814101). Necesitamos evidencia externa: archivos creados, fuentes verificadas, tests superados o criterios de aceptación observables.

Aquí ocurre algo parecido, pero un nivel por encima. Un agente puede superar todas sus pruebas técnicas y no producir una mejora organizativa.

Puede clasificar correctamente el 95 % de los correos y no reducir la cola. Puede generar un borrador en veinte segundos y hacer que una persona dedique diez minutos más a comprobarlo. Puede aumentar el número de respuestas enviadas y empeorar la resolución en el primer contacto. Puede ahorrar tiempo en un equipo desplazando trabajo a otro.

Mejorar una tarea no equivale a mejorar el trabajo: si la automatización ahorra minutos en un punto y añade revisiones en otro, solo ha trasladado el coste.

Un estudio publicado en *The Quarterly Journal of Economics* observó el despliegue de un asistente generativo entre más de 5.000 agentes de atención al cliente. La productividad no se definió como «el modelo escribe rápido», sino mediante conversaciones resueltas por hora, una medida que combinaba tiempo, volumen y resolución. El efecto medio fue positivo, pero no fue igual para todo el mundo: las mejoras se concentraron especialmente en las personas con menos experiencia.

En otro contexto, METR estudió a desarrolladores experimentados trabajando en sus propios repositorios. En su experimento de principios de 2025, los participantes creían que la IA los había acelerado, pero el tiempo observado mostraba una ralentización. Cuando el equipo intentó repetir la medición con herramientas más recientes, aparecieron problemas de selección y nuevas formas de trabajo, como usar varios agentes en paralelo, que hicieron menos fiable la estimación. En febrero de 2026 decidieron rediseñar el experimento.

Estos trabajos no permiten trasladar una cifra a cualquier empresa. Enseñan algo más importante: **el efecto depende de la tarea, de las personas, del contexto y de cómo definimos y medimos el resultado**. Incluso una prueba bien planteada puede necesitar correcciones cuando cambia la forma de trabajar.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)

---

## Qué medir antes de poner en marcha el piloto

Antes de introducir el agente necesitamos saber cómo funciona hoy el proceso. No para producir un dashboard enorme, sino para poder comparar.

En el ejemplo de atención al cliente, una línea base útil podría registrar el tiempo desde que entra una solicitud hasta que queda resuelta, cuánto tiempo permanece esperando, cuántas veces se reabre, cuántas revisiones necesita y qué errores o reclamaciones genera. Si solo medimos los minutos dedicados a redactar, habremos elegido como realidad una parte demasiado pequeña del sistema.

Conviene separar tres tipos de señales:

-

**Resultado:** tiempo total de resolución, solicitudes resueltas correctamente o satisfacción del cliente.

-

**Proceso:** tiempo de clasificación, búsqueda y redacción, porcentaje de borradores aceptados o número de revisiones.

-

**Efectos adversos:** errores, reclamaciones, escalados, trabajo desplazado, pérdida de aprendizaje o diferencias entre grupos.

Esta separación evita un engaño frecuente. Podemos mejorar una métrica intermedia y empeorar el resultado final. También podemos reducir el tiempo medio ocultando que las solicitudes más difíciles ahora tardan más o que una parte del equipo absorbe toda la revisión.

Aquí aparece otra lección de estadística que me llevo al trabajo con IA: **medir más no corrige medir mal.** Si probamos el agente solo con solicitudes fáciles, excluimos los fallos o no contamos el tiempo de quienes revisan, miles de registros seguirán ofreciendo una imagen falsa del proceso.

No se trata de medir todo. Se trata de medir lo suficiente para que la decisión no dependa de la fluidez de la demo ni de la sensación de velocidad.

---

## Cuándo continuar, corregir o detener la prueba

La pregunta más útil de un piloto no es «¿cómo demostraremos que funciona?». Es otra: **¿Qué tendría que ocurrir para que continuemos, corrijamos o paremos?**

Si no podemos responderla antes de empezar, cualquier resultado podrá reinterpretarse como un éxito. Cuando el tiempo mejore, diremos que la IA funciona. Si no mejora, diremos que falta entrenamiento. Si aumenta la revisión, diremos que es una fase temporal. Si aparecen errores, pediremos otro modelo. La hipótesis se vuelve imposible de refutar.

Un marco sencillo puede ayudarnos a fijar de antemano las condiciones de la prueba:

Observamos que ***[problema concreto y medible]***.

Creemos que se debe principalmente a ***[diagnóstico o mecanismo]***, basándonos en ***[evidencia disponible]***.

Probaremos*** [intervención acotada]*** en ***[ámbito***] durante ***[plazo].***

Antes de empezar, mediremos ***[línea base***].

Esperamos observar ***[cambio concreto]*** en ***[métricas de resultado].***

También vigilaremos ***[errores, costes desplazados, efectos adversos y grupos afectados].***

Consideraremos que funciona si ***[umbral y criterio de éxito]***.

Revisaremos el diagnóstico si ***[resultado que contradice la hipótesis]***.

Detendremos la prueba si ***[límites de daño o coste].***

Solo ampliaremos la intervención si ***[evidencia necesaria para escalar]***.

No hace falta que el documento sea largo. Hace falta que obligue a diferenciar lo que sabemos, lo que creemos y lo que vamos a observar.

El marco de gestión de riesgos de IA de NIST sigue una lógica compatible: antes de desplegar, propone entender el contexto y el uso previsto, definir el alcance, comparar beneficios y costes con referencias adecuadas, medir el comportamiento en condiciones parecidas a las reales y mantener mecanismos para corregir o desactivar el sistema si sus resultados no encajan con el propósito.

La plantilla no sustituye ese trabajo de gobernanza. Sirve para que el primer piloto no nazca ya desconectado de él.

---

## ¿Qué debe demostrar el piloto antes de escalar el agente?

Una demostración prueba que una máquina puede hacer algo; un **piloto debe probar que ese algo mejora un proceso real,** para unas personas concretas y bajo condiciones observables.

Escalar exige una pregunta adicional: **¿tenemos razones para pensar que la mejora se mantiene cuando ampliamos el volumen, los casos, los equipos y el tiempo?**

Son tres niveles distintos. Saltar del primero al tercero porque una respuesta impresiona es una manera rápida de convertir incertidumbre técnica en coste organizativo.

Una de las ideas que me llevo de estos meses es que los problemas complejos no suelen resolverse de una vez: se navegan. **Eso no significa que todo proyecto de IA sea un problema complejo.** El caso de los tickets no lo es. La transferencia es más pequeña y, precisamente por eso, más útil: incluso ante un problema operativo acotado, conviene diagnosticar antes de elegir la solución, comprobar nuestras suposiciones y decidir a partir de evidencia.

Por eso una estrategia de IA rigurosa no debería prometer que ya conoce el resultado. Debería explicar cómo aprenderá lo suficiente para tomar la siguiente decisión.

**Tools are great. Systems are better.**

En las últimas semanas hemos visto cómo construir un sistema con skills, agentes y arneses. Esta es la pieza que va antes: el problema que merece el sistema y la evidencia que exigiremos para conservarlo.

Una estrategia rigurosa no dice: «Sabemos que esto reducirá los costes un 20 %». Dice: «Esta es nuestra mejor explicación del problema, esta es la prueba que haremos y esto es lo que tendría que ocurrir para continuar, corregir o parar».

O, todavía más breve:

**La estrategia no consiste en prometer de antemano el resultado, sino en diseñar una prueba que permita distinguir cuándo avanzar, cuándo corregir y cuándo detenerse.**

**P. D.** Esta newsletter también nace de seis meses de trabajo compartido. Gracias a mis compañeros de equipo, **Edgar, Elena, Nuria y Steven**, por el tiempo, las conversaciones y todo el trabajo que hubo detrás de nuestro caso práctico. Una parte importante de lo que me llevo del programa la construimos entre los cinco.

[Compartir](https://ainalluna.substack.com/p/piloto-ia-disenar-medir-escalar?utm_source=substack&utm_medium=email&utm_content=share&action=share)

---

## Recursos

- [UNIR: Programa en Resolución de Problemas Complejos](https://www.unir.net/empresa/programa-resolucion-problemas-complejos/)

- [Richard Rumelt: *Strategy's strategist*](https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/strategys-strategist-an-interview-with-richard-rumelt)

- [NIST: AI Risk Management Framework Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)

- [*Generative AI at Work*, The Quarterly Journal of Economics](https://academic.oup.com/qje/article/140/2/889/7990658)

- [METR: *We are Changing our Developer Productivity Experiment Design*](https://metr.org/blog/2026-02-24-uplift-update/)

***Cuéntamelo. Siempre leo todo.***

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

# **Suscríbete a Think&Hack**

**Tools are great. Systems are better.**

Casos reales, flujos que funcionan y formas concretas de usar la IA sin perder el control del proceso.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
