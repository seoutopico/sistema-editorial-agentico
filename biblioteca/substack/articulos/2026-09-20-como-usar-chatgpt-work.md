---
id: 216545004
titulo: "Deja de explicarle lo mismo a ChatGPT. Monta un proceso con Work."
subtitulo: "Una guía paso a paso para crear tu primer flujo agéntico, guardar las instrucciones y volver a ejecutarlo sin abrir una terminal."
fecha: 2026-09-20
url: https://ainalluna.substack.com/p/como-usar-chatgpt-work
tipo: newsletter
audiencia: everyone
estado: completo
huella: 8300b014b9c219d63c20434d6d05e041f19bfd3e5a069e9684ae916669d6d636
---

[

![imagen](https://substackcdn.com/image/fetch/$s_!CvgI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F45bc47fb-0643-484a-ba1d-74ef3082fe24_1672x941.webp)

](https://substackcdn.com/image/fetch/$s_!CvgI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F45bc47fb-0643-484a-ba1d-74ef3082fe24_1672x941.webp)

*¿Cómo estás?*

*Soy Aina y esto es Think&Hack.*

Llevo meses hablando de agentes de IA.

Que si Claude Code por aquí, que si Codex por allá. Que si ahora le doy acceso a una carpeta, le preparo unas instrucciones y dejo que haga el trabajo.

Y sé que muchos me leéis y pensáis: «Esto tiene buena pinta», y ahí se queda la cosa.

Porque una cosa es utilizar ChatGPT y otra bastante distinta abrir una terminal y empezar a trabajar con archivos que se llaman `SKILL.md`.

Por mucho que me empeñe en decirte que no hace falta ser programador, la terminal sigue pareciendo la terminal y dar el salto cuesta.

Con ChatGPT Work podemos empezar a trabajar con un agente desde la interfaz de ChatGPT. En la práctica de hoy utilizaremos la aplicación de escritorio y una carpeta donde podrá leer y guardar los archivos del ejercicio.

Y para que no tengas que pensar qué demonios hacer con Work la primera vez que lo abras, he preparado un caso con mis newsletters. Vamos a pedirle que recupere la última, encuentre ideas y escriba borradores para Notes, las publicaciones cortas de Substack.

Si no tienes una newsletter, puedes seguir igualmente el ejercicio con la mía. Lo que vamos a aprender te servirá para pensar cómo organizar otros trabajos con tus propios documentos.

Vamos desde el principio. :)

## ¿Qué cambia cuando utilizas Work?

Cuando utilizas ChatGPT, le pides ideas, le pasas un texto para que lo revise, le preguntas algo… y vais iterando en la conversación.

Pero muchas veces eres tú quien va llevando el proceso: ahora lee este artículo, ahora saca cinco ideas, esta no me gusta, esta sí, vuelve al texto porque eso no lo he dicho…

Y cuando quieres repetir el trabajo con otro artículo, te encuentras buscando las instrucciones en una conversación anterior. O explicando otra vez lo mismo.

Con Work vamos a guardar las instrucciones y los archivos que necesita para que podamos volver a pedirle ese trabajo.

[

![imagen](https://substackcdn.com/image/fetch/$s_!KHKk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff034b314-c219-4582-a00a-d8bf053ac2cf_1456x819.webp)

](https://substackcdn.com/image/fetch/$s_!KHKk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff034b314-c219-4582-a00a-d8bf053ac2cf_1456x819.webp)

Quiero que Work guarde la newsletter, la lea, proponga cinco ideas y convierta tres en borradores. También quiero poder abrir la carpeta y entender qué ha hecho: qué artículo ha utilizado, qué ideas ha elegido y qué ha corregido antes de escribir.

Porque si una Note cuenta algo que yo no he dicho, necesito poder volver a la fuente y ver de dónde ha salido.

Y si un texto no me gusta, quiero poder corregirlo. Si el problema se repite, le pediré que cambie las instrucciones con las que escribe para tenerlo en cuenta la próxima vez.

## Qué vamos a construir

Primero vamos a crear un proyecto y darle acceso a una carpeta. Después le pediremos que prepare las skills: una con un programa para recuperar la newsletter y otras con las instrucciones para elegir ideas y escribir. Cuando las tengamos funcionando, las uniremos y veremos cómo programar el trabajo.

Las instrucciones de cada tarea quedarán guardadas en una **skill**. Por ejemplo, la de redacción tendrá que explicar cómo quiero que escriba, qué debe leer antes y dónde tiene que guardar los borradores. La próxima vez podremos pedirle que utilice esa skill en lugar de volver a explicárselo todo.

Además de instrucciones, una skill puede incluir recursos y pequeños programas. Lo veremos con la primera, que tendrá que descargar la newsletter. Si quieres ampliar esta parte, aquí tienes la [documentación oficial de skills](https://learn.chatgpt.com/docs/build-skills).

En nuestro caso vamos a preparar estas cuatro:

-

**`recuperar-newsletters`:** descarga el artículo completo y lo guarda sin duplicar los que ya tiene.

-

**`ideas-para-notes`:** lee el artículo y propone cinco ideas, explicando por qué merece la pena desarrollarlas y de qué parte del texto salen.

-

**`redactar-notes`:** escribe tres borradores a partir del artículo y de las ideas que hemos revisado.

-

**`flujo-newsletter`:** se encarga de que Work haga todo lo anterior en orden.

Cuatro skills pueden parecer muchas para sacar tres Notes. Pero piensa en lo que pasa cuando corriges un texto.

Si la apertura no te gusta, quieres cambiar la apertura. No necesitas descargar otra vez la newsletter ni empezar a explicarle todo desde el principio. Separar las instrucciones nos permite ajustar la parte que está fallando y conservar el trabajo que ya nos sirve.

Work irá utilizando las cuatro skills según la tarea que le toque hacer. Sigue siendo el mismo agente trabajando con distintas instrucciones.

He elegido cinco ideas y tres borradores para tener margen de selección. Puedes pedir otras cantidades cuando lo adaptes a tu caso.

## 1. Vamos a darle una carpeta

Para hacer el ejercicio necesitas tener Work disponible en tu cuenta y utilizar la aplicación de escritorio, porque vamos a trabajar con una carpeta de tu ordenador.

Crea una carpeta vacía con el explorador de archivos. Puedes llamarla `tutorial-newsletter`.

Abre la aplicación de ChatGPT, entra en **Work** y busca **Choose project**. Desde ahí puedes crear un proyecto con **New project** y **Create project**. Llámalo `Tutorial Work Newsletters Local`, que es el nombre que utilizaremos en los prompts.

[

![Pantalla inicial de Work con la opción Choose project debajo del cuadro de conversación.](https://substackcdn.com/image/fetch/$s_!G4Vm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9502d924-be83-4a23-9c5e-da292cf33887_1280x820.png)

](https://substackcdn.com/image/fetch/$s_!G4Vm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9502d924-be83-4a23-9c5e-da292cf33887_1280x820.png)Entra en Work y utiliza Choose project para crear el proyecto del ejercicio.

En **Choose source folders**, selecciona la carpeta que acabas de crear. El diálogo explica que ChatGPT podrá leer y editar lo que haya dentro. Revisa que has elegido la correcta antes de confirmar **Trust folder** y el trabajo local con **On your computer**.

[

![Diálogo Create project con el nombre del proyecto y el área para añadir carpetas que ChatGPT podrá leer y editar.](https://substackcdn.com/image/fetch/$s_!Vdji!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a7c81ac-1866-4e30-8c4b-783d78f8e288_1280x820.png)

](https://substackcdn.com/image/fetch/$s_!Vdji!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a7c81ac-1866-4e30-8c4b-783d78f8e288_1280x820.png)Escribe el nombre del proyecto y añade la carpeta en Add folders ChatGPT can read and edit.

Ahora vamos a organizar la carpeta. Donde veas `[CARPETA]` en los prompts, pon la ruta de la que acabas de seleccionar. Puedes copiarla desde el explorador de archivos. Utiliza la tuya, aunque en las capturas aparezca otra.

**Pega este primer prompt en el chat del proyecto:**

```
Trabaja en local y escribe solo dentro de [CARPETA]. Comprueba la ruta real y crea LEEME.md y los directorios biblioteca/articulos, biblioteca/control y tandas. Explica en el LEEME que biblioteca conserva las fuentes y tandas los resultados de cada ejecución; este tutorial prepara borradores, nunca publica. Confirma la ruta real, enumera lo creado y muestra el contenido de LEEME.md tras leerlo del disco.
```

La **biblioteca** guardará los artículos. Dentro de **tandas** quedarán las ideas, la revisión y los borradores de cada trabajo, juntos en una carpeta. Así podremos volver a ellos sin mezclarlos con los de la semana siguiente.

El archivo `LEEME.md` explica la organización. La extensión `.md` indica que es un archivo de texto en Markdown, un formato que permite escribir títulos, listas o enlaces sin necesitar un documento de Word.

[

![Respuesta de Work mostrando el archivo LEEME.md y las carpetas biblioteca y tandas creadas para la práctica.](https://substackcdn.com/image/fetch/$s_!KG3P!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1bc5b5aa-e9c0-4264-9019-37e739966155_1280x820.png)

](https://substackcdn.com/image/fetch/$s_!KG3P!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1bc5b5aa-e9c0-4264-9019-37e739966155_1280x820.png)El archivo LEEME explica para qué sirve cada carpeta: biblioteca guarda los artículos y tandas los trabajos que hagamos con ellos.

Abre el archivo y busca las carpetas que acaba de crear. Si solo te ha explicado cómo las organizaría, pídele que las cree. Vamos a necesitarlas en el siguiente paso.

## 2. Que lea la newsletter entera

Quiero que lea la newsletter entera antes de proponer nada. Si le damos solo un extracto, puede quedarse con una idea y perderse justo el párrafo en el que explico sus límites.

Esta primera skill va a incluir un **script**, un pequeño programa guardado que se encargará de consultar la publicación, recuperar el artículo y reconocer si ya lo había descargado.

En el prompt verás la palabra *determinista*. Significa que le pedimos al programa que siga unas reglas concretas: consultar la publicación, descargar el artículo y guardarlo. Work se encargará después de leerlo y decidir qué ideas propone.

El programa se lo vamos a pedir a Work. Para crear la skill utilizaremos `skill-creator`, que le ayuda a preparar y guardar sus instrucciones.

**En el mismo chat, envía este prompt:**

```
Usa skill-creator para crear e instalar una skill invocable recuperar-newsletters, limitada a este proyecto local. Comprueba cómo se registran realmente las skills en Work; no basta exportar un SKILL.md. Escribe solo dentro de [CARPETA]; si instalar requiere otra ruta, informa antes de escribir.

Su función es reunir fuentes, no proponer ideas ni redactar Notes. Crea un script determinista persistente, scripts/recuperar.py dentro de la skill, para mi sistema operativo y carpeta. Debe recuperar solo la newsletter pública más reciente de https://ainalluna.substack.com, no las Notes, con límites de tiempo y peticiones, sin credenciales ni datos de suscriptores.

Guarda título, URL canónica, fecha y texto en biblioteca/articulos; manifiesto e informe de disponibilidad en biblioteca/control. Distingue texto completo de extracto y falla honestamente si no hay contenido. Reutiliza publicaciones descargadas válidas sin duplicarlas. Ejecuta la primera recuperación y muestra el resultado leído del disco, la ruta del script y cómo invocar la skill. No crees aún las otras skills. No solicites acceso global ni reglas persistentes.
```

Fíjate en que le pedimos la última newsletter pública. Con una nos basta para hacer el ejercicio. También queremos el título, la fecha y el enlace, para poder volver al artículo cuando revisemos las ideas.

Además guardará un **manifiesto**: un archivo donde apunta qué artículo tiene y en qué estado está. Más adelante lo utilizará para reconocer cuáles ha procesado ya.

Cuando termine, abre el artículo que haya guardado. Vamos a ver qué ha recuperado.

[

![Lectura de la newsletter guardada, con título, fecha, URL, clasificación de texto completo y comienzo del artículo.](https://substackcdn.com/image/fetch/$s_!zj4U!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdb855a77-bfe5-457d-b356-2687005e92d6_1280x820.png)

](https://substackcdn.com/image/fetch/$s_!zj4U!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdb855a77-bfe5-457d-b356-2687005e92d6_1280x820.png)El artículo guardado, con su título, fecha, enlace y comienzo del texto. Work indica que conserva el contenido completo.

Revisa el principio y el final del artículo. Si ha guardado un extracto, pídele que consiga el texto completo antes de pasar a las ideas.

Ahora vamos a pedirle que lo haga otra vez. Quiero que reconozca el artículo que ya tiene, en lugar de crear otra copia. Escribe **`@recuperar-newsletters`**, selecciona la skill y añade:

```
Ejecuta la skill instalada para comprobar la fuente pública una segunda vez y demostrar reutilización sin duplicados. Conserva toda la evidencia. Muestra URL canónica, rutas del artículo, script, manifiesto e informe, estado antes y después, y fragmentos inicial y final leídos del artículo. Confirma si Work ha cargado la skill como tal; no confundas esa carga con leer manualmente su archivo.
```

Al repetirlo, Work reutilizó el artículo guardado y no creó otra copia.

Si no puede consultar la publicación, tendrá que decírtelo. Puede conservar el artículo anterior, pero necesita mirar si hay otro nuevo antes de afirmar que sigue siendo el último.

**Antes de avanzar, apunta los nombres que te haya devuelto Work.** Los vamos a utilizar en los siguientes prompts:

-

`[ID_ARTICULO]` es el identificador del artículo guardado. El de esta newsletter es `215931068`.

-

`[TANDA_PRACTICA]` será el nombre de la carpeta donde guarde las primeras ideas. En las capturas verás `ideas-para-notes-001`.

-

`[TANDA_FLUJO]` será la carpeta del trabajo completo que prepararemos después. En las capturas verás `flujo-newsletter-001`.

Los dos últimos aparecerán cuando hagamos esos pasos. Sustituye cada marcador por el nombre que tengas tú, sin los corchetes. Si no sabes cuál es, pídele a Work que te muestre la carpeta donde acaba de guardar el trabajo.

## 3. Elegir las ideas antes de ponerse a escribir

Con el artículo guardado, ya podemos pedirle que encuentre posibles Notes.

Pero quiero saber algo más que el título de cada propuesta. ¿Qué va a entender el lector al leerla? ¿Qué parte de la newsletter permite contar eso? ¿Está recuperando algo que expliqué o está proponiendo una aplicación nueva?

Vamos a guardar esos criterios en la segunda skill.

```
Crea con skill-creator la skill local invocable ideas-para-notes dentro de este proyecto, sin modificar recuperar-newsletters ni descargar otra vez el artículo. Una Note es una publicación corta en Substack. Esta etapa solo elige enfoques: lee la fuente completa guardada y propone cinco ideas distintas, cada una con URL, fragmento de respaldo localizado, hecho de la fuente, inferencia editorial, aprendizaje y motivo para desarrollarla. Distingue hechos, inferencias y propuestas; rechaza ideas sin apoyo.

Guarda instrucciones reutilizables y comprueba su detección real en Work. Para esta práctica, ejecuta la selección sobre la fuente [ID_ARTICULO] y guarda ideas.md en una carpeta nueva de tandas. Conserva resultados anteriores. No redactes Notes, publiques ni programes. Mantén las escrituras dentro de [CARPETA].
```

Work preparó cinco ideas y las guardó en `ideas.md`, dentro de una carpeta nueva en `tandas`. Si estás siguiendo el ejercicio, ese nombre es el que sustituirá a `[TANDA_PRACTICA]`.

Una de las ideas que propone es que las recomendaciones expliquen qué podemos hacer con ellas. Es algo que cuento en la newsletter: a Hacki le pido que me diga por qué una lectura me puede interesar y qué podría hacer a partir de ella.

De ahí podemos sacar una Note que ayude al lector a revisar sus propias recomendaciones. Pero no podemos prometerle que hacerlo va a aumentar sus suscripciones, porque yo no he demostrado eso en el artículo.

Vamos a revisar las cinco propuestas antes de redactar. Escribe **`@ideas-para-notes`** y elige la opción de skill.

[

![Selector de Work tras escribir @ideas-para-notes, con la skill y varias carpetas o archivos de nombre parecido.](https://substackcdn.com/image/fetch/$s_!hM8z!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff672e14f-34fc-477d-9725-87eb859307d3_1280x820.png)

](https://substackcdn.com/image/fetch/$s_!hM8z!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff672e14f-34fc-477d-9725-87eb859307d3_1280x820.png)Fíjate en el icono y en la descripción: la primera opción es la skill. Más abajo aparecen carpetas y archivos con nombres parecidos.

Añade este prompt:

```
Confirma si recibes las instrucciones adjuntas de la skill, sin confundirlo con leer manualmente su archivo. Revisa las cinco ideas de tandas/[TANDA_PRACTICA]/ideas.md contra biblioteca/articulos/[ID_ARTICULO].json. No crees otra tanda ni descargues nada. Conserva ideas.md y guarda las observaciones en revision.md junto a él. Muestra qué mantendrías, reformularías o descartarías, con respaldo y aprendizaje. No redactes Notes todavía ni publiques.
```

Le pedimos que guarde las correcciones en `revision.md`, junto a las ideas originales. Así podremos leer qué propuso primero y qué necesita cambiar antes de escribir.

En el menú **Skills** de la respuesta puedes comprobar cuál ha utilizado. Si acabas de crearla y no aparece en el selector, cierra y vuelve a abrir la aplicación con el mismo perfil; eso permitió que apareciera en este caso.

[

![Revisión de las cinco ideas con observaciones sobre respaldo, valoración y períodos, y el menú Skills abierto.](https://substackcdn.com/image/fetch/$s_!nAuV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff8390c15-a151-4daa-af96-a912915d7526_1280x820.png)

](https://substackcdn.com/image/fetch/$s_!nAuV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff8390c15-a151-4daa-af96-a912915d7526_1280x820.png)La revisión de las cinco ideas. Fíjate en los puntos 2 y 4: vamos a ver qué necesita cambiar antes de redactar.

### Dos correcciones que merece la pena mirar

En la segunda idea, Work propone dejar la utilidad de una recomendación sin evaluar hasta haberla leído. Tiene sentido: puedo tener un artículo pendiente porque no me ha dado tiempo a abrirlo.

Lo que yo cuento en la newsletter es que registro por separado qué he hecho con una recomendación y si me ha servido. No digo que tenga configurada esa regla concreta.

Podemos desarrollar la idea, pero tendrá que plantearla como algo que se podría hacer. Si la cuenta como una función que ya utilizo, estará añadiendo algo que no he explicado.

La cuarta idea necesita cuidar los números. En la newsletter explico que, entre el 7 y el 13 de septiembre, Think&Hack pasó de 378 a 392 suscriptores: hubo 16 nuevas suscripciones y el crecimiento neto fue de 14 suscriptores.

Después comparo las Notes publicadas entre el 17 de agosto y el 15 de septiembre, con datos al día 16: tres suscripciones atribuidas a Notes de Hacki y dos a las mías.

Si juntamos esas cifras sin explicar las fechas, podemos acabar contando que las cinco suscripciones atribuidas a Notes forman parte de las altas de esa semana. Y no es eso lo que dicen los datos. Cuando escriba la Note tendrá que conservar los períodos y distinguir mis publicaciones de las de Hacki.

Por eso quería revisar las ideas antes de escribir. Ahora podemos pasarle esas correcciones a la skill de redacción.

Y si quieres que la skill de ideas tenga en cuenta esos criterios la próxima vez, puedes pedirle que los incorpore a sus instrucciones:

```
Conserva una copia de las instrucciones actuales de ideas-para-notes antes de ajustarlas. Añade que una regla de valoración no confirmada por el artículo debe aparecer como propuesta, y que cada cifra debe conservar su período y fecha de corte. No conviertas atribución en causalidad. No sobrescribas ideas.md ni revision.md: la revisión debe permitir entender qué cambió. Muestra el cambio de instrucciones y comprueba que mantiene el objetivo de la skill.
```

Este paso es opcional y te lo dejo como ejercicio. Mira qué cambia en las instrucciones y comprueba que conserva la versión anterior. La próxima vez que le pidas ideas podrás revisar si ha aplicado la corrección.

Para continuar ahora, utilizaremos el archivo `revision.md` que acabamos de guardar.

## 4. Ahora sí: vamos a escribir las Notes

Tenemos el artículo, cinco ideas y una revisión. Vamos a utilizar las tres cosas.

No quiero que Work escriba mirando únicamente los títulos que acaba de proponer. Necesita volver al artículo y tener delante las correcciones para conservar el contexto.

Primero creamos la skill de redacción:

```
Usa skill-creator para crear la skill real redactar-notes en .agents/skills/redactar-notes dentro de [CARPETA]. Comprueba la carpeta y las instrucciones existentes; no dupliques una skill si ya existe.

Debe recibir ideas y revision.md de la misma tanda, volver al artículo completo y escribir tres borradores de Notes comprensibles sin leer la newsletter. Basa la voz en el artículo de Aina: sujetos y acciones concretos, sin metáforas de relleno ni experiencias inventadas. Formula propuestas como posibilidades y conserva los límites de cifras, períodos y causalidad dentro del propio borrador.

Aplica las correcciones de la revisión. Conserva los originales y guarda borradores.md junto a ellos, con textos publicables separados de las notas de evidencia. Comprueba su carga real en Work. No redactes todavía: primero creamos la skill y después la invocaremos. Nunca publiques ni programes. Si instalar requiere otra ruta, informa antes de escribir.
```

Le hemos pedido que guarde los borradores en la misma carpeta que sus ideas y su revisión. Así podremos seguir el recorrido de cada texto sin preguntarnos qué archivos pertenecen a este trabajo.

También hemos separado el texto de la Note de las anotaciones que explican su respaldo. Cuando revise el borrador, podré leerlo como lo vería alguien en Substack y, si tengo una duda, volver al fragmento del artículo que lo sostiene.

Selecciona **`@redactar-notes`**. Puede aparecer con el nombre **Redactar Notes**. Ahora sí, encárgale la redacción:

```
Redacta tres borradores usando ideas.md y revision.md de tandas/[TANDA_PRACTICA] y el artículo completo asociado. Aplica sus correcciones y guarda borradores.md en esa misma carpeta. Relee el archivo y coteja citas, cifras y períodos. Si falta una entrada o no corresponde a esta tanda, detente y explica qué falta. No publiques.
```

Aquí tienes el resultado: tres borradores, a partir de las ideas 1, 2 y 4.

Te enseño un fragmento del segundo:

>
>
> Puedo dejar un artículo sin leer porque esa semana no tengo tiempo. Eso todavía no me dice si la recomendación era útil.
>
>
>
> Con Hacki, el agente de IA que me propone lecturas para mi newsletter Think&Hack, puedo registrar dos cosas por separado: qué he hecho con una propuesta y si me ha servido.
>
>

Después utiliza «una opción sería» para introducir la idea de dejar la utilidad sin valorar. Fíjate en cómo ha incorporado la corrección: ahora se entiende que está proponiendo una posibilidad.

[

![Archivo borradores.md abierto en Work con el primer borrador y el comienzo del segundo.](https://substackcdn.com/image/fetch/$s_!qoYK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fda3ec184-f03e-4de2-8966-aea83e7bb5af_1280x820.png)

](https://substackcdn.com/image/fetch/$s_!qoYK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fda3ec184-f03e-4de2-8966-aea83e7bb5af_1280x820.png)Abre borradores.md para leer las Notes. En el visor de la derecha aparecen la primera y el comienzo de la segunda.

En el tercer borrador también aparecen los dos períodos de las métricas, con la aclaración de que aquellas suscripciones atribuidas no explican el crecimiento neto de la semana.

Abre tu archivo y lee los textos completos. Las aclaraciones tienen que entenderse al leer la propia Note. El lector de Substack no va a ver nuestras anotaciones.

Ahora me toca decidir si esos textos me sirven, qué quiero cambiar y cuáles publicaría. De momento se quedan como borradores en la carpeta.

## 5. Vamos a unir las skills

Hasta aquí le hemos ido pidiendo cada tarea por separado. Ya tenemos las instrucciones y sabemos qué archivos deja cada una.

Vamos a crear una skill que coordine todo: recuperar la newsletter, proponer las ideas, revisarlas, redactar y guardar el trabajo. Así la próxima vez podremos pedirle que lo haga seguido.

Hay un detalle que necesitamos explicarle. El artículo ya está descargado y lo hemos utilizado en los pasos anteriores. Ahora queremos probar las skills trabajando juntas y guardar ese resultado por separado.

Cuando termine, dejará apuntado que ha procesado esa newsletter. Ese registro le servirá para no volver a trabajar sobre ella cada vez que le pidamos buscar novedades.

Vamos a crear la skill que se encarga de esa coordinación:

```
Usa skill-creator para crear flujo-newsletter dentro de [CARPETA]. Lee antes las tres skills existentes y el script de recuperación. Conserva intacta la tanda de práctica.

Coordina recuperación, cinco ideas, revisión de esas ideas por Work contra el artículo, tres borradores y verificación. Usa la biblioteca común y una única carpeta tandas/flujo-newsletter-NNN con fuentes.md, ideas.md, revision.md, borradores.md y resumen.md. La revisión de Work no significa aprobación humana.

Comprueba que ideas acepta el destino de la coordinadora y que redactar consume la revisión de esa misma tanda. Si ajustas instrucciones, conserva sus versiones anteriores y explica el cambio. Work elige y redacta; el código solo recupera, mantiene estado y hace comprobaciones mecánicas.

Descargado no significa procesado: la fuente [ID_ARTICULO] debe alimentar la primera tanda completa. Marca procesada solo tras verificar los cinco resultados. Conserva trabajos previos, reanuda una tanda interrumpida sin duplicarla y no ejecutes dos flujos simultáneos. Después, si la consulta actual no encuentra una newsletter nueva, registra «sin novedades» sin otra tanda ni regreso a artículos antiguos. Un fallo de consulta es error, no ausencia de novedades. Primero crea y verifica la skill; no ejecutes aún, publiques ni programes.
```

El prompt le pide que lea las skills que ya existen. También permite ajustar cómo se pasan los resultados entre ellas, conservando sus instrucciones anteriores.

La skill de ideas necesita saber en qué carpeta guardar sus propuestas. La de redacción tiene que encontrar allí las ideas y la revisión que le corresponden.

Si no dejamos eso claro, podríamos terminar con ideas en una carpeta y borradores hechos a partir de otra revisión. Por eso le pedimos que compruebe cómo se pasan el trabajo las skills.

Cuando la skill esté creada, selecciona **`@flujo-newsletter`**, que puede aparecer como **Flujo Newsletter**, y envía:

```
Ejecuta ahora el flujo manual completo con la fuente real inicial [ID_ARTICULO], confirma la carga de instrucciones y verifica los archivos de la tanda. No publiques ni programes.
```

Al terminar, Work dejó cinco archivos en la misma carpeta: la referencia del artículo, las ideas, la revisión, los borradores y un resumen. Después marcó la newsletter como procesada.

[

![Resumen del trabajo en Work con enlaces al artículo, las ideas, la revisión y los borradores.](https://substackcdn.com/image/fetch/$s_!tQA_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe3816b8a-142a-435f-844e-91641bb1e6d5_1280x820.png)

](https://substackcdn.com/image/fetch/$s_!tQA_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe3816b8a-142a-435f-844e-91641bb1e6d5_1280x820.png)El resumen reúne los enlaces a los cinco archivos. Desde aquí puedes abrir las ideas, su revisión y los borradores.

Puede que las ideas cambien respecto a las que propuso antes. Está volviendo a leer y a escribir sobre el mismo artículo. Revisa que conserve su sentido y que los borradores incorporen las correcciones de esta tanda.

### ¿Y si se lo vuelvo a pedir?

Ahora que ha terminado, vamos a repetirlo.

Quiero comprobar qué hace cuando ya ha procesado la última newsletter. Si cada vez que se lo pido me deja otros tres borradores sobre el mismo artículo, acabaré revisando versiones que no necesitaba.

Utiliza otra vez **`@flujo-newsletter`** y añade:

```
Repite una sola vez el flujo. Comprueba la fuente pública actual y el estado procesado. Si no hay newsletter nueva, registra «sin novedades» en el manifiesto existente sin crear otra tanda ni modificar borradores. Compara antes y después los cinco resultados de [TANDA_FLUJO] y los tres de [TANDA_PRACTICA]. No publiques ni programes. Devuelve el resultado y el enlace al manifiesto.
```

Esta vez respondió «Sin novedades». Había consultado la publicación y reconocido que ya había trabajado con esa newsletter.

Las carpetas y los textos seguían igual: no creó otra tanda ni cambió los borradores anteriores. Eso es lo que queremos que ocurra cuando no haya un artículo nuevo.

[

![Respuesta de la repetición del flujo: sin novedades, misma newsletter y archivos anteriores conservados.](https://substackcdn.com/image/fetch/$s_!pFre!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fad8b3f20-dcf5-43b0-91f6-8afcc4e6a9e4_1280x820.png)

](https://substackcdn.com/image/fetch/$s_!pFre!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fad8b3f20-dcf5-43b0-91f6-8afcc4e6a9e4_1280x820.png)Work reconoce que ya ha procesado la última newsletter y conserva los archivos anteriores.

Si no puede consultar la publicación, tendrá que avisar del error. No queremos que confunda «no he podido mirar» con «no hay nada nuevo».

## 6. Dejarlo programado y comprobar qué pasa

Hasta ahora hemos sido nosotros quienes le hemos pedido que se ponga a trabajar. Vamos a ver cómo dejarle un horario para que empiece.

La skill explica qué tiene que hacer. La tarea programada le da la señal de empezar.

Como va a utilizar archivos de tu ordenador, necesitará que esté encendido y que la aplicación siga abierta a esa hora. Puedes ampliar esta parte en la [documentación de tareas programadas](https://learn.chatgpt.com/docs/automations).

En Work, abre **Scheduled**, pulsa **Create** y prepara estos campos:

-

**Nombre:** `Tutorial newsletter a Notes (Think&Hack)`.

-

**Runs on:** `This device`, para utilizar este equipo.

-

**Runs in:** el chat donde hemos preparado el flujo, dentro del proyecto local.

-

**Repeat:** `Weekly`.

-

**On:** `Sunday`.

-

**Time:** `6:00 PM`, las seis de la tarde.

Elige el chat que pertenece a tu carpeta del ejercicio. En este caso queremos continuar el trabajo allí, con el procedimiento que acabamos de preparar.

Comprueba también la zona horaria de la aplicación. Aquí estamos utilizando **Europe/Madrid**. Como el formulario no muestra un campo para elegirla, pídele a Work que compruebe cuál está usando antes de dar el horario por bueno. Escribir Madrid en el prompt no cambia la configuración.

En el campo de instrucciones, utiliza este texto. Recuerda sustituir `[CARPETA]` por la tuya; el nombre del proyecto es el que hemos usado desde el primer paso.

```
Aplica la skill real $flujo-newsletter en el proyecto Tutorial Work Newsletters Local y trabaja exclusivamente en [CARPETA]. Consulta la última newsletter pública de https://ainalluna.substack.com y continúa únicamente si hay una fuente nueva no procesada. Reúne la fuente completa, cinco ideas, revisión de Work, tres borradores y resumen en una sola tanda local; marca procesada solo después de verificar los resultados.

Si no hay novedades, deja constancia sin crear otra tanda ni modificar las anteriores. Invoca la skill existente y sus skills coordinadas; no sustituyas la lógica creativa por un script. Informa aquí del resultado y las rutas locales. Nunca publiques ni envíes mensajes externos. No amplíes permisos persistentes; ante un bloqueo, informa del error exacto y detente. Horario previsto: domingos a las 18:00 Europe/Madrid.
```

[

![Formulario de la tarea semanal en Work, con This device, el chat elegido y Sunday a las 6:00 PM.](https://substackcdn.com/image/fetch/$s_!SjhJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fda8f1ddb-7d15-4121-be6a-587f283590cb_1280x820.png)

](https://substackcdn.com/image/fetch/$s_!SjhJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fda8f1ddb-7d15-4121-be6a-587f283590cb_1280x820.png)This device indica que trabajará en este equipo. Debajo están el chat del proyecto y el horario: domingos a las seis de la tarde.

Guárdala y utiliza **Run now** para probarla en ese momento. No hace falta esperar al domingo para descubrir que le falta algo.

[

![Menú de la tarea creada con la opción Run now disponible.](https://substackcdn.com/image/fetch/$s_!AzBc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F968234fc-204f-4f91-bbe4-d66174a8260b_1280x820.png)

](https://substackcdn.com/image/fetch/$s_!AzBc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F968234fc-204f-4f91-bbe4-d66174a8260b_1280x820.png)Utiliza Run now para comprobar cómo arranca la tarea sin esperar al día programado.

### Antes de dejarla funcionando

Al pulsar Run now, el encargo llegó al chat y Work empezó a utilizar la skill. Pero aquí apareció un problema: la aplicación no pudo leer los archivos y pidió permiso para continuar por un fallo de su entorno de ejecución.

La tarea quedó bloqueada. Si necesita que haya alguien delante para autorizar ese paso, todavía no puedo dejarla trabajando sola.

[

![Chat con el encargo enviado por la tarea programada y una petición Allow once tras fallar el aislamiento.](https://substackcdn.com/image/fetch/$s_!Ah0d!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbfff96a-fde3-486a-a923-7f2deca8bc35_1280x820.png)

](https://substackcdn.com/image/fetch/$s_!Ah0d!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbfff96a-fde3-486a-a923-7f2deca8bc35_1280x820.png)Debajo de Sent by scheduled task aparece el nuevo encargo y, más abajo, la petición de permiso. El «Sin novedades» de arriba es la respuesta anterior, cuando se lo pedimos desde el chat.

Si te ocurre, utiliza **Pause** y mira qué ha pasado antes de dejarla activa. En este caso hace falta resolver el problema de la aplicación y volver a probar; cambiar el prompt no basta.

[

![Tarea del tutorial en la pestaña Paused, conservando la configuración semanal.](https://substackcdn.com/image/fetch/$s_!WDJM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbdbc3c2-0129-4174-8332-67337e9d23bc_1280x820.png)

](https://substackcdn.com/image/fetch/$s_!WDJM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbdbc3c2-0129-4174-8332-67337e9d23bc_1280x820.png)En Scheduled → Paused puedes comprobar que la tarea está en pausa y conserva su horario.

Por ahora puedo pedirle el trabajo desde el chat y revisar los archivos que me devuelve. La parte de dejarlo funcionando por su cuenta queda pendiente. Antes de hacerlo, quiero ver que termina sin pedir intervención y que, cuando publique otra newsletter, prepara sus borradores sin tocar los anteriores.

---

Si has llegado hasta aquí, ya has visto por dentro varias de las cosas que llevo meses contando cuando hablo de agentes: darles un espacio de trabajo, guardar instrucciones, separar tareas, revisar resultados y preparar una forma de repetirlas.

El ejemplo utiliza newsletters y Notes, pero puedes pensar en otro trabajo que conozcas bien. Un informe que preparas cada semana, documentos que tienes que revisar o apuntes que quieres convertir en material de estudio.

Empieza por algo cuyo resultado puedas evaluar. Así sabrás qué pedirle, cuándo se ha desviado y qué corrección merece quedar guardada para la próxima vez.

Me gustaría saber qué tarea tienes tú en mente. ¿Hay algo que ya haces con ChatGPT y para lo que acabas repitiendo las mismas explicaciones cada semana?

### ***Cuéntamelo. Siempre leo todo.***

[Deja un comentario](https://ainalluna.substack.com/p/como-usar-chatgpt-work/comments)

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

# **Suscríbete a Think&Hack**

**Tools are great. Systems are better.**

Casos reales, flujos que funcionan y formas concretas de usar la IA sin perder el control del proceso.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
