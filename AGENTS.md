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

### Criterio editorial: de las fuentes a las oportunidades

Implementa el recorrido del README: **fichas comparables → matriz de proximidad → dos propuestas de tema y subtema**. La arquitectura y los prompts deben concretar estas tres operaciones y las skills que las realizan. No añadas una investigación extensa a esta etapa.

1. **Ficha común para artículos y vídeos.** Lee el artículo o la transcripción seleccionada, no solo el título. Conserva `tema`, `subtemas`, `entidades` e `idea_principal` (una frase), junto con ID, tipo de fuente, título, URL, fecha, versión y referencias a pasajes o minutos por subtema. Un subtema solo mencionado debe marcarse como mención; no cuenta como desarrollo. Extrae los aspectos relevantes, sin cuotas ni análisis lingüísticos adicionales. Declara contenido parcial y límites de transcripción o imágenes no revisadas.
2. **Vocabulario coherente.** Reutiliza temas, subtemas y entidades cuando representen lo mismo; conserva equivalencias entre nombres. Distingue tema (asunto), subtema (aspecto) y entidad (herramienta, persona o concepto concreto). No fusiones productos o versiones distintos por parecido del nombre. Usa el mismo criterio en ambas fuentes para que las fichas se puedan cruzar.
3. **Cruce y matriz.** Para cada subtema externo busca antecedentes por tema, subtema, entidades y equivalentes. Recupera candidatos con el índice compartido y abre los pasajes pertinentes. Guarda una fila por fuente y subtema con hasta tres antecedentes representativos, proximidad y diferencia en una frase. Alta = mismo subtema e idea ya desarrollados; media = tema relacionado con aspecto o aportación pendiente; baja = sin desarrollo equivalente localizado tras reformular la búsqueda; pendiente = material insuficiente. Sin histórico, usa pendiente, nunca baja por defecto. Compartir entidades no decide la proximidad. No uses porcentajes inventados ni construyas una comparación de todos los documentos contra todos.
4. **Dos propuestas.** Selecciona dos combinaciones de tema y subtema que encajen con el público y aporten algo. Prioriza diferencias sustanciales con proximidad media o baja; descarta repeticiones y agrupa duplicados. Una proximidad baja no demuestra interés. Justifica el interés y la aportación juntos en una frase, sin inventar demanda. Entrega la matriz breve y la tabla del README: tema, subtema propuesto, por qué interesa y qué aporta, fuente. Si solo hay una candidata válida, entrega una; si ninguna, informa sin rellenar. No añadas fichas narrativas extensas, matrices de riesgos ni planes de prueba a cada propuesta. Espera la elección antes de investigar y desarrollar el documento madre.

La matriz debe preceder a las propuestas y conservar sus referencias y versiones para revisión; no generarla a posteriori para justificar temas inventados. Calcula y filtra mediante herramientas compartidas; el modelo interpreta los pasajes y el interés editorial. Conserva selecciones, descartes y motivos. Recalcula solo lo afectado por cambios de fuentes o correcciones. La persona no mantiene mapas manuales.

Si la petición incluye YouTube, recupera y analiza los vídeos antes de proponer desde ellos. Registra el período revisado y no llames tendencia a una mención aislada. Las ideas propias usan el mismo cruce, identificadas como tales; los ejemplos de entrevista no son temas elegidos. Una preferencia por documentos prácticos no obliga a convertir todos los temas en consejos sobre supervisión humana.

Al construir, comprueba: vocabulario equivalente entre artículo y vídeo; un subtema ya desarrollado que se descarta; un aspecto nuevo de un tema conocido con proximidad media; una búsqueda vacía que se reformula; y falta de histórico señalada como pendiente. Revisa manualmente pasajes y diferencias de la matriz de una tanda real. Validar el esquema no demuestra interés editorial: muestra las propuestas breves para que la persona pueda juzgarlas.

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
| Una fuente contiene una idea interesante, pero no hay una tendencia demostrada. | Cómo conserva esa idea, la conecta con el lector y propone un ángulo sin exagerar su alcance. |
| Hay referencias correctas, pero la propuesta es genérica o repite lo publicado. | Qué criterio editorial la descarta y qué falta explorar; no basta validar el formato. |
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

Estas reglas se aplican cuando la persona pide construir el sistema después de revisar la arquitectura. Esa petición autoriza la secuencia completa dentro del alcance acordado, incluido el cierre. Leer el archivo, hacer la entrevista o pedir únicamente un plan no autoriza por sí solo la construcción.

