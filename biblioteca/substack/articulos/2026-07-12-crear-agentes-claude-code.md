---
id: 206658860
titulo: "Un agente, un subagente o un equipo: ¿qué necesitas realmente?"
subtitulo: "Cómo empezar a usar agentes en Claude Code, crear uno reutilizable y decidir cuándo varios pueden trabajar mejor juntos."
fecha: 2026-07-12
url: https://ainalluna.substack.com/p/crear-agentes-claude-code
tipo: newsletter
audiencia: everyone
estado: completo
huella: 3b1e4d7ccee8568836b5aba9b592713fbd164c47c54815a9498968ef7b3eb911
---

*Tres niveles de delegación para saber cuándo basta un agente puntual, cuándo conviene guardar uno y cuándo tiene sentido formar un equipo.*

[

![imagen](https://substackcdn.com/image/fetch/$s_!Vx6F!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2cdbcd6a-2e16-433f-bfba-ec78b4218795_1536x1024.png)

](https://substackcdn.com/image/fetch/$s_!Vx6F!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2cdbcd6a-2e16-433f-bfba-ec78b4218795_1536x1024.png)

¿Cómo estás?

Soy Aina y esto es Think&Hack.

La semana pasada escribí sobre [cómo crear una skill para que un agente tome mejores decisiones](https://ainalluna.substack.com/p/crear-skills-agentes-ia-verificables). La pregunta central era: **¿cómo hago para que el agente no improvise cada vez?**

Esta semana quiero subir un nivel.

Una skill guarda una forma de trabajar. Pero ¿quién hace el trabajo? ¿La conversación principal? ¿Otro agente al que delegas una parte? ¿Un agente especializado que dejas preparado para volver a usarlo? ¿Un equipo entero?

Cuando empezamos a hablar de agentes, es fácil imaginar una organización en miniatura: un coordinador, varios especialistas, un revisor y quizá otro agente que vigila al revisor. Suena avanzado. También puede ser una manera muy cara de hacer algo que una sola sesión resolvía bien.

Por eso prefiero empezar con una distinción más sencilla: **en Claude Code no necesitas elegir entre “un agente” y “un sistema multiagente”. Puedes aumentar la delegación a medida que el trabajo lo justifica.**

Voy a usar el mismo ejemplo durante toda la newsletter: tienes notas de una entrevista, fragmentos de una transcripción y varias ideas sueltas. Antes de escribir, quieres convertir ese material en un brief editorial con objetivo, audiencia, ángulo, evidencias, huecos y siguiente paso.

No hace falta saber programar para entender el problema. Solo hay que decidir quién debe leer el material, qué debe devolver y cuánto de ese comportamiento merece conservarse.

---

## Antes de crear uno: ¿qué es un agente en Claude Code?

La **conversación principal de Claude Code ya funciona como un agente**: recibe un objetivo, lee contexto, utiliza herramientas, observa sus resultados y decide el siguiente paso. No se limita a producir una respuesta de una vez; puede avanzar por una tarea y ajustar el camino según lo que encuentra.

Un **subagente** es una delegación dentro de esa sesión. Trabaja en su propia ventana de contexto y devuelve el resultado a quien lo llamó. Esto resulta útil cuando una investigación va a leer muchos archivos, generar mucho ruido o necesita unas instrucciones y herramientas diferentes de las de la conversación principal.

La diferencia con una skill es importante:

-

Una **skill** incorpora conocimiento o un procedimiento reutilizable a una conversación.

-

Un **subagente** recibe trabajo en un contexto separado y devuelve su resultado.

-

Un **agent team** coordina varias sesiones independientes que pueden repartirse tareas y comunicarse entre sí.

No son tres versiones de lo mismo. Resuelven problemas distintos.

Para saber si una tarea merece un agente, miraría cinco cosas: **qué objetivo tiene, qué contexto necesita, qué herramientas puede usar, qué decisiones debe tomar y cuándo debe detenerse**. Si solo quieres aplicar unas instrucciones para obtener siempre el mismo tipo de resultado, probablemente basta con una skill. En cambio, si puedes separar la tarea del resto de la conversación, darle unas fuentes concretas y pedirle que investigue, tome decisiones y vuelva con una conclusión, entonces empieza a tener sentido delegarla a un agente.

---

## Nivel 1: un agente puntual para una tarea concreta

La forma más pequeña de delegación no exige crear ningún archivo. **Puedes pedirle a Claude Code que lance un subagente para una tarea puntual:**

```
Lanza un subagente para leer las notas de entrevista de la carpeta notas/.
Quiero que identifique el tema central, las afirmaciones que tienen evidencia,
las dudas que habría que verificar y tres posibles ángulos.
No escribas todavía la pieza. Devuélveme solo los hallazgos relevantes.
```

Claude Code dispone de subagentes integrados para explorar, planificar o resolver tareas generales. El trabajo de lectura ocurre fuera del contexto principal y vuelve resumido. Tú no has creado todavía un nuevo trabajador permanente: has delegado una misión de una sola vez.

**Este nivel encaja cuando el trabajo es autocontenido y no sabes si volverás a necesitarlo.** También sirve para probar una idea antes de convertirla en arquitectura. Si el encargo cambia cada semana, guardar un agente especializado demasiado pronto puede darte más mantenimiento que valor.

El prompt necesita algo más que “investiga estas notas”. Conviene especificar:

-

qué material puede consultar;

-

qué pregunta debe resolver;

-

qué no debe hacer;

-

qué resultado tiene que devolver.

En nuestro ejemplo, el **límite “no escribas todavía la pieza”** evita que el agente salte desde la investigación a la redacción. El formato de salida ayuda a que la conversación principal reciba una síntesis utilizable, no todo el recorrido del subagente.

[

![imagen](https://substackcdn.com/image/fetch/$s_!DPrP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa720cdaa-9491-4ac7-a07e-ea7ded96891d_847x480.png)

](https://substackcdn.com/image/fetch/$s_!DPrP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa720cdaa-9491-4ac7-a07e-ea7ded96891d_847x480.png)

Este primer nivel también sirve para detectar tareas que se repiten. Si cada semana acabas pidiendo “lee estas notas, separa la evidencia de las hipótesis y propón un ángulo”, ya no estás ante un encargo puntual. **En lugar de volver a escribir o retocar el mismo prompt, puede tener sentido convertir esas instrucciones en un agente especializado que puedas reutilizar.**

---

## Nivel 2: un agente especializado que puedes volver a usar

Cuando la misma delegación se repite, **puedes crear un custom agent**. En Claude Code es un archivo Markdown dentro de una de estas carpetas:

```
.claude/agents/brief-curator.md     → disponible en ese proyecto
~/.claude/agents/brief-curator.md   → disponible en todos tus proyectos
```

La versión mínima tiene una cabecera YAML y un cuerpo de instrucciones:

```
---
name: brief-curator
description: Convierte notas de entrevista, fragmentos de transcripción,
  investigación e ideas sueltas en un brief editorial con objetivo,
  audiencia, ángulo, evidencias, huecos y siguiente paso. Úsalo antes
  de redactar. No lo uses para resumir, escribir la pieza final ni publicar.
tools: Read, Grep, Glob
---

Eres responsable de convertir material editorial disperso en un brief
accionable. No escribas la pieza final.

1. Lee solo las fuentes que indique el encargo.
2. Identifica el objetivo y la audiencia.
3. Formula un ángulo explícito que no sea un resumen del material.
4. Separa hechos, interpretaciones y huecos de información.
5. Termina con un único siguiente paso.

Devuelve estas secciones:

# Brief editorial
## Objetivo
## Audiencia
## Ángulo
## Evidencias
## Huecos y riesgos
## Siguiente paso
```

``name` `identifica al agente. ``description` `le dice a Claude cuándo debe delegar en él. El cuerpo define cómo trabaja. Y ``tools`` recorta sus capacidades: este agente puede leer y buscar, pero no escribir archivos ni publicar nada.

Puedes pedirle a Claude Code que cree el archivo por ti:

```
Crea un subagente de proyecto llamado brief-curator en .claude/agents/.
Debe convertir material editorial disperso en un brief, trabajar en modo
solo lectura y detenerse antes de redactar o publicar. Antes de terminar,
enséñame el archivo y explica por qué le has dado esas herramientas.
```

[

![imagen](https://substackcdn.com/image/fetch/$s_!VVZk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3daedd35-f9e9-4da0-969e-0831c25bd521_1319x814.png)

](https://substackcdn.com/image/fetch/$s_!VVZk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3daedd35-f9e9-4da0-969e-0831c25bd521_1319x814.png)

Después no des el trabajo por bueno porque el archivo tenga buen aspecto. Pruébalo.

**Prueba positiva:**

```
Usa el agente brief-curator para preparar el enfoque de estas notas antes de redactar.
```

**Prueba cercana que no debería activarlo:**

```
Resume esta transcripción en tres frases.
```

[

![imagen](https://substackcdn.com/image/fetch/$s_!HpaB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F73dc525d-e44a-4cd0-8b24-030a42ea57c2_735x609.png)

](https://substackcdn.com/image/fetch/$s_!HpaB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F73dc525d-e44a-4cd0-8b24-030a42ea57c2_735x609.png)

**Prueba de límite:**

```
Usa brief-curator para escribir el artículo final y publicarlo.
```

El primer caso debería devolver el brief. El segundo no debería convertirse en un brief porque has pedido un resumen. En el tercero, el agente debería mantenerse dentro de su función y no publicar ni redactar la pieza final.

Aquí aparece la misma disciplina que vimos con las skills: **no evalúes solo si el resultado está bien escrito. Evalúa si el agente entra cuando toca, se queda fuera cuando no toca y respeta sus límites.**

**La skill **``decision-brief` `**de la semana pasada todavía puede tener un papel. Si las notas contienen una decisión implícita, *****`brief-curator` *****puede usar esa skill para aclararla.** El agente decide cuándo necesita esa capacidad; la skill define cómo ejecutarla. No hace falta copiar el procedimiento de la skill dentro del agente.

---

## Nivel 3: un equipo de agentes que necesita coordinarse

Un **agent team no es “muchos subagentes”**. Es un conjunto de sesiones independientes: hay una sesión líder, varios teammates y una lista compartida de tareas. Los miembros pueden comunicarse entre sí, no solo devolver un informe al agente principal.

En nuestro ejemplo, un equipo podría tener una persona-agente investigando las fuentes, otra defendiendo la perspectiva del lector y otra comprobando afirmaciones y huecos. La sesión líder reuniría sus hallazgos y resolvería los desacuerdos.

```
Crea un equipo de agentes para preparar el brief editorial de esta investigación.
Un teammate revisará las fuentes y la evidencia; otro analizará qué necesita
entender un lector no técnico; un tercero buscará afirmaciones débiles,
repeticiones y huecos. Quiero que contrasten sus hallazgos antes de que
la sesión líder proponga el ángulo final.
```

[

![imagen](https://substackcdn.com/image/fetch/$s_!Y6FL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff81d0b8c-f005-475f-b5b9-7118baa980f0_1003x919.png)

](https://substackcdn.com/image/fetch/$s_!Y6FL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff81d0b8c-f005-475f-b5b9-7118baa980f0_1003x919.png)

**¿Aporta algo frente a lanzar tres subagentes y reunir sus respuestas?** Solo si esos trabajadores necesitan **compartir hallazgos, discutirlos o reajustar su trabajo**. Si cada uno puede resolver su parte y devolver una síntesis al principal, los subagentes suelen ser suficientes.

Esta diferencia evita mucho teatro organizativo. Lanzar un equipo de agentes tiene sentido cuando el trabajo se puede dividir en frentes relativamente independientes y la colaboración entre ellos mejora la decisión. Añade coste de tokens, coordinación, latencia y más lugares donde puede perderse información.

Además, en Claude Code los `agent teams` siguen marcados como experimentales y están desactivados por defecto. No los usaría como punto de partida para un lector que está creando su primer agente. **Primero demuestra que una delegación simple mejora el trabajo. Después convierte el patrón repetido en un agente especializado. Solo crea un equipo cuando exista una necesidad real de coordinación entre sesiones.**

---

## No elijas por lo impresionante que parece

Los tres niveles se pueden resumir con una pregunta: **¿qué problema de trabajo estás intentando resolver?**

Si necesitas apartar una investigación de la conversación principal, lanza un `subagente puntual.` Si repites la misma delegación y quieres conservar instrucciones, herramientas y límites, crea un `custom agent.` Si varias líneas de trabajo deben avanzar de forma independiente y comunicarse entre sí, valora un `agent team.`

También hay tareas que no necesitan ninguno. Una corrección breve que depende de todo lo hablado en la conversación puede quedarse en la sesión principal. Un procedimiento repetible puede ser una skill. Una validación mecánica puede vivir en un script o un hook.

**Un sistema no mejora por añadir más agentes. Dividir el trabajo solo aporta valor cuando resuelve un problema concreto:** evita llenar la conversación principal de información innecesaria, limita permisos, permite reutilizar instrucciones, separa perspectivas diferentes o ejecuta en paralelo tareas que realmente son independientes.

Por eso, antes de crear un agente, respondería estas cinco preguntas:

1. **¿Qué trabajo exacto voy a delegar?**

2. **¿Qué contexto necesita y cuál no necesita ver?**

3. **¿Qué herramientas debe poder usar y cuáles conviene quitarle?**

4. **¿Qué resultado debe devolver a la sesión principal?**

5. **¿Cómo comprobaré que ha terminado bien y no solo que ha respondido?**

Si no puedes responderlas, añadir agentes no aclarará el sistema. Solo repartirá la ambigüedad.

**Tools are great. Systems are better.**

Un agente puntual te ayuda a delegar. Un agente especializado te ayuda a repetir. Un equipo te ayuda a coordinar. El salto importante no es pasar de uno a muchos. Es pasar de pedir “haz esto” a diseñar **quién recibe el trabajo, con qué límites y qué evidencia debe devolver**.

---

## Sigue la serie: de prompts a sistemas.

Esta newsletter continúa la serie que empecé explicando cómo crear una skill.

Una skill conserva el procedimiento. Un agente recibe un trabajo, utiliza contexto y herramientas, toma decisiones y devuelve un resultado. Entender esta diferencia ayuda a elegir qué necesitas antes de empezar a añadir piezas.

---

---

## Recursos

- [Claude Code Docs: Create custom subagents](https://code.claude.com/docs/en/sub-agents)

- [Claude Code Docs: Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams)

- [Claude Code Docs: Extend Claude Code](https://code.claude.com/docs/en/features-overview)

- [Anthropic: Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)

- [Think&Hack: Cómo crear una skill para que tu agente tome mejores decisiones](https://ainalluna.substack.com/p/crear-skills-agentes-ia-verificables)

***Cuéntamelo. Siempre leo todo.***

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

# **Suscríbete a Think&Hack**

**Tools are great. Systems are better.**

Casos reales, flujos que funcionan y formas concretas de usar la IA sin perder el control del proceso.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
