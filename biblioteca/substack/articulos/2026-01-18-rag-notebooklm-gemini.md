---
id: 183914023
titulo: "Think&Hack #17 — de 10 archivos a 300 sin código"
subtitulo: "Lo que usan las empresas grandes, gratis y sin código."
fecha: 2026-01-18
url: https://ainalluna.substack.com/p/rag-notebooklm-gemini
tipo: newsletter
audiencia: everyone
estado: completo
huella: 85a5a0ef3f1bb5281ebadf12b2db5e800bcab37938fcd1a2656142693ff4c4bb
---

¿Cómo estás?

Soy Aina y esto es Think&Hack.

**Esta semana** te enseño cómo montar tu propio sistema RAG sin tocar una línea de código. Y por qué la nueva integración de NotebookLM con Gemini cambia las reglas.

Las empresas grandes usan sistemas RAG para que la IA responda sobre su información interna. Tú puedes tener uno en 5 minutos sin escribir código.

[

![Crea tu RAG con Genimi + NotebookLM](https://substackcdn.com/image/fetch/$s_!LjCl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F56df0d7e-2a86-4788-be98-42ee512a36c8_2816x1536.png)

](https://substackcdn.com/image/fetch/$s_!LjCl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F56df0d7e-2a86-4788-be98-42ee512a36c8_2816x1536.png)Crea tu RAG con Genimi + NotebookLM

Diez archivos.

Ese es el límite de los Gems de Gemini. Diez documentos para crear tu “experto personalizado”.

Suena razonable. Hasta que haces cuentas:

-

Documentación de un proyecto: 15-20 archivos

-

Transcripciones de reuniones del trimestre: 12+

-

Informes mensuales, manuales, ese PDF de onboarding que nadie encuentra...

**De repente diez es nada.**

```
**Y ahí está el problema: **llevas meses copiando y pegando fragmentos de documentos en ChatGPT esperando que los recuerde. No los recuerda. Nunca los recordará.
```

---

Hasta ahora tenías dos opciones separadas:

-

**Gems de Gemini:** instrucciones personalizadas + máximo 10 archivos. Perfecto para tareas repetitivas con contexto pequeño.

-

**NotebookLM:** 50 fuentes gratis, 300 con el plan de pago (600 con Ultra). Análisis profundo pero encerrado en su propia interfaz.

En diciembre, Google lanzó algo que nadie explicó bien: ahora puedes conectar NotebookLM directamente con Gemini.

[

![RAG NotebookLM+Gemini](https://substackcdn.com/image/fetch/$s_!tVHG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3fb1e926-1be4-44f7-b667-5a6b224e3807_2816x1536.png)

](https://substackcdn.com/image/fetch/$s_!tVHG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3fb1e926-1be4-44f7-b667-5a6b224e3807_2816x1536.png)RAG NotebookLM+Gemini

Trescientos documentos. En tu chat de Gemini. Sin configurar nada.

---

NotebookLM hace algo que ChatGPT o Claude no hacen por defecto: no inventa. Si la respuesta no está en tus documentos, te lo dice. Punto. Sin alucinar. [Aquí expliqué cómo usarlo sin delegar tu pensamiento crítico](https://ainalluna.substack.com/p/2-notebooklm-lee-por-ti-ese-es-el).

Funciona así:

1.

Subes archivos (PDFs, webs, Google Docs, YouTube …)

2.

NotebookLM los trocea e indexa

3.

Cuando preguntas, recupera solo los trozos relevantes

```
**Eso es un RAG. Retrieval-Augmented Generation**. La arquitectura que usan las empresas grandes para que la IA responda sobre su información interna.
```

Solo que aquí no necesitas ingenieros. Solo arrastrar archivos.

---

Mi flujo real:

**Análisis puntual:**

1.

Crear notebook con todas las fuentes del proyecto

2.

Dejar que procese e indexe

3.

Desde Gemini → adjuntar el notebook al chat

4.

Preguntar combinando notebook + inteligencia de Gemini

**Consultas recurrentes:**

1.

Crear un Gem con instrucciones de tono y enfoque

2.

Exportar conclusiones clave de NotebookLM a Google Doc

3.

Añadir ese Doc como conocimiento del Gem

4.

Usar el Gem para consultas rápidas con contexto destilado

---

Imagina un notebook con todos los manuales de tu equipo, procesos de onboarding, guías de estilo, protocolos de cliente.

Tu equipo pregunta: *“¿Cómo entregamos un proyecto al cliente?”*

Respuesta exacta. Con referencia al documento original.

Pasas de buscar en una wiki a preguntar directamente. Con la fuente incluida.

---

Una limitación importante: Gemini ve las fuentes de tu notebook, no tus conversaciones anteriores con esas fuentes.

Si pasaste horas refinando un análisis en NotebookLM, Gemini no hereda ese trabajo. Solo ve los documentos originales.

La solución: exporta tus conclusiones a un Google Doc y añádelo como fuente adicional.

---

La pregunta no es si necesitas un sistema RAG.

La pregunta es cuánto tiempo vas a seguir copiando y pegando fragmentos de documentos en ChatGPT esperando que los recuerde.

NotebookLM no es perfecto. La integración solo funciona en web. Y sí, tienes que dedicar tiempo a organizar tus fuentes.

Pero es la forma más accesible de tener tu propio sistema de conocimiento con IA. Sin código. Sin infraestructura. Sin equipo técnico.

¿Ya lo has probado?

**Links:**

-

[NotebookLM](https://notebooklm.google.com/)

-

[Gems de Gemini](https://support.google.com/gemini/answer/14575153)

-

[Integración NotebookLM + Gemini](https://blog.google/technology/ai/notebooklm-gemini-integration/)

***Cuéntamelo. Siempre leo todo.***

![imagen](https://substackcdn.com/image/fetch/$s_!jAJ6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa6a28f5-efe2-4efb-93bc-87d726ddd0ec_56x56.png)

[Compartir](https://ainalluna.substack.com/p/gestion-memorias-llm?utm_source=substack&utm_medium=email&utm_content=share&action=share&token=eyJ1c2VyX2lkIjoxMzYyMjA1NDIsInBvc3RfaWQiOjE4MzY0NDA5MSwiaWF0IjoxNzY3ODg1MjYyLCJleHAiOjE3NzA0NzcyNjIsImlzcyI6InB1Yi01MTQzODkzIiwic3ViIjoicG9zdC1yZWFjdGlvbiJ9.ogb8FPT6dWkMpWFfH-NtxDdmKgVruaXNZy3s8XJ1tSo)

**Recomienda Think&Hacks**

Soy Aina. Responsable de IA generativa en Planeta.

Tres cosas rápidas:

1.

🔄 **Comparte:** Reenvía esto a quien siga confiando ciegamente en la memoria de ChatGPT.
💬 **Responde:** ¿Usas archivos de contexto externos? ¿Qué sistema tienes?
📩 **Suscríbete:** Si te han reenviado esto, [únete aquí](https://ainalluna.substack.com/)

¡Gracias por leer Think & Hack! Suscríbete gratis para recibir nuevos posts y apoyar nuestros trabajo.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)

**PS:** Si montas tu primer notebook esta semana, cuéntame qué tal. Me interesa saber qué casos de uso encuentras. Y si aún no conoces NotebookLM, [empieza por aquí](https://ainalluna.substack.com/p/2-notebooklm-lee-por-ti-ese-es-el).
