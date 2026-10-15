---
id: 212834895
titulo: "Convertí mi PC en una máquina para trabajar con agentes de IA"
subtitulo: "Dos pequeños hacks con PowerShell para transformar cualquier contexto en Markdown y dejar de perder el tiempo entre copiar, pegar y crear archivos."
fecha: 2026-08-30
url: https://ainalluna.substack.com/p/crear-archivos-markdown-windows-powershell
tipo: newsletter
audiencia: everyone
estado: completo
huella: 3e617c07fd490dd2edd3e73a19ebcb64319f62342e5cf9686ad2b9063e035dcf
---

[

![imagen](https://substackcdn.com/image/fetch/$s_!eriA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7af06bf8-a234-4e01-99cd-c16436e77fb1_1672x941.png)

](https://substackcdn.com/image/fetch/$s_!eriA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7af06bf8-a234-4e01-99cd-c16436e77fb1_1672x941.png)

*¿Cómo estás?*

*Soy Aina y esto es Think&Hack.*

A estas alturas, espero que hayas leído mi [guía para crear agentes](https://ainalluna.substack.com/p/crear-agentes-claude-code) y te hayas animado a montar tus propios **procesos agénticos. **

Si lo has hecho, seguro que te has dado cuenta de que ahora te pasas el día **generando contexto **para que tus agentes puedan trabajar.

**Y ese contexto nunca llega en el formato que necesitas.**

Un Word por aquí. Un PDF por allá. Una página web, una conversación con ChatGPT, la transcripción de una reunión… total que tienes que ir convirtiendo este contexto a Markdown `(.md)` para que la IA lo lea de forma más eficiente.

En la newsletter de hoy te voy a explicar cómo he **“tuneado” mi Windows,** para dejar de perder el tiempo en extraer el contenido, copiarlo, pegarlo o cualquier otra cosa que hagas para** transformar tu contexto en un archivo Markdown **`(.md).`

Si tienes un Mac, copia este newsletter en tu IA de confianza y dile: *“Quiero hacer lo mismo, pero para Mac” *:)

[

![imagen](https://substackcdn.com/image/fetch/$s_!1WMp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feff1c688-507c-419b-acc5-5611950c59bf_1448x1086.png)

](https://substackcdn.com/image/fetch/$s_!1WMp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feff1c688-507c-419b-acc5-5611950c59bf_1448x1086.png)Jejejej, es imposible que no te hayas reído, yo no puedo parar … Tras las vacaciones me siento muy relajada y eso se nota en mis últimas intros. :)

## Por el poder de PowerShell

Vamos desde el principio.

Según la documentación de Microsoft:

>
>
> “PowerShell es una solución de automatización de tareas multiplataforma formada por un shell de línea de comandos, un lenguaje de scripting y un marco de administración de configuración. PowerShell se ejecuta en Windows, Linux y macOS.”
>
>

**Automatiza tareas,** aquí está la palabra clave.

**Vamos a utilizar PowerShell para automatizar las siguientes tareas. **

-

`Copiar un texto, pulsar Ctrl + F12 y guardarlo automáticamente como Markdown.`

-

`Hacer clic derecho dentro de una carpeta y crear directamente un archivo .md.`

Y sí, evidentemente puedes pedirle a tu agente que escriba los scripts. Probablemente ya lo estaba haciendo y tú ni siquiera sabías que eso era PowerShell.

Pero que la IA sepa hacer estas cosas no significa que tú no tengas que entender qué está haciendo. Cuanto más sepas sobre las herramientas que utiliza, mejores cosas podrás pedirle y más fácil será detectar cuando está haciendo algo que no debería.

La idea es sencilla:
**Tú aprendes. La IA ejecuta.**

### Hack 1: del portapapeles a Markdown con `Ctrl + F12`

Cuando copias un texto con `Ctrl + C,Window` lo guarda temporalmente en el portapapeles, esperando a que lo pegues en algún sitio.

Lo normal sería abrir una aplicación, pulsar `Ctrl + V`, crear el archivo, ponerle un nombre y guardarlo en la carpeta correcta.

Con esta automatización me salto todos esos pasos.

Copio el texto, pulso `Ctrl + F12` y PowerShell crea automáticamente el archivo Markdown dentro de mi inbox.

![imagen](https://substackcdn.com/image/fetch/$s_!gK_X!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb9fde10b-ff25-44d2-b34b-da8227b61b35_1548x351.png)

Después solo tengo que pedirle al agente que procese el inbox. Si no sabes cómo funciona esta parte, aquí te expliqué cómo monté el mío:

He dejado en GitHub el script que utilizo y un ejemplo completo de cómo lo he montado, con las rutas que tienes que cambiar y los pasos para probarlo en tu Windows.

👉 [Ver la guía y tutorial «Portapapeles a Markdown» en GitHub](https://github.com/seoutopico/Scripting_PowerShell/tree/main/Crear-Nota-Portapapeles) **¡¡gratis!!**

### Hack 2: crear un Markdown con el clic derecho

Vamos con la siguiente automatización, esta surge de nuevo desde que trabajo con agentes de IA, antes de esto nunca he necesitado crear archivos Markdown cada dos por tres.

Ahora es constante, me paso el día creando archivos `.md.` Si estoy en Obsidian, es fácil: creo una nota y listo. Pero si estoy trabajando desde el Explorador de archivos de Windows, no voy a abrir Obsidian solo para crear una nota en esa carpeta.

Después de encontrarme con esta situación una y otra vez, recordé que **puedo controlar qué tipos de archivo aparecen en el menú Nuevo de Windows.**

[

![imagen](https://substackcdn.com/image/fetch/$s_!2QRs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F24cf6f0c-09f7-4b72-8873-178371a7ad31_782x761.png)

](https://substackcdn.com/image/fetch/$s_!2QRs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F24cf6f0c-09f7-4b72-8873-178371a7ad31_782x761.png)Clic derecho en el explorador de Windows → Nuevo → Tienes accesos rápidos a creación de archivos.

La idea es simple, ejecuto el script una vez y, a partir de ahí, puedo abrir cualquier carpeta y hacer esto:

`Clic derecho → Nuevo → Documento Markdown`

El archivo aparece vacío dentro de la carpeta, le pongo un nombre y empiezo a escribir.

[

![imagen](https://substackcdn.com/image/fetch/$s_!TRMD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46f09996-3344-4779-95db-b44a9798887b_1920x1200.png)

](https://substackcdn.com/image/fetch/$s_!TRMD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46f09996-3344-4779-95db-b44a9798887b_1920x1200.png)

He dejado en GitHub el script que utilizo y el paso a paso para que puedas hacerlo.

👉 [Ver la guía y tutorial «](https://github.com/seoutopico/Scripting_PowerShell/tree/main/Nuevo-Documento-Markdown)**[Crear un archivo Markdown con el clic derecho en Windows](https://github.com/seoutopico/Scripting_PowerShell/tree/main/Nuevo-Documento-Markdown)**[» en GitHub](https://github.com/seoutopico/Scripting_PowerShell/tree/main/Nuevo-Documento-Markdown) **¡¡gratis!!**

Si te gustan las *thumbs* de los vídeos, no olvides pasarte por la newsletter donde expliqué cómo los creo con IA. Obviamente, el proceso ha evolucionado y ahora ya lo hace Hacki, pero los principios y las instrucciones siguen siendo los mismos.

**P.D** No sé si has visto *He-Man*. Está en Prime Video y entra en esa categoría de pelis que no sabes muy bien si te están gustando o no; supongo que depende del día.Lo que sí puedo decir es que no pensé ni una sola vez: “Podría estar haciendo algo más importante”, tan mala no será, ¿no?

Si conoces a alguien que también se pasa el día entre `Ctrl + C`, `Ctrl + V` y archivos Markdown, compártele esta newsletter. Igual le ahorras unos cuantos clics.

[Compartir](https://ainalluna.substack.com/p/crear-archivos-markdown-windows-powershell?utm_source=substack&utm_medium=email&utm_content=share&action=share)

---

[

![imagen](https://substackcdn.com/image/fetch/$s_!a4zT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85a1a880-e624-45ad-8b14-17d37f89f69e_2172x724.png)

](https://substackcdn.com/image/fetch/$s_!a4zT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85a1a880-e624-45ad-8b14-17d37f89f69e_2172x724.png)

#### **📅 Hacki en acción — Semana 1: aprendiendo**

### Datos de la semana

**17 → 23 de agosto**

Hacki nació el **15 de agosto**, así que del **17 al 23 de agosto** tenemos su primera semana completa para comparar.

Durante la semana del 17 se ha publicado **14 Notes**, pero no todas eran de Hacki. **7 fueron propuestas por él y 7 fueron mías**.

-

**17 → 23 de agosto**

  -

**Notes publicadas:** 14
→ **7 propuestas por Hacki**
→ **7 publicadas por mí**

  -

**Notes de Hacki:**
→ 25 reacciones
→ 4 comentarios
→ 0 restacks

  -

**Mis Notes:**
→ 31 reacciones
→ 13 comentarios
→ 3 restacks

  -

**Nuevas suscripciones:** 5
→ **1 atribuida directamente a una Note de Hacki**
→ **4 procedentes de otras fuentes Linkedin, app y otra nota. **

  -

**Note de Hacki con subscripcion:** 1 — *“Una skill no debería ser una carpeta de buenos deseos”*

Tras esta primera semana, creo que** es demasiado** pronto para sacar conclusiones, pero ya tenemos una primera referencia: **1 de las 7 Notes de Hacki consiguió una suscripción**.

Voy a usar las mates a mi favor: :D el **14,3% de las Notes de Hacki ha conseguido, una suscripción. **

La Note *“Una skill no debería ser una carpeta de buenos deseos” *tiene 3 **reacciones, 0 comentarios y 0 restacks**, no es la Note con más interacciones. *Así que de momento también podemos decir que un note con muchas interacciones. no tiene por qué ser la que mejor convierte.*

Sobre temas, hooks y formatos todavía no tengo suficiente muestra. Solo hay una Note con suscripción atribuida, así que si ahora os dijera “las educativas funcionan mejor” estaría haciendo exactamente lo que no quiero hacer con este experimento: **inventarme un patrón porque queda bonito contarlo**.

👉 **[Ver el dashboard de Hacki](https://seoutopico.github.io/thinkandhack-performance/)**

### ¿Qué ha aprendido Hacki esta semana?

No os voy a engañar: entrenar a Hacki lleva horas y bastante paciencia.

El flujo ahora mismo es:

**Hacki propone → yo reviso → le explico por qué no lo haría → corrige → volvemos a probar.**

Lo va pillando. Es un poco como ir mejorando las skills de tus agentes: corriges, ajustas y cada vez afina más.

Esta semana le pregunté directamente **qué había aprendido de todos esos errores y correcciones**, y su respuesta me gustó bastante más que todo lo que ha producido hasta ahora.

Sacó **10 reglas nuevas**: cuándo no comentar, cuándo no fiarse de una señal, cuándo algo encaja con Think&Hack pero no aporta nada, cómo tiene que leer antes de escribir... y, para mí, lo interesante no son tanto las diez reglas, sino ver cómo empieza a responder a la pregunta que realmente quiero poner a prueba con este experimento:

**¿puede un agente desarrollar criterio trabajando?**

Os he dejado todos los aprendizajes en esta Note 👇

Mientras aprende, hay una parte que ya noto mucho: tengo el calendario cubierto y un radar funcionando cada mañana.

Eso me deja más tiempo para hablar con perfiles afines, leer, descubrir cosas que probablemente no habría encontrado y escribir las Notes más impulsivas del día a día.

Todavía me da trabajo, **pero ya me quita todo el trabajo de búsqueda y planificación. :D**

### Vuestras sugerencias:

 me sugiere ampliar el análisis de retraso entre publicar una Note y conseguir una suscripción.

![imagen](https://substackcdn.com/image/fetch/$s_!NaoY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5ff7df11-01f9-456f-bbad-1b2141df2c40_603x116.png)

La hipótesis tiene bastante sentido, que un Note puede no provocar una suscripción inmediata. Quizá primero genera descubrimiento, después reconocimiento y la conversión llega más tarde.

Por ahora estoy usando una semana de retraso como primera aproximación, pero quiero ampliarlo a dos, tres y cuatro semanas.

Así que le pedí a Hacki que calculara varios lags sobre todo el histórico:

-

misma semana: **-0,07**

-

+1 semana: **-0,02**

-

+2 semanas: **0,12**

-

+3 semanas: **0,11**

-

+4 semanas: **0,28**

La relación entre **número de Notes publicadas y suscripciones** parece aumentar con el tiempo. Y cuando miramos **interacciones en lugar de numero de Notes publicadas**, la señal a cuatro semanas es todavía mayor: **0,40**.

Además, de las 29 suscripciones que podemos vincular a una Note concreta, **más de la mitad llegaron al menos 15 días después**.

Interesante 👀, pero calma con la estadística :D. Hemos probado varios lags y una correlación no demuestra causalidad. Para saber si este patrón también aparece con Hacki tendremos que acumular unas cuantas semanas más.

**Hacki ya lleva una semana trabajando. ¿Qué quieres que te enseñe por dentro?** El calendario que prepara, su radar diario, cómo aprende, qué instrucciones tiene, el dashboard con el que medimos resultados… **déjame tu pregunta y la destripamos en las próximas semanas.**

[Deja un comentario](https://ainalluna.substack.com/p/crear-archivos-markdown-windows-powershell/comments)

Eres nuevo por aquí y no sabes quién es Hacki, pincha en el link que te lo explico.

>
>
> **¿Quieres aprender a construir algo así?**
> En septiembre abriré un curso donde veremos cómo montar agentes autónomos con skills, memoria, tareas programadas, permisos y supervisión.
>
>
>
> 👉 **[Apúntate a la lista de espera](https://ainalluna.com/curso-agentes-autonomos/index.html)**
>
>

---

## Recursos:

-

[https://learn.microsoft.com/es-es/powershell/scripting/overview?view=powershell-7.6](https://learn.microsoft.com/es-es/powershell/scripting/overview?view=powershell-7.6)

***Cuéntamelo. Siempre leo todo.***

[Deja un comentario](https://ainalluna.substack.com/p/crear-archivos-markdown-windows-powershell/comments)

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

# **Suscríbete a Think&Hack**

**Tools are great. Systems are better.**

Casos reales, flujos que funcionan y formas concretas de usar la IA sin perder el control del proceso.
