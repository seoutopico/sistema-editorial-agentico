# Crea tu sistema editorial con IA · Think&Hack

Soy **Aina Lluna**, creadora de [Think&Hack](https://ainalluna.substack.com/), donde comparto cómo aplico la IA a procesos de trabajo, con ejemplos y casos prácticos.

Este es el material de mi ponencia **«De chat a sistema: cómo las skills convierten la IA en tu equipo de marketing»**, para [ConIA Digital](https://conia.digital/), en Madrid, el 17 de octubre de 2026. Puedes consultar la [presentación de la ponencia](https://docs.google.com/presentation/d/18gthpXMVpU_P2g2LwNjFf7nDvIgb5ctnc1NFNk_2pHE/edit?slide=id.h7cfcbfaf388ee8c6_15_99#slide=id.h7cfcbfaf388ee8c6_15_99).

El punto de partida es el sistema editorial de Think&Hack. El método consiste en definir el proceso antes de construir: qué buscamos, qué información necesitamos, qué hace cada skill y qué decisiones conservamos las personas. Después construimos por etapas y comprobamos cada resultado. Aquí puedes aplicar ese método a tu propio caso, empezando por un sistema que llega hasta el documento madre.

Si quieres seguir mis pruebas y aprender a crear tus propios sistemas de IA, [lee y suscríbete a Think&Hack](https://ainalluna.substack.com/).

Este material te guía para diseñar y construir un sistema editorial adaptado a tu trabajo. Empiezas con dos archivos, respondes cinco preguntas y el agente crea tu arquitectura. Después lo construyes paso a paso.

El sistema seguirá este recorrido:

**Recuperar datos → analizar lo publicado → encontrar oportunidades → investigar y abrir nuevos ángulos → redactar un documento madre.**

El documento madre reúne la explicación, los hallazgos, ejemplos y fuentes para producir después newsletters, posts y otras piezas. La producción por canal y la voz de marca quedan para otro proceso.

## 1. Prepara tu proyecto

Descarga el repositorio y descomprime el ZIP si has usado esa opción. Para empezar necesitas estos dos archivos, con sus nombres originales:

- [README.md](README.md): este tutorial, las cinco preguntas y los mensajes para avanzar.
- [AGENTS.md](AGENTS.md): las instrucciones que guían al agente y sus criterios de revisión.

Elige dónde vas a trabajar:

### Con ChatGPT Work

Crea un proyecto y añade `README.md` y `AGENTS.md` a sus archivos o fuentes. Abre una conversación de Work dentro de ese proyecto. Si usas un proyecto local en la aplicación de escritorio, puedes vincular directamente la carpeta descargada. Los archivos subidos a un proyecto y una carpeta local son formas distintas de proporcionar contexto. [Guía oficial de proyectos de ChatGPT](https://learn.chatgpt.com/docs/projects?surface=app).

### Con Claude Code

Abre Claude, entra en **Code**, elige el entorno **Local** y selecciona la carpeta descargada. Los dos archivos deben estar en esa carpeta. Si ya utilizas Claude Code en otro entorno, abre allí la misma carpeta de trabajo. [Guía oficial de Claude Code en escritorio](https://code.claude.com/docs/en/desktop-quickstart).

## 2. Empieza la entrevista

Pega este mensaje:

```text
Lee README.md y empieza la entrevista guiada.
```

El agente debe leer también `AGENTS.md`, hacerte la primera pregunta y esperar tu respuesta. Te hará cinco preguntas, una a una, con ejemplos y opciones. No necesitas saber programar ni elegir tecnologías para responderlas.

![Arranque de la entrevista en Work: primera pregunta y respuesta de ejemplo](material_adicional/inicio-entrevista.png)

*Captura de la prueba de Aina: el agente inicia la entrevista y pasa a la segunda pregunta tras recibir la primera respuesta.*

Contesta con tu caso. Si no sabes qué elegir, díselo y el agente te ayudará a concretarlo. Si empieza a construir antes de terminar las preguntas, indícale: «Estamos en la entrevista. Continúa con la siguiente pregunta y espera mi respuesta».

Tienes las [respuestas de Think&Hack](material_adicional/RESPUESTAS-EJEMPLO.md) como referencia. Son opcionales: no necesitas subirlas ni usarlas para tu propio sistema.

## 3. Revisa tu arquitectura

Después de las cinco respuestas, el agente creará `ARQUITECTURA.md`. Este archivo **no viene incluido** porque se escribe con tus necesidades.

Debe explicar el recorrido, las fuentes, cómo recordará lo trabajado, las responsabilidades de las futuras skills y qué recibirás en el documento madre. El agente revisará los aspectos técnicos antes de entregarlo.

Tu revisión es práctica: ¿atiende a tu lector?, ¿usa tus fuentes?, ¿te ayuda con el trabajo que más te cuesta?, ¿el documento madre contiene lo que necesitas? Si algo no encaja, explícalo en el chat y pide corregir la arquitectura.

Conserva la versión revisada. Si trabajas con archivos subidos y el agente te entrega un archivo descargable, descárgalo y añade esa versión al proyecto para que esté disponible al continuar. Comprueba que solo se use la versión vigente.

## 4. Prepara la construcción

Cuando el diseño te encaje, pega:

```text
He revisado ARQUITECTURA.md y quiero preparar su construcción por etapas.
Lee también AGENTS.md y conserva el alcance acordado.

Presenta en el chat un plan breve y ordenado por dependencias. Para cada
etapa indica qué quedará funcionando y cómo se comprobará. Incluye tanto
las herramientas compartidas como las skills necesarias para usarlas.

Después redacta solo el prompt de la primera etapa, listo para copiar.
Debe indicar objetivo, alcance, entradas, entregables, comprobaciones
y cuándo detenerse. Distingue las pruebas locales de las comprobaciones
con fuentes reales. Comprueba qué permite hacer el entorno disponible
e indica cualquier requisito que falte antes de ejecutar.

No ejecutes el prompt ni generes todavía los siguientes. Mantén los
prompts de construcción en el chat, fuera de los archivos del proyecto.
```

Recibirás el plan y un único prompt de construcción. Para ejecutar y comprobar las etapas necesitarás un entorno que permita crear archivos y ejecutar las herramientas necesarias; el agente debe detectar sus posibilidades y carencias. Adjuntar documentos permite iniciar el diseño, pero no acredita acceso a tus cuentas ni a tu carpeta local.

## 5. Construye una etapa cada vez

Copia el prompt que acaba de generar el agente y envíalo precedido de:

```text
Ejecuta únicamente el siguiente prompt. Completa sus comprobaciones,
explica qué funciona y qué queda pendiente, y detente al terminar.
```

Cuando termine, revisa el resultado. Si quedan errores o requisitos necesarios sin resolver, pide corregirlos antes de continuar. Una prueba con datos ficticios no demuestra que el acceso a Substack o YouTube funcione: esos accesos se comprobarán en la etapa correspondiente.

Para preparar el siguiente paso, pega:

```text
Lee la arquitectura y revisa el estado real de lo construido.
Si la etapa anterior está completa y comprobada, redacta en el chat
únicamente el prompt de la siguiente etapa. Si falta algo necesario,
explica qué hay que resolver primero. No ejecutes todavía el prompt.
```

Repite el recorrido hasta completar las etapas. Si cambias de sesión, conserva la arquitectura y los archivos de trabajo; pide al agente que recupere el estado antes de continuar.

Cuando todas las etapas estén comprobadas, pide las instrucciones de uso del sistema y un primer recorrido con tus fuentes reales disponibles. Tú eliges la oportunidad que desarrollar y revisas el documento madre.

## Las preguntas de la entrevista

La sección siguiente es la guía que utilizará el agente. No tienes que rellenarla antes de empezar.

### 1. ¿Sobre qué tema preparas contenido y para qué lector concreto?

Completa: **«Ayudo a [tipo de persona] a [resolver un problema o conseguir algo] con contenido sobre [tema]».**

Ejemplo: «Ayudo a profesionales de formación a preparar sus clases con herramientas de IA».

Empezamos con un público y un tema principal. Si respondes «para todo el mundo» o das varios proyectos, el agente te ayudará a elegir uno para este primer sistema.

### 2. ¿Con qué material podemos empezar?

Indica estas dos partes; no necesitas tenerlas resueltas de antemano:

| Material propio | Fuentes externas |
|---|---|
| Newsletter o blog: indica dónde y cuántos artículos aproximadamente. | Tengo canales de YouTube de referencia: indica hasta tres para empezar. |
| Documentos o exportaciones: indica formato y cantidad aproximada. | Quiero usar YouTube, pero necesito ayuda para elegir canales. |
| Todavía no tengo contenido propio. | Prefiero empezar con ideas propias y buscar fuentes al investigar. |

Puedes combinar materiales propios. Un enlace no demuestra que el texto completo sea accesible: el diseño dejará pendientes los accesos que todavía no se hayan comprobado. Sin histórico, el sistema podrá investigar oportunidades, pero no afirmar qué repite de tus publicaciones. Otras fuentes podrán anotarse para valorar su incorporación después.

### 3. ¿Qué parte de tu proceso actual quieres mejorar primero?

Elige la que más trabajo te cuesta y cuenta brevemente cómo la haces hoy:

- **Encontrar temas:** no sé qué merece la pena desarrollar.
- **Investigar:** tengo temas, pero reunir y contrastar información me lleva demasiado tiempo.
- **Preparar material para escribir:** tengo fuentes y notas, pero me cuesta convertirlas en una explicación aprovechable.

Esta elección fija la prioridad del diseño; el recorrido mantiene sus cinco etapas. Tú elegirás la oportunidad que se desarrolla y revisarás el documento madre.

### 4. ¿Qué tipo de oportunidad prefieres que te proponga?

Elige una prioridad inicial:

- **Resolver dudas concretas** de tu lector.
- **Explicar novedades relevantes** y sus consecuencias.
- **Profundizar en temas ya tratados** con nuevas evidencias o ángulos, si hay histórico disponible.

Da un ejemplo de tema que aceptarías. Puedes añadir un tema que no te interese para concretar el límite. El agente comprobará que las propuestas ayuden al lector definido; la popularidad de un vídeo no bastará.

### 5. ¿Qué enfoque debe tener el documento madre?

Elige el que mejor sirva a tu trabajo posterior:

- **Explicativo:** desarrolla qué ocurre, por qué importa, ejemplos y consecuencias.
- **Práctico:** desarrolla cómo abordar una tarea, requisitos, pasos, ejemplos y límites.
- **Comparativo:** desarrolla alternativas, criterios, diferencias y cuándo conviene cada una.

Todos incluyen contenido desarrollado, fuentes, ángulos aprovechables y asuntos pendientes. Una entrega práctica no inventará pruebas ni resultados: distinguirá lo documentado de lo comprobado. Esta elección orienta el material, no crea todavía una newsletter o un post.

## Instrucciones de arranque para el agente

Antes de comenzar, lee completo `AGENTS.md` y aplica sus criterios. Si no está disponible, pide a la persona que lo adjunte junto con este README; no inventes las instrucciones que faltan.

Usa las preguntas anteriores en orden y espera cada respuesta. Los ejemplos de `material_adicional/` no son respuestas del usuario y no autorizan a saltar la entrevista. Genera la arquitectura solo después de completarla.

Los mensajes de las secciones 4 y 5 son acciones que la persona puede pedir más adelante. Leerlos no autoriza a preparar prompts ni a ejecutar la construcción. Trabaja solo en la fase solicitada.

## Qué incluye este material

```text
README.md
AGENTS.md
material_adicional/
  RESPUESTAS-EJEMPLO.md
  inicio-entrevista.png
```

Es un arranque guiado: tu arquitectura, tus skills y las herramientas se crearán durante el recorrido. La captura documenta el inicio de la entrevista; no demuestra por sí sola que un sistema completo esté construido o probado.
