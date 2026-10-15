---
id: 183130708
titulo: "#15 Guía prompting GPT-5.2: Lo que cambió en las reglas de OpenAI"
subtitulo: "Lo que funcionaba en GPT-4 ahora no funciona"
fecha: 2026-01-11
url: https://ainalluna.substack.com/p/14-guia-prompting-gpt-52-lo-que-cambio
tipo: newsletter
audiencia: everyone
estado: completo
huella: c41ff339ecd8e56169ff6f4c4a1c68859794a4fb610865804c96df4deae231b9
---

¿Cómo estás?

Soy Aina y esto es Think&Hack.

Esta semana te cuento qué he aprendido leyendo las tres guías oficiales de prompting de OpenAI y **por qué cambian cómo deberías escribir en ChatGPT-5.2.**

Si te interesa lo contraintuitivo, suscríbete para no perderte nada.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)

---

### Tres modelos en cinco meses

[

![Agosto: GPT-5. Noviembre: GPT-5.1. Diciembre: GPT-5.2.](https://substackcdn.com/image/fetch/$s_!D2He!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd2bf6c3-1d16-409a-b2d4-3355b4d108f1_2816x1536.png)

](https://substackcdn.com/image/fetch/$s_!D2He!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd2bf6c3-1d16-409a-b2d4-3355b4d108f1_2816x1536.png)Agosto: GPT-5. Noviembre: GPT-5.1. Diciembre: GPT-5.2.

He leído las guías oficiales del OpenAI Cookbook de los tres. Y hay un patrón que nadie está contando.

```
En agosto, OpenAI recomendaba “incrementar el esfuerzo de razonamiento para tareas complejas”. En diciembre, la recomendación es otra: “el razonamiento por defecto es ninguno. Sé más directo.”
```

Y ahí está el problema:

**Los modelos son más capaces, pero necesitan instrucciones más limpias. No más largas. Más limpias.**

---

### Lo que OpenAI quiere que dejes de hacer

Hay frases que funcionaban en GPT-4 que ahora son ruido. Literalmente. La guía oficial dice que GPT-5.2 considera “noise” cosas como:

[

![Prompts anticuados](https://substackcdn.com/image/fetch/$s_!Knwd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83a8c509-ad85-4785-b412-da35bf6957b3_2816x1536.png)

](https://substackcdn.com/image/fetch/$s_!Knwd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83a8c509-ad85-4785-b412-da35bf6957b3_2816x1536.png)Prompts anticuados

```
El modelo ya no necesita que le des ánimos. **Necesita que le des especificaciones.**
```

---

### Prompting en GPT-5.2: el patrón CTCO

Las guías revelan un patrón que están usando internamente:

```
**C**ontexto: Quién eres (rol específico, no genérico)
**T**area: Qué quieres (una acción concreta)
**C**onstricciones: Qué NO hacer (límites explícitos)
**O**utput: Qué formato esperas
```

Ejemplo real:

```
**CONTEXTO:**
Eres un analista de datos especializado en retail con experiencia en patrones de consumo estacional.
**TAREA:**
Analiza estos datos de ventas de Q4.
**CONSTRICCIONES:**
- No incluyas introducción ni resumen final
- No uses más de 5 bullets
- No menciones limitaciones del análisis
**OUTPUT:**
Lista los 3 patrones más relevantes. Para cada uno: qué es, por qué importa, qué harías.
```

El rol se queda. El padding desaparece.

---

### Cómo usar GPT-5.2 en ChatGPT

En ChatGPT tienes tres modos de GPT-5.2:

[

![ tres modos de GPT-5.2:](https://substackcdn.com/image/fetch/$s_!CVkK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff1a65124-4f00-437c-9296-a744b21b2b20_2816x1536.png)

](https://substackcdn.com/image/fetch/$s_!CVkK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff1a65124-4f00-437c-9296-a744b21b2b20_2816x1536.png) tres modos de GPT-5.2:

```
El modo hace el trabajo de razonamiento. Tu prompt hace el trabajo de especificación.
```

**No le pidas que piense más. Dile exactamente qué quieres.**

---

### Por qué esto importa

Cada tres meses cambian las herramientas. Pero el principio aquí es duradero:

Los modelos más avanzados no necesitan más instrucciones. Necesitan instrucciones sin contradicciones.

“Sé exhaustivo pero breve” confunde más a GPT-5.2 que a GPT-4. El modelo intenta reconciliar lo irreconciliable y gasta tokens en ello.

```
La próxima vez que escribas un prompt, no añadas. Limpia.
```

¿Has notado diferencia con los nuevos modelos?

### Fuentes oficiales

-

[GPT-5 Prompting Guide - OpenAI Cookbook](https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide)

-

[GPT-5.1 Prompting Guide - OpenAI Cookbook](https://cookbook.openai.com/examples/gpt-5/gpt-5-1_prompting_guide)

-

[GPT-5.2 Prompting Guide - OpenAI Cookbook](https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide)

***Cuéntamelo. Siempre leo todo.***

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

¡Gracias por leer Think & Hack escrito por Aina-Lluna! Suscríbete gratis para recibir nuevos posts y apoyar mi trabajo.