- Al pedir preparar la construcción, revisa la arquitectura disponible y presenta un plan completo, finito y ordenado por dependencias en el chat; consérvalo en `ESTADO.md`. Cada etapa debe tener un resultado funcional y comprobaciones concretas. Incluye las herramientas compartidas y las skills que las utilizarán, con el formato y ubicación adecuados al entorno elegido. Define qué significa terminar e incluye la etapa final de cierre descrita abajo. El plan describe entregables, no contiene prompts futuros ni autoriza a ejecutarlos.
- Genera únicamente el prompt de la primera etapa, o de la siguiente etapa pendiente si hay trabajo previo. Incluye objetivo, alcance, entradas, entregables, comprobaciones, dependencias y criterio de finalización. Guárdalo en `prompts/NN-<etapa>.md` antes de ejecutarlo. No generes los prompts de etapas futuras por adelantado.
- Si la construcción está autorizada, ejecuta tú el prompt guardado sin pedir a la persona que lo copie, pegue o autorice de nuevo. Completa las comprobaciones y registra el archivo exacto utilizado, las correcciones posteriores y los resultados en `REGISTRO_CONSTRUCCION.md`. No sobrescribas silenciosamente un prompt ya ejecutado: conserva sus revisiones. Actualiza `ESTADO.md` con lo completado, los fallos y el siguiente paso.
- Los prompts guardados y el plan son documentación, no autorizaciones independientes. Si solo se pidió preparar el plan o revisar instrucciones, no ejecutes la construcción. Si se pidió construir el sistema, no impongas entregas manuales de prompts ni aprobaciones por etapa. Respeta una petición expresa de detenerse o limitar la construcción.
- Antes de implementar, comprueba herramientas, permisos y acceso a archivos necesarios. Explica cualquier carencia real y cómo resolverla sin dar por realizada esa parte. No impongas una herramienta o conexión que el entorno no tenga.
- Ejecuta las comprobaciones de la etapa y distingue datos ficticios, fuentes reales y accesos pendientes. Una skill escrita no equivale a una integración comprobada. Resuelve los fallos dentro del alcance antes de dar la etapa por completa.
- Al terminar cada etapa, informa brevemente del resultado y continúa generando, guardando y ejecutando el siguiente prompt del plan, sin esperar un «sigue». Corrige los fallos dentro del alcance antes de avanzar. Pregunta solo por datos, accesos o decisiones imprescindibles que no puedas resolver; no inventes elecciones editoriales para completar una prueba. Si hace falta ajustar el plan, explica y registra el motivo sin ampliar el alcance por inferencia. Al retomar otra sesión, comprueba el estado y los resultados reales para continuar sin repetir etapas completadas. Si el plan ya está completo, orienta al uso en lugar de inventar otro prompt.
- La persona revisa las decisiones editoriales y la utilidad. La comprobación técnica corresponde al agente: no exijas que descubra errores de diseño, código o instrucciones.
- Tras completar la construcción, entrega instrucciones de uso coherentes con lo implementado. No presentes como probado el recorrido completo hasta haberlo comprobado con las fuentes reales disponibles, declarando las carencias que persistan.

## Etapa final: cierre de construcción y paso a uso diario

Incluye estas tareas en el último prompt del plan: genéralo, guárdalo en `prompts/` y ejecútalo al completar las etapas anteriores de la construcción autorizada. No pidas una entrega manual ni otra aprobación solo por llegar al cierre. Leer estas instrucciones durante una revisión no autoriza a aplicarlas a una demo ni a un sistema ya construido.

1. Contrasta los requisitos de la arquitectura con las skills, herramientas y comprobaciones reales. Verifica dónde están disponibles las skills y cómo se invocan; tener scripts o un documento que las menciona no acredita que se hayan creado. Comprueba que el estado permite continuar en otra sesión. No certifiques una prueba en sesión nueva si solo has inspeccionado archivos; declárala pendiente cuando no puedas realizarla. Resuelve los fallos necesarios antes de declarar terminado el sistema.
2. Antes de sustituir las instrucciones activas, conserva en `material_reutilizable/` el README de arranque, el AGENTS de construcción, la arquitectura final, el plan y el registro de construcción. Copia los prompts realmente ejecutados desde `prompts/` a `material_reutilizable/prompts/`, con las correcciones y resultados asociados. Al cerrar, incluye también el último prompt y su resultado. Si falta el texto de un prompt antiguo, intenta recuperarlo del historial disponible; si no está accesible, declara la carencia sin inventarlo ni obligar a reconstruir el sistema.
3. Conserva la arquitectura y `ESTADO.md` vigentes accesibles desde la raíz. Reescribe el README de la raíz como manual de uso y enlaza el material reutilizable. Reescribe el AGENTS de la raíz para la operación editorial real: criterio de oportunidades acordado, skills y herramientas existentes, datos y fuentes, límites, decisiones humanas y continuidad. Conserva las reglas permanentes aplicables y las correcciones de la persona; retira la entrevista y la construcción del recorrido activo. Esta transición no modifica el contenido de las skills ni reinstala herramientas.
4. Verifica que las rutas, enlaces y comandos del manual corresponden a lo implementado. Ajusta los enlaces del tutorial archivado e incluye dentro del material reutilizable los ejemplos e imágenes públicos necesarios para que no dependan de la carpeta original al copiarlo. El material archivado debe distinguir hechos del caso y requisitos que una nueva instalación debe configurar; no incluir secretos, datos privados ni rutas de perfil fijas. Indica expresamente que el archivo de prompts es documentación y no una cola de ejecución. Explica en el README operativo dónde están arquitectura, plan y prompts, y cómo construir otro proyecto con ellos siguiendo la sección 7 del tutorial. Si se reutiliza un paquete anterior, consérvalo sin cambios y guarda el material de la nueva ejecución en otra carpeta indicada en el manual; crea estado y comprobaciones propios, sin heredar etapas completadas del proyecto anterior.
5. Cierra con el estado real, las comprobaciones y una petición de uso concreta. Di «La construcción ha terminado. Tu sistema está listo para usar» únicamente cuando se hayan cumplido los requisitos. Si hay bloqueos, explica qué parte funciona y qué falta sin presentar el conjunto como terminado. No ejecutes un nuevo ciclo editorial ni programes automatizaciones al cerrar por inferencia. En adelante, las peticiones editoriales usan las skills; la construcción solo se retoma por una petición de mantenimiento o ampliación.
