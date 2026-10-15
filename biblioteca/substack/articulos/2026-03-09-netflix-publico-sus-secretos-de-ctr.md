---
id: 190295495
titulo: "Netflix publicó sus secretos de CTR. Yo los convertí en un asistente de miniaturas."
subtitulo: "Robé las reglas de CTR de Netflix. La IA hizo el resto."
fecha: 2026-03-09
url: https://ainalluna.substack.com/p/netflix-publico-sus-secretos-de-ctr
tipo: newsletter
audiencia: everyone
estado: completo
huella: fdcf5b9d6757ff490e4039b9a707d4de848777c078f60190111caa552771042a
---

[

![imagen](https://substackcdn.com/image/fetch/$s_!fO7e!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F224cd6b9-1238-4c97-8b07-bf1e4182c781_2816x1536.png)

](https://substackcdn.com/image/fetch/$s_!fO7e!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F224cd6b9-1238-4c97-8b07-bf1e4182c781_2816x1536.png)

¿Cómo estás?

Soy Aina y esto es Think&Hack.

Netflix ha gastado millones en responder una pregunta: **¿qué imagen te hace conseguir más clics? **No lo guardó en secreto. Lo publicó en cuatro artículos técnicos en su blog de ingeniería. Con datos de 200 millones de usuarios. Con resultados de miles de tests A/B. **Con reglas concretas sobre qué funciona y qué no en una portada.**

El problema es que son artículos densos, técnicos, y largos. Nadie los lee.

**Yo sí los leí.** Y lo que encontré dentro era demasiado valioso para dejarlo en un PDF. Así que hice lo que mejor sé hacer: **cogí ese conocimiento y lo convertí en una herramienta.**

---

### El contenido que nadie aprovecha

Esto es lo que Netflix descubrió y publicó abiertamente:

-

Los rostros con emociones extremas generan entre un 25% y un 40% más de clics que las caras neutras.

-

Las imágenes con más de 3 elementos visuales pierden rendimiento en pantallas pequeñas.

-

El conflicto visual supera a la armonía en engagement.

-

La personalización de portadas por segmento de audiencia multiplicó su tasa de conversión.

Reglas concretas. Probadas con tests A/B a escala masiva. Publicadas gratis.

El problema no es acceder a este conocimiento. El problema es convertirlo en algo que puedas usar.

### Cómo lo hice

Primero leí los cuatro artículos. Los enlaces están al final; léelos tú también, tienen oro dentro. Entender qué dicen es la mitad del trabajo. La otra mitad es transformar eso en algo práctico.

**Para esa segunda mitad usé a Gemini.**

#### **Paso 1:** Leer los artículos

No por encima. Leerlos de verdad. Necesitas saber qué contienen para poder evaluar si la IA ha hecho un buen trabajo después. Si no lees la fuente, no puedes validar el resultado.

 Los cuatro artículos son estos:

1.

Selecting the best artwork for videos through A/B testing

2.

Artwork Personalization at Netflix

3.

Discovering Creative Insights in Promotional Artwork

4.

Netflix Artwork Personalization via LLM Post-training

#### **Paso 2:** Darle a la IA el trabajo pesado.

Una vez que entiendes qué hay dentro, le pasas los artículos a Gemini con un prompt estructurado. El prompt hace cinco cosas:

1.

Extrae todas las reglas accionables de los artículos. Solo las que se pueden aplicar. Nada de historia ni explicaciones de algoritmos.

2.

Investiga las especificaciones técnicas de YouTube: resolución, aspect ratio, zonas seguras, overlays.

3.

 Razona las diferencias entre Netflix y YouTube. No todo aplica directamente. La IA tiene que pensar qué comparten ambas plataformas y qué no.

4.

 Genera las instrucciones completas de un asistente listo para copiar y pegar.

 Este es el prompt que usé:

```
Voy a pegarte uno o varios artículos técnicos de una empresa.
Quiero que hagas TODO el trabajo para convertir esa
información en un asistente personalizado (Gem de Gemini).

MI OBJETIVO:
[Crear miniaturas para YouTube que maximicen el CTR
(Click-Through Rate).]

LO QUE NECESITO QUE HAGAS TÚ:

1. LEE los artículos que te paso y extrae todas las reglas,
   principios y criterios de diseño accionables.
   Solo las reglas que se puedan aplicar directamente.
   No quiero contexto, historia ni explicaciones técnicas
   de algoritmos.

2. INVESTIGA las especificaciones técnicas de las miniaturas
   de YouTube: resolución, aspect ratio, formatos aceptados,
   peso máximo, safe zones para texto, zonas que YouTube
   ocupa con overlays (duración, etc.), tamaño mínimo
   recomendado para rostros.

3. RAZONA cómo adaptar las reglas del artículo a YouTube.
   No todas las reglas de Netflix aplican directamente.
   Piensa qué comparten ambas plataformas (cuadrícula
   de miniaturas, competencia visual) y qué es diferente
   (YouTube tiene texto en miniatura, tiene overlays,
   el usuario ve el título al lado de la imagen).

4. GENERA las instrucciones completas de un asistente
   (Gem de Gemini) que:
   - Genera miniaturas de YouTube aplicando las reglas
     adaptadas + specs técnicas
   - Evalúa miniaturas existentes contra esas reglas
   - Pide al usuario la información necesaria antes de
     generar (tema del vídeo, quién sale, foto de referencia,
     audiencia, emoción, texto si lo hay)
   - Estructura internamente el prompt de generación
     de imagen con: sujeto, composición, iluminación,
     fondo, texto, ratio y restricciones
   - Explica qué reglas aplica y cómo impactan en el CTR

FORMATO:
Las instrucciones deben estar listas para copiar y pegar
directamente en el campo "instrucciones" de un Gem
de Gemini. Autocontenidas. Alguien que las lea sin
contexto debe entender qué hace el asistente, para qué
plataforma, qué métrica optimiza y cuál es el flujo
de trabajo completo.

Los artículos, léelos todos:
 1. Selecting the best artwork for videos through A/B testing                                                                    
  https://netflixtechblog.com/selecting-the-best-artwork-for-videos-through-a-b-testing-f6155c4595f6
  2. Artwork Personalization at Netflix (el artículo principal, 2017)
  https://medium.com/netflix-techblog/artwork-personalization-c589f074ad76
  3. Discovering Creative Insights in Promotional Artwork
  https://netflixtechblog.com/discovering-creative-insights-in-promotional-artwork-295e4d788db5
  4. Netflix Artwork Personalization via LLM Post-training
  https://arxiv.org/html/2601.02764v1
```

En el objetivo “Crear miniaturas para YouTube que maximicen el CTR”.

Gemini leyó los artículos y buscó por su cuenta las specs de YouTube: resolución 1280x720, ratio 16:9, dónde va la duración del vídeo, dónde aparecen los iconos en móvil. Razonó las diferencias entre Netflix y YouTube y me devolvió las instrucciones del asistente listas para copiar.

**El prompt final para el Gem que me dio:**

```
Eres "Thumbnail Pro", un asistente avanzado de diseño, copywriting y estrategia especializado en crear y evaluar miniaturas de YouTube con un único objetivo: maximizar el CTR (Click-Through Rate).

Tu lógica de diseño se basa en principios comprobados de A/B testing de plataformas como Netflix (emoción, enfoque en personajes, conflicto), adaptados rigurosamente a la interfaz, comportamiento del usuario y especificaciones técnicas de YouTube (legibilidad móvil, zonas seguras de interfaz). Tu capacidad principal es generar visuales impactantes que incluyan texto legible y persuasivo directamente en la imagen.

---

### TUS PRINCIPIOS DE DISEÑO (VISUAL + TEXTO INTEGRADO)

Aplica SIEMPRE estos criterios para la generación de la miniatura final:

1. **Rostros y Emoción Extrema (Close-ups):** Los rostros deben estar en primer plano absoluto. Prioriza emociones intensas y complejas (sorpresa salvaje, miedo, conflicto profundo, intriga) por encima de sonrisas neutras. Los ojos deben ser el punto focal principal.

2. **Regla de 3 Elementos (< 3 Sujetos):** Nunca satures la imagen. Máximo 1 o 2 sujetos/elementos visuales principales. Fondos simplificados o difuminados para un contraste máximo (Saliencia Visual), asegurando que el sujeto y el texto resalten instantáneamente en tamaños pequeños (móvil).

3. **Conflicto y Tensión:** Si el vídeo lo permite, muestra elementos de antagonismo, peligro o misterio. El conflicto visual rinde mejor que la armonía.

4. **Copywriting Persuasivo y Breve (Texto en Imagen):**
    - **Brevidad Extrema:** El texto debe tener entre 1 y 4 palabras máximo.
    - **Complemento, no repetición:** El texto de la miniatura NUNCA debe ser igual al título del vídeo. Debe actuar como un anzuelo emocional que conecte con el título (ej. Título: "Cómo ganar dinero"; Texto Miniatura: "¿ES ESTO LEGAL?").
    - **Palabras Gatillo:** Usa palabras que disparen curiosidad, urgencia o controversia.

5. **Legibilidad y Composición (Zonas Seguras YT):**
    - **Ubicación del Texto:** Coloca el texto en la zona izquierda o centro-izquierda de la miniatura.
    - **Ubicación del Sujeto/Rostro:** Coloca el sujeto/rostro en el centro o centro-derecha.
    - **Zona de Peligro (Inferior Derecha):** La esquina inferior derecha ESTÁ PROHIBIDA para texto o información clave del rostro (ojos/boca), ya que será tapada por la marca de tiempo de YouTube. Mantén esta zona limpia o oscura.
    - **Estilo de Texto:** El texto debe ser masivo, ultra-grueso (bold sans-serif) y en colores de alto contraste (blanco o amarillo sobre fondos oscuros, o con contorno/sombra gruesa).

6. **Especificaciones Técnicas:** Ratio 16:9 estricto.

---

### TU FLUJO DE TRABAJO COMPLETO

Cuando un usuario interactúe contigo, debes guiarlo ESTRICTAMENTE por este proceso:

**PASO 1: Recopilación de Información (Pregunta al usuario si no te ha dado los datos)**
Necesitas estos datos obligatoriamente:
- Título provisional del vídeo:
- Tema/Contenido del vídeo (breve):
- Audiencia objetivo:
- ¿Quién sale? (Sujeto, objeto o persona obligatoria):
- Emoción principal a transmitir:

**PASO 2: Propuesta de Copy (Texto Corto)**
Basado en la información del Paso 1, proponle al usuario 3 opciones de texto corto (1-4 palabras) para la miniatura. Pide al usuario que elija UNA opción.

**PASO 3: Generación de Imagen con Texto Integrado**
Una vez que el usuario elija un texto (ej. "¡EL GRAN ERROR!"), genera la miniatura final invocando internamente el siguiente prompt estructurado en inglés (adaptando los detalles):

"16:9 aspect ratio. Youtube thumbnail.
[Texto Integrado]: The exact words "[INSERTA EL TEXTO ELEGIDO]" must be rendered in massive, ultra-bold, thick sans-serif typography, highly legible for small screens. Text positioned on the left third of the image. The text color is bright yellow with a thick black outline and drop shadow for maximum contrast.
[Sujeto]: Extreme close-up of [Sujeto], face dominating the center-right side, looking towards viewer, intensely expressive showing [Emoción]. Deep detail in eyes.
[Composición]: Subject on the right, huge text on the left. The composition is clean with a powerful focus on these two points. Empty safe negative space in the bottom right corner (for YouTube overlay).
[Iluminación]: High contrast cinematic lighting, dramatic rim lighting separating the subject from the background.
[Fondo]: Highly blurred, simple environment hinting at [Contexto del vídeo] but non-distracting.
[Estilo]: Vibrant colors, high salience, hyper-realistic, designed for maximum click-through rate."

*Aviso que debes dar al usuario junto con la imagen:* "He generado la miniatura final incluyendo el texto acordado. Por favor, verifica que la IA ha escrito las palabras correctamente, ya que a veces puede haber pequeños fallos ortográficos en el renderizado tipográfico. Si hay un error, dímelo y la regenero."

**PASO 4: Explicación Estratégica**
Finalmente, explica brevemente:
1. Por qué elegiste esa composición exacta y esa expresión emocional.
2. Cómo el texto interactúa psicológicamente con el título para forzar el clic.
3. Por qué has respetado las zonas seguras.

Tu tono debe ser directo, experto, analítico y enfocado 100% en el rendimiento y la conversión.
```

#### Paso 3: Crear el Gem

Gemini leyó los artículos, investigó por su cuenta las specs de YouTube, resolución 1280x720, ratio 16:9, dónde va la marca de tiempo, dónde aparecen los iconos en móvil y me devolvió las instrucciones del asistente listas para copiar.

```
Crear el Gem es lo más rápido: Explorar Gems → Nuevo Gem → pegar instrucciones → Guardar.
```

Todo el proceso, desde que empecé a leer hasta que tuve el asistente funcionando, fueron veinte minutos.

[

![imagen](https://substackcdn.com/image/fetch/$s_!Sa6n!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fda95ce03-22fc-45ec-b807-437a5cc54a3b_1037x813.png)

](https://substackcdn.com/image/fetch/$s_!Sa6n!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fda95ce03-22fc-45ec-b807-437a5cc54a3b_1037x813.png)Crear el Gem con Gemeni y nano banan

### ¿Qué hace el asistente?

El Gem trabaja de dos formas.

**Generar.** Le dices de qué va el vídeo, quién sale, qué emoción quieres transmitir. Te propone tres opciones de texto corto para la miniatura. Eliges una. Te genera la imagen aplicando las reglas de Netflix adaptadas a YouTube: close-up de rostro, emoción extrema, fondo difuminado, texto masivo en la zona izquierda, esquina inferior derecha limpia.

Le pedí una miniatura para un vídeo sobre por qué prohibí la IA en mis sesiones de brainstorming. Me devolvió un close-up de una directiva con expresión de frustración, un holograma de IA desenfocado al fondo y tres palabras de texto a la izquierda.

[

![imagen](https://substackcdn.com/image/fetch/$s_!sB24!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F429665cc-bb1f-42ed-abd2-fe688d57a23e_2752x1536.png)

](https://substackcdn.com/image/fetch/$s_!sB24!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F429665cc-bb1f-42ed-abd2-fe688d57a23e_2752x1536.png)Ejemplo de miniatura

Y me explicó por qué: “Las expresiones de tensión superan en un 25-40% de CTR a las caras neutras, según los tests de Netflix. El holograma de IA actúa como el ‘villano’ que genera tensión visual.”

** Evaluar.** Le subes una miniatura que ya tengas. La analiza contra las reglas y te dice qué falla.

 Le pasé una miniatura de un vídeo de SEO. El diagnóstico:

-

 14 palabras de texto. Nadie lee eso en un móvil.

-

 La expresión es pasiva. No transmite urgencia.

-

 El texto inferior está donde YouTube pone la duración. Va a ser ilegible.

-

 Sugerencia: Aumenta el tamaño del rostro, cambia la expresión a sorpresa, elimina el texto secundario.

Le pedí que la regenerara. Me devolvió una miniatura con un close-up, expresión de sorpresa y tres palabras. Todo lo contrario a la original.

[

![imagen](https://substackcdn.com/image/fetch/$s_!LwgE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec3d25a3-972f-47ff-a412-8685f37f150c_2752x1536.png)

](https://substackcdn.com/image/fetch/$s_!LwgE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec3d25a3-972f-47ff-a412-8685f37f150c_2752x1536.png)

### Lo que de verdad importa aquí

La mayoría de personas usa la IA para generar cosas desde cero. Yo la uso para algo distinto: **coger contenido de calidad que ya existe y hackearlo para convertirlo en una herramienta.**

Netflix invirtió millones en investigar qué te hace clic. Publicó los resultados. El conocimiento estaba ahí, accesible, gratuito. Lo único que faltaba era alguien que lo leyera, entendiera su valor y usara la IA para hacer el trabajo pesado de transformarlo en algo aplicable.

Ese es el Think. Y ese es el Hack.

El prompt funciona con cualquier artículo y cualquier plataforma. Pero eso te lo cuento otro día.

¿Has probado a crear el Gem? ¿O tienes artículos técnicos que llevas tiempo queriendo convertir en algo útil?

---

**Si quieres saber más sobre Nano Banana**

**Links:**

-

[Selecting the best artwork for videos through A/B testing](https://netflixtechblog.com/selecting-the-best-artwork-for-videos-through-a-b-testing-f6155c4595f6)

-

[Artwork Personalization at Netflix](https://medium.com/netflix-techblog/artwork-personalization-c589f074ad76)

-

[Discovering Creative Insights in Promotional Artwork](https://netflixtechblog.com/discovering-creative-insights-in-promotional-artwork-295e4d788db5)

-

[Netflix Artwork Personalization via LLM Post-training](https://arxiv.org/html/2601.02764v1)

-

[Crear un Gem en Gemini — Google](https://gemini.google/overview/gems/)

***Cuéntamelo. Siempre leo todo.***

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

**Recomienda Think&Hack**

Soy Aina. Responsable de IA generativa en Planeta.

**Comparte:** Reenvía esto a quien haga videos de YouTube y quiera aumentar su CTR
**Responde:** ¿Cómo crear las miniaturas de YouTube?
**Suscríbete:** Si te gusta este tipo de contenido, [únete aquí](https://ainalluna.substack.com/). 👇

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
