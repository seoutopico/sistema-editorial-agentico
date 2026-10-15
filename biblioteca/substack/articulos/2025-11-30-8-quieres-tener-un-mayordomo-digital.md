---
id: 180255237
titulo: "#8 Quieres tener un Mayordomo Digital con N8N?"
subtitulo: "Incluye guía práctica para construir tu mayordomo con N8N."
fecha: 2025-11-30
url: https://ainalluna.substack.com/p/8-quieres-tener-un-mayordomo-digital
tipo: newsletter
audiencia: everyone
estado: completo
huella: d4d948478cedc4a2f06adb6bc69dfafa3ae57b466405626ee8cb168b6af98e62
---

¿Cómo estás?

Soy Eva y hoy colaboro con **Think&Hack**. Aquí está la **#8 entrega** de esta newsletter.

Hablaremos de por qué tu necesidad de saber a qué hora juega tu equipo te está costando 15 minutos de vida cada vez, y cómo N8N puede ayudarte.

Si te interesa empezar a crear tus pinitos con N8N y estar al día de todo lo que puedes hacer con automatizaciones, suscríbete.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)

Si ya eres habitual, gracias por volver.

### **El Mayordomo Silencioso.**

Imagina que tienes un mayordomo.

Tú no vas al kiosco a buscar el periódico (y te distraes con las revistas, y compras chicles, y hablas con el vecino).

Tú te sientas a desayunar y el mayordomo deja sobre tu mesa una nota doblada. Sólo dice: *“ El partido es a las 21:00. Lo dan en tal canal”*. Y se retira.

Eso es lo que construí con N8N.

Un flujo de trabajo que no me pide atención. Me la regala.

No es una app. No tiene colores brillantes. No tiene scroll. Es un correo de texto plano que llega cada mañana a las 8:00 AM con la programación del día.

