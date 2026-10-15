---
id: 183644091
titulo: "#14 Memoria en ChatGPT, Gemini y Claude: Cómo funciona realmente "
subtitulo: "Antes de usarla, entiéndela."
fecha: 2026-01-07
url: https://ainalluna.substack.com/p/gestion-memorias-llm
tipo: newsletter
audiencia: everyone
estado: completo
huella: 6b07f44265087263c3340f71b8405d3668af5a0940cd683f0a43b7411511197a
---

¿Cómo estás?

Soy Aina y esto es Think&Hack.

Hoy volvemos a los básicos: cómo funciona realmente la memoria en ChatGPT, Gemini y Claude.

Si te interesa entender antes de implementar, suscríbete para no perderte nada.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)

---

[

![Memoria en ChatGPT, Gemini y Claude: Cómo funciona realmente ](https://substackcdn.com/image/fetch/$s_!aLBM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe759ed2d-6be2-4880-949d-469ef9d16eb7_2816x1536.png)

](https://substackcdn.com/image/fetch/$s_!aLBM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe759ed2d-6be2-4880-949d-469ef9d16eb7_2816x1536.png)Memoria en ChatGPT, Gemini y Claude: Cómo funciona realmente

Leo posts por ahí. LinkedIn, newsletters, varias redes. Todos hablando de crear asistentes que te ayudan con tus propósitos del 2026.

Y cada vez que leo uno me surge la misma duda.

*Si uso un GPT personalizado que no tiene memoria entre chats... ¿Cómo mantienes continuidad? ¿Le subes archivos con el contexto acumulado? ¿Trabajas siempre en el mismo chat?*

Nadie lo explica.

Así que decidí volver a los básicos. Buscar en la documentación oficial. Entender qué es un chat, qué es un proyecto, qué es un GPT, qué es un Gem. Cómo funciona la memoria en cada plataforma.

*Porque sospechaba que mucha gente está montando “asistentes de propósitos” sin entender la arquitectura que hay debajo.*

Y tenía razón.

---

### Cómo funciona la memoria en cada plataforma

Investigué las tres plataformas principales. Esto es lo que encontré:

**ChatGPT** tiene capas separadas que no se hablan entre sí:

[

![Tipo de memorias ChatGPT](https://substackcdn.com/image/fetch/$s_!eDbn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6fa68544-77bf-4cee-bbe5-f9e154110fc0_952x414.png)

](https://substackcdn.com/image/fetch/$s_!eDbn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6fa68544-77bf-4cee-bbe5-f9e154110fc0_952x414.png)Tipo de memorias ChatGPT

```
Y ahí está el problema: los GPTs tienen su propia memoria. No comparten nada con ChatGPT general ni entre ellos. Y no puedes usar GPTs dentro de Projects.
```

**Gemini** tiene Personal Context (memoria automática desde agosto 2025) y Saved Info que puedes editar. Pero los Gems, su equivalente a los GPTs, solo mantienen instrucciones. Cero memoria de conversaciones entre sesiones.

**Claude** tiene Memory que sintetiza conversaciones cada 24 horas, Projects con memoria aislada por proyecto, y Chat Search para buscar en tu historial via RAG.

---

### Por qué los GPTs no recuerdan nada

-

Un [GPT personalizado](https://ainalluna.com/blog/custom-gpts-en-chatgpt-crea-tu-agente-personalizado-para-tareas-especializadas) es un “quién eres” fijo.

-

No es un “qué has aprendido de mí”.

Puedes configurar instrucciones brillantes. Puedes definir una personalidad perfecta. **Pero cuando cierras el chat y abres uno nuevo, tu GPT no recuerda nada de lo que hablasteis.**

Las opciones reales para mantener continuidad:

**1. Un solo chat eterno.** Funciona hasta que la ventana de contexto explota. Semanas como mucho.

**2. Documentos de contexto manuales.** Cada sesión subes un archivo actualizado. Tedioso pero funciona.

**3. Projects en lugar de GPTs.** [ChatGPT Projects](https://ainalluna.com/blog/proyectos-en-chatgpt-organiza-tu-trabajo-y-maximiza-tu-productividad-con-ia) tiene memoria built-in. Claude Projects tiene memoria + búsqueda. Es lo más cercano a un asistente que “te conoce”.

---

### Qué preguntarte antes de montar tu asistente

Volví a pensar en esos posts de “crea tu asistente de propósitos”.

```
No es que estén mintiendo. Es que **están vendiendo la idea sin haber chocado con la realidad de usarlo más de tres días seguidos.**
```

-

La pregunta no es “cómo configuro mi GPT perfecto”.

-

La pregunta es: ¿**Qué arquitectura de memoria necesito para lo que quiero hacer?**

Y esa pregunta casi nadie se la hace antes de empezar.

**¿Has intentado crear un asistente de propósitos este enero? ¿Cómo lo resolviste?**

** **

[Compartir](https://ainalluna.substack.com/p/gestion-memorias-llm?utm_source=substack&utm_medium=email&utm_content=share&action=share)

**Cué*****ntamelo. Siempre leo todo.***

![imagen](https://substackcdn.com/image/fetch/$s_!jAJ6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa6a28f5-efe2-4efb-93bc-87d726ddd0ec_56x56.png)

**Recomienda Think&Hacks**

Soy Aina. Responsable de IA generativa en Planeta.

Tres cosas rápidas:

1.

🔄 **Comparte**: Reenvía esto a quien siga confiando ciegamente en la memoria de ChatGPT.

2.

💬 **Responde**: ¿Usas archivos de contexto externos? ¿Qué sistema tienes?

3.

📩 **Suscríbete**: Si te han reenviado esto, únete aquí 👇

¡Gracias por leer Think & Hack! Suscríbete gratis para recibir nuevos posts y apoyar nuestros trabajo.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
