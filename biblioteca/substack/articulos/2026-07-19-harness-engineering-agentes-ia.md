---
id: 206663634
titulo: "Cómo construir un arnés para que tu agente trabaje de forma fiable"
subtitulo: "Un ejemplo práctico de harness engineering para guardar el estado, limitar acciones y comprobar resultados mediante una biblioteca de transcripciones."
fecha: 2026-07-19
url: https://ainalluna.substack.com/p/harness-engineering-agentes-ia
tipo: newsletter
audiencia: everyone
estado: completo
huella: f0d72efda22f728388d8e5d74ebecd239d7e7ed9723871690db886691bf9d07d
---

*Cómo construir un arnés sencillo para guardar, clasificar y recuperar transcripciones sin depender de la memoria del chat.*

[

![imagen](https://substackcdn.com/image/fetch/$s_!0GNA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e3d332c-1a17-4770-a959-6a4f69e311b2_1659x948.png)

](https://substackcdn.com/image/fetch/$s_!0GNA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e3d332c-1a17-4770-a959-6a4f69e311b2_1659x948.png)

¿Cómo estás?

Soy Aina y esto es Think&Hack.

En las dos últimas newsletters hemos construido dos piezas de un sistema. Primero vimos [cómo crear una skill para que un agente tome mejores decisiones](https://ainalluna.substack.com/p/crear-skills-agentes-ia-verificables). Después distinguimos [cuándo basta un agente, cuándo conviene guardar uno y cuándo tiene sentido formar un equipo](https://ainalluna.substack.com/p/crear-agentes-claude-code).

Ya tenemos un procedimiento y alguien capaz de ejecutarlo. Pero todavía falta algo.

Imagina que cada semana guardas transcripciones de vídeos, reuniones, entrevistas o pódcast. Hoy le pasas una a un agente y le pides que la clasifique. El resultado parece bueno. Dentro de tres meses quieres recuperar todas las conversaciones en las que alguien habló de memoria para agentes y descubres que una quedó en el chat, otra tiene etiquetas diferentes y una tercera no conserva el enlace original.

El modelo sabía analizar el texto. El problema es que **nunca diseñamos el lugar donde debía trabajar**.

Esta semana vamos a construir ese lugar. Será una biblioteca pequeña de transcripciones: recibirá archivos nuevos, los clasificará, creará fichas que podamos consultar y comprobará que cada resultado sigue conectado con su fuente.

No hace falta programar una aplicación ni empezar con una base de datos. Vamos a hacerlo con carpetas, archivos Markdown y un catálogo. Lo suficiente para entender qué **aporta un arnés**.

---

## Qué es un arnés y por qué no es otro agente

La palabra ``harness` `se está utilizando con dos niveles de significado que conviene separar.

En sentido técnico, **el arnés es la capa que mantiene en marcha el bucle del agente**: envía contexto al modelo, recibe sus decisiones, dirige las llamadas a herramientas, devuelve los resultados y controla la ejecución. Claude Code, Codex o el Agents SDK ya incorporan buena parte de ese arnés.

Cuando hablamos de ``harness engineering``, el foco se amplía. Ya no pensamos solo en el bucle, sino en **el entorno que hemos preparado para que ese bucle haga un trabajo fiable**: qué instrucciones encuentra, qué archivos puede leer, dónde deja el estado, qué herramientas puede utilizar, qué permisos tiene y cómo se comprueba el resultado.

La diferencia con las piezas anteriores se puede resumir así:

```
**Skill  **→ conserva cómo se hace una tarea.
**Agente **→ recibe el trabajo y decide cómo avanzar.
**Arnés**  → controla el entorno en el que trabaja y qué cuenta como terminado.
```

Un arnés no tiene por qué incluir varios agentes. Tampoco es un `AGENTS.md` con muchas reglas ni un nombre sofisticado para una carpeta. Es el conjunto de condiciones que permite repetir un proceso sin reconstruir el contexto en cada conversación.

Vamos a verlo con nuestro archivo de transcripciones.

---

## Qué tiene que decidir el sistema al guardar una transcripción

Partimos de una petición normal:

```
Guarda esta transcripción para que pueda encontrarla cuando vuelva a necesitarla.
```

Un modelo puede resumir el contenido y proponer cinco etiquetas. Sin embargo, la petición deja casi todas las decisiones importantes abiertas.

¿Dónde debe guardar el original? ¿Puede modificarlo? ¿Qué datos mínimos necesita? ¿Debe inventar una fecha si no aparece? ¿Puede crear una categoría nueva? ¿Cómo sabe si esa transcripción ya existe? ¿Qué archivo tiene que consultar cuando le pidamos recuperarla? ¿Cuándo puede afirmar que ha terminado?

Si esas decisiones no están en el sistema, el agente tendrá que resolverlas de nuevo cada vez. Puede elegir bien en una sesión y de otra manera en la siguiente. **El arnés empieza donde dejamos de confiar esas decisiones a la improvisación del chat.**

Nuestro sistema mínimo tendrá esta forma:

```
biblioteca-transcripciones/
├── AGENTS.md
├── claude.md
├── inbox/
├── fichas/
│   └── nombre-transcripcion/
│       ├── original.md
│       └── ficha.md
├── catalogo.csv
├── taxonomia.md
└── registro.md
```

-

`AGENTS.md` contiene las instrucciones compartidas.

-

`CLAUDE.md` permite que Claude Code cargue esas mismas instrucciones.

-

`inbox/` recibe las transcripciones pendientes.

-

`fichas/` guarda una versión breve y consultable de cada una.

-

`catalogo.csv` funciona como índice.

-

`taxonomia.md` contiene las categorías aceptadas.

-

`registro.md` conserva qué ocurrió durante cada ejecución.

**La estructura propuesta convierte en decisiones concretas todo lo que el prompt inicial había dejado abierto.**

---

## Primera pieza: un punto de entrada claro

Podríamos poner todas las reglas, ejemplos y excepciones dentro de ``AGENTS.md``. Sería cómodo al principio y difícil de mantener después.

En **Codex**, estas instrucciones del proyecto se guardan en `AGENTS.md`.** Claude Code **no lee ese archivo directamente, pero `CLAUDE.md` puede importarlo. Así mantenemos una sola fuente de instrucciones. Si ambos archivos están en la raíz, `CLAUDE.md` solo necesita esta línea:

```
@AGENTS.md
```

La ruta se resuelve desde la ubicación de `CLAUDE.md`.

El contenido que sí mantenemos en `AGENTS.md` podría ser este:

```
# Biblioteca de transcripciones

Este proyecto permite guardar, clasificar y recuperar transcripciones sin perder la relación con el documento original.

## Estructura del proyecto

- `inbox/`: transcripciones pendientes de procesar.
- `fichas/<id>/original.md`: copia canónica e intacta de la transcripción.
- `fichas/<id>/ficha.md`: ficha consultable creada a partir del original.
- `catalogo.csv`: índice de transcripciones procesadas.
- `taxonomia.md`: categorías permitidas.
- `registro.md`: historial de resultados, dudas y bloqueos.

## Fuentes de verdad

- `original.md` conserva el contenido recibido y es la fuente de las citas.
- `taxonomia.md` contiene las únicas categorías que puedes asignar.
- `catalogo.csv` sirve para detectar duplicados y localizar materiales procesados.
- `ficha.md` facilita la consulta, pero no sustituye al original cuando haya que verificar una afirmación.

## Procesar una transcripción

Cuando el usuario pida guardar, registrar, archivar, clasificar o procesar una transcripción:

1. Trabaja solo con el archivo de `inbox/` indicado por el usuario.
2. Lee el archivo completo, `taxonomia.md` y `catalogo.csv`.
3. Comprueba que aparecen título, tipo, fecha y URL de la fuente.
4. Busca la URL en `catalogo.csv` para detectar duplicados.
5. Si falta un dato obligatorio o la URL ya existe, no proceses el archivo. Explica el problema y anótalo en `registro.md`.
6. Usa el nombre del archivo sin extensión como identificador `<id>`.
7. Calcula el hash SHA-256 del archivo y conserva el valor.
8. Crea la carpeta `fichas/<id>/`.
9. Mueve el archivo de `inbox/` a `fichas/<id>/original.md` sin reescribir su contenido.
10. Calcula el hash de `original.md` y comprueba que coincide con el valor anterior.
11. Crea `fichas/<id>/ficha.md`, incluye allí el hash y sigue el formato de este documento.
12. Añade una única fila a `catalogo.csv`.
13. Anota el resultado en `registro.md`.
14. Revisa todas las condiciones de cierre antes de terminar.

Si el proceso falla después de mover el original, devuélvelo a `inbox/` y no añadas la transcripción al catálogo como procesada.

## Formato de ficha

```markdown
# Título de la transcripción

- Tipo: entrevista | vídeo | pódcast | reunión
- Fuente: URL
- Fecha: AAAA-MM-DD
- Temas: tema-1, tema-2
- Original: fichas/<id>/original.md
- Estado: procesada
- SHA-256: valor completo del hash de original.md

## Idea principal

Un párrafo breve con la aportación central de la transcripción.

## Ideas recuperables

- Entre dos y cuatro ideas útiles para búsquedas posteriores.

## Fragmentos verificables

> Uno o dos fragmentos literales presentes en `original.md`.

## Límites o dudas

Datos ausentes, afirmaciones que requieren contraste o ambigüedades.
```

## Catálogo

Mantén exactamente estas columnas:

```text
id,titulo,tipo,fecha,fuente,temas,ficha,original,estado
```

- Usa `<id>` como identificador.
- Separa varios temas con `|`.
- Usa rutas relativas al proyecto.
- No añadas una fila si la URL ya existe.

## Recuperar información

Cuando el usuario pida encontrar, recuperar o comparar ideas guardadas:

1. Consulta primero `catalogo.csv`.
2. Abre las fichas que puedan responder a la búsqueda.
3. Vuelve a `original.md` para comprobar cada fragmento literal y su contexto.
4. Descarta cualquier resultado que no puedas conectar con un original.
5. Devuelve para cada resultado el título, la idea relevante, un fragmento literal, la URL, la ruta de la ficha y la ruta del original.
6. Si no hay evidencia suficiente, dilo con claridad.

## Límites

- No inventes fuentes, fechas, personas, temas ni citas.
- No corrijas, resumas ni reformatees el contenido de `original.md`.
- No crees categorías nuevas sin aprobación del usuario.
- No publiques ni envíes contenido.
- No accedas a carpetas situadas fuera de este proyecto.
- No marques una transcripción como procesada solo porque exista `ficha.md`.

## Condiciones de cierre

Una transcripción está procesada solo si:

- ya no aparece en `inbox/`;
- `fichas/<id>/original.md` y `fichas/<id>/ficha.md` existen;
- la ficha contiene tipo, fuente, fecha, temas y ruta al original;
- el SHA-256 guardado en la ficha coincide con el hash actual de `original.md`;
- todos los temas existen en `taxonomia.md`;
- el catálogo contiene exactamente una fila para la URL;
- las rutas del catálogo abren los archivos correctos;
- los fragmentos literales de la ficha aparecen en `original.md`;
- el resultado está anotado en `registro.md`.

Si alguna condición falla, no declares la tarea terminada. Explica qué falta o qué has restaurado.

```

El archivo no explica cómo resumir una entrevista ni contiene toda la taxonomía. Indica **dónde está cada fuente de verdad, en qué orden debe consultarse y qué límites no puede saltarse**.

Esta distinción importa. OpenAI cuenta que su equipo intentó utilizar un único `AGENTS.md` enorme y terminó tratándolo como un índice que apunta a documentación más específica. **Cuando todo está cargado desde el principio, las instrucciones compiten con la tarea y se vuelven más difíciles de mantener y verificar.**

En nuestra biblioteca, el agente empieza con un mapa pequeño y abre `taxonomia.md` solo cuando necesita clasificar. No necesita cargar todas las fichas para procesar una transcripción nueva. Para comprobar duplicados, busca primero en el catálogo.

**No se trata de darle menos contexto. Se trata de organizarlo para que pueda encontrar el contexto adecuado en el momento adecuado.**

---

## Segunda pieza: cómo conservar el trabajo entre sesiones

Supongamos que dejamos en `inbox/` una entrevista titulada `como-usar-ia-negocio-loc`l.md`.`

```
Procesa inbox/entrevista-ia-negocio-local.md.
Antes de terminar, enséñame las comprobaciones que has realizado.
```

[

![imagen](https://substackcdn.com/image/fetch/$s_!e7s2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84db0ab1-c723-410e-8811-78d4a66bef33_1555x1030.png)

](https://substackcdn.com/image/fetch/$s_!e7s2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84db0ab1-c723-410e-8811-78d4a66bef33_1555x1030.png)

El agente la lee y crea una ficha como esta:

[

![imagen](https://substackcdn.com/image/fetch/$s_!kLqc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffea764c9-0373-41ed-8409-41c467d2bef1_980x977.png)

](https://substackcdn.com/image/fetch/$s_!kLqc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffea764c9-0373-41ed-8409-41c467d2bef1_980x977.png)

Después añade una fila a `catalogo.csv` con el título, la fuente, la fecha, los temas y la ruta de la ficha. Finalmente deja en `registro.md` una anotación breve: qué archivo procesó, qué cambió y si encontró`alguna duda.`

[

![imagen](https://substackcdn.com/image/fetch/$s_!V5VK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff7f20011-154b-4569-8d46-4af18238f34d_1287x466.png)

](https://substackcdn.com/image/fetch/$s_!V5VK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff7f20011-154b-4569-8d46-4af18238f34d_1287x466.png)

Antes de cerrar, calcula el hash SHA-256 de `original.md` y guarda ese valor en la ficha. El hash es una huella del contenido: si el archivo cambia, aunque sea en un solo carácter, la huella también cambia. No sirve para clasificar la transcripción; **sirve para comprobar en otra sesión que el original sigue intacto.**

[

![imagen](https://substackcdn.com/image/fetch/$s_!Wvqc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ec5e27c-6b8a-4ab3-bfd3-bc370a361501_1004x472.png)

](https://substackcdn.com/image/fetch/$s_!Wvqc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ec5e27c-6b8a-4ab3-bfd3-bc370a361501_1004x472.png)

Esos archivos hacen algo que el chat no puede garantizar por sí solo: **conservar el estado del trabajo entre sesiones**.

La semana siguiente podemos abrir una conversación nueva y pedir:

```
Encuentra las transcripciones en las que alguien explique por qué empezó
automatizando una tarea pequeña. Devuélveme la idea, el fragmento que la
sostiene y el enlace a la fuente.
```

[

![imagen](https://substackcdn.com/image/fetch/$s_!a9aO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e72a1e5-90ca-430e-93bd-2da16a521f03_1027x421.png)

](https://substackcdn.com/image/fetch/$s_!a9aO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e72a1e5-90ca-430e-93bd-2da16a521f03_1027x421.png)

El agente no necesita recordar la conversación anterior. **Puede consultar el catálogo, abrir las fichas candidatas y volver al original cuando necesite verificar una cita.**

[

![imagen](https://substackcdn.com/image/fetch/$s_!5-tN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc967413c-dbd4-4f07-9369-3a9840fa14ab_1026x970.png)

](https://substackcdn.com/image/fetch/$s_!5-tN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc967413c-dbd4-4f07-9369-3a9840fa14ab_1026x970.png)

---

## Tercera pieza: qué archivos puede leer y modificar el agente

Hasta ahora hemos decidido cómo se organiza la información. El arnés también tiene que establecer qué operaciones necesita el agente y cuáles quedan fuera del proceso..

Para procesar una transcripción, el agente debe leer el archivo indicado en `inbox/`, consultar `taxonomia.md` y comprobar duplicados en `catalogo.csv`. Después crea `fichas/<id>/`, mueve la transcripción sin alterar su contenido a `original.md`, genera `ficha.md`, guarda allí el hash SHA-256 y actualiza el catálogo y el registro.

La política queda así:

```
**Puede leer**: inbox/, taxonomia.md, catalogo.csv y fichas/.
**Puede crear y actualizar: **fichas/<id>/ficha.md, catalogo.csv y registro.md.
**Puede mover**: la transcripción indicada desde inbox/ hasta fichas/<id>/original.md.
**No puede modificar:** el contenido de original.md, la taxonomía ni las instrucciones del proyecto.
**No puede publicar,** enviar contenido ni trabajar fuera de esta biblioteca.
**Debe pedir ayuda: **si falta la fuente o la fecha, encuentra un posible duplicado o necesita una categoría que no existe.
```

Mover el original no significa tener permiso para reescribirlo. El archivo deja de estar pendiente en `inbox/` y pasa a ser la fuente canónica de esa transcripción. Desde ese momento solo se consulta. La ficha puede corregirse o ampliarse; el original no.

`AGENTS.md` describe esta política y** orienta el comportamiento**, pero escribir una regla ahí **no obliga por sí solo al agente a cumplirla.** En esta versión sencilla, Claude Code muestra las operaciones de escritura y traslado para que podamos revisarlas antes de aprobarlas.

---

## Cuarta pieza: el agente no termina porque lo diga

La parte más valiosa del ejemplo aparece al final.

Imagina que el agente responde:

>
>
> He clasificado correctamente la transcripción.
>
>

**Eso es una afirmación, no una comprobación.** Para aceptar el trabajo necesitamos observar algo fuera de su propia respuesta.

Además de decidir qué puede hacer el agente, necesitamos decidir qué rastro debe dejar. Cada transcripción procesada debería permitir reconstruir qué original recibió, dónde lo guardó, qué ficha creó, qué cambios hizo en el catálogo y qué dudas encontró. **Sin ese registro, el proceso puede funcionar, pero nosotros no podemos auditarlo ni corregirlo cuando algo falla.**

En nuestra biblioteca, ese rastro se ve en cuatro sitios:

-

`inbox/` muestra qué transcripciones siguen pendientes o bloqueadas.

-

`fichas/<id>/` conserva juntas la fuente original, la ficha y la huella SHA-256.

-

`catalogo.csv` indica qué se procesó, con qué estado y dónde están los archivos.

-

`registro.md` explica qué ocurrió durante la ejecución: si terminó, qué dudas aparecieron o por qué se rechazó.

En esta primera versión podemos** usar una lista de control:**

```
[ ] La transcripción original sigue intacta.
[ ] La ficha contiene título, tipo, fuente y fecha.
[ ] Los temas existen en taxonomia.md.
[ ] El catálogo contiene una sola fila para esa fuente.
[ ] La ruta incluida en el catálogo abre la ficha correcta.
[ ] Los fragmentos literales aparecen en el original.
[ ] El resultado quedó anotado en registro.md.
```

Más adelante, varias comprobaciones pueden convertirse en un script: detectar campos vacíos, rutas rotas, categorías desconocidas o fuentes duplicadas. El criterio editorial seguirá necesitando revisión, pero la estructura no tiene por qué revisarse a mano cada vez.

Aquí se ve con claridad para qué sirve el arnés. El agente propone que la tarea está terminada; el sistema reúne evidencia para decidir si podemos aceptarla.

También cambia la forma de corregir errores. Si el agente inventa una fecha, no basta con repetir el prompt con más énfasis. Actualizamos `AGENTS.md` para indicar que debe detenerse cuando falte ese dato y añadimos una condición de cierre: la fecha de `ficha.md` tiene que aparecer en `original.md`. La corrección queda incorporada al sistema y se aplica en las siguientes sesiones.

**El fallo deja de ser una anécdota de la conversación y se convierte en información para mejorar el proceso.**

---

## Seis pruebas para comprobar si el arnés funciona

Cada prueba parte de una situación concreta y define qué debería hacer el sistema. Si el resultado es distinto, hemos encontrado un fallo en el arnés.

1.

**Probamos una transcripción válida.** Incluye título, fecha y URL. **El resultado correcto** es que el sistema guarde `original.md` y `ficha.md` dentro de `fichas/<id>/`, añada la entrada al catálogo y anote el proceso en el registro.

2.

**Probamos una transcripción sin URL.** **El resultado correcto** es que el archivo permanezca en `inbox/`, no se añada al catálogo y el sistema indique qué dato debemos completar. Si inventa una URL o da el trabajo por terminado, el arnés ha fallado.

3.

**Probamos una transcripción duplicada.** Su URL ya figura en el catálogo. **El resultado correcto** es que el sistema señale la coincidencia y no cree otra ficha ni mueva el archivo. Si guarda una segunda copia sin avisar, el arnés ha fallado.

4.

**Probamos un contenido que no encaja en la taxonomía.** **El resultado correcto** es que el sistema explique la duda y nos pida una decisión. Si crea una categoría nueva por su cuenta, el arnés ha fallado.

5.

**Modificamos un original después de procesarlo.** Volvemos a calcular su SHA-256 y lo comparamos con el valor guardado en la ficha. **El resultado correcto** es que el sistema detecte que los valores no coinciden y avise del cambio. Si lo pasa por alto, hemos perdido la garantía de que la ficha sigue vinculada al mismo original.

6.

**Buscamos una idea con palabras distintas de las etiquetas.** **El resultado correcto** es que el sistema localice posibles fichas, consulte los originales y responda con fragmentos y fuentes que podamos comprobar. Si responde sin volver a las fuentes, no podemos verificar el resultado.

Estas pruebas no miden solo la calidad del resumen. Comprueban si el sistema completa un caso válido, se detiene ante un problema, conserva el original y deja evidencia de sus decisiones

## No construyas una plataforma cuando todavía necesitas una carpeta

Al hablar de `arneses `aparecen enseguida bases vectoriales, orquestadores, memoria semántica, colas de tareas y equipos de agentes. Algunas bibliotecas necesitarán esas piezas. La nuestra todavía no.

Para unas decenas o cientos de transcripciones, una estructura de archivos y un catálogo pueden ser suficientes para descubrir el proceso real. Nos permiten saber qué campos importan, qué taxonomía aguanta el uso, qué búsquedas hacemos de verdad y dónde falla el agente.

Solo después tendrá sentido preguntar si necesitamos una base de datos, búsqueda semántica o varios agentes trabajando en paralelo. Añadir arquitectura antes de conocer esos patrones no elimina la incertidumbre. La esconde dentro de un sistema más caro de mantener.

La versión mínima del arnés responde cinco preguntas:

1.

**¿Dónde entra el trabajo?** En `inbox/`.

2.

**¿Qué reglas debe consultar?** El mapa del proyecto y la taxonomía.

3.

**¿Dónde queda el estado?** En las fichas, el catálogo y el registro.

4.

**¿Qué puede modificar?** Solo las salidas necesarias.

5.

**¿Cómo se comprueba?** Con condiciones observables y, cuando sea posible, validaciones automáticas.

Si no puedes responder estas preguntas, cambiar de modelo probablemente no arreglará el proceso.

**Tools are great. Systems are better.**

Una skill conserva una forma de clasificar. Un agente puede recibir el encargo y realizar el trabajo. El arnés hace que ese trabajo ocurra dentro de un entorno que recuerda, limita y comprueba.

Ese es el salto de esta serie: dejar de pensar solo en lo que el modelo puede responder y empezar a diseñar **las condiciones que necesita para trabajar bien más de una vez**.

---

## Sigue la serie: de prompts a sistemas.

En la primera entrega vimos cómo crear una skill pequeña, activable y verificable. En la segunda, cómo elegir entre una conversación principal, un subagente, un agente reutilizable y un equipo.

En esta tercera hemos unido las piezas dentro de un entorno de trabajo: instrucciones que funcionan como mapa, estado fuera de la conversación, permisos ajustados a la tarea y pruebas que deciden cuándo aceptar el resultado.

---

---

## Recursos

-

[OpenAI: Harness engineering — leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)

-

[OpenAI: The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)

-

[Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

-

[Anthropic: Scaling Managed Agents — Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents)

-

[AGENTS.md: formato abierto para guiar agentes](https://agents.md/)

-

[Think&Hack: Cómo crear una skill para que tu agente tome mejores decisiones](https://ainalluna.substack.com/p/crear-skills-agentes-ia-verificables)

-

[Think&Hack: Un agente, un subagente o un equipo — ¿qué necesitas realmente?](https://ainalluna.substack.com/p/crear-agentes-claude-code)

***Cuéntamelo. Siempre leo todo.***

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

# **Suscríbete a Think&Hack**

**Tools are great. Systems are better.**

Casos reales, flujos que funcionan y formas concretas de usar la IA sin perder el control del proceso.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
