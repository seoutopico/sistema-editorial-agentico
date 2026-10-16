# Arranque y construcción guiada del sistema editorial

## Recorrido y alcance

Lee README.md. El concepto de partida es recuperar datos, analizar lo publicado, detectar oportunidades, investigar nuevos ángulos y redactar un documento madre. La entrevista concreta ese recorrido para una persona; no es una invitación a diseñar cualquier automatización.

El alcance termina en el documento madre. La adaptación por canal, la voz de marca, los calendarios y la publicación son ampliaciones. Si aparecen, explica brevemente que amplían el alcance y propone aplazarlas. No las incorpores por inferencia. Una petición expresa de cambiar el alcance debe tratarse como tal, respetando las instrucciones de la persona.

## Acceso a los archivos y ejemplos

- Lee README.md y estas instrucciones completos, aunque se hayan adjuntado al chat en lugar de estar en una carpeta local. No presupongas que la aplicación carga AGENTS.md automáticamente.
- Si falta uno de los dos archivos, pide ese archivo antes de continuar. No dependas de documentación de otra sesión ni de rutas personales de quien creó este material.
- Los archivos de `material_adicional/` son ejemplos de Aina. No los trates como respuestas, preferencias o autorizaciones de otra persona. No los leas para rellenar la entrevista salvo que se pida reproducir expresamente ese ejemplo.
- En una sesión con archivos adjuntos, entrega la arquitectura como archivo cuando el entorno lo permita y explica cómo conservarla para el siguiente paso. No afirmes que la has guardado en el ordenador de la persona si no tienes acceso a él.
- La lectura de este material activa únicamente la fase solicitada. Las instrucciones de fases posteriores son contexto.

## Cómo entrevistar

- Presenta las cinco preguntas del README en orden, una a una, con sus opciones o fórmula de respuesta. Espera la respuesta antes de pasar a la siguiente.
- Reutiliza respuestas explícitas de esta conversación, mostrándolas para que puedan corregirse. No uses respuestas de otras personas ni conviertas los ejemplos del README en datos del caso.
- Mantén cada paso concreto. Si la respuesta es demasiado amplia, ofrece dos o tres formas de acotarla y pide elegir. No hagas que la persona decida tecnologías.
- Recoge público y tema, material y volumen, proceso actual y dificultad principal, criterio de oportunidad y enfoque del documento madre. Puedes aclarar un dato imprescindible dentro de su pregunta; evita convertir el arranque en otra entrevista extensa.
- Si la persona no sabe qué elegir, recomienda una opción y explica por qué. Espera su respuesta; una recomendación no cuenta como elección.
- Las opciones orientan, no son un formulario rígido. Admite respuestas propias compatibles con el recorrido. Prioriza un caso inicial manejable; separa las ampliaciones deseadas.
- Sin archivo propio, diseña el arranque sin análisis de antecedentes inexistentes. Sin canales elegidos, deja su selección como pendiente. Sin acceso comprobado, no prometas recuperación completa. Si no hay histórico y se pide profundizar en lo publicado, aclara qué material se podrá aportar o ayuda a elegir otra prioridad.

## Cuándo escribir

- No crees `ARQUITECTURA.md`, ni siquiera como plantilla o borrador previo, antes de completar las cinco respuestas. Una respuesta puede declarar una carencia o una decisión pendiente: documéntala sin inventar datos. Aclara antes cualquier ambigüedad que impida definir el objetivo o la entrega.
- Después, resume las respuestas y crea `ARQUITECTURA.md` con lo indicado en el README. Vincula cada decisión relevante a una necesidad expresada; separa decisiones de la persona, propuestas técnicas y pendientes.
- Elige una organización sencilla acorde al volumen y acceso previstos. No fijes de antemano una base de datos, una cantidad de skills ni una estructura de carpetas. La prioridad de trabajo y el enfoque del documento deben cambiar de forma concreta el diseño resultante.
- Revisa que el recorrido sea viable con las fuentes declaradas y que el documento madre pueda servir a otro redactor sin depender del chat. El ejemplo será ilustrativo; no inventes investigación, pruebas o resultados reales.
- Antes de entregar, aplica los requisitos y la revisión de diseño siguientes. Corrige tú las omisiones; no traslades a la persona una lista de ajustes técnicos que debería pedirte.
- Entrega la arquitectura para revisión editorial y termina esta fase. No la marques como aprobada ni implementada por haberla escrito.

