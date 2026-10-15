# Plan de la ponencia · De chat a sistemas (ConIA Madrid, 17 oct 2026, 20 min)

Fecha del plan: 2026-10-14. La primera ejecución se rechazó por calidad (plantilla, ejemplos inventados, sin buenas prácticas). La versión 2, con el patrón visual real de Aina y solo material del repositorio, está descrita en `ponencia/LEEME.md`, que sustituye a la estructura de la sección 4 de este plan.

## 1. Qué he entendido

**Fuentes leídas**

| Fuente | Qué aporta |
|---|---|
| HANDOFF de la conversación anterior | Narrativa aprobada de las diapositivas 1–8, objetivo y proceso de la demo, contrato técnico, reglas de colaboración |
| Repo `conia` (ARQUITECTURA.md, prompts 00–08, SKILL.md de `recuperar-newsletters`, biblioteca con 5 artículos reales) | El caso de uso real: 8 skills, 5 fases, fichas con esquema fijo, puntos de control humanos |
| Transcripción vídeo «Anthropic dejó de crear agentes» | Cuatro principios: guardar código probado, cargar contexto solo cuando hace falta, convertir correcciones en instrucciones permanentes, verificar antes de entregar |
| Transcripción taller Fred Harper | Anatomía de SKILL.md, descripción como disparador, tres niveles de carga, «escribe lo que la IA no sabe», «dile qué no hacer», «si te repites tres veces, es una skill» |
| Guion oral y PPTX MujeresEnSEO | Regla base (cuantitativo → script, cualitativo → IA como clasificador), Skill ≠ Agente ≠ Script, arnés Default-FAIL |
| Dos PPTX locales de hoy en Descargas (21 y 16 diapositivas) | Dos versiones alternativas con guion y tiempos. **Ninguna sigue la narrativa aprobada del handoff** (Pipo, SEO, radar, El fundador) |

**Lo que no he podido leer:** las dos Google Slides. Google Drive pide reautenticar (`/mcp`) y la extensión de Chrome no está conectada. Trabajo con el handoff como fuente de verdad de lo aprobado.

**Estado real:** diapositivas 1–8 aprobadas, 9 (método Think&Hack), 10 (objetivo) y 11 (proceso) diseñadas. Falta todo el bloque técnico (12 en adelante) y el cierre. Ahí está el atasco.

## 2. Diagnóstico: por qué estás encasquillada

Tienes tres decks compitiendo y dos de ellos empiezan por la definición de Skill. El handoff decidió lo contrario: primero el proceso Think&Hack, después cada pieza técnica como respuesta a una necesidad concreta. Las versiones de Descargas rompen esa decisión y por eso no encajan.

Segundo problema: el vocabulario. El repo y el guion de MujeresEnSEO hablan de «criterio», «determinista», «contrato», «evidencia», «arnés». Para marketing no técnico cada una de esas palabras necesita una definición en una frase antes de usarse. Sin eso, el bloque técnico se convierte en una lista de definiciones sueltas, que es justo lo que el handoff prohíbe.

## 3. Vocabulario que vamos a definir en escena

Cada término aparece una sola vez, con un ejemplo del proceso Think&Hack, y se reutiliza siempre con la misma palabra.

| Término | Definición llana | Ejemplo Think&Hack |
|---|---|---|
| Tomar una decisión | Elegir entre varias opciones mirando información y aplicando una regla que podemos escribir | ¿Este tema es nuevo, amplía algo que ya publicamos o ya está cubierto? |
| Criterio | La regla escrita que usamos para decidir, con ejemplos de sí y de no | «No proponemos un tema si no podemos aportar algo que el vídeo original no demuestra» |
| Trabajo que sale siempre igual (determinista) | Una operación que con los mismos datos da el mismo resultado. No hace falta pensar, hace falta repetir | Descargar las newsletters, comparar si un artículo ha cambiado, contar cuántos canales hablan de un tema |
| Skill | Una carpeta con instrucciones escritas que explica cuándo se usa, cómo se hace una tarea y qué no se puede hacer | `recuperar-newsletters/SKILL.md` |
| Script | Un programa que hace una operación de las que salen siempre igual | `recuperar_newsletters.py` |
| Agente | La IA cuando recibe un objetivo, consulta lo que necesita, usa herramientas y decide dentro de unos límites | El que lee los artículos parecidos y decide la cobertura |
| Contrato | Lo que una etapa se compromete a entregar a la siguiente, con campos fijos | La ficha de cada artículo (tema, enfoque, tesis, nivel) |
| Evidencia | Una prueba que existe fuera de la respuesta de la IA: un archivo, una fuente, un resultado de comprobación | `afirmaciones.json` con cada afirmación marcada como verificada, refutada o sin confirmar |
| Arnés | El entorno que ejecuta el proceso y comprueba que cada etapa ha dejado lo que tenía que dejar | Si no existe la investigación aprobada, no se puede redactar |
| Carga progresiva | La IA lee primero solo el nombre y la descripción de cada skill; el resto, solo cuando la usa | 8 skills disponibles, solo una cargada cada vez |

