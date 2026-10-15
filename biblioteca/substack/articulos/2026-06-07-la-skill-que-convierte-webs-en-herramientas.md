---
id: 200734614
titulo: "La skill que convierte webs en herramientas para agentes IA."
subtitulo: "Creé una skill que convierte cualquier flujo de navegador en un script reutilizable: leer, actuar, publicar o retirar sin navegar clic a clic."
fecha: 2026-06-07
url: https://ainalluna.substack.com/p/la-skill-que-convierte-webs-en-herramientas
tipo: newsletter
audiencia: everyone
estado: completo
huella: 696c34f9daa72e24b289a3deaff59543cad3bfa1c64422f026b1eb29f89b5b05
---

[

![imagen](https://substackcdn.com/image/fetch/$s_!O0Em!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0edb0d2e-9898-461b-9503-c899b3dc852f_1672x941.png)

](https://substackcdn.com/image/fetch/$s_!O0Em!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0edb0d2e-9898-461b-9503-c899b3dc852f_1672x941.png)

¿Cómo estás?

Soy Aina y esto es Think&Hack.

Imagínate que tienes una acción que repites cada semana. Entras en Google Search Console para retirar una URL, abres Substack para publicar una nota, revisas LinkedIn para guardar posts del feed o entras en una web de reporting porque necesitas descargar un reporte concreto, pero para llegar hasta él tienes que hacer siempre los mismos cuatro clics.

Ninguna de esas tareas es especialmente difícil. **Lo pesado es repetirlas.** Y lo más absurdo empieza cuando se las *pides a un agente: el agente abre la web, mira la página, interpreta botones, espera modales, vuelve a mirar, decide el siguiente paso y actúa como si nunca hubiera visto ese flujo antes.*

A mí eso me empezó a molestar por una razón muy concreta. Si yo ya sé qué quiero hacer, si la web ya permite hacerlo y si el navegador ya tiene sesión, cookies, DOM, formularios y llamadas internas, **¿por qué la automatización sigue viviendo como una conversación improvisada?**

Esta semana he creado una skill para resolver justo eso: `browser-console-automation`. La idea no es que la IA haga clic más rápido. La idea es convertir cualquier flujo repetible de navegador en un script guardado que puedas ejecutar otra vez.

Si puedes hacerlo dentro del navegador, probablemente puedes enseñarle al agente a repetirlo sin que vuelva a preguntarse cada vez dónde tiene que hacer clic.

Si quieres aprender a convertir la IA en sistemas útiles, suscríbete a Think&Hack.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)

## El problema: el agente vuelve a empezar cada vez.

Cuando le dices a un agente que navegue por una web, lo normal es pedirle que actúe como actuarías tú. Que mire la página, encuentre el botón, haga clic, espere a que cargue, vuelva a mirar y siga con el siguiente paso.

Para una prueba rápida funciona. El problema aparece cuando esa acción no es una prueba, sino algo que repites cada semana. Ahí el agente vuelve a hacer lo mismo que tú: redescubrir el camino.

No recuerda que primero hay que abrir el filtro, después cambiar la fecha, luego pulsar exportar y finalmente confirmar. O lo recuerda solo dentro de esa conversación, que en la práctica es casi lo mismo que no recordarlo.

La web no ha cambiado. La tarea no ha cambiado. Pero el agente vuelve a gastar contexto, tiempo y criterio en entenderla desde cero.

Ese es el problema que quería resolver.

---

## La solución: sacar el flujo de la conversación.

La idea de la skill es que, cuando un flujo ya está claro, deje de vivir como instrucciones sueltas en un prompt y pase a vivir como una colección reutilizable.

El navegador no es solo una pantalla. También es un entorno donde puedes ejecutar JavaScript, leer el DOM, disparar eventos, rellenar formularios, aprovechar las cookies de sesión y detectar las llamadas internas que la propia web hace cuando pulsas un botón.

Mi skill aprovecha justo eso: en lugar de hacer que el agente navegue clic a clic, ejecuta un único script dentro de la página con `browser_evaluate` de Playwright MCP. El script hace el trabajo y el agente recibe el resultado.

Misma web. Pero ya no estás automatizando una coreografía: estás ejecutando un procedimiento.

---

### El salto: de conversación a sistema

Vamos con **un ejemplo complejo**, porque una tarea simple no enseña bien lo que hace esta skill. Retirar una URL, bajar una tabla o publicar una nota ya son casos interesantes, pero siguen siendo acciones aisladas. **Yo quería probar algo más parecido a mi trabajo real: un flujo completo de research para decidir qué merece entrar en Think&Hack esta semana.**

La prueba fue esta: construir un radar de ideas para newsletter cruzando tres fuentes distintas — LinkedIn, Product Hunt y Hacker News — y devolver no solo datos, sino señales editoriales. **Es decir: qué temas se están moviendo, por qué importan para mi audiencia y qué ángulo podría convertirlos en una newsletter.**

No quería un scraping suelto. Quería ver si la skill podía convertir varias webs en un sistema repetible.

#### **1. Primero instalé la skill en un repo nuevo.**

El primer paso fue preparar un proyecto limpio y pedirle a Claude Code que instalara la skill ahí, para no mezclar el experimento con mi sistema editorial principal.

**Prompt:** Instala esta skill en este repo crea una carpeta nueva y configura como un proyecto de Claude Code. https://github.com/seoutopico/claude_skills/tree/master/browser-console-automation

[

![imagen](https://substackcdn.com/image/fetch/$s_!VKsi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd41b8bc1-24b4-4da6-8ac7-423866900de5_1743x478.png)

](https://substackcdn.com/image/fetch/$s_!VKsi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd41b8bc1-24b4-4da6-8ac7-423866900de5_1743x478.png)

[

![imagen](https://substackcdn.com/image/fetch/$s_!sBbl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F700f1c46-8b3c-43af-9f02-c26326fb0ee2_1914x727.png)

](https://substackcdn.com/image/fetch/$s_!sBbl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F700f1c46-8b3c-43af-9f02-c26326fb0ee2_1914x727.png)

#### 2. Después le pedí el radar completo.

Una vez instalado, no le pedí “extrae posts” ni “rasca Product Hunt”. Le pedí el resultado que yo necesitaba de verdad.

**Prompt: **Quiero construir el “radar de ideas para newsletter”

OBJETIVO

Cruzar 3 fuentes y devolverme señales editoriales para mi newsletter (Think&Hack, audiencia: profesionales de contenido/SEO/IA generativa en castellano):

 1. LinkedIn

 2. Product Hunt (lanzamientos AI de los últimos 7 días)

 3. Hacker News (front page + best, últimos 7 días)

[

![imagen](https://substackcdn.com/image/fetch/$s_!gPMe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca8c04d0-e1b3-4862-8187-5fd7af25d143_938x616.png)

](https://substackcdn.com/image/fetch/$s_!gPMe!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca8c04d0-e1b3-4862-8187-5fd7af25d143_938x616.png)

#### 3. El proceso de construcción.

[

![imagen](https://substackcdn.com/image/fetch/$s_!1XEi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F628a0900-254b-4380-a254-85c004f9fcab_1363x450.png)

](https://substackcdn.com/image/fetch/$s_!1XEi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F628a0900-254b-4380-a254-85c004f9fcab_1363x450.png)

[

![imagen](https://substackcdn.com/image/fetch/$s_!4Qov!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc39be896-2a30-441f-a029-79bc5e94c855_1010x452.png)

](https://substackcdn.com/image/fetch/$s_!4Qov!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc39be896-2a30-441f-a029-79bc5e94c855_1010x452.png)

Aquí empieza lo interesante: la skill no intenta resolverlo todo como una conversación improvisada. Divide el problema en fuentes, crea una colección para cada una y deja escrito cómo volver a ejecutarla.

**La primera pasada tarda más porque está construyendo el sistema:** entiende cada web, decide si conviene leer el DOM o usar una llamada interna, escribe el `scrape.js`, crea el `meta.md` y guarda la colección. En mi prueba completa, con Opus en esfuerzo alto, tres fuentes, calibración y el informe final, la sesión costó 5,36 dólares. Pero esa inversión solo ocurre una vez. La siguiente ejecución ya no empieza desde cero.

![imagen](https://substackcdn.com/image/fetch/$s_!oan0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b79afb7-0b58-4699-99a7-9367a63c5f1d_915x162.png)

La parte más visual fue LinkedIn. Al abrir el feed, Playwright no tenía sesión iniciada, así que hice login manualmente en el navegador controlado por la skill. No le di credenciales al agente. Simplemente entré yo, como entraría cualquier día.

Desde ahí, la skill pudo trabajar con mi sesión abierta y guardar las cookies en el perfil persistente para futuras ejecuciones.

[

![imagen](https://substackcdn.com/image/fetch/$s_!vAz1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F11dbdc29-a6e4-4d68-a50e-0a96531ca05d_1101x430.png)

](https://substackcdn.com/image/fetch/$s_!vAz1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F11dbdc29-a6e4-4d68-a50e-0a96531ca05d_1101x430.png)

[

![imagen](https://substackcdn.com/image/fetch/$s_!lUio!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96dd76e6-cc21-4265-bacb-ddd008510bda_1911x1030.png)

](https://substackcdn.com/image/fetch/$s_!lUio!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96dd76e6-cc21-4265-bacb-ddd008510bda_1911x1030.png)

[

![imagen](https://substackcdn.com/image/fetch/$s_!SRh4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb72e0747-78e4-4113-8765-ed01970d14cb_1086x824.png)

](https://substackcdn.com/image/fetch/$s_!SRh4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb72e0747-78e4-4113-8765-ed01970d14cb_1086x824.png)

[

![imagen](https://substackcdn.com/image/fetch/$s_!UqMZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7dc5641-7a92-4327-912a-81a2fbfbf420_1119x941.png)

](https://substackcdn.com/image/fetch/$s_!UqMZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7dc5641-7a92-4327-912a-81a2fbfbf420_1119x941.png)

#### 4. El resultado

El resultado no fue “un scraper”. Fue un radar editorial. **Increíble. ¡Se queda corto!**

[

![imagen](https://substackcdn.com/image/fetch/$s_!egvX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbdfbf12-118f-4b95-8d15-07ccfb6fbd7e_1638x1026.png)

](https://substackcdn.com/image/fetch/$s_!egvX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbdfbf12-118f-4b95-8d15-07ccfb6fbd7e_1638x1026.png)

Tal como ves en la imagen, quedaron tres archivos CSV auditables y un informe final en Markdown:

-

Hacker News: 100 historias de los últimos 7 días.

-

Product Hunt: 68 lanzamientos del leaderboard semanal.

-

LinkedIn: 23 posts de mi feed personal.

Después cruzó esas tres fuentes y generó seis señales editoriales para Think&Hack, cada una con contexto, fuerza de señal y posible ángulo de newsletter. La más fuerte fue GEO: en la misma semana aparecían señales en LinkedIn, herramientas comerciales y discusión técnica. La segunda fue memoria y contexto para agentes: Product Hunt estaba lleno de productos vendiendo justo esa capa.

**Leer el informe:** [https://github.com/seoutopico/claude_skills/blob/master/browser-console-automation/ejemplos/ejemplo-radar-ideas-ThinkHack.md](https://github.com/seoutopico/claude_skills/blob/master/browser-console-automation/ejemplos/ejemplo-radar-ideas-ThinkHack.md)

[

![imagen](https://substackcdn.com/image/fetch/$s_!TNEV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb1692c0-97cd-4c65-9fab-956a79374482_1055x330.png)

](https://substackcdn.com/image/fetch/$s_!TNEV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb1692c0-97cd-4c65-9fab-956a79374482_1055x330.png)

**Y aquí está la parte importante: no solo me dio un informe. Me dejó tres colecciones reutilizables.**

La próxima vez no tengo que volver a decirle cómo mirar Hacker News, cómo leer Product Hunt o cómo recorrer mi feed de LinkedIn. Puedo ejecutar esas colecciones, volver a cruzar las señales y generar otro radar. La primera vez construyes el sistema. La segunda vez lo usas.

**Eso es lo que convierte esta skill en algo distinto a “hacer scraping”.**

**Bonus:** Le decimos que nos lo guarde como un flujo repetible. Pero ten en cuenta que ahora pude lanzar esas colecciones por sí solas siempre que quieras.

### 5. Comparación de costes

La captura no enseña una demo bonita. Enseña el coste real de convertir una idea en un sistema reutilizable.

[

![imagen](https://substackcdn.com/image/fetch/$s_!qfxa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F39c449c4-f663-4e08-879f-927a4bb68470_954x366.png)

](https://substackcdn.com/image/fetch/$s_!qfxa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F39c449c4-f663-4e08-879f-927a4bb68470_954x366.png)

[

![imagen](https://substackcdn.com/image/fetch/$s_!fyh5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3b8df754-8939-4911-a6b1-fbe02078f537_935x356.png)

](https://substackcdn.com/image/fetch/$s_!fyh5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3b8df754-8939-4911-a6b1-fbe02078f537_935x356.png)

Si al leer esto has pensado **“quiero probarlo”**, probablemente conoces a alguien que también debería verlo. **Compártelo.**

[Compartir](https://ainalluna.substack.com/p/la-skill-que-convierte-webs-en-herramientas?utm_source=substack&utm_medium=email&utm_content=share&action=share)

---

## Casos de usos

El radar de ideas es solo un ejemplo.

Lo importante no es LinkedIn, Product Hunt o Hacker News. Lo importante es el patrón: una web abierta, una sesión ya iniciada, **una tarea repetible y un script que queda guardado para la próxima vez.**

Ahí es donde esta skill empieza a ser útil.

**1. Un radar semanal sobre cualquier fuente cerrada**

Puedes convertir una web que revisas a mano en una fuente estructurada.

No hace falta que tenga API. No hace falta que tenga exportador. Si el contenido está en el navegador, la skill puede recorrerlo, extraerlo y devolverlo como CSV.

Por ejemplo: posts de LinkedIn, lanzamientos de Product Hunt, hilos de comunidades privadas, resultados de un portal, fichas de un marketplace o elementos de un dashboard interno.

La primera vez construyes la colección.
La segunda vez la ejecutas.

**2. Un inventario vivo de lo que cambia en una web**

Hay webs que no quieres leer una vez. Quieres vigilarlas.

La skill puede extraer la misma pantalla cada semana y comparar contra la ejecución anterior: qué apareció, qué desapareció, qué cambió de estado, qué sigue igual y qué merece atención.

Esto sirve para URLs en Search Console, contenidos en un CMS, productos en un ecommerce, incidencias en un panel, leads en un CRM o publicaciones en una comunidad.

No estás haciendo scraping por curiosidad.
Estás convirtiendo una interfaz en un sistema de seguimiento.

**3. Una acción repetible que deja de vivir en tu cabeza**

Hay flujos que no quieres delegar a ciegas, pero tampoco quieres repetir siempre.

Retirar una URL. Publicar una nota. Cambiar un estado. Aprobar un elemento. Rellenar una solicitud. Lanzar una exportación. Confirmar una operación.

La skill puede guardar ese flujo como una colección accionable: abre la pantalla, ejecuta el procedimiento, verifica el resultado y pide confirmación si la acción tiene impacto.

No es una macro que improvisa clics.
Es un procedimiento guardado.

**4. Un pseudo-API para herramientas que nunca pensaron en agentes**

Este es el caso más importante.

Muchas herramientas que usamos cada día son cajas cerradas: tienen datos, botones, tablas, filtros, formularios y estados, pero no están pensadas para conectarse con un agente.

Esta skill abre una vía intermedia.

No necesitas esperar a que exista una API.
No necesitas copiar y pegar.
No necesitas que el agente redescubra la web cada vez.

Si puedes verlo en el navegador, puedes intentar estructurarlo.
Si puedes repetirlo, puedes guardarlo como colección.
Si puedes guardarlo como colección, esa web empieza a comportarse como una herramienta invocable por IA.

La primera ejecución construye el procedimiento.

La segunda ejecución ya no es conversación.

Es sistema.

---

Con [YouTube convertí una API pública en un agente de research](https://ainalluna.substack.com/p/analizar-youtube-ia). Con mi [Growth Editor convertí métricas de newsletters en lecciones](https://ainalluna.substack.com/p/mejorar-newsletter-ia) que el sistema carga antes de escribir. Con esta skill, *convierto webs normales en procedimientos reutilizables.*

**La idea de fondo es la misma: dejar de pedirle a la IA que improvise y empezar a darle piezas que pueda ejecutar.**

**Descargar Skill: **[https://github.com/seoutopico/claude_skills/tree/master/browser-console-automation](https://github.com/seoutopico/claude_skills/tree/master/browser-console-automation)

## **Te dejo las dos fechas clave para esta semana:**

-

**[Martes 9, online y gratis](https://conia.digital/conia-online-2026#registro-section)**[, CONIA Online. El sistema entero, por dentro.](https://conia.digital/conia-online-2026#registro-section)

-

**[Sábado 13, presencial](https://www.eventbrite.es/e/entradas-mujeresenseo-summit-barcelona-2026-1989238539019)**[, Barcelona. El método SEO y diez voces más en una sala.](https://www.eventbrite.es/e/entradas-mujeresenseo-summit-barcelona-2026-1989238539019)

Puedes venir a una.
Puedes venir a las dos.

Y si vienes a Barcelona, me encantará ponernos cara, hablar después de la charla y tomarnos ese café.

¿Te veo en CONIA, en Barcelona o en los dos?

***Cuéntamelo. Siempre leo todo.***

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

# **Suscríbete a Think&Hack**

Casos reales, flujos que funcionan y formas concretas de usar la IA sin perder el control del proceso.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
