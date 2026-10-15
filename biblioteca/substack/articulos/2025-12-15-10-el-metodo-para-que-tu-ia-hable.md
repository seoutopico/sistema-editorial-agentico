---
id: 181575255
titulo: "#10 El método para que tu IA hable como tú"
subtitulo: "Parte 2 creando tu identidad"
fecha: 2025-12-15
url: https://ainalluna.substack.com/p/10-el-metodo-para-que-tu-ia-hable
tipo: newsletter
audiencia: everyone
estado: completo
huella: 9625e4326bddac374f118802d9c38cf6e78e1e6ec2c2eb674fe0518294f72719
---

¿Cómo estás?

Soy Aina y esto es Think&Hack.

La semana pasada expliqué por qué borré la memoria de ChatGPT.

-

**El problema: **la memoria nativa amplifica el sesgo complaciente.

-

**La solución:** sustituirla por archivos de contexto que tú controlas.

Recibí bastantes mensajes. Y había un patrón claro.

**“Vale, lo entiendo. Pero... ¿Cómo creo esos archivos exactamente?”**

Hoy te doy el primer archivo: tu ADN Verbal.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)

---

📚 **Esta es la parte 2 de 5 de la serie “Sistema de escritura con IA”**

1.

 [Por qué borré la memoria de ChatGPT](https://ainalluna.substack.com/p/borrar-memoria-chatgpt) ← Reset

2.

 ** [El método para que tu IA hable como tú](https://ainalluna.substack.com/p/10-el-metodo-para-que-tu-ia-hable) ← Voz**

3.

 [Para quién escribe tu IA](https://ainalluna.substack.com/p/11-para-quien-escribe-tu-ia-si-no) ← Audiencia

4.

 [Cómo entreno a ChatGPT para mi negocio](https://ainalluna.substack.com/p/perfil-negocio-chatgpt) ← Negocio

5.

 [Proyectos en ChatGPT: El sistema completo](https://ainalluna.substack.com/p/proyectos-chatgpt-sistema) ← Integración

---

[

![El método para que tu IA hable como tú](https://substackcdn.com/image/fetch/$s_!ful2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48ce5760-628a-4446-9da3-6618f5720999_2816x1536.png)

](https://substackcdn.com/image/fetch/$s_!ful2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48ce5760-628a-4446-9da3-6618f5720999_2816x1536.png)El método para que tu IA hable como tú

---

## Lo que no quedó claro

En la newsletter #9 hablé de crear “archivos .md por categoría” (Perfil base, Estado actual, Base de conocimiento, Historial).

El concepto era correcto. La ejecución, demasiado abstracta.

Aquí está el problema: esas categorías son útiles para organizar información general sobre ti. Pero si lo que quieres es que la IA escriba como tú, necesitas algo más específico.

Necesitas un **ADN Verbal**.

No es un perfil genérico de “quién eres”. Es un análisis estructurado de cómo suenas cuando escribes: tu tono, tu ritmo, tus frases recurrentes, lo que nunca dirías.

**La diferencia:**

[

![ADN Verbal](https://substackcdn.com/image/fetch/$s_!efUC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84326288-d746-4000-b76c-4654a3761ac2_794x246.png)

](https://substackcdn.com/image/fetch/$s_!efUC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84326288-d746-4000-b76c-4654a3761ac2_794x246.png)**ADN Verbal**

El perfil genérico le dice a la IA qué pensar.
El ADN Verbal le dice cómo sonar.

## Qué vas a crear

Un archivo JSON estructurado con:

-

**Tu esencia**: Quién eres como comunicador, no tu cargo

-

**Tu tono**: Formal, cercano, técnico, accesible... y en qué proporción

-

**Tus patrones**: Cómo estructuras ideas, cómo transicionas, cómo enfatizas

-

**Tus frases**: Las que usas siempre, las que nunca usarías

-

**Tus límites**: Lo que NUNCA suenas (esto es crítico para evitar output genérico)

```
**¿Por qué JSON y no texto normal?** Porque la estructura fuerza precisión. “Soy directa” es vago. Un array de frases que usas realmente es concreto. La IA puede trabajar con datos específicos, no con descripciones vagas.
```

---

## Lo que necesitas antes de empezar

**3-5 piezas de tu mejor escritura.**

No cualquier cosa que hayas escrito. Tu mejor trabajo. El contenido donde piensas “esto suena exactamente como yo”.

Pueden ser:

-

Newsletters o artículos de blog

-

Posts de LinkedIn que funcionaron bien

-

Emails importantes que escribiste con cuidado

-

Documentos internos donde tu voz es clara

Cópialos en documentos separados o tenlos listos para subir.

---

## El prompt

Copia esto en ChatGPT 5.2 (recomiendo usar el modelo “Thinking” para este tipo de análisis estructurado):

```
Necesito que analices mis muestras de escritura y crees un perfil Voice DNA en formato JSON.

Voy a subir 3-5 piezas de mi escritura. Analízalas en profundidad en estas dimensiones:

**1. Esencia y visión del mundo**
- ¿Quién soy como comunicador?
- ¿Cuál es mi perspectiva fundamental?
- ¿Cómo me posiciono ante mi audiencia?

**2. Paleta emocional**
- ¿Qué emociones expreso con más frecuencia?
- ¿Cuál es mi rango emocional?

**3. Arquitectura de frases**
- ¿Cuáles son mis patrones típicos de frase?
- ¿Cómo creo ritmo?
- ¿Cómo transiciono entre ideas?

**4. Patrones de voz**
- ¿Cómo estructuro mis pensamientos?
- ¿Qué frases uso repetidamente?
- ¿Cómo enfatizo puntos importantes?

**5. Características de tono**
- ¿Formal o casual?
- ¿Técnico o accesible?
- ¿Cómo mezclo registros?

**6. Rasgos únicos**

- ¿Qué hace mi voz distintivamente mía?
- ¿A qué NUNCA sueno?

Después del análisis, crea un archivo JSON con esta estructura:

{

  “_meta”: {
    “tipo”: “perfil_voz”,
    “actualizado”: “[fecha de hoy YYYY-MM-DD]”
  },

  “identidad_central”: {
    “_instrucciones”: “Quién eres como comunicador - tu esencia, no tu cargo.”,
    “quien_eres”: “[descripción detallada]”,
    “que_haces”: “[cómo comunicas y aportas valor]”,
    “tu_angulo”: “[tu perspectiva única]”
  },

  “personalidad”: {
    “_instrucciones”: “Cómo te perciben - tu energía.”,
    “rasgos”: [”rasgo1”, “rasgo2”, “rasgo3”],
    “energia”: “[descripción de tu energía comunicativa]”
  },

  “tono”: {
    “_instrucciones”: “La sensación que transmite tu escritura.”,
    “tono_principal”: “[descripción]”,
    “tono_secundario”: “[descripción]”,
    “nivel_formalidad”: “[1-10 con descripción]”
  },

  “estilo_comunicacion”: {
    “_instrucciones”: “Cómo estructuras y entregas ideas.”,
    “longitud_frases”: “[cortas/largas/mixtas con descripción]”,
    “estilo_parrafos”: “[descripción]”,
    “usa_preguntas”: true/false,
    “usa_listas”: true/false,
    “progresion_ideas”: “[cómo desarrollas argumentos]”
  },

  “frases_caracteristicas”: {

    “_instrucciones”: “Palabras y frases que usas naturalmente.”,
    “frases_apertura”: [”frase1”, “frase2”, “frase3”],
    “frases_transicion”: [”frase1”, “frase2”, “frase3”],
    “frases_enfasis”: [”frase1”, “frase2”, “frase3”],
    “frases_cierre”: [”frase1”, “frase2”, “frase3”]
  },

  “limites_de_voz”: {
    “_instrucciones”: “CRÍTICO: Lo que NUNCA suenas. Esto previene output genérico.”,
    “nunca_suena_como”: [”descripción1”, “descripción2”, “descripción3”],
    “frases_prohibidas”: [”frase1”, “frase2”, “frase3”],
    “temas_que_evita”: [”tema1”, “tema2”, “tema3”]
  },

  “rango_emocional”: {

    “_instrucciones”: “Qué emociones aparecen en tu escritura.”,
    “emociones_principales”: [”emoción1”, “emoción2”, “emoción3”],
    “como_muestras_entusiasmo”: “[descripción]”,
    “como_muestras_frustracion”: “[descripción]”,
    “como_generas_confianza”: “[descripción]”
  },

  “ejemplos”: {

    “_instrucciones”: “Fragmentos que son quintaesencialmente TÚ.”,
    “ejemplo_1”: {
      “texto”: “[cita de tu escritura]”,
      “por_que_es_tu_voz”: “[explicación]”
    },

    “ejemplo_2”: {
      “texto”: “[cita de tu escritura]”,
      “por_que_es_tu_voz”: “[explicación]”
    }
  }
}

Sé específico, no genérico. Captura patrones, no solo palabras. Hazlo accionable para que la IA pueda escribir como yo.
```

![adn-verbal.json](https://substackcdn.com/image/fetch/$s_!fbrQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88b8d78b-8b7a-4a67-bd87-ab764b36b406_3850x900.png)

adn-verbal.json

---

## Paso a paso

**1. Abre ChatGPT**

Ve a [chatgpt.com](http://chatgpt.com). Si tienes cuenta de pago, selecciona GPT-5.2 Thinking en el selector de modelo (es mejor para análisis estructurado).

**2. Pega el prompt**

Copia el prompt de arriba y pégalo en el chat.

**3. Sube tus muestras de escritura**

Arrastra tus 3-5 documentos al chat, o copia y pega el texto directamente después del prompt.

**4. Espera el análisis**

GPT-5.2 Thinking puede tardar 1-2 minutos en analizar todo. Es normal. Está procesando patrones, no solo leyendo.

**5. Revisa el resultado**

Lee el JSON generado. ¿Te reconoces? ¿Captura cómo escribes realmente?

Si algo no encaja, dile: “La sección de [X] no me representa. En realidad yo [descripción]. Ajústalo.”

**6. Guarda el archivo**

Copia el JSON final y guárdalo como adn-verbal.json en algún lugar accesible.

---

## Cómo usarlo

Cuando quieras que ChatGPT escriba como tú:

1.

Abre un chat nuevo (recuerda: memoria desactivada)

2.

Arrastra tu archivo adn-verbal.json al chat

3.

Escribe lo que necesitas

Ejemplo: “Usando mi perfil de voz, escribe un post de LinkedIn sobre [tema].”

```
La IA ya no tiene que adivinar cómo suenas. Tiene un mapa.
```

>
>
> **Siguiente **[Para quién escribe tu IA](https://ainalluna.substack.com/p/11-para-quien-escribe-tu-ia-si-no) ← Audiencia
>
>

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