[

![imagen](https://substackcdn.com/image/fetch/$s_!3hPj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6cafe9a9-f1e2-4fc5-a7d6-68601bf6ea39_1024x1024.png)

](https://substackcdn.com/image/fetch/$s_!3hPj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6cafe9a9-f1e2-4fc5-a7d6-68601bf6ea39_1024x1024.png)

### **Lo que la automatización hace realmente (SÍ vs NO)**

La mayoría piensa que automatizar con herramientas como n8n o Zapier es para “ahorrar tiempo”. Se equivocan. Es para **ahorrar carga cognitiva**.

**Lo que tu App de Deportes hace:**

-

**Tragarte su Publicidad**

-

**Diseño PUSH agresivo:** Te bombardea con lo que *ellos* quieren que veas.

-

**Ruido:** Mezcla el dato que buscas con 90% de basura para retenerte.

-

**Extracción:** Su objetivo es extraer tus datos y tu tiempo.

**Lo que el Mayordomo (n8n) hace:**

-

**Cero Publicidad**

-

**Diseño PULL selectivo:** Solo busca lo que *tú* has definido como valioso.

-

**Señal:** Separa el grano de la paja antes de que llegue a tus ojos.

-

**Servicio:** Su objetivo es entregarte valor y desaparecer.

### **La Guía Práctica: “construye a tu Mayordomo”**

No necesitas ser ingeniero de software para montar esto. Sólo necesitas entender la lógica de bloques.

He usado **n8n** (una herramienta de automatización de flujos de trabajo, opensource y visual) porque me permite conectar cosas sin escribir código complejo.

Aquí tienes la arquitectura del “Mayordomo Silencioso”:

**1. El Disparador (The Trigger):**

-

**Nodo:** Schedule Trigger.

-

**Configuración:** “Cada día a las 08:00 AM”.

-

*Filosofía:* Tú decides cuándo recibes la información, no cuando la app te manda una notificación push.

**2. La Fuente (The Source):**

-

**Nodo:** HTTP Request.

-

**Acción:** Conectar a una API de deportes gratuita (como TheSportsDB o API-Football).

-

**Petición:** “Dame los eventos de HOY”.

-

*Filosofía:* Vas a la fuente cruda. Sin interfaz. Sin anuncios. Datos puros.

**3. El Filtro (The Bouncer):**

-

**Nodo:** Filter o IF.

-

**Lógica:** “¿Es el equipo = ‘FC Barcelona’ OR ‘Nadal’?”

-

*Filosofía:* Aquí está la magia. El algoritmo eres tú. Tú defines qué es relevante. Si no juega tu equipo, el correo no se envía. El silencio también es información.

**4. La Entrega (The Delivery):**

-

**Nodo:** Gmail o Telegram.

-

**Formato:** Texto plano. “Hola Eva. Hoy juega el Barça a las 21:00 vs Madrid. TV: Dazn.”

-

*Filosofía:* Sin imágenes. Sin clicks. Lectura de 3 segundos. Fin.

Figura del workflow:

[

![imagen](https://substackcdn.com/image/fetch/$s_!4jnM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F120b8ba4-3150-4a16-b67a-9bf07ede734b_1586x490.png)

](https://substackcdn.com/image/fetch/$s_!4jnM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F120b8ba4-3150-4a16-b67a-9bf07ede734b_1586x490.png)

Y a partir de este workflow esto es lo que recibo cada día a las 8am en mi correo electrónico:

```
Asunto: Tu Guía Deportiva para Hoy - Sábado 29 de Noviembre de 2025

¡Hola aficionado al deporte!

Aquí tienes la programación deportiva completa para hoy, **sábado 29 de noviembre de 2025**, desde las 10:00 hasta las 23:00 horas. Un día cargado de fútbol, con especial atención al FC Barcelona, y otras competiciones destacadas.

###  FÚTBOL

** FC BARCELONA - Destacado Especial**

*   **11:45 - 13:45 (Gol):** **LaLiga Santander: FC Barcelona - Atlético de Madrid (3-1)**

    *   *Reposición del partido. Revive la victoria del Barça.*

*   **15:30 - 16:10 (Esport 3):** Gol a gol: FC Barcelona - Deportivo Alavés

    *   *Previa y análisis del partido de hoy.*

*   **16:10 - 18:10 (Esport 3):** Un dia de partit: FC Barcelona - Deportivo Alavés

    *   *Retransmisión EN DIRECTO del partido de LaLiga.*

*   **18:10 - 19:20 (Esport 3):** Gol a gol: FC Barcelona - Deportivo Alavés

    *   *Postpartido y análisis del encuentro.*

*   **21:20 - 22:30 (Esport 3):** Gol a gol: FC Barcelona - Deportivo Alavés

    *   *Resumen y análisis en profundidad.*

**Otros Partidos y Programas de Fútbol**

*   **10:00 - 11:45 (Gol):** Directo Gol

    *   *Seguimiento de todos los partidos de la jornada.*

*   **13:45 - 15:30 (Gol):** Directo Gol

*   **15:30 - 18:30 (Gol):** Directo Gol: Minuto a Minuto

*   **18:30 - 20:30 (Gol):** **LaLiga Hypermotion: Albacete Balompié - RC Deportivo de la Coruña**

    *   *Partido en DIRECTO de la Segunda División.*

*   **19:55 - 20:25 (Teledeporte):** Resúmenes LaLiga EA Sports

*   **20:45 - 22:45 (Gol):** Directo Gol: Minuto a Minuto

*   **22:45 - 01:00 (Gol):** Directo Gol

###  TENIS

*Lamentablemente, hoy no hay retransmisiones de tenis ni participación de Carlos Alcaraz en la parrilla televisiva.*

###  FÚTBOL SALA

*   **12:50 - 14:45 (Teledeporte):** **Liga Nacional de Fútbol Sala: Barça - Illes Balears Palma Futsal**

    *   *Partido en DIRECTO de la LNFS.*

###  GOLF

*   **14:45 - 17:00 (Teledeporte):** Open de España Femenino

  ###  MOTOR

*   **22:30 - 23:00 (Esport 3):** FIA World Rally Championship: Rally Saudi Arabia

    *   *Resúmenes y avances del rally.*

###  PROGRAMAS DE ANÁLISIS Y ACTUALIDAD DEPORTIVA

*   **10:15 - 11:15 (Teledeporte):** El pebetero

*   **15:10 - 15:25 (laSexta):** La Sexta deportes

*   **21:35 - 21:40 (Telecinco):** ElDesmarque Telecinco

*   **22:05 - 23:00 (Teledeporte):** Estudio Estadio, la previa

#  RECOMENDACIONES PERSONALES DEL DÍA

1.  ** FC Barcelona - Deportivo Alavés (16:10 - 18:10, Esport 3):** **El plato fuerte del día.** No te pierdas el partido en directo del Barça en LaLiga. Siempre es un evento de gran interés.

2.  ** Albacete - Deportivo de La Coruña (18:30 - 20:30, Gol):** Un clásico de la lucha por el ascenso en LaLiga Hypermotion. Un partido que promete emoción y pasión.

3.  ** Croacia - Dinamarca (20:25 - 22:00, Teledeporte):** Para los amantes de los deportes de equipo, un duelo de alto nivel en el Mundial Femenino de Balonmano entre dos potencias europeas.

¡Disfruta de un gran día de deportes!
```

**Regalo:** Si quieres el JSON de este workflow para importarlo en tu n8n y dejar de perder tiempo, responde en comentarios con la palabra “MAYORDOMO” y por supuesto suscríbete.

Además si quieres profundizar más en N8N te dejo el **enlace gratuito del curso “N8N en 30 dias”** de mi amigo Mike.

Link de mi amigo mike Fort:

** **

** Gracias Think&hackers por llegar hasta aquí !!!!**

![imagen](https://substackcdn.com/image/fetch/$s_!jAJ6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa6a28f5-efe2-4efb-93bc-87d726ddd0ec_56x56.png)

**Recomienda Think & Hacks**

Solo te pido tres cosas rápidas:

1.

🔄 **Comparte:** Reenvía este correo a ese compañero que sigue estancado en 2023.

2.

💬 **Comenta:** Dale a “responder” y dime: ¿Qué modelo usas tú fuera de ChatGPT?

3.

📩 **Suscríbete:** ¿Llegas tarde? para recibir la próxima antes que nadie.

.
