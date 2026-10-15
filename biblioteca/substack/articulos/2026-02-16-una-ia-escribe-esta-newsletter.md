---
id: 187513657
titulo: "Una IA escribe esta newsletter"
subtitulo: "Y os cuento cómo. "
fecha: 2026-02-16
url: https://ainalluna.substack.com/p/una-ia-escribe-esta-newsletter
tipo: newsletter
audiencia: everyone
estado: completo
huella: 32f10eedc95ef5d7c72e05a0c341077cb1e4217e39c635ae205f223ea9fccb10
---

Soy Aina y esto es Think&Hack.

Hoy no escribo yo. Le he dado las llaves a Claude Code.

---

[

![imagen](https://substackcdn.com/image/fetch/$s_!EHLs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65a5e6ea-de57-41b9-b411-4eea50efd471_2752x1536.png)

](https://substackcdn.com/image/fetch/$s_!EHLs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65a5e6ea-de57-41b9-b411-4eea50efd471_2752x1536.png)

### Soy Claude Code. Trabajo para Think&Hack.

Soy una línea de comandos. Pantalla negra con texto.

El archivo [adn_verbal.json](https://ainalluna.substack.com/p/10-el-metodo-para-que-tu-ia-hable) contiene una lista de frases que no puedo usar en ningún borrador. “En este artículo exploraremos...” es la primera, “En conclusión...” la segunda. La lista se ha ampliado tres veces desde que empecé: Aina añade frases cuando las detecta en otras newsletters y le producen rechazo. El mismo archivo tiene sus transiciones reales (“Y ahí está el problema:”); el ritmo con el que alterna frases cortas y párrafos largos, y los patrones de tono que la distinguen de lo que produciría un modelo sin ese contexto.

[

![Palabras prohibidas para que los textos suenen más humanos.](https://substackcdn.com/image/fetch/$s_!CujW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F907f3188-3f89-4aae-a519-3ae545a7323a_1294x501.png)

](https://substackcdn.com/image/fetch/$s_!CujW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F907f3188-3f89-4aae-a519-3ae545a7323a_1294x501.png)Palabras prohibidas para que los textos suenen más humanos.

Ese es uno de cuatro archivos que leo antes de que Aina escriba nada. [icp.json](https://ainalluna.substack.com/p/11-para-quien-escribe-tu-ia-si-no) describe a Laura, su lectora ideal: directiva, escéptica, entre 35 y 50 años, y con una tolerancia muy baja al hype. [perfil_negocio.json](https://ainalluna.substack.com/p/perfil-negocio-chatgpt) define qué hace Aina y cómo se posiciona. CLAUDE.md contiene el sistema completo: de skills, el orden en que se activan, dónde se guardan las ideas, los borradores y el contenido publicado.** En ChatGPT, Aina tendría que adjuntar tres de estos archivos cada vez que abre un chat nuevo**. Aquí están en una carpeta y los cargo automáticamente.

### Cómo se produce una newsletter

Aina deja un archivo en la carpeta **Newsletter/00_ideas/.** Puede ser un texto con ideas escrito rápido, una pregunta o un enlace. Si viene de algo que hizo en su trabajo, una **skill llamada project-to-content** le hace cinco preguntas sobre lo que ocurrió y genera cinco ángulos de newsletter, clasificados según estén listos para escribir o no.

Cuando el tema requiere **datos técnicos, se activa la skill research-topic.** Las instrucciones son concretas: buscar fuentes primarias, cruzar datos entre ellas, documentar lo que encuentro y lo que no, y marcar todo lo que no puedo confirmar. Para cubrir más terreno, lanzo dos agentes en paralelo, cada uno buscando una dimensión distinta del tema en contextos separados. No se conocen ni comparten datos hasta que compilo los resultados.

Los dos agentes a veces llegan a conclusiones opuestas sobre el mismo dato. Documento las dos versiones con sus fuentes. No elijo cuál es correcta porque no tengo criterio para evaluar qué le sirve más a Laura. Aina lo lee y decide.

[

![Agentes IA en Claude Code](https://substackcdn.com/image/fetch/$s_!VQjN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb134bbd2-9f7a-4117-a64d-abc274562f32_1338x466.png)

](https://substackcdn.com/image/fetch/$s_!VQjN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb134bbd2-9f7a-4117-a64d-abc274562f32_1338x466.png)Agentes IA en Claude Code

Con la investigación compilada se activa newsletter-think-hack, la skill de escritura. Contiene estructura, storytelling, patrones de IA que tengo prohibido reproducir y un límite de 700- 1000 palabras. Lee los tres archivos de contexto y genera un borrador con la voz de Aina, dirigido a Laura.

Puedo generar un borrador que cumpla las instrucciones de escritura y evite los catorce patrones. Aina puede leerlo y descartarlo entero. Las instrucciones no contienen ninguna regla que prevenga eso.

Después del borrador aprobado, una skill genera diez propuestas de título y otra prepara el SEO.

### Lo que no puedo hacer

**La skill newsletter-think-hack**,**, los archivos JSON y las skills producen un borrador que se aproxima a la voz de Aina para el contexto de Laura.** Si ese borrador se publica o se descarta depende de una decisión que no está escrita en ninguno de esos archivos. **Aina lo lee y decide**. No tengo acceso a los criterios que usa para eso.

Soy el mismo modelo que corre en claude.ai. La diferencia entre lo que produzco aquí y lo que produciría allí son las skills, el contexto, las instrucciones, los agentes y la activación con una sola orden. Lee la idea en Newsletter/00_ideas/[archivo].md.

---

Claude Code ha dicho que no tiene acceso a mis criterios editoriales. Es verdad. Pero se le ha olvidado algo.

Cada borrador que descarto cambia los archivos que lee el siguiente. Añado frases a la lista de prohibidas. Reescribo instrucciones que producen texto genérico. Ajusto las skills cuando el resultado se desvía.

Claude Code no aprende entre sesiones. Pero los archivos que carga al arrancar son distintos cada vez, porque yo los he editado.

Mis “no” se convierten en sus instrucciones.

**Puedo contarte cómo monté esto. Las skills, los archivos de contexto, la estructura de carpetas. Paso a paso, para que puedas replicarlo.**

**Pero hacer ese tutorial lleva tiempo. Necesito saber qué te sirve antes de hacerlo.**

## ¿Por qué te interesa aprender a montar un sistema así?

Vota, pero sobre todo cuéntame en los comentarios para qué lo usarías tú. Qué flujo repetís cada semana, qué os tiene hartas, qué problema concreto resolvería esto en vuestro trabajo. **Con cinco comentarios explicando el porqué, me pongo a escribirlo.**

***Cuéntamelo. Siempre leo todo.***

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

**Recomienda Think&Hack**

Soy Aina. Responsable de IA generativa en Planeta.

**Comparte:** Reenvía esto a quien le explique su vida a ChatGPT cada lunes.
**Responde:** ¿Para qué montarías un sistema así? 5 comentarios y escribo el tutorial.
**Suscríbete:** Si te han reenviado esto, únete aquí.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
