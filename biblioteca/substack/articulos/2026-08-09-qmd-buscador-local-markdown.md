---
id: 210041929
titulo: "Tu IA no necesita memoria. Necesita fuentes que pueda comprobar."
subtitulo: "Cómo usar QMD para convertir archivos Markdown en una base local de recuperación: búsquedas por palabra, por significado y respuestas conectadas con documentos reales."
fecha: 2026-08-09
url: https://ainalluna.substack.com/p/qmd-buscador-local-markdown
tipo: newsletter
audiencia: everyone
estado: completo
huella: 5b454222ef4890bbdefc1130370513bf955d22d52afd82a6a7fa81b6fe42037c
---

[

![imagen](https://substackcdn.com/image/fetch/$s_!7nJy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc8b762f3-5e7d-4fcc-a416-e66ec86089d2_1536x1024.png)

](https://substackcdn.com/image/fetch/$s_!7nJy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc8b762f3-5e7d-4fcc-a416-e66ec86089d2_1536x1024.png)

¿Cómo estás?

Soy Aina y esto es Think&Hack.

Tienes documentos por doquier dentro de tu ordenador.

Newsletters publicadas. Notas de proyectos. Transcripciones. Procesos. Prompts. Decisiones. Resúmenes. Capturas. Ideas que guardaste porque algún día iban a servir para algo.

**Todo está escrito. El problema es encontrarlo.**

Para encontrar algo en tu ordenador, normalmente tienes que recordar dónde lo guardaste, conocer la ruta del archivo y acordarte del nombre que le pusiste. O, al menos, conservar una vaga idea del tipo: *«Creo que escribí sobre esto en algún documento…»*. Entonces lo abres, haces una lectura rápida y cruzas los dedos para que sea el correcto.

Si tienes algo más de experiencia, también puedes pedirle a una IA que busque en tu ordenador con una pregunta como: *«¿En qué documento hablé sobre…?»*. Sin embargo, hoy quiero presentarte **una solución mejor**.

Te cuento cómo he resuelto la búsqueda de archivos en mi ordenador gracias a **QMD**, una herramienta que me permite disponer de un buscador interno, gratuito y completamente local para mis archivos en Markdown: `los .md` que genera la IA.

---

## El error: llamar memoria a cualquier cosa

A estas alturas, y más aún si sigues esta newsletter, probablemente ya sepas **las IA tienen un problema de memoria:** no conservan automáticamente todo el contexto entre una sesión y la siguiente.

Ya lo expliqué al analizar [cómo funciona la memoria en ChatGPT, Gemini y Claude](https://ainalluna.substack.com/p/gestion-memorias-llm),

Para proporcionarles contexto y cierta continuidad, solemos recurrir a documentos que explican cómo deben trabajar con nuestros datos, además de sistemas de _logs_ que registran lo ocurrido durante cada sesión. De esta forma, construimos **una especie de memoria externa para la IA**.

Para mantener toda esta información ordenada, es habitual utilizar índices de documentos, como un archivo `index.md`. La idea es sencilla: enviamos a la IA a ese índice y confiamos en que, desde allí, pueda localizar lo que necesitamos.

Cuando trabajamos con pocos archivos, este sistema puede funcionar. Sin embargo, a medida que aumenta la cantidad de documentos y crece nuestro contexto, **el proceso se vuelve cada vez menos eficiente.** La IA necesita leer más contenido, aumenta el consumo de _tokens_ y, en muchos casos, solo obtenemos un resumen de lo que cree haber encontrado. Además, si no le pedimos explícitamente que indique la ubicación del archivo, podemos terminar con una respuesta útil, pero sin saber de qué documento procede.

Todo este sistema de recuperación de ideas, búsqueda de archivos y generación de respuestas basadas en nuestros propios documentos puede mejorarse con **QMD**.

QMD es una herramienta diseñada para indexar tus carpetas, o tus _vaults_, si trabajas con Obsidian, para poder **encontrar cualquier información en cuestión de segundos y mostrarte el documento original del que procede.**

[

![imagen](https://substackcdn.com/image/fetch/$s_!n2hA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8eb45009-542f-4d8b-abe5-686f7daf39e3_936x860.jpeg)

](https://substackcdn.com/image/fetch/$s_!n2hA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8eb45009-542f-4d8b-abe5-686f7daf39e3_936x860.jpeg)*QMD recupera el documento sobre “memoria” y muestra la ruta del archivo original, que permite comprobar la respuesta.*

---

## Cuando recuerdas la idea, pero no las palabras.

Imagina una carpeta en la que guardas todas las newsletters que has publicado en Markdown. Los archivos son legibles, están ordenados y permanecen bajo tu control. Sin embargo, encontrar una idea concreta exige recordar **en qué newsletter la escribiste** o **qué palabras utilizaste**.

A veces, una búsqueda tradicional es suficiente. Si escribes «memoria», el buscador puede encontrar la newsletter en la que aparece esa palabra exacta.

Pero ¿qué ocurre cuando no recuerdas las palabras que utilizaste?

Quizá lo que quieres preguntar es:

>
>
> ¿Dónde expliqué cómo funciona la memoria en los LLM?
>
>

Es posible que ningún archivo contenga esa frase exacta. Tal vez en el texto hablaste de recuperación de información, fuentes, contexto, memoria externa o NotebookLM. **La idea está en tus documentos, pero las palabras de tu consulta no coinciden con las que utilizaste al escribirlos.**

QMD resuelve este problema creando un índice local de tus carpetas y ofreciendo tres formas de buscar:

-

`search` realiza una búsqueda léxica mediante **BM25**. Es rápida y funciona especialmente bien cuando conoces las palabras utilizadas en el documento.

-

`vsearch` compara el significado de tu consulta con los vectores generados a partir de los fragmentos de texto. Resulta útil cuando una misma idea puede estar expresada con palabras diferentes.

-

`query` combina la búsqueda léxica y la búsqueda vectorial con la expansión de la consulta y un proceso de _reranking_. Es la opción más completa y precisa, aunque también requiere más tiempo y recursos.

[

![imagen](https://substackcdn.com/image/fetch/$s_!tzsw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff260ba0b-fd48-46fc-9f9d-dcc6fb881fbc_709x268.jpeg)

](https://substackcdn.com/image/fetch/$s_!tzsw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff260ba0b-fd48-46fc-9f9d-dcc6fb881fbc_709x268.jpeg)

Una vez localizado el resultado, `get` permite recuperar y abrir el documento original.

Esto es importante porque encontrar una respuesta no basta. Si el sistema no te permite consultar la fuente, no puedes comprobar si ha recuperado el documento correcto ni revisar el contexto en el que aparecía la información.

Por eso utilizo QMD como **buscador local sobre mi conocimiento escrito**.

---

## Antes de instalar: decide qué quieres buscar.

Puede resultar tentador conectar QMD a la carpeta más grande de tu ordenador y dejar que busque entre todos tus documentos.

Pero **tener más archivos no siempre significa obtener mejores resultados**.

Imagina que pones en una misma caja tus newsletters, notas personales, manuales técnicos y transcripciones. Cuando busques una idea, QMD tendrá que revisar contenidos muy distintos que, en ocasiones, utilizan palabras parecidas.

Por eso es mejor separar los documentos por su función. Por ejemplo:

-

una colección para newsletters;

-

otra para notas personales;

-

otra para documentación técnica.

De esta forma, puedes indicar en qué colección quieres buscar y evitar que una consulta sobre escritura termine mostrando resultados de un manual de software.

[

![imagen](https://substackcdn.com/image/fetch/$s_!-LeZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec5a91da-9056-4c8d-9a2d-79268198d55f_944x744.jpeg)

](https://substackcdn.com/image/fetch/$s_!-LeZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec5a91da-9056-4c8d-9a2d-79268198d55f_944x744.jpeg)*Ejemplo de una consulta de QMD limitada con `-c newsletterPublicadas`: busca únicamente entre las newsletters publicadas y muestra la ruta de cada resultado.*`-c newsletterPublicadas`: busca únicamente entre las newsletters publicadas y muestra la ruta de cada resultado.*

Piensa en las colecciones como si fueran estanterías. Si buscas una novela, tiene más sentido revisar la estantería de literatura que recorrer toda la biblioteca.

También ayuda que los documentos estén bien organizados. Un archivo con un título claro, una fecha y un enlace a la fuente ofrece más información que un bloque de texto sin contexto.

**QMD puede encontrar una idea aunque no recuerdes las palabras exactas, pero no puede recuperar información que nunca guardaste.**

Antes de instalarlo, decide qué carpetas contienen información que realmente quieres consultar. No necesitas indexarlo todo: necesitas indexar lo que tenga sentido buscar.

---

## Paso 1: instala QMD y comprueba que funciona

Para seguir este tutorial necesitas tener instalado **Node.js 22 o una versión posterior**. QMD también funciona con Bun, pero en este tutorial utilizaré `npm`, una opción habitual en Windows.

Antes de continuar, abre PowerShell y comprueba tu versión de Node.js:

```
node --version
```

[

![imagen](https://substackcdn.com/image/fetch/$s_!EZO-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99fa23d6-fe57-488b-a893-0feb268e5e9b_265x82.jpeg)

](https://substackcdn.com/image/fetch/$s_!EZO-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99fa23d6-fe57-488b-a893-0feb268e5e9b_265x82.jpeg)

Si aparece `v22` o un número superior, ya puedes instalar QMD con este comando:

```
npm install -g @tobilu/qmd
```

Cuando termine la instalación, ejecuta:

```
qmd --version
qmd status
```

El primer comando muestra la versión de QMD instalada. El segundo muestra su estado general.

En este punto todavía no has añadido ninguna carpeta, por lo que no aparecerá ninguna colección.

QMD no modifica tus archivos Markdown para realizar las búsquedas. En su lugar, crea un índice independiente en tu ordenador, parecido al catálogo de una biblioteca. **Tus documentos permanecen intactos y continúan siendo la fuente original.**

La primera vez que utilices la búsqueda semántica, QMD descargará los modelos que necesita. Este proceso requiere conexión a internet y puede tardar un poco más de lo habitual.

Después, **el índice y las búsquedas permanecen en tu ordenador**.

---

## Paso 2: añade tu primera carpeta.

Ahora vamos a indicar a QMD dónde están los documentos que queremos buscar.

En QMD, una **colección** es simplemente una carpeta que has añadido al buscador. No mueve ni copia tus archivos: solo le indica dónde debe encontrarlos.

Supongamos que guardas tus newsletters en esta carpeta:

```
D:\mi-vault\newsletterPublicadas
```

Para añadirla, ejecuta este comando en PowerShell:

```
qmd collection add "D:\mi-vault\newsletterPublicadas" --name newsletterPublicadas
```

La primera parte indica la ubicación de la carpeta. Con `--name` le asignamos un nombre corto que utilizaremos después para buscar dentro de ella.

En este caso, la colección se llamará `newsletterPublicadas`.

Cuando termine el proceso, comprueba que se ha añadido correctamente:

Revisa el resultado:

```
qmd collection list
```

Este comando muestra todas las colecciones disponibles. Deberías ver tu nueva colección en la lista.

[

![imagen](https://substackcdn.com/image/fetch/$s_!0AZC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd60c5e2f-2895-499a-a8c8-dbbe58581809_685x709.jpeg)

](https://substackcdn.com/image/fetch/$s_!0AZC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd60c5e2f-2895-499a-a8c8-dbbe58581809_685x709.jpeg)

También puedes comprobar qué archivos ha encontrado QMD dentro de ella:

```
qmd ls newsletterPublicadas
```

A partir de ahora, cuando añadas, elimines o modifiques documentos dentro de la carpeta, ejecuta:

```
qmd update
```

Este comando actualiza el índice para que los cambios aparezcan en las próximas búsquedas.

**QMD no sustituye la organización de tus carpetas: utiliza la estructura que ya tienes para ayudarte a encontrar la información.**

## Paso 3: prepara la búsqueda por significado.

**La colección ya está lista para buscar palabras exactas.** Sin embargo, para **encontrar ideas** expresadas de formas diferentes, QMD necesita analizar el significado de tus documentos.

Ejecuta este comando:

```
qmd embed
```

QMD dividirá los documentos en fragmentos y preparará cada uno para la búsqueda semántica. Este proceso puede tardar unos minutos, especialmente la primera vez o si tienes muchos archivos.

Cuando termine, comprueba el estado:

```
qmd status
```

Ahora deberías ver tanto los documentos indexados como los fragmentos preparados para la búsqueda semántica.

[

![imagen](https://substackcdn.com/image/fetch/$s_!ddkt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F806b317e-715c-4e14-887d-6edf6dd90cfa_604x284.jpeg)

](https://substackcdn.com/image/fetch/$s_!ddkt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F806b317e-715c-4e14-887d-6edf6dd90cfa_604x284.jpeg)

**Solo necesitas generar los embeddings una vez.** Después, cuando añadas o modifiques archivos, podrás actualizar el índice para incorporar los cambios.

## Paso 4: prueba las tres formas de buscar

Ahora que los documentos están preparados, vamos a probar las tres formas de búsqueda que ofrece QMD.

### Buscar palabras exactas

Empecemos por la opción más sencilla:

```
qmd search "memoria" -c newsletterPublicadas
```

[

![imagen](https://substackcdn.com/image/fetch/$s_!BbPF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff5b40ef7-ff86-48fe-a40d-16d90ebb3eee_944x686.jpeg)

](https://substackcdn.com/image/fetch/$s_!BbPF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff5b40ef7-ff86-48fe-a40d-16d90ebb3eee_944x686.jpeg)La búsqueda textual encuentra los documentos de la colección `newsletterPublicadas` que contienen el término `memoria`.

`search `busca las palabras que escribes. Funciona bien cuando recuerdas un nombre, una frase, una sigla o cualquier término que aparece literalmente en el documento.

En este caso, QMD busca la palabra `memoria` dentro de las newsletters y ordena los resultados según su relevancia.

### Buscar por significado

Ahora vamos a expresar la misma idea sin utilizar la sigla RAG:

```
qmd vsearch "cómo hacer que una ia sepa quien soy antes de responder" -c newsletterPublicadas -n 5
```

[

![imagen](https://substackcdn.com/image/fetch/$s_!rppf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb95731f7-2ad3-413d-ad9f-ad99e3d47e71_941x801.jpeg)

](https://substackcdn.com/image/fetch/$s_!rppf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb95731f7-2ad3-413d-ad9f-ad99e3d47e71_941x801.jpeg)La búsqueda semántica recupera newsletters relacionadas con la personalización de la IA, la audiencia y la conservación del contexto.

En este caso, el primer resultado es una newsletter sobre instrucciones personalizadas para ChatGPT, Claude y Gemini. El segundo explica cómo definir para quién escribe la IA, y el tercero aborda la pérdida de contexto durante una conversación.

Ninguno de esos títulos coincide literalmente con la consulta. Sin embargo, `vsearch` identifica que conceptos como **personalización, identidad, audiencia y contexto** están relacionados con la idea de que una IA sepa quién eres antes de responder.

Los resultados tampoco tienen todos la misma precisión. El primer documento se ajusta directamente a la pregunta, mientras que los siguientes se acercan al tema desde otros ángulos.

Esa es la diferencia respecto a `search`: **`vsearch` no se limita a encontrar las palabras que has escrito, sino que busca documentos relacionados con el significado de la consulta**`vsearch` no se limita a encontrar las palabras que has escrito, sino que busca documentos relacionados con el significado de la consulta**.

### Combinar ambos tipos de búsqueda

Para realizar una búsqueda más completa, utiliza `query`:

```
qmd query "cómo hacer que una ia sepa quien soy antes de responder" -c newsletterPublicadas -n 5
```

[

![imagen](https://substackcdn.com/image/fetch/$s_!CCwU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F024879f4-d987-4eaa-93ab-99a951161b7d_945x912.jpeg)

](https://substackcdn.com/image/fetch/$s_!CCwU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F024879f4-d987-4eaa-93ab-99a951161b7d_945x912.jpeg)`query` combina distintas formas de búsqueda y vuelve a ordenar los resultados según su relevancia.

A diferencia de `vsearch`, `query` no se basa únicamente en la similitud de significado. Amplía la consulta, combina la búsqueda textual con la semántica y vuelve a ordenar los documentos encontrados.

En esta prueba, coloca en primer lugar la newsletter sobre cómo definir para quién escribe una IA, con una puntuación del 93 %. Después aparecen el artículo sobre instrucciones personalizadas y otro documento relacionado con sistemas de agentes.

Esto no significa que el primer resultado sea siempre el correcto. Significa que QMD ha combinado varias señales y considera que ese documento es el que mejor responde a la consulta.

``query``** resulta especialmente útil cuando la pregunta es conceptual o ambigua, aunque puede tardar más porque realiza varios pasos antes de mostrar los resultados.**`query` resulta especialmente útil cuando la pregunta es conceptual o ambigua, aunque puede tardar más porque realiza varios pasos antes de mostrar los resultados.**

La elección depende de lo que recuerdes:

-

Utiliza `search` cuando conozcas las palabras exactas.

-

Utiliza `vsearch` cuando recuerdes la idea, pero no cómo la escribiste.

-

Utiliza `query` cuando quieras combinar ambas estrategias y obtener una selección más elaborada.

---

## Paso 5: conecta QMD con tu agente.

Hasta ahora has utilizado QMD desde PowerShell. También puedes conectarlo con un agente compatible con MCP para que busque y recupere documentos sin que tengas que ejecutar cada comando manualmente.

La configuración depende del agente que utilices.

Si trabajas con **Claude Code**, la documentación de QMD recomienda instalar su _plugin_:

```
claude plugin marketplace add tobi/qmd
claude plugin install qmd@qmd
```

En otros clientes compatibles con MCP, puedes añadir QMD manualmente con esta configuración:

```
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

Guarda el bloque en el archivo de configuración MCP de tu agente y reinicia la herramienta para aplicar los cambios.

También puedes pedirle al propio agente que realice esta configuración:

```
Configura QMD como servidor MCP utilizando el comando `qmd mcp`.

Añade la configuración necesaria, reinicia la conexión si hace falta
y comprueba que las herramientas de QMD estén disponibles.
```

Aun así, conviene revisar el cambio: no todos los agentes utilizan el mismo archivo ni el mismo formato de configuración.

Una vez conectado, puedes hacer una petición como esta:

```
Usa QMD y busca solo en la colección newsletterPublicadas.

Quiero recuperar lo que he publicado sobre la memoria y el estado de los agentes.

Devuélveme:
- las tres fuentes más relevantes;
- la idea principal de cada una;
- un fragmento que sostenga esa interpretación;
- la ruta del documento;
- las contradicciones o los huecos que detectes.

No completes la respuesta con conocimientos externos.
Si QMD no encuentra pruebas suficientes, indica qué buscaste
y qué información falta.
```

[

![imagen](https://substackcdn.com/image/fetch/$s_!Ynxs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F86f1f303-b1de-4c36-8a4d-b53786a1e435_949x924.jpeg)

](https://substackcdn.com/image/fetch/$s_!Ynxs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F86f1f303-b1de-4c36-8a4d-b53786a1e435_949x924.jpeg)Claude Code utiliza QMD mediante MCP para buscar información sobre memoria y estado de los agentes únicamente en la colección `newsletterPublicadas`.

En la captura se puede ver que el agente no empieza a responder directamente. Primero llama a la herramienta de QMD, amplía la consulta y busca dentro de la colección indicada.

Después utiliza los documentos recuperados para construir la respuesta:

[

![imagen](https://substackcdn.com/image/fetch/$s_!OvPB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe09fdfcd-53c1-4f97-ad3e-ba0f52f38d52_932x816.jpeg)

](https://substackcdn.com/image/fetch/$s_!OvPB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe09fdfcd-53c1-4f97-ad3e-ba0f52f38d52_932x816.jpeg)El agente devuelve las fuentes recuperadas por QMD junto con su ruta, puntuación, idea principal y un fragmento del documento.

Cada resultado queda vinculado a un archivo concreto. Esto permite revisar la fuente original y comprobar si la interpretación del agente se sostiene realmente en el texto.

Pero la respuesta no termina en una lista de documentos. Como se lo pedimos en el _prompt_, el agente también compara las fuentes e identifica contradicciones y lagunas:

[

![imagen](https://substackcdn.com/image/fetch/$s_!sbhk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F588f7eed-69b8-433c-8f95-f0b0ac403fa7_908x481.jpeg)

](https://substackcdn.com/image/fetch/$s_!sbhk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F588f7eed-69b8-433c-8f95-f0b0ac403fa7_908x481.jpeg)Claude Code compara las fuentes recuperadas y señala cambios de postura, cuestiones no resueltas y contenidos que podrían necesitar una actualización.

En este caso, el agente distingue entre una evolución de postura y una contradicción directa. También detecta cuestiones que los documentos todavía no responden, como qué ocurre con el estado entre sesiones o cómo se mantiene la memoria del agente a largo plazo. (Ideas para nuevas newsletters)

Esta es una de las ventajas de conectar QMD con un agente: **no solo recuperas documentos, sino que puedes pedirle que los compare, encuentre vacíos y señale qué conocimiento falta**.

MCP no carga todos tus archivos en el contexto del agente. Le permite **buscar primero, recuperar únicamente las fuentes necesarias y analizarlas después**.

## De guardar información a poder encontrarla.

Al principio te decía que tienes documentos por todas partes: newsletters, notas, transcripciones, decisiones, procesos e ideas que guardaste porque algún día podían servirte.

**El problema no era que faltara información. Era no poder encontrarla cuando la necesitabas.**

QMD no crea una memoria nueva ni reorganiza tus archivos por ti. Indexa las carpetas que ya tienes, permite buscar por palabras o por significado y te devuelve el documento original para que puedas comprobar la fuente.

Cuando lo conectas con tu agente mediante MCP, el sistema da un paso más: el agente puede buscar únicamente en la colección adecuada, recuperar los documentos necesarios y construir una respuesta vinculada a ellos.

**Tools are great. Systems are better.**

Instalar QMD requiere un comando. Lo valioso aparece cuando decides qué documentos entran, cómo los separas y cómo debe utilizarlos tu agente.

Entonces tus archivos dejan de ser una acumulación de cosas que esperas recordar y se convierten en **conocimiento que puedes volver a encontrar**.

---

## Recursos

-

[QMD: repositorio y documentación oficial](<https://github.com/tobi/qmd>)

-

[QMD: versiones publicadas](<https://github.com/tobi/qmd/releases>)

-

[Model Context Protocol: introducción oficial](<https://modelcontextprotocol.io/docs/getting-started/intro>)

-

[Artículo más técnico para ampliar información](https://x.com/ArtemXTech/status/2028330693659332615)

* **Cuéntamelo. Siempre leo todo.***

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

# **Suscríbete a Think&Hack**

**Tools are great. Systems are better.**

Casos reales, flujos que funcionan y formas concretas de usar la IA sin perder el control del proceso.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
