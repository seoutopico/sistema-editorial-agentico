---
id: 219821904
titulo: "He montado un pequeño equipo de IA para que mis aplicaciones no parezcan un Frankenstein"
subtitulo: "Así he creado con Codex un sistema de diseño, componentes reutilizables y dos agentes de IA: uno construye y otro revisa."
fecha: 2026-10-11
url: https://ainalluna.substack.com/p/crear-sistema-diseno-codex-agentes-ia
tipo: newsletter
audiencia: everyone
estado: completo
huella: dd56cb63208385327728e001e26f47ddd79d258cd8550f52c2e498a755a9dd18
---

[

![imagen](https://substackcdn.com/image/fetch/$s_!hufr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9b465207-5312-4993-8981-35012ec9ffc3_1672x941.png)

](https://substackcdn.com/image/fetch/$s_!hufr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9b465207-5312-4993-8981-35012ec9ffc3_1672x941.png)

*¿Cómo estás?
Soy Aina y esto es Think&Hack.*

Si has probado a crear una aplicación con IA, quizá te haya pasado algo parecido. Consigues una pantalla que te gusta, le pides que añada otra y empiezan las sorpresas. Los botones ya no tienen el mismo aspecto, los espacios cambian y aparece un formulario que parece sacado de otra aplicación.

Así que empiezas a corregir. Que utilice los mismos colores, que recupere aquel botón que ya habíais preparado, que mantenga el estilo de la primera pantalla… Y cuando abres una conversación nueva, vuelta a empezar. :)

El problema es que estamos tomando decisiones de diseño que después no quedan recogidas en ningún sitio que la IA pueda consultar y reutilizar. Y cuanto más crece la aplicación, más cosas tenemos que recordar y revisar.

Esta semana vamos a ponerle solución construyendo **nuestro propio sistema de diseño con nuestra IA agéntica preferida (Codex, Claude Code…). **Tendremos colores, reglas visuales y componentes reutilizables, además de un catálogo donde podremos verlos, probarlos y consultar cómo utilizarlos.

Pero también vamos a preparar algo que me parece especialmente interesante: **un arnés de trabajo con instrucciones, skills y dos agentes especializados**. Uno se encargará de construir los componentes y otro de revisar lo que ha hecho. Así, cuando pidamos una pantalla nueva, Codex tendrá un procedimiento para aprovechar lo que ya existe, crear lo que falta y comprobar el resultado.

Y lo vamos a probar construyendo una pantalla real a partir de nuestros componentes.

Vamos desde el principio. :)

Si te gusta probar la IA y entender cómo puedes aprovecharla en tu trabajo, suscríbete a Think&Hack. Por aquí comparto lo que voy aprendiendo, mis experimentos y cómo puedes probarlos tú. :)

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)

---

## Antes de empezar: ¿qué vamos a construir?

Vamos a preparar **un sistema de diseño que podamos reutilizar en nuestras aplicaciones**. Ahí guardaremos los colores, las reglas visuales y los componentes que vayamos creando, como botones, formularios o tablas.

También construiremos un catálogo para ver esos componentes, probar cómo se comportan y consultar cómo utilizarlos. Y lo interesante es que no serán ejemplos independientes: **los componentes que veamos en el catálogo serán los mismos que después utilizaremos en nuestras aplicaciones**.

Pero tener los componentes guardados es solo una parte. También necesitamos que Codex sepa dónde encontrarlos, cuándo reutilizarlos y qué hacer cuando necesitemos uno nuevo.

Para eso prepararemos nuestro **arnés de trabajo**: un conjunto de instrucciones, skills y agentes que guiarán el proceso. Tendremos un agente encargado de construir componentes y otro que revisará el resultado antes de incorporarlo al sistema.

Empezaremos con algo pequeño: nuestros colores, un catálogo básico y un botón `Button` con dos variantes. Cuando lo tengamos funcionando, daremos el siguiente paso y construiremos una pantalla más completa para comprobar cómo se reutiliza todo lo anterior.

## 1. Prepara una carpeta que puedas abrir y probar.

En este ejemplo utilizamos React para construir la interfaz, TypeScript para describir los datos que aceptan los componentes y Vite para crear el proyecto y verlo en el navegador. Node.js y npm permiten ejecutar esas herramientas e instalar sus dependencias. Trabajaremos desde Visual Studio Code con Codex.

