---
id: 189540705
titulo: "¿Cómo auditar tu visibilidad en Google AI Overviews?"
subtitulo: "Por fin una herramienta gratuita para saber si la IA de Google te cita."
fecha: 2026-03-02
url: https://ainalluna.substack.com/p/como-auditar-tu-visibilidad-en-google
tipo: newsletter
audiencia: everyone
estado: completo
huella: 15eac8b8f0480b5ff7a09e013f8bc48c8cbacde5eb0c20ad62db9c3c02c73273
---

---

Soy Aina y esto es Think&Hack.

Nuestro objetivo era ser el primero en Google; ahora, ser el primer resultado citado en AI Overviews. Nada ha cambiado, sólo ha cambiado el dónde; tu nuevo objetivo es ser mencionado por AI Overviews y, al final, tener impacto en LLM’s como ChatGPT.

Hoy te voy a explicar no sólo cómo *auditar tu visibilidad en AI Overviews* de Google, sino cómo alcanzarla con una *sencilla estrategia*, todo con *herramientas gratuitas.*

[

![imagen](https://substackcdn.com/image/fetch/$s_!GP7I!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc9926f09-12a6-406b-a83a-482c357cba33_2752x1536.png)

](https://substackcdn.com/image/fetch/$s_!GP7I!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc9926f09-12a6-406b-a83a-482c357cba33_2752x1536.png)

### El problema

Google ya no solo ordena resultados. Ahora genera respuestas. Y cuando las genera, elige a quién citar como fuente.

Ese bloque se llama AI Overview. En España aparece en una de cada cinco búsquedas. Y va a más.

La pregunta que ninguna herramienta me respondía:

-

¿En cuántas de mis keywords aparece ese bloque?

-

¿Me cita Google o cita a otros?

-

¿Quién se está llevando esos slots?

-

¿Cuántas fuentes usa en cada respuesta?

Eso no sale en Search Console. No sale en Semrush. No sale en Ahrefs.

Así que me hice mi propia extensión de Chrome.

Se llama Extractor AI Overviews y hace algo muy simple: buscas una keyword en Google, y si aparece un bloque de IA, la extensión te dice a quién está citando. A ti o a tu competencia.

### ¿Cómo audito mi visibilidad en Google AI Overviews?

**La extensión funciona de dos formas.**

**Mientras navegas.** Buscas en Google como haces siempre. Si la búsqueda activa un AI Overview, el icono de la extensión se ilumina. Lo abres y ves directamente qué webs está citando Google, cuántas fuentes usa y si tu dominio aparece entre ellas. Un clic y se envía al Sheet. Sin interrumpir lo que estabas haciendo.

[

![imagen](https://substackcdn.com/image/fetch/$s_!KWHe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4342f266-28e0-46cd-810e-2de1357f0b5b_1124x638.png)

](https://substackcdn.com/image/fetch/$s_!KWHe!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4342f266-28e0-46cd-810e-2de1357f0b5b_1124x638.png)

**Por lotes.** Exportas tus keywords de Google Search Console, Semrush o donde sea. Las cargas en la extensión, le das a iniciar y ella hace el trabajo.

[

![imagen](https://substackcdn.com/image/fetch/$s_!Rt_n!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fadf24c82-4dea-4891-ae19-d145771d6fd6_1920x1032.png)

](https://substackcdn.com/image/fetch/$s_!Rt_n!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fadf24c82-4dea-4891-ae19-d145771d6fd6_1920x1032.png)

Cuando termina, tienes el mapa completo en una Google Sheet. Auditoría hecha. Gratis. Ahora toca actuar.

De un vistazo sabes: qué porcentaje de tus keywords activan AI Overview, en cuáles te cita Google, en cuáles cita a tu competencia y a ti no, y quién se repite como fuente.

Las keywords donde aparece AI Overview, pero no te cita, son las **oportunidades**. Ahí es donde te **falta contenido o el que tienes no sirve.**

### **¿Qué hago con eso?**

El Sheet te deja dos grupos claros:

-

**Keywords donde apareces citado** → estás dentro. No toques nada.

-

**Keywords donde aparece AI Overview pero cita a tu competencia y no a ti** → esas son tus oportunidades. Abre las URLs que cita Google, mira qué tienen ellos que no tienes tú y crea o mejora tu contenido.

Si quieres ir un paso más allá, los datos de la Sheet los puedes pasar por un GPT personalizado (Analista SEO para AI Overviews) que te dice exactamente qué tipo de contenido está citando Google, qué te falta para entrar y cómo atacar a tu oportunidad.

**Ejemplo resultado de GPT personalizado. 👇**

```
## 🔍 Query: que libro leer de fantasia en 2026
### Intención: informacional (recomendaciones) con matiz comercial | Complejidad: media (comparativa + selección)

---

## 📊 Resumen del AIO
- **Palabras**: 241 (vs media ~169) → AIO *más largo de lo normal*
- **Fuentes citadas**: 3 (vs media ~7,2) → pocas fuentes, pero muy concentradas en UGC
- **Estructura**:
  - 1 bloque de **párrafo-resumen** con varios títulos + meses de publicación
  - seguido de una **cadena de “tarjetas”**: título de TikTok, título del hilo de Reddit y fecha
  - No hay listas claras tipo bullet; mezcla resumen + metadatos de las tarjetas

### Fan-out potencial (sub-queries que Google probablemente generó)
Para responder a “qué libro leer de fantasía en 2026”, el sistema parece haber descompuesto en cosas como:

- “most anticipated fantasy books 2026”
- “fantasy book releases january 2026”
- “romantasy 2026 tiktok recommendations”
- “libros más esperados de fantasía 2026 reddit”
- “red god pierce brown release date 2026”
- “novedades romantasy 2026 en español”
- “dark fae romantasy books 2026”

### Idioma y mercado
- **Query:** español (España/Latam)
- **Texto del AIO:** español, pero con títulos de libros en inglés
- **Fuentes:**
  - TikTok: creadora hispanohablante
  - 2 hilos de Reddit en inglés (con parámetro `tl=es-419`, es decir, mostrados traducidos para hispanohablantes)
→ Google mezcla **UGC anglo** + **creadora española de TikTok** para servir una respuesta en español.

---

## 🔗 Análisis de fuentes

| # | Dominio | Tipo | Anchor | Por qué fue citada |
|---|---------|------|--------|--------------------|
| 1 | tiktok.com | Social / UGC vídeo | Guía completa para leer Romantasy en 2026 | Contenido muy específico para *romantasy* y para el año 2026, en español, con formato guía. Alta conexión semántica con parte del AIO (“Quick Silver (Fae oscuro), Azarraí (romantasy)…”). Probable origen de la parte romántica y de subgéneros (fae oscuro, romantasy), además de aportar señal de frescura y engagement social. |
| 2 | reddit.com | UGC / foro | ¡Libros que más esperas para 2026/2027! : r/Fantasy | Hilo de comunidad preguntando por los libros más esperados de 2026/2027. De aquí salen títulos como *To Ride a Rising Storm* y *The Spell For Unraveling* y posiblemente menciones a *Silent Pa…* (Silent Palace/Silent… en el snippet). Es UGC fresco (jul 2025), con listas de libros directamente relacionados con “most anticipated fantasy 2026”. |
| 3 | reddit.com | UGC / foro | ¿Los libros más esperados de 2026? : r/Fantasy | Otro hilo casi idéntico pero de fecha posterior (dic 2025). Probablemente refuerza los mismos títulos (To Ride a Rising Storm, The Spell For Unraveling, Red God, etc.). Google lo usa para corroborar consenso de la comunidad y completar la lista de “títulos esperados” para 2026. UGC muy alineado con la query + alta frescura temporal. |

### Qué fragmentos parecen salir de cada fuente

- **Reddit (2 y 3):**
  - “To Ride a Rising Storm de Moniquill Blackgoose (enero)”
  - “The Spell For Unraveling de Rochelle Hassan (abril)”
  - “Red God de Pierce Brown”
  - Fechas concretas (enero, abril, septiembre) y formulación de “títulos más esperados / anticipated”.
- **TikTok (1):**
  - “Quick Silver (Fae oscuro), Azarraí (romantasy)”
  - Tono de recomendación cercana, centrado en *romantasy* y tropos (fae, romance fuerte, etc.).
  - El propio uso de “Guía completa para leer Romantasy en 2026” como etiqueta refuerza que el AIO absorbe titulares y copy del vídeo.

---

## 🧩 Patrones detectados

- **Sesgo de plataforma:**
  - 100% **UGC** → Reddit (foro) + TikTok (social vídeo).
  - 0 medios editoriales, 0 blogs especializados, 0 webs de editoriales.
- **Sesgo temporal:**
  - Fechas de los hilos 2025 (julio y diciembre) → Google prioriza **frescura extrema** para una query con año (2026).
- **Diversidad de tipos:**
  - Solo 2 plataformas, pero una es vídeo corto y otra foro de texto → mezcla mínima, pero ambas **comunidad / recomendación**.
- **Gap de autoridad:**
  - Faltan webs de referencia tipo editoriales, portales de reseñas, grandes medios culturales en español.
  - Esto abre hueco enorme para **un buen artículo SEO en español**.
- **Patrón geográfico/idiomático:**
  - Query en español → Google mete un TikTok en español + Reddit traducido (parámetro `tl=es-419`).
  - Claramente hay **poca oferta sólida en español**, por eso tira tanto de UGC anglo traducido.

---

## 🎯 Oportunidades

### Tipo de contenido con más probabilidad de citación

- **Artículo evergreen + temporal**:
  “Los libros de fantasía que tienes que leer en 2026 (con romantasy incluida)”
- Enfocado a:
  - Novedades 2026 (internacional + traducciones al español)
  - Subgéneros que ya aparecen en el AIO: **epic fantasy + romantasy + fae oscuro**

### Formato óptimo

- **Extensión**: 2.000–2.500 palabras, con pasajes de 130–160 palabras fácilmente extractables.
- **Estructura**:
  - Intro corta con respuesta directa (primeras 150 palabras = resumen + mini-lista).
  - Listas tipo **ItemList**: “Top X libros de fantasía que leer en 2026”.
  - H2/H3 descriptivos en forma de pregunta:
    - “¿Qué libros de fantasía leer en 2026 si eres principiante?”
    - “Mejores novedades de romantasy para 2026”.
  - Tabla o bullets con: título, autor, subgénero, fecha de publicación, si está/estará en español.
- **Multimedia**:
  - Portadas de libros, excerpt de reseñas, y **un vídeo corto incrustado** (YouTube o TikTok) con “mis 5 recomendaciones para 2026”.

### Señales de autoridad (E-E-A-T + técnico)

- Bio del autor/a: dejar claro que lee mucha fantasía, menciona años de experiencia, participación en clubs de lectura, etc.
- Citar 1–2 fuentes fuertes por sección (editoriales, Goodreads, webs oficiales).
- Markup:
  - `Article` + `ItemList` (lista de libros)
  - `FAQPage` con 3–5 preguntas típicas.
- Datos concretos:
  - Mes/año de publicación
  - Subgénero y público (YA, adulto, new adult).
- Enlazar a tiendas/editoriales oficiales (mejor que solo Amazon).

### Timing

- Actualizar el artículo **cada trimestre** de 2025–2026:
  - Añadir nuevos anuncios
  - Ajustar fechas de publicación
  - Marcar claramente “Última actualización: mes año”.

### Plataformas complementarias

- **TikTok**: replicar la idea de “Guía completa para leer fantasía/romantasy en 2026” con tu branding + link al artículo.
- **Reddit / comunidades**:
  - Publicar hilos tipo “Most anticipated fantasy releases 2026 (in Spanish)” enlazando a tu listado.
  - Participar aportando valor (no solo drop de links).

---

## 📝 Plantilla competitiva

### Título sugerido

> **Qué libro de fantasía leer en 2026: 21 novedades imprescindibles (epic, romantasy y fae oscuro)**

### Meta description (ejemplo)

> Los mejores libros de fantasía para leer en 2026: novedades épicas, romantasy, fae oscuro y sagas esperadas. Guía clara, en español, con fechas y dónde conseguirlos.

### H1

> **Qué libro de fantasía leer en 2026: guía completa de novedades y sagas**

### Estructura H2/H3

- **H2: Resumen rápido: 7 libros de fantasía que leer sí o sí en 2026**
  - H3: 3 novedades de fantasía épica muy esperadas
  - H3: 3 libros de romantasy para 2026
  - H3: 1 apuesta diferente si quieres salir de tu zona de confort
- **H2: Cómo elegir tu próximo libro de fantasía en 2026 (en 3 pasos)**
  - H3: Define tu subgénero: épica, urbana, romantasy o fae oscuro
  - H3: Longitud, tono y público (YA, adulto, new adult)
  - H3: Dónde conseguir las novedades en español
- **H2: Novedades de fantasía épica más esperadas de 2026**
  - H3: Continuaciones de sagas famosas
  - H3: Nuevas sagas que empiezan en 2026
- **H2: Romantasy en 2026: libros con magia y romance que no puedes perderte**
  - H3: Romantasy con fae oscuro
  - H3: Romantasy con torneos, pruebas o concursos mágicos
- **H2: Libros de fantasía autoconclusivos para 2026**
- **H2: Preguntas frecuentes sobre qué leer de fantasía en 2026 (FAQ)**

### Primer párrafo (50–70 palabras, respuesta directa)

> Si en 2026 quieres leer fantasía y no sabes por dónde empezar, céntrate en unas pocas novedades clave: continuaciones muy esperadas, nuevos inicios de saga y algo de romantasy si te atrae el romance. A continuación encontrarás una lista corta, clara y ordenada por subgéneros para que elijas tu próxima lectura sin perder tiempo comparando reseñas.

### Schema markup recomendado (esqueleto)

```html id="shzhhf">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Qué libro de fantasía leer en 2026: 21 novedades imprescindibles",
  "author": {
    "@type": "Person",
    "name": "Tu Nombre"
  },
  "datePublished": "2025-12-15",
  "dateModified": "2026-02-01",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://tudominio.com/que-libro-fantasia-leer-2026"
  },
  "articleSection": [
    "Resumen rápido",
    "Novedades de fantasía épica 2026",
    "Romantasy 2026",
    "Libros autoconclusivos de fantasía"
  ],
  "mainEntity": {
    "@type": "ItemList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "item": {
          "@type": "Book",
          "name": "Título de libro 1",
          "author": "Autor 1"
        }
      },
      {
        "@type": "ListItem",
        "position": 2,
        "item": {
          "@type": "Book",
          "name": "Título de libro 2",
          "author": "Autor 2"
        }
      }
    ]
  }
}
</script>
```

Nada ha cambiado. Sigues necesitando saber dónde estás y dónde no. Solo ha cambiado el dónde.

Una auditoría que te dice dónde estás y una estrategia que te dice qué hacer. Sin pagar 200€/mes por otra herramienta.

**👇👇 Descarga la extensión de Chrome: Extractor AI Overviews 👇👇**

[Descargar aquí](https://github.com/seoutopico/chrome_extension_extractor-ai-overviews)

*El repo incluye la extensión, el Apps Script, el prompt del asistente, y una guía de estrategia.*

**ℹ️ Un aviso:** la extensión detecta el AI Overview buscando los selectores CSS que Google usa ahora mismo. Si Google cambia los IDs de esas clases, deja de funcionar. E

Pero esa es la gracia. Esto no es un producto. Es una idea con código que puedes abrir, leer y adaptar. La hice con Claude Code. Si quieres mejorarla, cambiarla o construir la tuya desde cero, hoy puedes.

Los AI Overviews cambian. Las fuentes que Google cita hoy para una keyword pueden ser otras mañana. Esto no es un análisis que haces una vez. Es una auditoría recurrente.

**Nada ha cambiado. Solo ha cambiado el dónde.**

¿Sales citado?

***Cuéntamelo. Siempre leo todo.***

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

**Recomienda Think&Hack**

Soy Aina. Responsable de IA generativa en Planeta.

**Comparte:** Reenvía esto a quien dependa del tráfico orgánico y no sepa qué es un AI Overview.
**Responde:** ¿Estás midiendo tu presencia en respuestas de IA o solo tus rankings? **Suscríbete:** Si te han reenviado esto, [únete aquí](https://ainalluna.substack.com/). 👇

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
