---
id: 184848409
titulo: "Think&Hack #18 — Lo que nadie explica de Nano Banana Pro"
subtitulo: "Gemini 3 Pro razona antes de renderizar. Te muestro cómo estructurar prompts para que el modelo piense, no adivine."
fecha: 2026-01-21
url: https://ainalluna.substack.com/p/nano-banana-pro-prompts
tipo: newsletter
audiencia: everyone
estado: completo
huella: 1ff3dd705381ed39dce0db8c2c664df58a12ad249c046458160c33be339cbdbf
---

## ¿Cómo estás?

Soy Aina y esto es Think&Hack.

**Esta semana** te cuento cómo funciona **Nano Banana Pro**, por qué es estructuralmente diferente a los modelos anteriores, y el patrón que uso para que entienda exactamente qué quiero.

Los generadores de imagen han evolucionado en dos años más que en la década anterior. Pero el salto no es de calidad visual. Es de comprensión.

[

![cómo funciona Nano Banana Pro](https://substackcdn.com/image/fetch/$s_!b4D2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc1ce15d-caa3-43e7-b596-2faf5459962f_2816x1536.png)

](https://substackcdn.com/image/fetch/$s_!b4D2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc1ce15d-caa3-43e7-b596-2faf5459962f_2816x1536.png)cómo funciona **Nano Banana Pro**

Antes la generación de imágenes funcionaba así: describes lo que quieres, el modelo adivina, generas veinte variaciones, eliges la menos mala.

El problema no era la calidad técnica. Era que el modelo no entendía tu intención. Solo hacía match de palabras con patrones visuales.

---

[

![Cómo funciona nano banana pro](https://substackcdn.com/image/fetch/$s_!16DS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fefc3db38-0bda-4a4f-8279-674628416f91_2816x1536.png)

](https://substackcdn.com/image/fetch/$s_!16DS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fefc3db38-0bda-4a4f-8279-674628416f91_2816x1536.png)Cómo funciona nano banana pro

Nano Banana Pro está construido sobre **Gemini 3 Pro** (modelo `gemini-3-pro-image-preview`). No es un generador de “imágenes bonitas”. Es un modelo que **planifica la escena antes de renderizarla**, usa el modo “Thinking” para razonar sobre composición, física de luz y relaciones entre objetos.

```
**Dónde usarlo:** Gemini app (selecciona “Create Image” + modelo “Thinking”), Google Slides, AI Studio, Adobe Firefly, Photoshop, Figma, Canva, NotebookLM.
```

---

Antes de darte el patrón, necesitas saber qué dejar de hacer.

**Olvídate de:**

-

“4K, masterpiece, trending on artstation” — ruido que el modelo ignora

-

Listas interminables de adjetivos — menos es más

-

Prompts vagos tipo “una imagen profesional” — necesita especificidad

**Limitaciones reales:**

-

Caras pequeñas o distantes pueden salir deformes

-

Ortografía en textos largos requiere revisión manual

-

Ediciones de iluminación extrema (día a noche) no funcionan bien

-

Datos numéricos en infografías: verificar siempre

-

Todas las imágenes llevan watermark SynthID (invisible pero detectable)

---

## **El patrón SCIER: la estructura que sí funciona**

Las IA de Google revelan un patrón que nadie está explicando bien. Lo llamo SCIER:

```
**[S]**ujeto = adjetivos + qué quieres en la imagen
**[C]**omposición = tipo de plano
**[I]**luminación = luz, hora visual
**[E]**stilo = estética que buscas
**[R]**atio = ratios específicos, límites
```

**Ejemplo aplicado:**

```
Professional woman in her 40s working on a laptop (SUJETO);
in a modern coffee shop interior with exposed brick and large windows (COMPOSICIÓN);
soft natural lighting from the left, shallow depth of field (ILUMINACIÓN);
photorealistic style, editorial photography look (ESTILO);
16:9 aspect ratio, upper body shot for thumbnail (RATIO)
```

---

## **Vocabulario útil por categoría**

**Ángulos de cámara:**

-

POV shot / first person view — perspectiva del espectador

-

bird’s eye view — desde arriba

-

Dutch angle — inclinado

-

extreme close-up / macro — detalle

-

isometric view — 3D sin distorsión de perspectiva

**Iluminación:**

-

golden hour, blue hour, harsh midday sun

-

dramatic chiaroscuro, rim lighting

-

volumetric fog, neon glow

**Estilos:**

-

photorealistic, cinematic

-

flat design, vector art

-

concept art, matte painting

**Ratios:**

-

16:9 — presentaciones, vídeos

-

9:16 — móvil, stories

-

1:1 — iconos, logos

---

## **Ejemplo de como usar la estructura **SCIER

Quería ver cómo quedaría Think&Hack en Times Square. Antes: Photoshop + horas ajustando perspectiva.

**Lo que usé:**

1.

Foto de Times Square (Google Images)

2.

Logo de Think&Hack

3.

Nano Banana Pro

[

![Crear imágenes en Gemini de Google](https://substackcdn.com/image/fetch/$s_!5AOp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3bb453e3-d116-4c45-bfce-d7559ab59d26_1372x1059.png)

](https://substackcdn.com/image/fetch/$s_!5AOp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3bb453e3-d116-4c45-bfce-d7559ab59d26_1372x1059.png)Crear imágenes en Gemini de Google

---

**Prompt tonto (lo que haría sin pensar):**

```
pon mi logo en times square, que quede profesional y bonito, 4K, realista

```

**El modelo razonó por el (PRO):**

>
>
> *Analyzing Visual Integration* — Integrando visualmente el logo en la pantalla más grande.
>
>
>
> *Integrating Logo Details* — Aplicando textura LED, brillo, contraste. Renderizado final a 4K con detalles fotorrealistas.
>
>
>
> *Verifying Logo Placement* — Confirmando la posición del logo.
>
>

**Resultado:** Logo colocado. Fondo blanco plano. Parece un pegote.

[

![imagen](https://substackcdn.com/image/fetch/$s_!49XE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd47b2d17-f824-4df4-8480-18a4d3c636ad_1344x1745.png)

](https://substackcdn.com/image/fetch/$s_!49XE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd47b2d17-f824-4df4-8480-18a4d3c636ad_1344x1745.png)Ejemplo resultado de un prompt “malo” en nano banana

---

**Prompt con SCIER + razonamiento:**

```
Study image 2.
Subject: Logo from image 1 with tagline "Think first. Hack later."
Composition: Replace the large corner billboard content
Lighting: Match the overcast daylight from the original
Style: Photorealistic, integrated with the billboard surface
Restrictions: Keep all other elements unchanged

```

“Study” mejora el razonamiento del modelo. SCIER da la estructura.

**El modelo pensó antes de ejecutar:**

>
>
> *Focusing on the Scene* — Analizando la escena de Times Square, capturando la esencia del entorno.
>
>
>
> *Analyzing the Advertisement Goal* — Evaluando la necesidad de crear un anuncio para el billboard. Priorizando la integración del logo y tagline.
>
>
>
> *Analyzing Precise Integration* — Confirmando que el contenido del billboard se actualizó según las instrucciones. Verificando que la integración y la iluminación coinciden.
>
>
>
> *Verifying Exact Compliance* — Comprobando que la imagen generada cumple todos los requisitos.
>
>

[

![Ejemplo de un buen prompt en nano banana](https://substackcdn.com/image/fetch/$s_!ULqT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc53201ea-950b-4dbf-a8cf-6979d6e6e574_1344x2289.png)

](https://substackcdn.com/image/fetch/$s_!ULqT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc53201ea-950b-4dbf-a8cf-6979d6e6e574_1344x2289.png)Ejemplo de un buen prompt en nano banana

---

**La lección:**

```
La diferencia no es SI el modelo razona, sino SOBRE QUÉ razona
```

-

Le dije “4K, realista” → razonó sobre resolución y texturas.

-

Le dije “Study” → razonó sobre entender la escena primero.

[

![Diferencia entre los prompts](https://substackcdn.com/image/fetch/$s_!NIFa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5c2162f4-0117-4877-bcbb-4c812fa87e30_2816x1536.png)

](https://substackcdn.com/image/fetch/$s_!NIFa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5c2162f4-0117-4877-bcbb-4c812fa87e30_2816x1536.png)Diferencia entre los prompts

¿Ves el fondo blanco? Yo no lo pedí. Tampoco pedí otro color. El modelo decidió.

Si quieres control total, especifica todo. Si no, el modelo razona y elige por ti.

**La diferencia no es el modelo. Es la estructura del prompt.**

**Cuándo usarlo:**

-

Validar cómo se ve tu marca en un contexto real

-

Presentaciones a cliente: “así quedaría en X ubicación”

-

Probar creatividades antes de comprar el espacio publicitario

**Cuándo NO usarlo:**

-

Si necesitas precisión exacta de la logo (puede distorsionar ligeramente)

-

Material final para producción (watermark SynthID)

-

Cuando la foto del lugar tiene mala calidad (garbage in, garbage out)

---

Nano Banana Pro no es mejor en todo. Las limitaciones están ahí: caras distantes, textos largos, precisión de logos. Pero para ideación rápida, mockups de concepto y trabajo visual iterativo, el salto respecto a lo anterior es real.

**La diferencia no es que genere “mejor”. Es que comprende.**

¿Ya lo has probado? ¿Qué resultados estás teniendo con el patrón SCIER?

Cuéntamelo. Siempre leo todo.

**Links:**

-

[Gemini App](https://gemini.google.com/) — selecciona modelo “Thinking”

-

[AI Studio](https://aistudio.google.com/)

-

[Documentación Nano Banana](https://ai.google.dev/gemini-api/docs/image-generation)

-

[Google DeepMind - Gemini 3 Pro Image](https://deepmind.google/models/gemini-image/pro/)

---

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

**Recomienda Think&Hack**

Soy Aina. Responsable de IA generativa en Planeta.

**Comparte:** Reenvía esto a quien siga escribiendo “4K masterpiece trending on artstation”.
**Responde:** ¿Qué generador de imagen usas? ¿Qué resultados te da?
**Suscríbete:** Si te han reenviado esto, [únete aquí](https://ainalluna.substack.com/)

---

**PS:** Si quieres entender la filosofía de “traducción, no invención” que hay detrás, [aquí expliqué Nano Banana cuando salió](https://ainalluna.substack.com/p/4-y-la-maquina-dibujo-exactamente).

Esto es lo que aprendo aplicando IA cada día. Te lo cuento cada semana.
