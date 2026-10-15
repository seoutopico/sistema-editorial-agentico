---
id: 202814101
titulo: "Agentes de IA para SEO: procesos con evidencia"
subtitulo: "Cómo diseñar procesos SEO con IA usando scripts para datos, agentes para criterio y checks para evitar análisis inventados."
fecha: 2026-06-21
url: https://ainalluna.substack.com/p/seo-con-ia-agentes-sin-alucinar
tipo: newsletter
audiencia: everyone
estado: completo
huella: 0c545330f9e01458f93cf2b9cd58ab721178f4dbd3c4a48e0a144e5f867f9ad6
---

[

![imagen](https://substackcdn.com/image/fetch/$s_!owvM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5f4bec2c-1e04-4d90-82d2-f9ab2ce3f3d8_1600x900.jpeg)

](https://substackcdn.com/image/fetch/$s_!owvM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5f4bec2c-1e04-4d90-82d2-f9ab2ce3f3d8_1600x900.jpeg)

¿Cómo estás?

Soy Aina y esto es Think&Hack.

El otro día di una charla en [MujeresEnSEO](https://www.mujeresenseo.es/) Barcelona sobre una pregunta que aparece cada vez más en SEO: **cómo usar agentes de IA sin que el análisis se convierta en una caja negra elegante**.

La pregunta suele formularse como "¿cómo evito que la IA alucine?", pero creo que así nos quedamos cortos. A veces el problema no es que el modelo alucine porque sí, sino que **le damos un proceso donde puede inventar, saltarse pasos o mezclar datos sin que nada lo frene**.

Si le pides a una IA "analiza mi contenido, encuentra oportunidades SEO y dime qué debería publicar", probablemente te devolverá algo bien escrito. Puede tener títulos, clusters, prioridades y una explicación convincente. El problema es que **no siempre podrás saber qué parte viene de datos reales, qué parte viene de una inferencia razonable y qué parte es una apuesta presentada con mucha seguridad**.

Por eso la tesis de la charla era esta:

**No se trata de pedirle a la IA que sea más cuidadosa. Se trata de diseñar un proceso donde tenga que trabajar con datos, límites y pruebas.**

Hoy quiero convertir esa charla en una explicación práctica. No como una demo cerrada, sino como un marco que puedes aplicar a tus propios procesos SEO.

Si quieres aprender a convertir la IA en sistemas útiles, suscríbete a **Think&Hack**.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)

---

## El error habitual: pedir una estrategia entera en una sola conversación

La IA puede ayudar muchísimo en SEO, pero conviene tener claro dónde está el riesgo. **El riesgo aparece cuando mezclamos en una sola petición tareas que son de naturaleza distinta.**

Por ejemplo, en un análisis editorial hay **tareas objetivas**: extraer entidades de un corpus, limpiar columnas, contar apariciones, calcular cobertura, consultar demanda externa o cruzar dos tablas. Esas tareas no necesitan creatividad. **Necesitan repetibilidad.**

También hay **tareas cualitativas**: decidir si una entidad pertenece al territorio de una marca, detectar polisemia, interpretar intención de búsqueda, priorizar un backlog o decidir si un gap merece una pieza propia. Esas tareas sí necesitan **criterio, contexto y una lectura editorial**.

El error es pedirle al modelo que haga todo eso a la vez. Cuando lo haces, el resultado puede sonar coherente, pero **pierdes trazabilidad**. No sabes qué calculó, qué interpretó, qué asumió y qué inventó porque no tenía una fuente clara.

La primera regla del sistema es separar esas responsabilidades.

**Lo objetivo debe ir a lógica determinista. Lo cualitativo puede ir a IA, pero como clasificador dentro de un marco, no como oráculo.**

---

## La regla práctica: scripts, skills y agentes

En la charla usé tres piezas para explicar esta separación: scripts, skills y agentes. No son palabras intercambiables. Cada una sirve para una cosa distinta.

[

![imagen](https://substackcdn.com/image/fetch/$s_!jnXS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdb5b7fb1-31aa-4245-8054-3a742dbe1384_1836x956.png)

](https://substackcdn.com/image/fetch/$s_!jnXS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdb5b7fb1-31aa-4245-8054-3a742dbe1384_1836x956.png)

Un **script** es **código determinista**. Sirve para tareas que deben salir igual cada vez: leer archivos, llamar a una API, limpiar datos, cruzar CSVs, validar columnas o detectar si una fase tiene evidencia. **Si una operación no debería depender del humor del modelo, no se la pidas al modelo. Escríbela como script.**

Una **skill** es **método empaquetado**. Sirve para que la IA sepa cómo hacer una tarea concreta sin que tengas que explicársela desde cero cada vez. Una skill puede decir: "cuando crees un proyecto nuevo, lee el corpus, infiere un brief inicial, crea esta estructura de carpetas y deja estos archivos". **La skill no decide por ti; reduce variabilidad en el proceso.**

Un **agente** aplica **criterio en una fase delimitada**. No debería recibir una tarea gigantesca como "hazme una estrategia SEO", porque ahí cabe cualquier cosa. Un agente útil recibe una responsabilidad concreta, por ejemplo: "lee estas entidades, lee este brief y decide cuáles pertenecen al territorio, cuáles son ruido y cuáles son marca".

La diferencia parece técnica, pero en realidad es muy práctica. **Cuando algo falla, puedes saber dónde mirar.** Si falla una columna, miras el script. Si falla el método, miras la skill. Si falla una decisión cualitativa, revisas el agente y su brief.

Sin esa separación, todo queda mezclado en una conversación. Y cuando todo vive en una conversación, todo puede sonar bien aunque el proceso esté mal.

---

## Ejemplo SEO: detectar gaps de entidades

Para aterrizarlo, usé un caso real: Think&Hack como corpus editorial.

La pregunta era sencilla: con todo lo que ya he publicado, ¿puedo saber de qué habla realmente mi contenido y compararlo con lo que la gente busca alrededor de ese territorio?

El sistema analiza newsletters publicadas y busca gaps de entidades. Un gap, en este contexto, **no es simplemente una keyword que tiene volumen**. Es una entidad o tema con demanda externa que está cerca de tu territorio, pero que tu contenido cubre poco o nada.

La diferencia importa. **Si solo miras keywords, puedes acabar persiguiendo volumen suelto.** Si miras entidades, cobertura y territorio, puedes tomar decisiones editoriales más defendibles.

El flujo del sistema fue este:

1.

Primero se ingiere el contenido publicado y se convierte en una tabla de posts.

2.

Después, un script extrae entidades con Google Natural Language.

3.

Otro paso limpia menciones irrelevantes y normaliza datos.

4.

Un agente cura entidades leyendo el brief del proyecto.

5.

Un script consulta Google Trends alrededor del territorio.

6.

Otro script cruza demanda externa con cobertura interna.

7.

Un agente convierte los gaps en backlog editorial.

8.

Otro agente redacta un informe usando solo la evidencia generada.

Fíjate en el patrón: **la IA no hace todo**. La IA entra donde hace falta criterio. El código entra donde hace falta repetibilidad.

---

## Qué hizo cada pieza en el caso real

En Think&Hack, el sistema analizó **37 newsletters publicadas**. La extracción inicial encontró **10.068 menciones de entidades en bruto**. Después de la limpieza objetiva quedaron **1.791 menciones y 839 entidades únicas**.

Hasta aquí, la IA no tenía que opinar demasiado. Había que extraer, limpiar y ordenar datos. **Esa parte es aburrida, pero sostiene todo lo demás.**

Después entró el agente` `entity-curator`.` **Su trabajo no era "hacer SEO"**, sino responder una pregunta concreta: de todas esas entidades, ¿cuáles pertenecen al territorio real de Think&Hack?

Ese agente trabajó contra un brief. El brief decía que Think&Hack habla de IA generativa aplicada a procesos, productividad, contenido, SEO/GEO, prompting, memoria, agentes y automatización. También definía **anti-territorio: sentidos que parecen relevantes, pero no lo son**.

Por ejemplo, "memoria" puede significar memoria de contexto en un LLM, pero también RAM, una canción o cualquier otro sentido que Google Trends arrastre. "Agentes" puede significar agentes de IA, pero también agentes inmobiliarios, forestales o de Hacienda. Sin anti-territorio, el sistema podría interpretar ruido como oportunidad.

Después de esa curación, quedaron **66 entidades dentro del territorio real**. A partir de 17 semillas consultadas en Google Trends, el sistema detectó **354 gaps: 172 en crecimiento y 182 consolidados**.

[

![imagen](https://substackcdn.com/image/fetch/$s_!X9oq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F50e137c5-28a6-430c-bf24-f3db57a94e8d_1600x900.jpeg)

](https://substackcdn.com/image/fetch/$s_!X9oq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F50e137c5-28a6-430c-bf24-f3db57a94e8d_1600x900.jpeg)

El resultado final **no fue una lista de ideas generadas por IA**, sino dos entregables conectados con evidencia: `editorial_backlo`.csv` e `informe.md`.`

**El informe:** [https://github.com/seoutopico/ai-entity-gap-seo/blob/main/projects/think-hack/outputs/informe.md](https://github.com/seoutopico/ai-entity-gap-seo/blob/main/projects/think-hack/outputs/informe.md)

---

## El aprendizaje importante: un gap no es una orden de publicar.

Este punto es clave. **Un gap no es automáticamente una buena idea de contenido.**

Puede haber demanda y aun así no convenirte. Puede ser una búsqueda demasiado genérica, una polisemia, una intención que no encaja con tu audiencia o una entidad donde no tienes autoridad suficiente. **Publicar sobre todo lo que tiene volumen no es estrategia; muchas veces es dispersión.**

Por eso el agente `gap-strategist` no recibía la orden de "escribe sobre todos los gaps". Recibía algo más concreto: leer `gaps.csv`, leer las entidades ya cubiertas, leer el brief y **convertir solo lo relevante en backlog editorial**.

En el caso de Think&Hack, la oportunidad más clara fue Claude Code. No salió de una intuición, sino de cruzar cobertura interna con demanda externa. El corpus ya mencionaba Claude Code en 4 posts, así que había una base real de autoridad, pero alrededor aparecía demanda no cubierta: `what is claude code`, `claude code agents`, `claude code mcp`, `claude code documentation`, `claude code pricing` y `codex vs claude code`.

Eso ya no es "la IA me ha dado ideas". Es una lectura editorial basada en señales: **hay entidad, hay cobertura previa, hay demanda externa y hay un cluster posible**.

La recomendación no fue publicar una pieza suelta sobre IA, sino **construir una arquitectura**: una guía práctica para no desarrolladores, una pieza sobre agents, otra sobre memoria de contexto, una comparativa con Codex, una guía sobre MCP y una pieza sobre precios. Esa diferencia es la que separa una lista de ocurrencias de una estrategia editorial.

---

## El arnés: cómo evitar que la IA cierre en falso

La parte más importante del sistema no es la extracción de entidades ni el backlog. **La parte más importante es el arnés de verificación.**

[

![imagen](https://substackcdn.com/image/fetch/$s_!LCPt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2347a60-1e9c-4bef-9d3a-cbf9651a56fd_1600x900.jpeg)

](https://substackcdn.com/image/fetch/$s_!LCPt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2347a60-1e9c-4bef-9d3a-cbf9651a56fd_1600x900.jpeg)

El arnés aplica una regla de **Default-FAIL**: una fase no está hecha porque la IA diga que está hecha. **Está hecha si existe la evidencia en disco, con las columnas correctas, con contenido y sin fases anteriores saltadas.**

Esto parece un detalle técnico, pero **cambia completamente el incentivo**. Si el criterio de éxito es "dime que has terminado", el modelo puede responder que ha terminado. Si el criterio de éxito es "existe este CSV con estas columnas exactas y `bin/check.py` pasa", la conversación cambia.

En el repo, una fase marcada como completada solo se acepta si su archivo existe y respeta el contrato. Si el estado dice que la fase está hecha pero falta el CSV, el check falla. Si las columnas no coinciden, el check falla. Si una fase posterior está marcada como hecha sin que una anterior tenga evidencia, el check falla.

Esta es la frase que resume la idea:

**No escribas más reglas. Haz que el atajo no compile.**

Los modelos optimizan hacia el criterio de éxito que les damos. **Si el atajo puntúa igual que el camino correcto, tenderán a elegir el atajo.** No por maldad, sino porque el sistema se lo permite. El arnés hace que el atajo deje de ser rentable.

---

## Cómo aplicar este marco a tu propio proceso SEO

Si quieres llevar esta idea a tu trabajo, **no necesitas empezar construyendo un repo entero**. Puedes empezar con una auditoría muy simple de tus flujos actuales.

Primero, **separa las tareas objetivas de las tareas cualitativas**. Si una tarea consiste en contar, cruzar, validar, limpiar o consultar datos, probablemente debería vivir en un script, una hoja bien estructurada o una automatización determinista. No hace falta gastar criterio de IA en algo que debe ser reproducible.

Después, **identifica dónde sí necesitas criterio**. Ahí la IA puede aportar mucho, pero conviene darle un rol estrecho. En vez de pedirle "haz una estrategia", pídele que clasifique entidades contra un brief, que detecte polisemia, que agrupe gaps por intención o que priorice oportunidades con una justificación explícita.

Luego, **escribe el brief**. Este paso suele parecer secundario, pero es lo que evita que la IA decida en abstracto. Un buen brief define el tema, la audiencia, las entidades núcleo, el tono, los límites y el anti-territorio. Sin brief, la IA interpreta "oportunidad" como algo genérico; con brief, puede evaluar si esa oportunidad tiene sentido para ti.

Por último, **define qué evidencia debe quedar**. Antes de lanzar el proceso, decide qué archivo, tabla, resumen o validación demostrará que la fase está hecha. No esperes al final para preguntar si te fías. Diseña desde el principio cómo vas a comprobarlo.

---

## La diferencia entre usar IA y construir un sistema

Sin IA, este proceso también se podría hacer. Podrías exportar contenido, revisar entidades, mirar Trends y priorizar un backlog manualmente, pero sería lento, irregular y difícil de repetir.

Con IA, aceleras las partes cualitativas: curar entidades, detectar polisemia, interpretar territorio, agrupar gaps y convertir oportunidades en decisiones editoriales. Pero eso solo funciona bien cuando **la IA no está sola**. Necesita datos, contratos, contexto y checks.

Ese es el cambio que me interesa. **La IA no sustituye el sistema; se vuelve útil cuando el sistema la contiene.**

Por eso creo que la conversación importante en SEO e IA no es "mira lo que me ha generado", sino "mira cómo sé que puedo fiarme de esto". El salto real no es pasar de no usar IA a usar IA. El salto real es pasar de **prompt -> respuesta** a **proceso -> evidencia -> decisión**.

En el primer modelo, la confianza depende de la fluidez del texto. **En el segundo, depende del rastro que deja el proceso.** Y en SEO eso importa mucho, porque el coste de una mala decisión editorial no siempre se ve al momento. Puedes publicar 30 piezas antes de darte cuenta de que estabas persiguiendo ruido.

La IA puede acelerar muchísimo ese error o puede ayudarte a verlo antes. **La diferencia no está en el prompt; está en el sistema.**

---

## Tools are great. Systems are better.

Las herramientas están muy bien, pero **las herramientas sueltas no crean criterio**. Puedes tener el mejor modelo, el mejor scraper, el mejor dashboard y el mejor generador de contenidos, y aun así no tener un sistema de decisión.

Un sistema define **qué entra, qué se transforma, quién decide, qué evidencia queda y qué pasa si algo falla**. Para mí, esa es la madurez que toca ahora con IA aplicada a SEO: no delegar a ciegas, no pedir estrategias completas a una caja negra y no confundir velocidad con mejora.

**El repo** que enseñé en la charla está aquí: [https://github.com/seoutopico/ai-entity-gap-seo](https://github.com/seoutopico/ai-entity-gap-seo)

No lo presento como una herramienta cerrada ni como "el método definitivo", sino como una forma de pensar. Cada equipo tendrá sus fuentes, sus límites, su autoridad y sus datos, pero la arquitectura mental sí es reutilizable: **scripts para lo objetivo, skills para el método, agentes para el criterio y evidencia para confiar**.

Si al leer esto has pensado "esto es justo lo que me falta cuando intento usar IA para SEO", probablemente conoces a alguien que también debería leerlo.

[Compartir](https://ainalluna.substack.com/p/seo-con-ia-agentes-sin-alucinar?utm_source=substack&utm_medium=email&utm_content=share&action=share)

## Recursos:

**El repo** : [https://github.com/seoutopico/ai-entity-gap-seo](https://github.com/seoutopico/ai-entity-gap-seo)

**El PPT: **[https://docs.google.com/presentation/d/1SczoGvEUj3kzYGuXZw6xpNDRcaJ71AngAdE_SMYNOeQ/edit?usp=sharing](https://docs.google.com/presentation/d/1SczoGvEUj3kzYGuXZw6xpNDRcaJ71AngAdE_SMYNOeQ/edit?usp=sharing)

***Cuéntamelo. Siempre leo todo.***

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

# **Suscríbete a Think&Hack**

**Tools are great. Systems are better.**

Casos reales, flujos que funcionan y formas concretas de usar la IA sin perder el control del proceso.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