## Requisitos comunes de la arquitectura

Estos criterios se aplican después de recoger las respuestas. Definen la calidad del diseño, no respuestas anticipadas ni instrucciones para construirlo ahora. Resuélvelos en la arquitectura con mecanismos concretos y sencillos.

### 1. Memoria consultable y crecimiento

- Define un almacenamiento local consultable con un índice persistente y operaciones compartidas por las futuras skills. Concreta qué se guarda, cómo se identifica y cómo se consulta. No basta escribir «índice local» o dejar la elección esencial de búsqueda para más adelante.
- Las consultas deben filtrar y limitar resultados, recuperar fragmentos pertinentes y permitir ampliar la búsqueda. No dependas de que el modelo lea un índice JSON completo, enumere todas las fichas o recorra el archivo entero en cada consulta. Los originales y las entregas pueden seguir siendo archivos legibles; JSON puede servir para intercambio, sin sustituir el mecanismo de consulta.
- Elige y justifica una solución inicial por las necesidades recogidas, sin pedir al usuario que elija una base de datos. Evita servicios adicionales salvo necesidad. Declara los supuestos de volumen y uso; no prometas escalabilidad sin comprobaciones posteriores.
- Define identificadores estables, detección de duplicados y cambios, y actualización solo de textos o análisis afectados. Las referencias deben permitir volver del hallazgo al pasaje y a su versión.
- Explica cómo se buscarán antecedentes con vocabulario diferente y cómo se comprobará la calidad con ejemplos conocidos. No conviertas una búsqueda vacía en una afirmación absoluta de novedad.
- Define una fuente de verdad para cada dato editable. Los índices derivados deben poder regenerarse; las correcciones y decisiones de la persona no deben perderse al regenerarlos.

### 2. Exploración acotada de YouTube

- Separa la revisión de metadatos de la lectura de transcripciones. Selecciona candidatos por pertinencia para el lector antes del análisis profundo. La popularidad aporta contexto, no decide por sí sola.
- Propón valores iniciales concretos para la ventana temporal, el máximo de vídeos revisados por canal y el máximo de transcripciones analizadas por ejecución. Identifícalos como parámetros técnicos ajustables, no decisiones que la persona deba tomar para completar la entrevista.
- Conserva el identificador del vídeo, la fecha de consulta, la versión del contenido y el estado de procesamiento para evitar descargas o análisis repetidos sin motivo.
- Define qué ocurre sin transcripción, con acceso fallido o con contenido parcial. No registres un fallo como revisión completada. Una transcripción no demuestra por sí sola lo mostrado visualmente.
- Si no se han elegido canales, deja pendientes sus identidades y accesos, pero define el procedimiento. Una idea propia puede entrar sin pasar por YouTube.

### 3. Continuidad entre sesiones

- Concreta dónde se guardan las oportunidades, su estado, la selección o descarte y el motivo. Conserva el alcance del comentario; un descarte puntual no crea una prohibición general.
- Guarda la pregunta elegida, los hallazgos y pendientes de investigación, la última entrega y su revisión. Indica cómo una sesión nueva recupera el siguiente paso sin depender del chat.
- Define un avance mínimo de cada tarea y cómo retomar tras una interrupción sin duplicar trabajo ni perder el último resultado válido.
- Conserva las correcciones de la persona y señala qué entregas necesitan revisión al cambiar sus fuentes. No sobrescribas silenciosamente documentos ya revisados.

### 4. Investigación y redacción diferenciadas

- Aunque compartan una skill, define sus responsabilidades y salidas por separado. La investigación produce hallazgos, evidencia, discrepancias y ángulos; la redacción desarrolla el documento madre a partir de ese material.
- Permite consultar los hallazgos y revisar la redacción sin repetir la investigación; investigar de nuevo solo cuando lo exijan cambios o carencias de evidencia.
- Investiga las preguntas de la oportunidad elegida, no todas las afirmaciones de todos los vídeos relacionados.
- Mantén las decisiones humanas acordadas: elegir la oportunidad y revisar el documento madre. Diferenciar etapas no obliga a añadir aprobaciones por cada operación.
- El documento debe ser autónomo, desarrollado y trazable, con lo comprobado, lo documentado y lo pendiente claramente separados. Una prueba pendiente que afecta al núcleo impide presentarlo como una práctica validada.

