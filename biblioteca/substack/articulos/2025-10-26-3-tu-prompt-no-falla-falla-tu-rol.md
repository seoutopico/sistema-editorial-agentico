---
id: 177152947
titulo: "#3 Tu prompt no falla: falla tu rol"
subtitulo: "Cómo evitar respuestas promedio activando roles específicos y aportando el contexto que importa."
fecha: 2025-10-26
url: https://ainalluna.substack.com/p/3-tu-prompt-no-falla-falla-tu-rol
tipo: newsletter
audiencia: everyone
estado: completo
huella: 6b2a1c3907ebf4c392f3c04105831ce31960e3c6d85b64e72af6d6839c34e1c4
---

[

![imagen](https://substackcdn.com/image/fetch/$s_!CVEt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b847241-27c9-4486-a76b-f2792ed2cbab_1141x635.png)

](https://substackcdn.com/image/fetch/$s_!CVEt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b847241-27c9-4486-a76b-f2792ed2cbab_1141x635.png)

¿Cómo estás? Por si es tu primera vez aquí, me presento: soy Aina y te doy la bienvenida a **Think&Hack**, una newsletter donde te cuento ideas y procesos para pensar mejor, decidir mejor y ejecutar mejor.

Aquí está la **#3 entrega**, cómo pasar de copiar prompts a diseñarlos con cabeza.

**Hoy hablaremos de por qué tus prompts siguen sin funcionar.**

Y no es culpa de la herramienta.

De roles, contexto, y los dos principios que sí importan cuando las modas cambian cada tres meses.

Si te interesa entender cómo funcionan las cosas de verdad, no solo copiar plantillas, suscríbete para no perderte las próximas entregas.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)

Si ya eres habitual de Think&Hack, muchas gracias por estar aquí de nuevo.

**Una reflexión sobre roles, contexto y por qué la herramienta que uses es lo de menos.**

*…y entonces todos preguntaron “¿qué herramienta uso?” en lugar de “¿cómo funciona esto realmente?”*

**Mi semana**

Esta semana di mi primera clase de IA aplicada al mundo editorial en la UPF de Barcelona.

Y me encantó.
Pero no por lo que esperaba.

No fue el temario. No fue sentirme experta. Fue estar tres horas rodeada de gente joven que te mira y te dice *“no estoy de acuerdo contigo” *.

Una estudiante levantó la mano y cuestionó algo que yo daba por obvio. Y en lugar de sentir que perdía autoridad, pensé: *qué bien que me hagan pensar*.

**Sigo odiando que me den la razón automáticamente.**

`Para tener muchas verdades propias necesitas escuchar muchas verdades ajenas.`

Aunque te incomoden.
Especialmente si te incomoden.

Y esto me llevó a pensar: ¿por qué le pedimos a la IA que nos dé respuestas que confirmen lo que ya pensamos, en lugar de usarla para cuestionar nuestras propias ideas?

Trabajar con IA no es tan diferente a trabajar con personas.

Si solo escuchas voces que validan tus certezas, te quedas donde estás.

---

## **Nadie quiere empezar por el principio**

En mis clases, antes de hablar de herramientas, suelo hace una pregunta: *“¿Alguien sabe cómo funciona realmente un modelo de lenguaje?”*

Silencio incómodo.

Todo el mundo quiere saber *qué* herramienta usar. ChatGPT, Claude, Gemini, Perplexity... La lista crece cada semana.

Pero nadie pregunta *cómo* funcionan.

Y ahí está el problema: puedes tener acceso a los mejores modelos del mundo y seguir obteniendo respuestas mediocres, genéricas, inútiles. El tipo de respuesta que te hace pensar “esto lo podría haber encontrado en Google en 2015”.

**Hay dos cosas que, una vez las entiendes, da igual qué modelo uses o qué herramienta salga mañana:**

1.

Cómo funciona la **asignación de roles**

2.

Cómo el **contexto** transforma una respuesta correcta en una respuesta útil

La herramienta cambia cada tres meses.

Estos principios no.

## **Por qué el rol es lo único que realmente importa**

Cuando le preguntas algo a ChatGPT o a cualquier LLM sin asignar un rol, estás hablando con un modelo que tiene acceso a millones de perspectivas simultáneamente.

Y eso suena bien hasta que te das cuenta de que **tener acceso a todas las perspectivas es como no tener ninguna.**

Te da un promedio. Una mezcla. Lo más probable estadísticamente que alguien diría sobre ese tema.

Correcto, sí.
Pero genérico.
Y por tanto inútil.

## **Qué pasa realmente cuando asignas un rol**

Un LLM no es una base de datos donde buscas información.

**Es un espacio semántico multidimensional donde cada palabra activa conexiones específicas.**

Cuando dices *“Eres un experto en X”*, no estás decorando el prompt para que suene profesional.

Estás **activando un subconjunto específico del conocimiento del modelo.**

Es como tener una biblioteca enorme pero solo encender las luces de una sección concreta.

## **El ejemplo que lo explica todo: Angelina Jolie**

Sin rol específico, pregunta: *“Háblame de Angelina Jolie”*

El modelo te da: actriz de Hollywood, activista humanitaria, embajadora de ACNUR, madre de seis hijos, expareja de Brad Pitt, directora de cine...

Todo mezclado. Sin jerarquía. Sin filtro.

Ahora prueba esto:

```
**ROL 1:** *“Eres un crítico de cine especializado en actuación. Analiza la carrera de Angelina Jolie.”

**Respuesta centrada en:** evolución interpretativa, elección de roles, técnica actoral, filmografía crítica.*
```

```
**ROL 2:** *“Eres un analista de causas humanitarias. Analiza el trabajo de Angelina Jolie.”

***Respuesta centrada en:** labor con refugiados, impacto de su activismo, efectividad de su rol como embajadora de ACNUR.
```

```
**ROL 3:** *“Eres un experto en branding personal de celebridades. Analiza a Angelina Jolie.”

***Respuesta centrada en:** construcción de imagen pública, gestión de crisis mediáticas, estrategia de marca personal.
```

Misma persona.
Misma información disponible en el modelo.
**Tres análisis completamente distintos.**

No porque la IA “finja” ser experta. Porque **el rol activa diferentes redes semánticas dentro del modelo.**

## **Lo que realmente hace un rol **

Cuando entrenas un modelo de lenguaje, no le enseñas hechos aislados.

Le enseñas **relaciones entre conceptos.**

“Angelina Jolie” está conectada semánticamente con:

-

Actuación → técnica interpretativa → premios → filmografía

-

Humanitarismo → ACNUR → refugiados → activismo

-

Fama → paparazzi → relaciones → imagen pública

Todas esas conexiones existen simultáneamente.

```
**El rol decide qué caminos semánticos recorre el modelo.
**
**Sin rol:** recorre todos a la vez, te da un promedio.
**Con rol específico:** activa solo las conexiones relevantes para esa expertise.
```

## **Por qué esto cambia todo**

No estás cambiando la información. **Estás cambiando la perspectiva desde donde el modelo mira esa información.**

Ejemplo real:

```
**Sin rol: ***“¿Cómo mejoro mi estrategia de contenidos?”

***Respuesta:** Lista genérica de mejores prácticas. Consistencia, valor agregado, segmentación, análisis de métricas... Todo correcto. Todo inútil.
```

```
**Con rol: ***“Eres un estratega de contenidos que ha trabajado 15 años en medios editoriales tradicionales adaptándose a digital. ¿Cómo mejoro mi estrategia de contenidos para una editorial independiente?”

***Respuesta:** Análisis específico sobre desafíos de transición editorial tradicional→ digital, estrategias de nicho para competir con grandes, tácticas de comunidad vs viralidad.
```

**Esa es la diferencia.**

## **Los tres tipos de roles que realmente funcionan**

### **1. Rol de expertise único**

*“Eres un economista especializado en la Gran Depresión de 1929.”*

No le pides información sobre 1929. Le pides que analice situaciones contemporáneas aplicando marcos conceptuales históricos.

Ejemplo: *“Analiza la crisis actual del sector tech usando lecciones de la Gran Depresión.”*

### **2. Rol multi-expertise (el más potente)**

*“Eres un neurocientífico cognitivo que además comprende psicología del consumidor.”*

Aquí pides síntesis de dos campos que normalmente no conversan.

Ejemplo: *“Explica por qué las notificaciones push generan adicción usando tanto neurociencia como estrategia de retención de usuarios.”*

### **3. Rol adversario (el que nadie usa)**

*“Actúa como economista keynesiano. Ahora actúa como economista de escuela austríaca. Debate la misma política fiscal desde ambas perspectivas.”*

Usas al modelo para explorar un tema desde ángulos opuestos. No para que te dé LA respuesta, sino para que **mapee el espacio completo de posibilidades.**

## **Técnica avanzada: Cambio secuencial de roles**

No tienes que quedarte con un solo rol por conversación.

Puedes hacer esto:

```
**PASO 1:** Eres historiador. Analiza este problema desde precedentes históricos

*[Respuesta del modelo]*

**PASO 2:** Ahora eres psicólogo organizacional. Analiza el mismo problema desde dinámicas de comportamiento humano.

*[Respuesta del modelo]*

**PASO 3:** Ahora eres estratega de negocios. Sintetiza ambas perspectivas anteriores y dame recomendaciones accionables.
```

**Cada rol construye sobre el anterior. Cada capa añade profundidad.**

## **Por qué funciona mejor que “experto genérico”**

La mayoría escribe: *“Eres un experto en marketing”*

Eso no activa nada específico. Es demasiado amplio.

Marketing incluye: SEO, branding, publicidad, growth hacking, PR, influencer marketing, email marketing...

**El modelo no sabe qué subconjunto activar**. Entonces activa todos. Y te da un promedio diluido.

**Mejor:**

-

*“Eres un especialista en marketing de contenidos B2B para SaaS empresarial”*

-

*“Eres un experto en growth hacking para productos de consumo con presupuesto limitado”*

-

*“Eres un estratega de marca personal para profesionales independientes”*

**Cuanto más específico el rol, más útil la respuesta.**

## **El error que comete el 90% (y cómo evitarlo)**

**ERROR:** Escribir roles vagos pensando que así el modelo tiene “más libertad”.

```
*“Eres un experto que sabe de todo”* → Inútil. El modelo ya “sabe de todo”. Por eso necesitas filtrar.
```

**CORRECTO:** Roles específicos que activan expertise concreta.

```
*“Eres un arquitecto de software que ha migrado sistemas legacy a microservicios en empresas financieras”*
```

Ahora el modelo no te da “principios generales de arquitectura”. Te da análisis específico de desafíos de migración en contextos regulados.

## **La única pregunta que importa sobre roles**

No es *“¿Qué rol uso?”*

Es: **“¿Desde qué perspectiva específica quiero que el modelo piense sobre este problema?”**

Porque cuando dominas eso, los roles dejan de ser “trucos de prompt” y se convierten en herramientas de pensamiento.

---

>
>
> `Si quieres entender cómo funcionan los mecanismos de atención y búsqueda semántica detrás de los roles, lo explico con más profundidad aquí → `[La importancia de asignar un rol al prompt](https://ainalluna.com/blog/la-importancia-de-asignar-un-rol-al-prompt)
>
>

---

**Recomendación: Domina n8n y pon tu vida en piloto automático (gratis)**

![imagen](https://substackcdn.com/image/fetch/$s_!k4wW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F996e0541-00d7-4e50-8d82-8df086693c73_457x183.png)

Usar la IA en un LLM es solo el principio; la eficiencia llega cuando **automatizas**. Quien **aterriza mis ideas en negocios**, **[Mike Fort](https://substack.com/@mafortperera)**, ha lanzado un curso **gratuito** para aprender **n8n** desde cero, sin conocimientos técnicos. En **30 días** conectarás tus herramientas, activarás **agentes de IA** y **ahorrarás horas** cada semana con flujos prácticos y plantillas reales.

👉 **Inscríbete gratis y empieza hoy:** [https://link.monem.io/Fl0faJ1AoR](https://link.monem.io/Fl0faJ1AoR)

---

## **Pero el rol sin contexto es como tener un chef sin ingredientes**

Entender la asignación de roles es el primer paso.

Pero hay algo más fundamental que casi nadie explica: **el contexto es lo que transforma una respuesta correcta en una respuesta útil.**

Y aquí está el problema: confundimos contexto con cantidad de información.

Le damos al modelo 10,000 palabras de briefing pensando *“con más datos, mejor respuesta”*.

**Pero el contexto no es volumen. Es relevancia específica.**

Es la diferencia entre decirle a alguien *“necesito ayuda con marketing”* y decirle *“trabajo en una editorial independiente con 3 personas de equipo, presupuesto limitado, audiencia de 40-55 años que lee no-ficción, y necesito estrategia para próximo lanzamiento que compite con títulos de grandes editoriales”*.

Mismo tema.
Mundos distintos de utilidad.

---

## **El problema oculto: IA sin memoria ni contexto**

Cada vez que abres ChatGPT o algun LLM es como contratar un consultor brillante que no sabe nada de ti.

No sabe tu industria.
No conoce tu proyecto.
No tiene idea de qué decisiones ya tomaste, qué intentaste que falló, qué restricciones tienes.

Entonces hace lo único que puede: generalizar.

Le preguntas sobre productividad y te da consejos que podrían aplicar a un CEO de startup, a un estudiante universitario o a alguien gestionando una panadería familiar.

**Respuestas correctas pero genéricas.**

Como un nutricionista recomendando “comer saludable” sin saber tus alergias, tu presupuesto, tus objetivos ni tu contexto real.

---

## **Los tres tipos de contexto que nadie te explica**

Aquí está lo que la mayoría no entiende: **hay tres formas de dar contexto a una IA. Y necesitas dominar las tres.**

### **CONTEXTO 1: Lo que escribes en el prompt**

Es lo más obvio pero lo que peor se hace.

```
**La mayoría escribe:** *“Dame ideas para mi negocio”

***Cuando deberían escribir:** *“Trabajo en editorial independiente, 3 personas de equipo, audiencia 45-60 años interesada en ensayo político. Competimos con grandes editoriales con presupuestos 20x mayores. Último lanzamiento vendió 3,000 copias en 6 meses. Dame ideas para próximo lanzamiento considerando estas limitaciones.”*
```

**Los 5 elementos del contexto efectivo en el prompt:**

**1. Restricciones específicas
** No “poco presupuesto”. Sino “€2,000 para 3 meses, sin opción de contratar”

**2. Decisiones previas
** “Ya probamos Facebook sin resultados. Instagram funciona pero alcance cayó 40% en 6 meses”

**3. Audiencia real, no ideal
** No “profesionales interesados en tecnología”. Sino “CTO de empresas 50-200 empleados, no early adopters, pero con presión de innovar”

**4. Éxitos y fracasos
** “Nuestro mejor contenido fue X (500% más engagement). Lo peor fue Y (nadie lo leyó)”

**5. Limitaciones no negociables
** “No puedo cambiar de sector. No puedo contratar. No puedo alargar plazos más de 2 meses”

Esto es lo que todos conocen.

Pero hay dos niveles más potentes que casi nadie usa.

---

### **CONTEXTO 2: Lo que le enseñas con documentos**

![imagen](https://substackcdn.com/image/fetch/$s_!DxW9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb34b35c0-b362-4823-905c-c158a01367be_532x195.png)

Aquí es donde la mayoría cree que usar IA es “subir un PDF y hacerle preguntas”.

No.

**Cuando subes documentos, estás convirtiendo a la IA en experto de TU material específico.**

Ejemplo real de cómo cambia todo:

**Sin documentos:
** *“Eres experto en diseño instruccional. ¿Cómo mejoro mi curso?”*

Respuesta: Principios genéricos de diseño instruccional que encuentras en cualquier libro.

**Con documentos subidos (tu temario, feedback de alumnos anteriores, grabaciones de clases):
** *“Analiza mi material de curso y dime qué secciones generan más confusión según los patrones que identifiques en el feedback. Sugiere reestructuración específica.”*

Respuesta: Análisis de TUS materiales específicos, identificando patrones reales en feedback de TUS estudiantes, con sugerencias basadas en lo que YA tienes.

**Lo que puedes subir como contexto documental:**

-

Tu trabajo previo (artículos, presentaciones, proyectos)

-

Feedback recibido (comentarios, correos, evaluaciones)

-

Referentes que quieres emular (PDFs, transcripciones)

-

Datos propios (reportes, analytics, casos de estudio)

-

Frameworks internos (guías de estilo, procesos, metodologías)

Esto funciona con herramientas como NotebookLM, Claude , ChatGPT con archivos, Gemini con Google Drive.

**El cambio fundamental:**

Ya no preguntas *“¿cómo hago X en general?”*

Preguntas *“¿cómo hago X considerando ESTOS documentos específicos que subo a la conversación?”*

---

### **CONTEXTO 3: Lo que la IA investiga por ti**

[

![imagen](https://substackcdn.com/image/fetch/$s_!RJ0G!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d3e7a0d-8861-40e7-81a7-657912fd6f7f_717x349.png)

](https://substackcdn.com/image/fetch/$s_!RJ0G!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d3e7a0d-8861-40e7-81a7-657912fd6f7f_717x349.png)

Este es el nivel que más gente ignora y el más potente para contexto profundo.

**No le pides a la IA que responda con lo que ya sabe. Le pides que investigue primero.**

Mira la diferencia:

**Enfoque tradicional:
***“Eres experto lingüista en castellano. Analiza contradicciones en prompts de IA.”*

Respuesta basada en conocimiento general del modelo. Correcta, pero genérica.

**Enfoque con investigación contextual:**

Eres experto lingüista centrado en análisis de patrones del hablar.

ANTES de responder, quiero que investigues:

-

Papers académicos sobre contradicción pragmática y semántica

-

Estudios lingüísticos sobre inconsistencias en actos de habla directivos

-

Técnicas computacionales para detección de contradicciones

-

Análisis del discurso y contradictorio

Una vez investigado, actúa como experto en prompts engineering detectando comportamientos extraños en los LLMs considerando toda esa investigación previa.

**Qué hace esto:**

1.

La IA primero **BUSCA **información actualizada sobre el tema

2.

Luego **ANALIZA **con ese contexto fresco

3.

Finalmente **RESPONDE **con conocimiento específico, no general

---

## **Cómo combinar los tres contextos (aquí está la magia)**

La mayoría usa solo uno. Los que destacan combinan los tres estratégicamente.

**EJEMPLO REAL - Estrategia de contenido:**

```
**CONTEXTO 1 (Prompt):**Eres estratega de contenidos con 15 años en medios editoriales.
Mi situación:
- Newsletter sobre IA para profesionales NO técnicos
- 2,500 suscriptores, apertura 38%, clicks 4%
- Envíos semanales, formato largo (1,500-2,000 palabras)
- Mejor contenido: casos reales. Peor: tutoriales técnicos
- Audiencia: 35-50 años, directivos y consultores

**CONTEXTO 2 (Documentos subidos):**
- Últimos 20 newsletters enviados
- Analytics de engagement por sección
- Comentarios y respuestas de lectores
- 3 newsletters de referentes que admiras

**CONTEXTO 3 (Investigación):**

ANTES de dar recomendaciones:

1. Investiga tendencias actuales en newsletters de nicho profesional
2. Analiza qué formatos están funcionando en 2025 para audiencia 35-50
3. Busca casos de éxito de newsletters que lograron alto engagement sin viralidad masiva **LUEGO, considerando mis documentos subidos y mi contexto específico, dame estrategia de diferenciación realista.**

```

**Resultado: Respuesta que combina:**

-

Tu situación específica (contexto 1)

-

Análisis de TU contenido real (contexto 2)

-

Tendencias actuales del mercado (contexto 3)

**Esto no es una respuesta genérica. Es consultoría estratégica personalizada.**

---

### **El test antes de preguntar**

✅ ¿Di contexto específico en mi prompt?
✅ ¿Podría subirle documentos?
✅ ¿Debería pedirle que investigue primero?

Si respondes sí a los tres, estás jugando en otra liga.

---

### **Las dos preguntas que importan**

No es *“¿Qué herramienta uso?”*
No es *“¿Qué prompt funciona mejor?”*

```
Es: **“¿Desde qué perspectiva quiero que el modelo piense?”** (Rol)

Y: **“¿Qué combinación de contextos necesito para que esta respuesta sea útil y no genérica?”** (Contexto)
```

Cuando dominas eso, da igual que uses ChatGPT, Claude, Gemini o lo que salga mañana.

La herramienta cambia cada tres meses. **El principio no.**

***¿Has probado combinar rol + los tres tipos de contexto? ¿Cuál usas más y cuál nunca has explorado?***

*Cuéntame tu experiencia. Siempre leo todo.*

---

![imagen](https://substackcdn.com/image/fetch/$s_!jAJ6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa6a28f5-efe2-4efb-93bc-87d726ddd0ec_56x56.png)

**Recomienda Think & Hacks**

Como responsable de IA generativa en Editorial Planeta, mi trabajo no es implementar IA.

**Es evitar que mi empresa pierda dinero implementando IA mal.**

La diferencia entre ambas cosas es exactamente lo que encontrarás aquí: **la brecha entre lo que Silicon Valley promete y lo que realmente funciona cuando tienes 500 empleados, sistemas legacy, y un margen que defender.** Por qué la mayoría de estrategias de IA están diseñadas para fracasar (spoiler: porque son estrategias de consultoría, no de negocio), y cómo las pocas que funcionan pueden mover tu P&L sin dinamitar tu operación.

**Otra mirada a la tecnología. La de quien la implementa, no la vende.**

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
