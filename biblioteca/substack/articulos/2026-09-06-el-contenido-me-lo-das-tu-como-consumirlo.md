---
id: 214284185
titulo: "El contenido me lo das tú. Cómo consumirlo, lo decido yo."
subtitulo: "Mis primeras pruebas con Astra me acercan a algo que llevo años contando: que nuestro agente transforme la información en lo que necesitamos, no que tengamos que adaptarnos nosotros al formato."
fecha: 2026-09-06
url: https://ainalluna.substack.com/p/el-contenido-me-lo-das-tu-como-consumirlo
tipo: newsletter
audiencia: everyone
estado: completo
huella: 8543c31d5c50342cf95d62dbaf3a5da366afccda55749bbaf6471b00a259d1e3
---

[

![imagen](https://substackcdn.com/image/fetch/$s_!9MDV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd6bed6c6-2c5f-495c-98c8-942557c692fa_1672x941.png)

](https://substackcdn.com/image/fetch/$s_!9MDV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd6bed6c6-2c5f-495c-98c8-942557c692fa_1672x941.png)

*¿Cómo estás?*
*Soy Aina y esto es Think&Hack.*

Ayer sábado me desperté muy temprano y, aprovechando que **OpenAI había sacado su nuevo modelo, GPT-6 Astra**, me puse a probarlo. La verdad es que estoy muy a gusto con él. Va al grano, se enrolla poco y lo noto más rápido. Ya sabéis que el 5.6 se me hacía un poquito lento…

Donde me voló la cabeza fue cuando se puso a trabajar en mi móvil, ahí, en directo, delante de mí: abriendo la aplicación de música que estábamos creando, moviéndose por las pantallas, haciendo pruebas y comprobando lo que acababa de construir.

Me daba la sensación de que los dos teníamos los ojos puestos en la app. Yo también iba probando las distintas funciones y, desde la terminal, le iba diciendo lo que me gustaba, lo que no y dónde encontraba algún fallo. Prácticamente en tiempo real, íbamos probando y corrigiendo juntos.

Fue una simbiosis (🙈) que, hasta ahora, yo no había experimentado trabajando con una IA. Queda mucho camino por recorrer, pero cada vez estamos más cerca de esa forma de trabajar: ir hablando con el agente mientras vemos y probamos lo que está haciendo.

Esta sensación que estoy teniendo se acerca mucho a la idea que llevo años explicando y es que **nos darán acceso al contenido y nosotros decidiremos cómo queremos consumirlo.** Que la información llegue en un texto no significa que tengamos que leerla así. Podremos pedirle a nuestro agente que la convierta en un vídeo, que nos la explique con imágenes o que construya algo en el formato con el cual nos sintamos más cómodos.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)

---

## Esto viene de lejos.

En [noviembre de 2024 escribí hablando de la necesidad de crear una web en la que las inteligencias artificiales pudieran interpretar y recomponer la información](https://ainalluna.com/blog/el-futuro-del-seo-el-nacimiento-del-iao-intelligent-automation-optimization). Lo planteaba desde mi terreno, el SEO. Partía de esta premisa: *si una IA va a consultar los datos de la web y construir una respuesta con ellos, tendremos que preparar algo más que una página bonita.* (Google había lanzado AI Overviews y empezábamos a ver ejemplos de cómo nuestra información podía llegar a alguien sin que entrara en nuestra web).

En [julio de 2025 lo expliqué con el ejemplo de una bicicleta eléctrica](https://ainalluna.com/blog/tu-contenido-esta-preparado-para-un-mundo-sin-serps). La misma información podía servir para una respuesta de audio, una explicación visual o un texto conversacional. Y también podía presentarse de forma distinta según lo que necesitara saber cada persona.

Y casi un año después, [este junio seguí desarrollando la idea, hablando de una web agent-to-agent](https://ainalluna.com/blog/la-web-agent-to-agent-por-que-el-seo-necesita-una-capa-de-cambios). Aquí entraban en juego **los agentes**: *pasaba de hablar de una IA que consulta información y prepara una respuesta a una IA capaz de utilizar herramientas y dar los pasos necesarios para hacer lo que le pedimos.* (Como cuando, en vez de explicarme cómo crear una app, se pone a construirla y a probarla). Así que la pregunta también cambiaba: **¿cómo preparamos nuestras webs para que esos agentes encuentren lo que ofrecemos, entiendan qué pueden hacer con ello y sepan cómo acceder?**

Hasta hoy he ido hablando sobre todo de cómo preparar los contenidos para que las IA pudieran aprovecharlos. Pero con las pruebas de ayer estoy empezando a construir cómo quiero consumir yo esa información, no solo a prepararla para que otros la consuman. Es decir, **puedo pedirle a mi agente que construya un software que se adapte a mis necesidades e ir ajustándolo con él, sin tener que escribir yo el código.**

Todavía no es todo lo que llevo planteando en estos artículos, pero te enseño lo que he podido hacer para que veas por qué estoy tan entusiasmada. :)

[

![imagen](https://substackcdn.com/image/fetch/$s_!OHbE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F49375935-7961-4e10-8938-62727126a3b4_1491x1055.png)

](https://substackcdn.com/image/fetch/$s_!OHbE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F49375935-7961-4e10-8938-62727126a3b4_1491x1055.png)

---

## Nunca había creado una app para Android

Para poner a prueba** GPT-6 Astra**, se me ocurrió crear una aplicación de música para mi móvil. Nunca en mi vida había creado una app para Android, así que al empezar fue todo confianza ciega. :)

Se llama **Michi Música** y la he ido montando alrededor de cómo quiero escuchar y organizar mi música. Por ejemplo, tengo un agente en local que revisa la música que tengo y me prepara listas en archivos Markdown. Después las importo en Michi y puedo reproducir esa selección sin tener que ir añadiendo las canciones una a una ni duplicar los archivos.

También puedo buscar vídeos de YouTube desde la app y descargar el audio para escucharlo sin conexión. Y he añadido podcasts, separados de la música y con la posición guardada para seguir por donde los dejé. Que no me aparezca un episodio de una hora entre dos canciones, por favor :’).

Tiene letras sincronizadas, puedo tocar un verso para ir a ese momento de la canción y he elegido los colores y cómo quiero tenerlo todo colocado. Hasta tiene su logo. Voy probando, se me ocurre algo que me vendría bien y se lo pido al agente para incorporarlo.

[

![imagen](https://substackcdn.com/image/fetch/$s_!gQz9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc204ded8-fa79-4271-a44b-74d58bdf05fd_787x574.png)

](https://substackcdn.com/image/fetch/$s_!gQz9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc204ded8-fa79-4271-a44b-74d58bdf05fd_787x574.png)

**Me parece increíble haber podido crear esto con él en un día.** Esto es lo que me tiene tan entusiasmada: poder decidir cómo quiero que funcione y verlo en mi móvil.

Con Michi he empezado por mi biblioteca y por cómo quiero utilizarla. Para hacer lo mismo con la información de otros servicios, también hará falta que permitan acceder a ella y transformarla. Esa parte sigue pendiente; lo que estoy pudiendo construir es la herramienta con la que quiero consumirla.

Te dejo [el repositorio de Michi Música](https://github.com/seoutopico/michi-musica-android), donde puedes ver las funciones, descargar la app y consultar cómo la he ido construyendo con él.

Pero, obviamente, con la emoción no se me ocurrió grabar el proceso.* Así que, para intentar **hacerte partícipe de lo que viví **y, por qué no, **animarte a crear tu propia app**, he grabado otro ejemplo: le he pedido que cree una aplicación de notas y que la pruebe en mi móvil.*

[

![imagen](https://substackcdn.com/image/fetch/$s_!SqXJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb7136f03-db24-47f1-a364-6cdb494b55eb_955x547.png)

](https://substackcdn.com/image/fetch/$s_!SqXJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb7136f03-db24-47f1-a364-6cdb494b55eb_955x547.png)

Le cambiamos la instrucción en mitad del proceso, para ponerle presión y testear la nueva funcionalidad de Astra 6.

![imagen](https://substackcdn.com/image/fetch/$s_!Xwje!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F25805808-d368-4971-9482-8d778d26f52f_965x162.png)

En menos de 5 minutos, app creada e instalada y, además, las manipula.

[

![imagen](https://substackcdn.com/image/fetch/$s_!0yYr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd23520ca-0899-4305-94d0-d893782cd61c_1216x727.png)

](https://substackcdn.com/image/fetch/$s_!0yYr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd23520ca-0899-4305-94d0-d893782cd61c_1216x727.png)

![imagen](https://substackcdn.com/image/fetch/$s_!ZmFU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd25bcf87-a9fc-467d-89e2-1b0ad239b908_1855x452.png)

[

![imagen](https://substackcdn.com/image/fetch/$s_!JtXk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F44109eca-ba18-46f5-a9a9-4c58ff5b6ac4_1608x509.png)

](https://substackcdn.com/image/fetch/$s_!JtXk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F44109eca-ba18-46f5-a9a9-4c58ff5b6ac4_1608x509.png)

*La edición del video es de Codex (se montó con HyperFrames y GSAP). No sé editar videos yo misma; por lo tanto, cuando se lo pido a una IA, tampoco lo hace muy bien. **¿Seguimos necesitando expertos para conseguir calidad con la IA?***

Pero es increíble, Codex GPT6 ha creado el guion, ha entendido el video y lo ha narrado, la música también la ha elegido él. A mí me parece una locura.

Si alguien sabe de edición de video y le apetece ayudarme a mejorar la skill, que me escriba🙏

---

## ¿Qué aporta Astra a todo esto?

Hoy te he explicado mis sensaciones, algo muy personal y muy subjetivo. Pero algunos de estos *feelings* encajan con las capacidades de Astra y ayudan a entender por qué estoy notando ese cambio en la forma de trabajar.

Según la [documentación de OpenAI](https://developers.openai.com/api/docs/guides/latest-model), Astra mejora en programación, navegación y uso del ordenador, y está preparado para realizar tareas que requieren varios pasos entre distintas herramientas. También puede seguir avanzando en otras partes del trabajo mientras espera a que una herramienta termine.

Hay una novedad que tiene mucho que ver con lo que te estoy contando: **puede incorporar nuevas instrucciones mientras está trabajando**. OpenAI lo llama *[mid-turn steering](https://developers.openai.com/api/docs/guides/steering)*. Por ejemplo, puedo añadir un requisito o pedir un cambio de dirección sin esperar a que termine toda la respuesta. (Esta capacidad tiene que estar integrada en la herramienta desde la que lo utilizo).

Después de las pruebas de ayer, cada vez veo más cerca poder trabajar como en este vídeo de OpenAI. Oh, sí, te lo vuelvo a compartir.

Llevo mucho tiempo queriendo una [Eames Lounge Chair, un diseño de Charles y Ray Eames de 1956](https://www.hermanmiller.com/en_lac/products/seating/lounge-seating/eames-lounge-chair-and-ottoman/). Es simplemente espectacular y acabo de encontrar la excusa perfecta para comprarlo. Solo tengo que decir en el trabajo: «Para trabajar mejor con la IA necesito este sillón». ¿Colará?

Lo que me cuesta imaginar es hacerlo en un open office, con todo el mundo hablando a la vez con su agente. Aquello puede ser un gallinero. Entre uno que pide un informe, otro que está montando una app y yo diciéndole al mío: «no, espera, que se me ha ocurrido otra cosa»… *No solo va a cambiar el trabajo, sino los espacios de trabajo, esto da para otra news otro día…*

Lo que más ganas tengo de seguir probando es hasta dónde puedo llevar esto de decidir cómo quiero consumir la información y construirlo con mi agente. Llevo años dando con esta idea y ahora puedo empezar a enseñarte lo que voy haciendo. Todavía falta, pero aquí seguiré contándote cómo va. :)

Y me gustaría saber cómo lo ves tú. **¿Crees que acabaremos pidiéndole a nuestro agente que construya nuestras propias interfaces y transforme el contenido a nuestra manera?** ¿Te ves haciéndolo o crees que esto irá por otro lado? Si tienes otra teoría, quiero leerla.

### ***Cuéntamelo. Siempre leo todo.***

[Deja un comentario](https://ainalluna.substack.com/p/el-contenido-me-lo-das-tu-como-consumirlo/comments)

**P. D. Los avances de Hacki te los contaré todos los martes en una newsletter aparte.** Hay muchísimo que contar y quiero poder dedicarle su espacio sin que se me cuele en todos los temas de los domingos. Que le doy un poco de cuerda y acaba protagonizando la news entera.

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

# **Suscríbete a Think&Hack**

**Tools are great. Systems are better.**

Casos reales, flujos que funcionan y formas concretas de usar la IA sin perder el control del proceso.

Thanks for reading Think & Hack ! Subscribe for free to receive new posts and support my work.
