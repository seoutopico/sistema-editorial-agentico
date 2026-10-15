---
id: 193045310
titulo: "YouTube regala los datos de todos sus canales. Yo los convertí en un agente de research."
subtitulo: "Monté un agente que analiza 30 vídeos de cualquier creador en 3 minutos. "
fecha: 2026-04-06
url: https://ainalluna.substack.com/p/analizar-youtube-ia
tipo: newsletter
audiencia: everyone
estado: completo
huella: 33a5aca4eae61cd746e9a07561fa1837fb979fc1703210e8816e73b75519ef93
---

[

![imagen](https://substackcdn.com/image/fetch/$s_!34ai!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8b8a710d-13a5-4108-b6c1-1b134f94b599_2816x1536.png)

](https://substackcdn.com/image/fetch/$s_!34ai!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8b8a710d-13a5-4108-b6c1-1b134f94b599_2816x1536.png)

¿Cómo estás?

Soy Aina y esto es Think&Hack.

Analizar un canal de YouTube a mano es un trabajo ingrato. Abres vídeo por vídeo, apuntas views, comparas fechas, intentas intuir patrones en los títulos.** Dos horas para sacar un informe que, además, envejece rápido.**

Y lo peor es que los datos ya existen.

**YouTube tiene una API pública que devuelve información de cualquier canal: **visualizaciones, likes, comentarios, títulos, fechas, suscriptores. No es un problema de acceso. Es un problema de método: convertir datos en criterio.

Yo creé, un agente.

---

## De datos sueltos a análisis útil

La API de YouTube devuelve campos para detectar patrones que no ves navegando por la plataforma:

-

Qué temas generan más views y cuáles pasan desapercibidos

-

¿Qué formatos de título correlacionan con mejor rendimiento?

-

si los vídeos con invitados funcionan mejor que los vídeos en solitario

-

Cuál es el engagement real de cada vídeo

-

Cada cuánto publica un canal y si crece, se estanca o cae

Con los 30 vídeos más recientes de un canal, ya puedes construir un análisis que a mano te llevaría horas.

**El problema no es acceder a estos datos. El problema es que nadie los recoge, los ordena y los analiza de forma sistemática.**

## Lo que construí

Construí un agente que convierte esa API pública en un analista de canales de YouTube.

Le das un handle. El agente resuelve el canal, recoge los últimos 30 vídeos, pide sus estadísticas y genera un research completo con métricas, ranking de rendimiento y conclusiones sobre qué contenido funciona mejor.

Lo construí con Claude Code como un **skill**: un archivo de instrucciones que le dice al agente qué datos pedir, qué métricas calcular y en qué formato devolver el análisis.

***Y aquí está la diferencia con una herramienta cerrada: el skill es un archivo de texto que puedes abrir, leer y modificar.** ¿Quieres que analice 50 vídeos en vez de 30? Cambias un número. ¿Quieres que el informe incluya una sección sobre frecuencia de publicación? Añades una línea a las instrucciones. ¿Quieres que compare dos canales? Le dices cómo. No dependes de lo que un producto decida ofrecerte. Tú decides qué preguntas hace el agente y en qué formato te entrega las respuestas.*

No improvisa. Sigue un protocolo.

El resultado es un markdown listo para leer en Obsidian, Notion o cualquier editor. No una tabla para interpretar después, sino un informe para tomar decisiones.

[

![imagen](https://substackcdn.com/image/fetch/$s_!c1U6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27d97c37-342d-490f-b813-2b6d5be6caf5_949x931.png)

](https://substackcdn.com/image/fetch/$s_!c1U6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27d97c37-342d-490f-b813-2b6d5be6caf5_949x931.png)*El agente ejecutando las 3 peticiones a la API de YouTube en tiempo real. Primero resuelve quién es el canal. Después obtiene los 30 vídeos más recientes. Después pide todas las estadísticas de golpe. Cada bloque JSON que ves es una respuesta directa de YouTube.*

**Un comando. Un handle. Tres minutos.**

[

![imagen](https://substackcdn.com/image/fetch/$s_!x061!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb4c5e5ce-c557-448c-82a4-196fb54f1a5a_937x748.png)

](https://substackcdn.com/image/fetch/$s_!x061!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb4c5e5ce-c557-448c-82a4-196fb54f1a5a_937x748.png)*Research completado: 180 líneas de markdown con tabla de vídeos, métricas y análisis. El agente ya detectó que “I Asked Claude to Make Me as Much Money as Possible” es el vídeo estrella del canal con 97.808 views.*

---

## ¿Qué hace el agente?

El skill hace dos cosas.

**Recoger.** Se conecta a la API de YouTube y descarga los datos en bruto de los 30 vídeos más recientes: título, views, likes, comentarios y fecha.

**Analizar.** Ordena los vídeos por rendimiento, calcula el engagement medio del canal, detecta qué temas y formatos aparecen en los vídeos que mejor funcionan, identifica los que peor rinden y genera un documento con tres bloques:

1.

Qué funciona

2.

Qué no funciona

3.

Qué haría después

El resultado es un markdown que puedes abrir en Obsidian, en Notion o en cualquier editor. **Un informe de research listo para tomar decisiones, no una tabla de datos para interpretar.**

Lo lancé contra el canal de Peter Yang, un creador sobre IA con 78.600 suscriptores. El agente detectó, por ejemplo, que los vídeos sobre OpenClaw dominan su top 7, que los tutoriales con invitados rinden mejor que los vídeos en solitario y que un vídeo sobre Claude Opus supera las 92.000 views, mientras que otro sobre Gemini se queda en 4.400.

**Eso no es intuición. Es patrón.**

Y ese patrón te sirve para decidir qué tema tocar, qué formato priorizar y qué tipo de contenido repetir.

*Ejemplo del resultado*

El skill completo está publicado y es abierto: [youtube-channel-research en GitHub](https://github.com/seoutopico/claude_skills/tree/master/youtube-channel-research). Si quieres ver el informe que genera antes de instalarlo: [resultado completo de Peter Yang](https://github.com/seoutopico/claude_skills/blob/master/examples/youtube-channel-research/youtube-research-peteryangyt.md).

[Descargar Skill](https://github.com/seoutopico/claude_skills/tree/master)

Funciona con cualquier canal público y puedes adaptar el formato del informe a lo que necesites.

## Por qué esto importa

La mayoría de personas usa la IA para buscar información que ya existe en internet. Yo la uso para algo distinto: **coger fuentes de datos públicas que nadie aprovecha y convertirlas en herramientas.**

Con Netflix convertí artículos técnicos en un Gem de Gemini. Con YouTube, una API pública en un agente de Claude Code. Los datos ya estaban ahí. Lo que faltaba era alguien que escribiera las instrucciones correctas y dejara que la IA hiciera el trabajo pesado.

**Ese es el Think. Y ese es el Hack.**

Esto no va solo de YouTube.

Funciona con cualquier canal público, pero sobre todo con cualquier fuente de datos pública que hoy nadie esté aprovechando bien. La idea no es “usar una herramienta”. La idea es convertir una fuente en un sistema útil.

Y eso sí escala.

Si tienes una fuente de datos pública que hoy miras a mano, probablemente puedas convertirla en un flujo de trabajo mejor. Más rápido. Más consistente. Más útil.

---

**Si quieres saber más:**

**Fuentes y links**

-

[Skill de YouTube Research — repositorio completo con instrucciones de instalación](https://github.com/seoutopico/claude_skills/tree/master/youtube-channel-research)

-

[YouTube Data API v3 — Documentación oficial](https://developers.google.com/youtube/v3)

***Cuéntamelo. Siempre leo todo.***

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

## **Recomienda Think&Hack**

***¿Me echas una mano para que esta newsletter llegue a más personas? **Si te ha servido, reenvíasela a alguien a quien también le pueda ayudar.*

>
>
> **Comparte:** Reenvía esto a alguien que analiza canales de YouTube a mano.
>
>

[Compartir](https://ainalluna.substack.com/p/analizar-youtube-ia?utm_source=substack&utm_medium=email&utm_content=share&action=share)

>
>
>
> **Responde:** ¿Tienes fuentes de datos públicas que no estás aprovechando?
>
>

[Deja un comentario](https://ainalluna.substack.com/p/analizar-youtube-ia/comments)

>
>
>
> **Suscríbete:** Si te han reenviado esto, [únete aquí](https://ainalluna.substack.com/).
>
>

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