Palabras que evitamos en escena: «determinista» (se dice «sale siempre igual»), «LLM», «tokens», «frontmatter», «BM25», «SHA-256», «YAML».

## 4. Estructura propuesta: 22 diapositivas, 20 minutos

Bloques A y B son lo aprobado. El bloque C es lo nuevo. Cada diapositiva del bloque C abre con la necesidad del proceso que resuelve.

### Bloque A · Introducción (aprobada) · 0:00–4:30

| # | Diapositiva | Tiempo | Estado |
|---|---|---|---|
| 1 | Portada | 0:15 | Aprobada |
| 2 | Ponente | 0:20 | Aprobada |
| 3 | Pipo (TikTok, 35.200 seguidores) | 0:40 | Aprobada |
| 4 | Análisis de entidades SEO | 0:40 | Aprobada |
| 5 | Radar de ideas Think&Hack | 0:40 | Aprobada |
| 6 | ¿Qué tiene que ver un náufrago con el SEO? | 0:20 | Guion aprobado |
| 7 | El fundador: objetivo, vídeo 25 s, análisis | 1:20 | Guion aprobado |
| 8 | Tesis: De chat a sistemas | 0:35 | Guion aprobado |

### Bloque B · Método, objetivo y proceso (diseñado) · 4:30–7:30

| # | Diapositiva | Tiempo | Qué debe entender la sala |
|---|---|---|---|
| 9 | Método Think&Hack: objetivo → proceso → piezas | 0:45 | No se empieza por la tecnología |
| 10 | Objetivo: crear contenido para Think&Hack a partir de oportunidades reales | 0:45 | Qué queremos y las dos restricciones: no inventar, no perder lo aprendido |
| 11 | Proceso: 5 etapas con retorno al inventario | 1:30 | El flujo de trabajo, sin tecnología todavía. Transición: «no todas las etapas necesitan el mismo tipo de trabajo» |

### Bloque C · Del proceso a las piezas (nuevo) · 7:30–18:00

| # | Diapositiva | Tiempo | Necesidad del proceso que resuelve | Pieza que se introduce | Material real del repo |
|---|---|---|---|---|---|
| 12 | Dos tipos de trabajo | 1:00 | Separar lo que sale siempre igual de lo que exige mirar y elegir. Aquí se define «tomar una decisión» y «criterio» | Ninguna todavía: solo la separación | Tabla de las 5 etapas con dos columnas (del contrato técnico del handoff, simplificada) |
| 13 | Necesidad: que el método no dependa de que yo lo recuerde | 1:00 | Cada semana repito a la IA cómo descargar y revisar lo publicado | **Skill** | `recuperar-newsletters/SKILL.md` en pantalla, resaltado: cuándo se usa, qué lee, qué escribe |
| 14 | Por dentro de una skill | 1:15 | Qué escribo yo y qué no hace falta escribir | Anatomía: nombre, descripción, pasos, referencias, scripts. Principio Harper: escribe lo que la IA no sabe y lo que no debe hacer | Carpeta real `.agents/skills/recuperar-newsletters/` |
| 15 | Necesidad: tener 8 skills sin que la IA lea las 8 cada vez | 0:45 | Si lo carga todo, se confunde y cuesta más | **Carga progresiva** en tres pasos: descubre, activa, usa recursos | Las 8 descripciones en una columna, una abierta |
| 16 | Necesidad: que la descarga salga igual hoy y en marzo | 1:00 | Comparar huellas, detectar cambios, no inventar un artículo que no se pudo descargar | **Script**. Principio Anthropic: guarda el código que ya funcionó, no lo reescribas | `recuperar_newsletters.py` y `control/inventario.json` reales |
| 17 | Necesidad: decidir si un tema es oportunidad | 1:15 | Hay que leer los artículos parecidos y aplicar el criterio | **Agente** con límites: lee, decide cobertura y aportación, entrega un JSON. La decisión final la aplica un script con las cuatro condiciones | Las cuatro condiciones de `detectar-oportunidades` y una oportunidad `.md` de ejemplo |
| 18 | Necesidad: que cada etapa sepa qué le llega y qué entrega | 0:45 | Sin esto, cada paso interpreta el anterior de forma distinta | **Contrato** = ficha con campos fijos | Ficha de artículo real (tema, enfoque, tesis, entidades, nivel) |
| 19 | Necesidad: que nadie redacte sin investigación aprobada | 1:00 | El proceso tiene tres puntos donde decide una persona | **Arnés**: ejecuta, comprueba que existe la entrega, para si falta. «Una fase no está hecha porque la IA lo diga; está hecha si su archivo existe» | Diagrama de las 5 etapas con los 3 rombos humanos |
| 20 | Necesidad: no publicar «reduce un 80 % el tiempo» sin fuente | 1:00 | Verificar antes de entregar. Principio Anthropic: tu primer vistazo no debería ser el primer vistazo del agente | **Evidencia**: cada afirmación verificada, refutada o sin confirmar | Ejemplo de `afirmaciones.json` y el verificador crítico de `investigar-tema` |
| 21 | Necesidad: que la corrección de hoy sirva mañana | 1:00 | Una skill no aprende sola. La corrección se escribe en `estilo.md` y la siguiente redacción la lee | **Aprender**: borrador vs publicado → regla | `registrar-resultado`: comparación y regla «no abrir con pregunta retórica» |
| 22 | El sistema completo | 1:00 | Las 5 etapas con sus skills, scripts, agentes y puntos humanos. Cierre del hilo: esto es «tu equipo de marketing» | Mapa final | Diagrama de ARQUITECTURA.md traducido a lenguaje llano |