Instala VS Code y una versión LTS de Node.js compatible con la versión de Vite que vayas a utilizar. Abre una carpeta vacía, por ejemplo `mi-design-system`, y entra en **Terminal → Nuevo terminal**. Comprueba la instalación ejecutando cada consulta por separado:

```
node -v
npm -v
```

Ambas deben devolver un número de versión. Si alguna no se reconoce, revisa la instalación y vuelve a abrir el editor antes de continuar.

Dentro de esa carpeta, crea la plantilla de React con TypeScript:

```
npm create vite@latest . -- --template react-ts
```

El punto indica que los archivos se crearán en la carpeta actual. Este paso se hace una sola vez.

![01 · Creación del proyecto y dirección local que muestra la terminal.](https://substackcdn.com/image/fetch/$s_!d-bN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59e62e81-8ac6-4c46-b33a-8de94fb5cfd3_800x133.png)

*01 · Creación del proyecto y dirección local que muestra la terminal.*

Al terminar, verás los archivos en el explorador de VS Code. `src` contiene el código de la aplicación; `package.json`, las dependencias y los comandos disponibles.

[

![02 · Estructura de partida del ejercicio. Las instrucciones del proyecto las prepararemos más adelante.](https://substackcdn.com/image/fetch/$s_!KVF5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbc05893-8a39-4883-81ea-ec6662b6d68e_305x507.png)

](https://substackcdn.com/image/fetch/$s_!KVF5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbc05893-8a39-4883-81ea-ec6662b6d68e_305x507.png)*02 · Estructura de partida del ejercicio. Las instrucciones del proyecto las prepararemos más adelante.*

Si el asistente de instalación no lo ha hecho ya, instala las dependencias y arranca el servidor, en ese orden:

```
npm install
npm run dev
```

Abre la dirección indicada en la terminal, normalmente `http://localhost:5173/`. Debería aparecer la página de ejemplo. Mantén esa terminal abierta mientras trabajas; puedes detener el servidor con `Ctrl+C` y arrancarlo otro día con `npm run dev`.

Ahora instala la extensión oficial de Codex, publicada por OpenAI, desde Extensiones de VS Code, abre su panel e inicia sesión. Mantén abierta la carpeta completa del ejercicio.

**Antes de seguir:** comprueba que ves los archivos, que la página carga en el navegador y que Codex puede inspeccionar ese mismo proyecto. Más adelante integraremos shadcn/ui como base de componentes; crear la plantilla no realiza esa integración.

## 2. Define el proyecto antes de pedir pantallas

El primer encargo a Codex consiste en concretar qué vamos a construir. Dale el objetivo, quién lo utilizará y uno o dos ejemplos de aplicaciones en las que quieras reutilizar el sistema. Adjunta también la paleta y la referencia visual: nombrarlas en el chat no permite consultarlas.

Pídele que inspeccione lo que ya existe, distinga tus decisiones de sus recomendaciones y resuelva las dudas en pequeñas rondas. En esta fase queremos una propuesta, así que delimita el trabajo a leer, preguntar y documentar.

[

![03 · Primera conversación de definición: Codex separa el estado del proyecto, las decisiones aportadas y las preguntas pendientes.](https://substackcdn.com/image/fetch/$s_!RPpF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc07f1bc3-640f-4a2a-a4f4-eb7435c7859f_1292x976.png)

](https://substackcdn.com/image/fetch/$s_!RPpF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc07f1bc3-640f-4a2a-a4f4-eb7435c7859f_1292x976.png)*03 · Primera conversación de definición: Codex separa el estado del proyecto, las decisiones aportadas y las preguntas pendientes.*

En nuestro ejemplo aparecen preguntas sobre los usuarios, la tecnología y las referencias. A partir de ahí concretamos la primera entrega con `Button` y dejamos para después otras ampliaciones. También aclaramos el orden: preparar el arnés antes de construir.

Revisa que la propuesta incluya objetivo, tecnología, organización de archivos, identidad visual, alcance inicial y criterios de aceptación. Las decisiones provisionales deben seguir marcadas como provisionales: una sugerencia de tipografía o de color no se convierte en una decisión tuya por aparecer en la respuesta.

Cuando estés conforme, pide que guarde lo aprobado en `docs/project-definition.md` y abre el archivo para revisarlo.

[

![04 · La definición queda guardada dentro del proyecto, con acuerdos, decisiones provisionales y pendientes.](https://substackcdn.com/image/fetch/$s_!11TU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3212d8af-de7c-42e9-aeb7-d6a11daea646_1862x972.png)

](https://substackcdn.com/image/fetch/$s_!11TU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3212d8af-de7c-42e9-aeb7-d6a11daea646_1862x972.png)*04 · La definición queda guardada dentro del proyecto, con acuerdos, decisiones provisionales y pendientes.*

**La salida de esta etapa es un documento que puedas volver a consultar.** Ahí debe quedar claro qué se construirá primero y qué condiciones tendrá que cumplir.

## 3. Haz que una conversación nueva pueda orientarse

La definición recoge qué queremos construir. Ahora vamos a documentar cómo trabajar en ese proyecto.

Encarga a Codex que lea la definición, revise las instrucciones existentes y prepare `AGENTS.md` en la raíz. Este archivo debe señalar dónde está la definición y recoger reglas breves: respetar el alcance, reutilizar componentes y tokens, conservar los cambios existentes y comprobar cada entrega según su naturaleza.

Los *tokens* son valores compartidos, como colores, espacios o radios de borde. Tenerlos centralizados permite aplicar un mismo criterio a todas las piezas.

[

![05 · Instrucciones persistentes del proyecto: referencia a la definición, reglas de trabajo y criterios de reutilización.](https://substackcdn.com/image/fetch/$s_!Q_kW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ea31da0-2148-47fd-bd47-249cc37f17e6_1871x969.png)

](https://substackcdn.com/image/fetch/$s_!Q_kW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ea31da0-2148-47fd-bd47-249cc37f17e6_1871x969.png)*05 · Instrucciones persistentes del proyecto: referencia a la definición, reglas de trabajo y criterios de reutilización.*

Comprueba que los comandos citados coinciden con los disponibles en `package.json`. Evita copiar toda la definición dentro de las instrucciones: mantener dos versiones de la misma decisión acaba generando contradicciones.

Para probarlo, abre una conversación nueva de Codex en la misma carpeta. Sin pegar el historial, pide una lectura del contexto: qué instrucciones tiene activas, cuál es la primera entrega aprobada y qué decisiones siguen pendientes. Limita esa prueba a consultar y resumir.

Compara la respuesta con los documentos. En nuestro caso debía reconocer `Button`, sus dos variantes, el catálogo mínimo y los pendientes visuales. Si el resumen no encaja, revisa la carpeta abierta, el nombre exacto de `AGENTS.md` y si existen otras instrucciones que lo sustituyan.

**Lo que estamos comprobando es que puede recuperar el contexto guardado.** Conviene repetir esa comprobación cuando cambien de forma relevante las reglas del proyecto.

## 4. Convierte la construcción en un procedimiento repetible

Ya tenemos reglas generales. La siguiente pieza será una **skill**: un procedimiento para una tarea concreta. En este caso, añadir o modificar componentes del sistema y sus ejemplos en el catálogo.

La llamamos `design-system-component` y la guardamos en `.agents/skills/design-system-component/SKILL.md`. Su descripción debe explicar cuándo utilizarla; el cuerpo, qué consultar, qué pasos seguir y qué entregar.

Al encargarla, incluye este recorrido:

1.

Leer la definición y delimitar el componente solicitado.

2.

Inspeccionar la infraestructura y distinguir lo instalado de lo previsto.

3.

Reutilizar tokens y componentes existentes.

4.

Implementar únicamente el alcance encargado y preparar ejemplos reales.

5.

Comprobar variantes y estados afectados, y registrar resultados para la revisión.

[

![06 · Skill constructora creada. La validación del archivo es el primer control; su comportamiento se comprueba con una tarea real.](https://substackcdn.com/image/fetch/$s_!EU8F!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc5947288-b0e4-43db-ad9e-d7a419eaff00_1871x1000.png)

](https://substackcdn.com/image/fetch/$s_!EU8F!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc5947288-b0e4-43db-ad9e-d7a419eaff00_1871x1000.png)*06 · Skill constructora creada. La validación del archivo es el primer control; su comportamiento se comprueba con una tarea real.*

La primera prueba puede ser de planificación: pide que aplique la skill a `Button`, identifique requisitos previos, proponga los archivos que tocaría y describa las comprobaciones. Todavía sin modificar nada.

Debería detectar si faltan shadcn/ui, los estilos, los tokens, las exportaciones o la estructura del catálogo. También debe conservar las dos variantes aprobadas y señalar las decisiones visuales pendientes.

Revisa el plan y resuelve esas decisiones. Después encarga la preparación técnica necesaria: integrar la base elegida, configurar los estilos y organizar el sistema y el catálogo. Comprueba que el proyecto sigue arrancando antes de pedir la implementación de `Button`.

Al construirlo, pide una única implementación reutilizable y ejemplos que la consuman. El catálogo inicial del ejercicio quedó así:

[

![07 · Primera entrega del catálogo: introducción, colores y botones reales con una identidad visual compartida.](https://substackcdn.com/image/fetch/$s_!uz9J!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F066f9389-2b83-4420-b973-3a544a353bc0_1519x847.png)

](https://substackcdn.com/image/fetch/$s_!uz9J!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F066f9389-2b83-4420-b973-3a544a353bc0_1519x847.png)*07 · Primera entrega del catálogo: introducción, colores y botones reales con una identidad visual compartida.*

La separación también se ve en los archivos: el componente vive dentro del sistema de diseño y el catálogo se encarga de mostrarlo.

[

![08 · Ubicación del componente Button y sus estilos dentro del sistema de diseño.](https://substackcdn.com/image/fetch/$s_!vrf4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F089539e0-afdd-4460-aa1b-5608b213d572_270x762.png)

](https://substackcdn.com/image/fetch/$s_!vrf4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F089539e0-afdd-4460-aa1b-5608b213d572_270x762.png)*08 · Ubicación del componente Button y sus estilos dentro del sistema de diseño.*

En su página podemos comparar las variantes principal y secundaria, activar el botón y revisar sus estados normal, hover, foco, pulsado y deshabilitado.

[

![09 · Página de Button: variantes, zona de prueba, estados y ejemplos de uso.](https://substackcdn.com/image/fetch/$s_!3ADK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d913aef-35a1-46c3-ad31-fa3dffd2451a_1024x1352.png)

](https://substackcdn.com/image/fetch/$s_!3ADK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d913aef-35a1-46c3-ad31-fa3dffd2451a_1024x1352.png)*09 · Página de Button: variantes, zona de prueba, estados y ejemplos de uso.*

**Compruébalo también con el teclado:** llega al botón con Tab, verifica que el foco sea visible y pruébalo con Enter o Espacio. Al deshabilitarlo, no debería ejecutar la acción. Acompaña la revisión visual con las comprobaciones técnicas que el proyecto tenga disponibles.

## 5. Prepara una revisión separada

Con el primer componente construido, necesitamos contrastarlo con lo que habíamos definido. Para ello creamos `design-system-review` en `.agents/skills/design-system-review/SKILL.md`.

Esta skill debe guiar la inspección del código, el comportamiento del catálogo y la accesibilidad dentro del alcance del encargo. Cada incidencia tiene que explicar el problema, su impacto, dónde ocurre y qué evidencia lo demuestra. Conviene distinguir errores, mejoras opcionales y comprobaciones pendientes.

[

![10 · Skill de revisión preparada. Esta captura muestra la creación y validación del archivo; la evaluación de la aplicación es un paso posterior.](https://substackcdn.com/image/fetch/$s_!Owhg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa353f736-38ae-407d-936a-0436c407866c_1922x1025.png)

](https://substackcdn.com/image/fetch/$s_!Owhg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa353f736-38ae-407d-936a-0436c407866c_1922x1025.png)*10 · Skill de revisión preparada. Esta captura muestra la creación y validación del archivo; la evaluación de la aplicación es un paso posterior.*

Prueba la revisión en una sesión nueva, separada de la construcción. Puedes pedir que evalúe `Button` y el catálogo sin mencionar la skill, y observar si la selecciona. Si no lo hace, revisa la descripción de activación y repite la prueba.

El revisor debe obtener sus propias evidencias. Guarda el informe separado de la entrega del constructor, lee los hallazgos y encarga después las correcciones necesarias. Una skill describe un procedimiento; para una revisión independiente también hace falta separar quién construye de quién revisa.

La decisión visual final sigue siendo tuya: que algo compile no confirma que respete la identidad que querías.

## 6. Conecta las piezas y pide una pantalla completa

El siguiente paso es que el agente principal pueda coordinar ese recorrido cuando le pidas una pantalla. Primero consulta el sistema, identifica qué puede reutilizar y encarga al constructor las piezas que faltan. Después pasa la entrega a un revisor separado, gestiona las correcciones e integra el resultado.

En el proyecto del ejemplo documentamos dos roles en `.codex/agents/`: `ds-component-builder.toml` y `ds-component-reviewer.toml`. Cada uno referencia su skill. Las reglas de coordinación quedan en `AGENTS.md`.

Esas reglas delimitan los encargos, evitan que dos agentes escriban en los mismos archivos a la vez y establecen la secuencia construcción → revisión → corrección → integración. En nuestro ejercicio fijamos hasta dos rondas de corrección; si queda un problema, el principal debe explicarlo con evidencia y proponer el siguiente paso.

[

![11 · Roles de construcción y revisión, junto con sus reglas de coordinación.](https://substackcdn.com/image/fetch/$s_!rKBP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F514793bb-6dc6-4fd9-9264-972467ec8d08_1911x1035.png)

](https://substackcdn.com/image/fetch/$s_!rKBP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F514793bb-6dc6-4fd9-9264-972467ec8d08_1911x1035.png)*11 · Roles de construcción y revisión, junto con sus reglas de coordinación.*

Crear los archivos no demuestra que la delegación funcione. Abre una sesión nueva, comprueba que el cliente reconoce los roles y prueba el recorrido con un encargo pequeño pero completo.

El nuestro fue una **pantalla de solicitudes con búsqueda por asunto, filtro por estado y tabla**, usando datos ficticios locales. Debía aparecer como ejemplo del catálogo, con su propio enlace. Al pedirla, no mencionamos las skills ni repartimos manualmente el trabajo: queríamos observar cómo se aplicaban las reglas guardadas.

[

![12 · El constructor consulta el contexto y aplica la skill a los controles y la tabla reutilizables.](https://substackcdn.com/image/fetch/$s_!olnh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F214237a4-ee54-4172-98fb-1e39abef9a8d_920x362.png)

](https://substackcdn.com/image/fetch/$s_!olnh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F214237a4-ee54-4172-98fb-1e39abef9a8d_920x362.png)*12 · El constructor consulta el contexto y aplica la skill a los controles y la tabla reutilizables.*

A continuación entra el revisor. En la captura explica que obtendrá evidencias propias y que está comprobando filtros, navegación, foco y presentación móvil.

[

![13 · Revisión separada de los componentes y del ejemplo de solicitudes.](https://substackcdn.com/image/fetch/$s_!BA03!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2924622f-bd95-4aad-8daf-6dda494ba271_919x347.png)

](https://substackcdn.com/image/fetch/$s_!BA03!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2924622f-bd95-4aad-8daf-6dda494ba271_919x347.png)*13 · Revisión separada de los componentes y del ejemplo de solicitudes.*

El seguimiento permite ver la intervención de ambos roles y las comprobaciones que se van comunicando. Para dar la entrega por buena, contrasta ese informe con la pantalla y con las evidencias guardadas.

![14 · Seguimiento del trabajo: búsqueda, filtros combinados, limpieza, estado vacío y controles por teclado.](https://substackcdn.com/image/fetch/$s_!p3aW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F700357c3-339c-40f1-a0b9-258709b1f1a5_902x161.png)

*14 · Seguimiento del trabajo: búsqueda, filtros combinados, limpieza, estado vacío y controles por teclado.*

El catálogo crece con las piezas necesarias para esa pantalla. En el resultado aparecen `Input`, `NativeSelect` y `Table`, además de `Button`.

[

![15 · Catálogo ampliado: la tabla tiene su propia página, ejemplos, estados e instrucciones de uso.](https://substackcdn.com/image/fetch/$s_!zVid!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb44119c6-cf54-4320-8da1-72fd7bf4283c_1804x941.png)

](https://substackcdn.com/image/fetch/$s_!zVid!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb44119c6-cf54-4320-8da1-72fd7bf4283c_1804x941.png)*15 · Catálogo ampliado: la tabla tiene su propia página, ejemplos, estados e instrucciones de uso.*

La pantalla de solicitudes combina esas piezas. El botón de limpiar filtros reutiliza el botón secundario que ya habíamos definido.

[

![16 · La pantalla de solicitudes reutiliza los componentes del sistema; las anotaciones señalan el vínculo con Button.](https://substackcdn.com/image/fetch/$s_!NKn4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F18d1186c-d286-4737-b399-a102db03715f_1864x1842.png)

](https://substackcdn.com/image/fetch/$s_!NKn4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F18d1186c-d286-4737-b399-a102db03715f_1864x1842.png)*16 · La pantalla de solicitudes reutiliza los componentes del sistema; las anotaciones señalan el vínculo con Button.*

Para comprobar la entrega, busca un asunto, combina la búsqueda con un estado y limpia los filtros. Prueba también una combinación sin resultados, recorre los controles con el teclado y revisa una pantalla estrecha. La tabla debe poder desplazarse sin ensanchar toda la página. Finalmente, comprueba que el ejemplo tenga enlace y que su dirección abra correctamente.

## 7. Comprueba que podrás reutilizarlo de verdad

La reutilización debe verse también en el código. En este proyecto, el sistema concentra tokens y componentes en `src/design-system/` y los expone desde un punto de entrada común. El catálogo los importa; los datos y la lógica de solicitudes quedan en la aplicación.

[

![17 · Uso de Button desde el sistema compartido y ejemplo de importación documentado en el catálogo.](https://substackcdn.com/image/fetch/$s_!pE-a!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff483aab3-383a-48bb-8c2f-637ecd8baba6_1646x524.png)

](https://substackcdn.com/image/fetch/$s_!pE-a!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff483aab3-383a-48bb-8c2f-637ecd8baba6_1646x524.png)*17 · Uso de Button desde el sistema compartido y ejemplo de importación documentado en el catálogo.*

Cuando añadas otra pantalla, empieza por consultar lo que ya existe. Si necesita una pieza nueva, repite el circuito: requisitos, construcción, revisión, integración y comprobación. Si cambia una pieza compartida, revisa también los lugares que la utilizan.

Para llevarlo a otro proyecto, conserva los componentes, sus estilos, tokens y dependencias, y adapta las instrucciones a la nueva aplicación. La publicación como paquete o la sincronización entre repositorios será una decisión posterior; este ejercicio deja preparada la separación que permitirá abordarla.

Al terminar tienes un catálogo que puedes abrir, componentes que puedes probar y decisiones que una nueva sesión puede consultar. La siguiente pantalla ya tendrá una base sobre la que trabajar.

---

## 🛠️ ¿Quieres crear tu propio sistema de diseño?

Si te apetece montar algo parecido para tus aplicaciones, he preparado **un curso paso a paso para crear tu sistema de diseño con Codex,** acompañado de los prompts que necesitas en cada fase.

Empezaremos definiendo el proyecto y preparando las instrucciones para Codex. Después construiremos los componentes y su catálogo, crearemos las skills de construcción y revisión y configuraremos los dos agentes para que puedan trabajar de forma coordinada.

Además de los prompts, tendrás las explicaciones para utilizarlos, qué resultados esperar y cómo comprobar que cada parte funciona. También encontrarás un ejemplo resuelto y una plantilla para preparar el contexto de tu proyecto.

La idea es que puedas seguir el proceso con tu propia aplicación, sin tener que preparar todas las instrucciones desde cero.

## Crea tu sistema de diseño con Codex

El curso paso a paso y los prompts para montar tu sistema de diseño y tu equipo de agentes.

[Quiero crear mi sistema de diseño →](https://ainalluna.gumroad.com/l/sistema-diseno-codex)

---

## ¿Y tú, cómo estás trabajando con tus agentes?

Yo he empezado por un sistema de diseño porque quería dejar de corregir los mismos detalles visuales cada vez que añadía una pantalla. Pero preparar este pequeño equipo también me ha servido para pensar en qué tareas quiero que intervenga cada agente y qué necesito comprobar antes de dar algo por terminado.

Y ahora tengo curiosidad: **¿has probado a repartir el trabajo entre varios agentes o sigues trabajando con uno al que le vas encargando todo?**

#### ***Cuéntamelo. Siempre leo todo.***

[Deja un comentario](https://ainalluna.substack.com/p/crear-sistema-diseno-codex-agentes-ia/comments)

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

# **Suscríbete a Think&Hack**

**Tools are great. Systems are better.**

Si te gusta probar la IA y entender cómo puedes aprovecharla en tu trabajo, suscríbete a Think&Hack. Por aquí comparto lo que voy aprendiendo, mis experimentos y cómo puedes probarlos tú. :)

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
