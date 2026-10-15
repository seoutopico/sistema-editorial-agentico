---
id: 205019542
titulo: "Cómo crear una skill para que tu agente tome mejores decisiones."
subtitulo: "Qué debe ir en la skill, qué debe quedar fuera y cómo saber si realmente mejora el resultado."
fecha: 2026-07-05
url: https://ainalluna.substack.com/p/crear-skills-agentes-ia-verificables
tipo: newsletter
audiencia: everyone
estado: completo
huella: 1ec49ffae6bc19bc99dc94bc4ffcd14fa1e6211afcaa33d47fd3b90796c9bd7b
---

*Cómo diseñar una skill pequeña, activable y verificable sin convertirla en otra carpeta de documentación.*

[

![imagen](https://substackcdn.com/image/fetch/$s_!6z-o!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcdaa308c-0c87-4a40-8ce7-311725b33bdb_1672x941.png)

](https://substackcdn.com/image/fetch/$s_!6z-o!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcdaa308c-0c87-4a40-8ce7-311725b33bdb_1672x941.png)

¿Cómo estás?

Soy Aina y esto es Think&Hack.

Estos días estoy preparando el módulo de skills de un curso de IA aplicada para una escuela de negocios.

Cuando estaba preparando el tema, me di cuenta de una cosa: una skill casi nunca falla porque alguien no sepa escribir Markdown. Falla antes, cuando la usamos como carpeta de instrucciones y no como una forma de cambiar cómo trabaja un agente.

Me he traído esta parte del módulo porque esa confusión aparece enseguida cuando intentas pasar de prompts sueltos a procesos con IA.

La pregunta es sencilla:

**¿Cómo hago para que el agente no improvise cada vez? **

Una buena skill no organiza información. Cambia una conducta del agente bajo condiciones concretas. Decide cuándo se activa, qué tarea resuelve, qué deja fuera, qué recursos consulta y cómo se comprueba que ha funcionado.

Si quieres llevar la IA a procesos reales, con agentes, skills y sistemas verificables, escríbeme. Estoy preparando más formaciones y acompañamientos sobre esto.

Vamos a verlo con un ejemplo pequeño: una skill para trabajar con notas de reuniones.

---

## El error: “ayuda con reuniones”

Imagina que quieres crear una skill para trabajar mejor con notas de reuniones.

La versión mala:

```
---
name: meeting-helper
description: Ayuda con reuniones.
---
```

Y en el cuerpo del archivo:

```
# Meeting helper

Resume reuniones de forma clara.
Extrae acuerdos.
Sé conciso.
Organiza la información.
Incluye próximos pasos.
```

**Suena razonable. También es demasiado amplia.**

¿Tiene que hacer un acta completa? ¿Una agenda? ¿Un resumen ejecutivo? ¿Una lista de tareas? ¿Un documento de decisión? ¿Debe inferir acuerdos implícitos? ¿Puede crear responsables si no aparecen? ¿Debe activar cuando alguien pida tickets?

El agente no lo sabe.

Y si el agente no lo sabe, decidirá por aproximación. A veces acertará. A veces no. Lo peligroso es que muchas veces sonará bien aunque haya elegido mal.

Yo prefiero empezarlo por otro lado: no crear “una skill para reuniones”, sino acotar una tarea mucho más concreta:

```
Convertir notas de reunión, conversación o discusión técnica en un brief de decisión.
```

Con este cambio, la skill` decision-brief` no intenta gestionar reuniones. Acota una tarea más pequeña y más útil: c**onvertir una conversación con mucho texto en una decisión clara, con opciones, riesgos y siguiente acción.**

---

## ¿Qué es técnicamente una skill?

Una skill es una carpeta autocontenida. La unidad mínima es esta:

```
decision-brief/
└── SKILL.md
```

Una versión más completa puede tener archivos de apoyo:

```
decision-brief/
├── SKILL.md
├── references/
│   └── decision-quality-rubric.md
├── assets/
│   └── brief-template.md
└── scripts/
    └── check-brief-structure.py
```

**SKILL.md **es el archivo obligatorio. Dentro tiene dos partes.

La primera es la **cabecera YAML**: unas líneas entre `---` que` el agente` lee como configuración. Ahí viven campos como `name` y `description`.

```
---
name: decision-brief
description: Usa esta skill cuando el usuario necesite convertir notas desordenadas en un brief de decisión.
---
```

La segunda parte es el cuerpo en **Markdown**. Ahí escribes el procedimiento, el formato de salida, los límites y las comprobaciones.

```
# Decision brief

Usa esta skill para convertir material desordenado de conversación en un brief breve de decisión.

## Procedimiento

1. Lee las notas con mirada orientada a decisión.
2. Separa contexto, opciones, decisión, riesgos y siguiente acción.
3. Si la decisión no está sostenida por las notas, dilo.
4. No inventes responsables, fechas ni compromisos.
5. Revisa la salida antes de terminar.
```

-

**references/ **sirve para conocimiento que no hace falta leer siempre: una rúbrica larga, reglas internas, documentación o ejemplos extensos.

-

**assets/ **sirve para materiales de salida: una plantilla oficial, un formato corporativo o un archivo base.

-

**scripts/** sirve para operaciones mecánicas: validar columnas, comprobar secciones, transformar datos o detectar errores repetibles.

**No hace falta crear todas esas carpetas en cada skill.** Lo importante es decidir qué papel cumple cada pieza: lo que el agente necesita siempre va en `SKILL.md`; lo que solo necesita a veces va en `references/`; las plantillas van en `assets/`; y las comprobaciones repetibles van en `scripts/`.

---

## ¿Cómo sabe el agente si debe usar la skill?

Aquí conviene bajar al detalle. Una skill no se activa por magia: **el entorno donde trabajas la descubre y la pone a disposición del agente.**

En **Codex**, una skill de proyecto puede vivir en:

```
.agents/skills/decision-brief/SKILL.md
```

**Codex **también puede leer skills personales desde:

```
$HOME/.agents/skills/decision-brief/SKILL.md
```

En **Claude Code**, una skill de proyecto vive en:

```
.claude/skills/decision-brief/SKILL.md
```

Y una personal en:

```
~/.claude/skills/decision-brief/SKILL.md
```

A partir de ahí hay cuatro situaciones.

**1. Invocación automática.** El agente no lee todas las skills completas desde el principio. Primero ve una lista resumida con señales como el `nombre `y la` description`. Si la petición encaja con una de ellas, entonces carga esa skill completa.

**2. Invocación explícita.** Tú puedes forzar una skill por su nombre. En **Codex **puedes escribir `$decision-brief` o abrir `/skills`. En **Claude Code** puedes usar `/decision-brief. `En este caso no esperas a que el agente la sugiera: la llamas directamente.

**3. Bloqueo de invocación automática.** Hay skills que no quieres que el agente elija por su cuenta. En **Codex **puedes añadir un archivo `agents/openai.yaml `dentro de la carpeta de la skill:

```
policy:
  allow_implicit_invocation: false
```

Con eso, **Codex **no debería elegir esa skill solo porque la petición se parezca a la descripción. Seguiría disponible si la llamas de forma explícita.

En **Claude Code**, la misma intención puede declararse en la cabecera YAML:

```
---
name: decision-brief
description: Convierte notas desordenadas en un brief de decisión.
disable-model-invocation: true
---
```

Eso significa: el usuario puede llamarla, pero **Claude **no debería cargarla por decisión propia.

**4. Desactivación.** Si una skill ya no debe estar disponible, no basta con retocarla `description`. Puedes sacarla de las carpetas que **Codex **descubre, desinstalarla si venía empaquetada o dejarla instalada pero apagada desde `~/.codex/config.toml`:

```
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```

En **Claude Code** puedes ocultarla con `skillOverrides`, por ejemplo, marcándola como `"off"` en la configuración local.

Esto es lo práctico: **carpeta descubierta para que exista, **`description `**clara para que el agente pueda elegirla, nombre explícito para forzarla y política de invocación para controlar cuándo no debe entrar sola.**

Ahora sí se entiende por qué la `description `es tan importante.

---

## La `description` del skill

La `description` no resume la skill. Le dice al agente cuándo debe usarla y cuándo no.

**Una mala descripción** dice:

```
description: Ayuda con reuniones.
```

**Una buena descripción** dice qué intención cubre, qué entradas espera, qué salida produce y qué tareas cercanas quedan fuera.

En el ejemplo de `decision-brief`, podría quedar así:

```
---
**name:** decision-brief
description: Usa esta skill cuando el usuario necesite convertir notas de reunión, conversaciones, hilos de chat o apuntes técnicos desordenados en un brief de decisión con contexto, opciones, decisión, riesgos y siguiente acción. Úsala cuando la decisión pueda ser explícita, implícita o todavía no esté sostenida por evidencia suficiente. No la uses para actas completas, registros legales, planes de proyecto, creación de tickets ni resúmenes genéricos.
---
```

**Fíjate en la diferencia: no promete “ayudar con reuniones”. Dice qué trabajo hace y qué trabajos parecidos quedan fuera.**

Por ejemplo, esta skill debería activarse cuando la **petición apunta a una decisión**:

Sácame la decisión, los riesgos y el siguiente paso de estas notas.

O cuando el usuario ya sospecha que **hubo una decisión**, pero necesita ordenarla:

`Esta conversación terminó en una decisión implícita. Ordénala para compartirla.`

En cambio, **NO** debería activarse si la **petición pide otro tipo de trabajo**:

`Hazme un acta completa con asistentes, agenda y todos los acuerdos. Convierte esto en tickets para Jira.`

La prueba es simple: escribe ejemplos en los que la skill debería entrar y ejemplos parecidos en los que debería quedarse fuera. Si no puedes distinguir unos de otros, la skill todavía está demasiado poco definida.

## Las instrucciones: qué hace el agente cuando la skill se activa

La `description `ayuda a decidir si la skill debe activarse. El cuerpo en Markdown explica qué tiene que hacer el agente a partir de ahí.

En esa parte conviene **escribir solo las instrucciones que necesita siempre**: el procedimiento, los criterios de decisión, el formato de salida y las comprobaciones básicas.

Para `decision-brief,` el núcleo podría ser:

```

## Procedimiento
1. Lee el material con mirada orientada a decisión.
2. Clasifica el estado de la decisión: explícita, implícita o no sostenida por las notas.
3. Extrae solo el contexto necesario.
4. Lista opciones relevantes, no todos los comentarios.
5. Escribe la decisión o declara que no hay evidencia suficiente.
6. Recoge riesgos y dudas sin inventar.
7. Termina con una siguiente acción concreta si aparece en las notas.
8. Valida el brief antes de cerrarlo.
```

El formato de salida también puede ir en el cuerpo de la skill si forma parte del comportamiento habitual:

```
# Decision brief
## Contexto
## Opciones consideradas
## Decisión
## Riesgos y dudas
## Siguiente acción
```

Los materiales que no hacen falta en cada uso deberían ir aparte.

-

Un documento con criterios de revisión puede ir en `references/,` y el `SKILL.md` debe indicar cuándo consultarlo.

-

Si tu organización usa un modelo fijo de brief, ese archivo puede ir en `assets/.`

-

Si hay una validación que se puede automatizar, puede ir en `scripts/.`

**La regla práctica es esta:** `la description`** **ayuda a activar la skill, el Markdown guía el trabajo y los archivos de apoyo se consultan solo cuando aportan algo a esa tarea.

---

## Cuando una skill intenta hacer demasiado

Una skill también se estropea por exceso.

Pasa cuando el `SKILL.md`** intenta contenerlo todo**: teoría, procedimiento, ejemplos largos, plantillas, casos históricos, excepciones, notas de mantenimiento y deseos de calidad. Hay mucho material, pero poca prioridad.

También pasa cuando l**a skill cubre demasiadas fases**. Si `decision-brief` empieza a crear tickets, actualizar un plan, redactar un correo, programar seguimiento y decidir por el equipo, ya no es una skill pequeña. Es un proceso entero comprimido en un archivo.

El problema es que el agente puede ver demasiado pronto el formato final y correr hacia él sin hacer bien el razonamiento previo.

Por ejemplo, si `decision-brief` contiene a la vez **instrucciones para leer notas, plantilla final, ejemplos largos, reglas de calidad, casos especiales, pasos para crear tickets y pasos para mandar un email**, el agente puede saltar demasiado rápido a **“generar un brief” **y dedicar menos atención a lo importante: **separar decisión, opciones, riesgos y evidencia.**

La solución no siempre es escribir más instrucciones. A veces es **dividir:**

```
decision-brief       -> aclara la decisión
decision-to-tickets  -> convierte una decisión validada en tareas
stakeholder-update   -> prepara comunicación para el equipo
```

Antes de cerrar una skill, revisa cada frase con esta pregunta:

**¿Esto cambia alguna decisión del agente?**

1.

**¿Le dice cuándo debe activarse la skill?** => Se queda.

2.

**¿Ordena los pasos que debe seguir el agente?** => Se queda.

3.

**¿Marca qué debe evitar?** => Se queda.

4.

**¿Indica qué recurso consultar y cuándo?** => Se queda.

5.

**¿Explica cómo revisar la salida?** => Se queda.

6.

**¿Suena bien, pero no cambia lo que el agente hará?** => Probablemente sobra.

---

## Cinco preguntas antes de escribir una skill

Antes de cerrar una skill, revisa cada frase con esta pregunta:

-

**¿Qué tarea repetida quieres mejorar?** => Convertir notas desordenadas en un brief de decisión.

-

**¿Qué hace mal el agente sin skill?** => Resume demasiado, mezcla opciones con decisiones o inventa responsables.

-

**¿Qué criterio experto debe aplicar?** => Leer buscando decisión, opciones, riesgos, evidencia y siguiente acción.

-

**¿Cuándo no debe activarse?** => Cuando se piden actas completas, tickets, planes de proyecto, registros legales o resúmenes genéricos.

-

**¿Qué error debe evitar?** => Convertir cualquier conversación en un resumen bonito pero poco útil.

Después viene la prueba incómoda: lanza la misma petición con y sin skill.

Si la salida es igual, la skill no aporta. Si solo está más ordenada, tampoco basta.

Una skill empieza a tener sentido cuando evita un error que antes ocurría. En `decision-brief`, ese error es claro: inventar decisiones, esconder la falta de evidencia o mezclar contexto, opciones, riesgos y siguiente acción.

**Eso ya empieza a ser sistema.**

**Tools are great. Systems are better.**

Por eso vuelvo al punto de partida: una skill no falla porque alguien no sepa escribir Markdown.

Falla cuando no hemos decidido qué comportamiento queremos cambiar.

Si la skill solo guarda instrucciones, el agente seguirá improvisando con mejor envoltorio. Si la skill define cuándo activarse, qué tarea resolver, qué dejar fuera y cómo comprobar la salida, entonces empieza a parecerse a un sistema.

Y esa es la parte que más me interesa llevar a equipos y formaciones: pasar de usar IA como una colección de herramientas sueltas a diseñar procesos que aguantan el uso real.

[Compartir](https://ainalluna.substack.com/p/crear-skills-agentes-ia-verificables?utm_source=substack&utm_medium=email&utm_content=share&action=share)

---

## Sigue la serie: de prompts a sistemas

Esta newsletter es la primera parte de una serie sobre cómo pasar de prompts sueltos a sistemas de trabajo con IA.

Aquí hemos visto cómo crear una skill para conservar una forma de trabajar. En la siguiente entrega explico **cuándo conviene mantener la tarea en la conversación, cuándo crear un agente reutilizable y cuándo varios agentes pueden trabajar mejor juntos**.

---

---

## Recursos

-

[OpenAI Developers: Agent Skills en Codex](<https://developers.openai.com/codex/skills>)

-

[Claude Code Docs: Extend Claude with skills](<https://code.claude.com/docs/en/skills>)

-

[Agent Skills: overview del estándar abierto](<https://agentskills.io/home>)

-

[SkillJuror: Measuring How Agent Skill Organization Changes Runtime Behavior](<https://arxiv.org/abs/2606.11543>)

-

[Under the Hood of SKILL.md: Semantic Supply-chain Attacks on AI Agent Skill Registry](<https://arxiv.org/abs/2605.11418>)

-

[Think&Hack: Agentes de IA para SEO: procesos con evidencia](<https://ainalluna.substack.com/p/seo-con-ia-agentes-sin-alucinar>)

-

[Think&Hack: Cómo convertí mi inbox en un sistema verificable de agentes](<https://ainalluna.substack.com/p/como-converti-mi-inbox-en-un-sistema>)

***Cuéntamelo. Siempre leo todo.***

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

# **Suscríbete a Think&Hack**

**Tools are great. Systems are better.**

Casos reales, flujos que funcionan y formas concretas de usar la IA sin perder el control del proceso.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