### Bloque D · Cierre · 18:00–20:00

| # | Diapositiva | Tiempo |
|---|---|---|
| 23 | Cómo empezar mañana: un encargo real, tus correcciones, una prueba con otro caso | 1:15 |
| 24 | Tools are great. Systems are better. + Preguntas y enlaces | 0:45 |

Son 24 diapositivas en total. Si hay que recortar, se fusionan 15 con 14 y 18 con 17.

## 5. Puntuación de cada bloque (1 = inseguro, 5 = listo)

| Punto | Nota | Por qué |
|---|---|---|
| Bloque A (1–8) | 5 | Aprobado. No lo toco; solo lo reproduzco en el nuevo archivo |
| Bloque B (9–11) | 4 | Diseñado; falta el diagrama de las 5 etapas con retorno |
| Vocabulario definido (sección 3) | 4 | Es mi propuesta; necesita tu visto bueno, sobre todo «tomar una decisión» y «arnés» |
| Orden del bloque C | 4 | Sigue la secuencia del handoff (separar → skill → estructura → activación → agente → scripts → arnés → verificación → aprender). He movido scripts antes del agente porque el repo los usa antes, y así el agente llega cuando ya hay «suelo» |
| Materiales reales del repo | 3 | Solo existe la skill 01 construida. Las fichas, oportunidades y `afirmaciones.json` las tendré que crear como ejemplos verosímiles a partir de los esquemas de ARQUITECTURA.md, y rotularlos como «ejemplo» en notas |
| Tiempos | 3 | 20 minutos con 24 diapositivas obliga a 45–75 s por diapositiva técnica. Es factible solo si el guion de cada una es de 90–120 palabras |
| Glossa | 2 | El handoff dice que no está validada su integración. Propongo no mencionarla en escena y dejarla en notas |
| Animaciones | 3 | Ver sección 6 |

## 6. Cómo lo voy a construir

**Formato.** Un archivo PPTX nuevo, 16:9, con el look & feel Think&Hack: fondo crema `#EAE7DC`, texto `#1F2937`, acento coral `#FD6534`, gris `#555B61`, Inter para texto y Consolas para archivos y código. Lo genero con código (python-pptx) para que cada diapositiva sea editable y lo puedas importar a Google Slides.

**Guion.** Cada diapositiva lleva en notas: tiempo, qué debe entender la sala, guion oral de 90–120 palabras y fuente. Mismo formato que la versión de 21 diapositivas de Descargas, que es un buen patrón.

**Imágenes.** Nada de stock. Diagramas de proceso dibujados con formas nativas (cajas, flechas, rombos de decisión) y capturas reales de archivos del repo con tipografía de código. Las ilustraciones de Pipo, SEO y radar se reutilizan de tu deck.

**Animaciones.** Las animaciones de PowerPoint no sobreviven bien al paso a Google Slides. Propongo construir la progresión como diapositivas consecutivas (la 11 aparece etapa a etapa, la 15 abre una skill, la 19 ilumina los rombos). En pantalla se ve como animación y es editable en cualquier herramienta. Si prefieres animaciones nativas, lo hago en PowerPoint y asumimos que en Google Slides se pierden.

## 7. Preguntas que necesito resolver antes de generar

1. ¿La base es el handoff (Pipo, SEO, radar, El fundador) o alguno de los dos PPTX de Descargas de hoy? Asumo el handoff salvo que digas lo contrario.
2. ¿Puedes reautenticar Google Drive con `/mcp`? Así leo las Google Slides reales, reutilizo tus imágenes de las diapositivas 1–8 y puedo escribir la copia directamente en Drive. Sin eso, entrego un PPTX y lo importas tú.
3. Vocabulario: ¿aceptas «sale siempre igual» en vez de «determinista» y «arnés» con la definición de la sección 3?