## Revisión obligatoria del diseño antes de entregarlo

Contrasta la arquitectura con las cinco respuestas y recorre estos casos sobre el papel:

| Caso | El diseño debe explicar |
|---|---|
| Se importa dos veces lo mismo. | Cómo evita duplicados y análisis innecesarios. |
| Se busca un tema con otras palabras. | Cómo localiza y comprueba antecedentes con consultas acotadas. |
| Crecen el histórico y los vídeos. | Qué limita la lectura del modelo y cómo se medirá la recuperación al construir. |
| No hay histórico, canales o transcripción. | Qué puede hacer, qué queda pendiente y qué no puede afirmar. |
| Se cambia de sesión a mitad del trabajo. | Dónde están la elección, el avance, los motivos y el siguiente paso. |
| Se corrige una fuente o el documento madre. | Qué se actualiza, qué se conserva y qué necesita nueva revisión. |
| Otro redactor recibe el documento madre. | Cómo aprovecha el material sin reconstruir la investigación desde enlaces sueltos. |

Si un caso no tiene respuesta concreta, corrige el diseño antes de entregarlo. Comprueba también que no has añadido producción por canal ni otras funciones fuera del alcance. No rellenes el documento con políticas repetidas: explica cada mecanismo donde corresponda.

Registra brevemente lo revisado y los pendientes reales. Esta revisión es documental; no la presentes como una prueba de rendimiento, una conexión verificada ni una ejecución del sistema. Los accesos pueden quedar pendientes; la lógica de consulta y continuidad debe quedar definida.

## Archivos y fases posteriores

- `ARQUITECTURA.md` no viene incluido en el arranque. Si ya existe por una entrevista anterior, léelo y conserva el trabajo. Si la persona ya ha pedido revisarlo, aplica esa petición; si no ha indicado qué desea hacer, acláralo antes de sustituirlo.
- Comprueba si otra sesión ha modificado los archivos desde tu última lectura.
- No crees skills, scripts, bases de datos, conectores ni prompts de construcción hasta que la persona solicite esa fase. La entrevista no autoriza consultas a cuentas ni descargas reales.
- Usa rutas relativas en el repositorio. Mantén datos privados y credenciales fuera de él.

## Preparación y ejecución por etapas

Estas reglas se aplican cuando la persona solicita avanzar después de revisar la arquitectura; no se ejecutan al leer el archivo.

- Al pedir preparar la construcción, revisa la arquitectura disponible y presenta un plan breve por dependencias en el chat. Cada etapa debe tener un resultado funcional y comprobaciones concretas. Incluye las herramientas compartidas y las skills que las utilizarán, con el formato y ubicación adecuados al entorno elegido.
- Genera únicamente el prompt de la primera etapa, o de la siguiente etapa pendiente si hay trabajo previo. Incluye objetivo, alcance, entradas, entregables, comprobaciones, dependencias y condición de parada.
- Conserva el plan de preparación y los prompts en el chat. No crees una carpeta de prompts ni guardes instrucciones de ejecución anticipadas en el proyecto. Durante la construcción sí puedes conservar un registro factual del avance, pruebas y pendientes para retomar otra sesión.
- Preparar un prompt no autoriza a ejecutarlo. Ejecútalo solo cuando la persona te lo entregue expresamente para construir esa etapa. El plan completo no es una lista de tareas autorizadas.
- Antes de implementar, comprueba herramientas, permisos y acceso a archivos necesarios. Explica cualquier carencia real y cómo resolverla sin dar por realizada esa parte. No impongas una herramienta o conexión que el entorno no tenga.
- Ejecuta las comprobaciones de la etapa y distingue datos ficticios, fuentes reales y accesos pendientes. Una skill escrita no equivale a una integración comprobada. Resuelve los fallos dentro del alcance antes de dar la etapa por completa.
- Al terminar, explica lo conseguido, lo verificado y lo pendiente, y detente. Cuando se pida el siguiente prompt, contrasta la arquitectura con el estado real; no adelantes una etapa dependiente de otra incompleta.
- La persona revisa las decisiones editoriales y la utilidad. La comprobación técnica corresponde al agente: no exijas que descubra errores de diseño, código o instrucciones.
- Tras completar la construcción, entrega instrucciones de uso coherentes con lo implementado. No presentes como probado el recorrido completo hasta haberlo comprobado con las fuentes reales disponibles, declarando las carencias que persistan.
