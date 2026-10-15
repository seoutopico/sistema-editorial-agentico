---
id: 186168347
titulo: "He conectado ChatGPT con mi WordPress"
subtitulo: "Me propuso un año de contenido en 3 segundos"
fecha: 2026-02-02
url: https://ainalluna.substack.com/p/chatgpt-wordpress-calendario-editorial
tipo: newsletter
audiencia: everyone
estado: completo
huella: d73aaff79455b29aeb604de1d46685674a55305811cc8b9f2d16118574166bf7
---

¿Cómo estás?

Soy Aina y esto es Think&Hack.

Esta semana te cuento cómo hice que ChatGPT leyera mi WordPress y me propusiera un calendario editorial basado en lo que ya tengo publicado.

847 posts. Cero idea de qué hacer con ellos.

[

![He conectado ChatGPT con mi WordPress](https://substackcdn.com/image/fetch/$s_!nM_q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3f48e43d-abb5-4c15-bc1b-3e023723220e_1024x1024.png)

](https://substackcdn.com/image/fetch/$s_!nM_q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3f48e43d-abb5-4c15-bc1b-3e023723220e_1024x1024.png)He conectado ChatGPT con mi WordPress

El otro día estaba mirando un proyecto abandonado. Info-playas.com. Una web de playas españolas que dejé de actualizar hace tiempo.

847 posts. Guías de playas, servicios, accesos. Contenido que en su momento funcionaba y ahora acumula polvo digital.

**Me hice la pregunta obvia: ¿Qué hago con esto?**

Y entonces me acordé de algo que escribí la semana pasada. Que el contenido no se inventa, se extrae. Que cada proyecto terminado tiene al menos cinco ángulos de contenido.

Pero 847 posts. No voy a revisarlos uno a uno.

---

### Y ahí está el problema

La mayoría piensa que necesita más ideas. Lo que necesita es un sistema que lea las que ya tiene.

Tenemos años de contenido acumulado y ninguna forma práctica de analizarlo. Los CMS te dicen cuántas visitas tiene cada post. No te dicen qué patrones hay entre ellos, qué temas nunca desarrollaste del todo, qué contenido podrías actualizar.

**Eso requiere lectura. Análisis. Tiempo que no tenemos.**

O una IA que pueda leerlo por ti.

### Lo que hice

Los GPTs personalizados de ChatGPT tienen algo que mucha gente no conoce: Actions. La capacidad de conectarse con APIs externas.

[

![Acciones ChatGPT](https://substackcdn.com/image/fetch/$s_!s__4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3246e79e-4f7b-4510-afd7-36bf74ff00e4_959x808.png)

](https://substackcdn.com/image/fetch/$s_!s__4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3246e79e-4f7b-4510-afd7-36bf74ff00e4_959x808.png)Acciones ChatGPT

Y WordPress tiene una API REST activada por defecto desde hace años. Tu contenido ya está disponible en formato JSON. Solo hay que conectar los puntos.

Esto es lo que configuré:

![actions_custom_gpts_chatgpt](https://substackcdn.com/image/fetch/$s_!Y8-9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07444b8d-3c48-47c1-80e0-a499f023bc6e_537x204.png)

actions custom gpts chatgpt

### La prueba real

Le pedí a mi GPT: “Busca contenido sobre niños en info-playas.com”.

[

![Resultado wordpress custom gpts chatgpt](https://substackcdn.com/image/fetch/$s_!MEiL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa655599b-02d7-4786-8bdc-79d860265e15_612x803.png)

](https://substackcdn.com/image/fetch/$s_!MEiL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa655599b-02d7-4786-8bdc-79d860265e15_612x803.png)Resultado wordpress custom gpts chatgpt

Ocho posts que había olvidado que existían. Pero lo mejor no es la búsqueda. Es lo que viene después.

El GPT me pregunta: “¿Qué quieres hacer con este contenido?” Y me ofrece: un resumen, un nuevo artículo SEO basado en ellos, reutilizarlos para redes sociales, o fusionar varios en uno solo.

De una búsqueda, un calendario editorial completo. Del archivo que ya tenía.

### Lo que necesitas

No hace falta saber programar. Solo entender dos cosas:

**1. Tu WordPress ya tiene API**

Prueba esto en tu navegador:

https://tudominio.com/wp-json/wp/v2/posts

Si ves un bloque de JSON, ya está funcionando.

**2. El GPT necesita un schema**

Es un archivo que le dice a ChatGPT qué puede pedirle a tu web. Los endpoints, los parámetros, el formato.

El schema completo está en el bonus. Copia, pega, cambia tu dominio.

```
 {
    "openapi": "3.1.0",
    "info": {
      "title": **"[PON TU WEB]** API",
      "description": "API para acceder a posts de **[PON TU WEB]**",
      "version": "1.0.0"
    },
    "servers": [
      {
      **  "url": "https://tudominio.com/wp-json/wp/v2"**
      }
    ],
    "paths": {
      "/posts": {
        "get": {
          "summary": "Listar posts",
          "operationId": "listPosts",
          "parameters": [
            {
              "name": "per_page",
              "in": "query",
              "required": false,
              "schema": {
                "type": "integer",
                "default": 10
              }
            },
            {
              "name": "page",
              "in": "query",
              "required": false,
              "schema": {
                "type": "integer",
                "default": 1
              }
            },
            {
              "name": "_fields",
              "in": "query",
              "required": false,
              "schema": {
                "type": "string",
                "default": "id,title,slug,excerpt,link"
              }
            }
          ],
          "responses": {
            "200": {
              "description": "Lista de posts"
            }
          }
        }
      },
      "/posts/{id}": {
        "get": {
          "summary": "Obtener post por ID",
          "operationId": "getPostById",
          "parameters": [
            {
              "name": "id",
              "in": "path",
              "required": true,
              "schema": {
                "type": "integer"
              }
            },
            {
              "name": "_fields",
              "in": "query",
              "required": false,
              "schema": {
                "type": "string",
                "default": "id,title,content,link"
              }
            }
          ],
          "responses": {
            "200": {
              "description": "Post completo"
            }
          }
        }
      }
    }
  }
```

### Por qué esto importa

La semana pasada hablé de extraer contenido de lo que ya haces. Esta semana lo automatizamos.

El patrón es el mismo. No inventar. Extraer. Pero ahora con una herramienta que puede leer años de archivo en segundos.

Volví a mirar esos 847 posts. Ya no son contenido abandonado. Son materia prima para el próximo año de calendario editorial.

La pregunta no es de qué escribo esta semana. La pregunta es qué tengo que aún no he explotado.

¿Tienes un WordPress lleno de contenido acumulado?

## 📩 ¿Quieres la guía completa?

***Si quieres el paso a paso con capturas para configurar tu GPT (sin tocar código), déjame un comentario con tu caso de uso y te la envío.***

Cuéntamelo. Siempre leo todo.

**Fuentes:**

-

[OpenAI GPT Actions Documentation](https://platform.openai.com/docs/actions/introduction)

-

[WordPress REST API Reference](https://developer.wordpress.org/rest-api/reference/posts/)

---

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

**Recomienda Think&Hack**

Soy Aina. Responsable de IA generativa en Planeta.

**Comparte:** Reenvía esto a quien tenga años de contenido en WordPress acumulando polvo.
**Responde:** ¿Tienes un archivo de posts que no sabes cómo reutilizar? Cuéntame.
**Suscríbete:** Si te han reenviado esto, [únete aquí](https://ainalluna.substack.com/)

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
