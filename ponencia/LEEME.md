# Bloque técnico de «De chat a sistemas» · versión 2

Generado el 2026-10-14. Sustituye por completo a la primera versión.

## Qué cambió respecto a la primera versión

- **Patrón visual tuyo**, no de plantilla: título grande en Inter Bold, subtítulo corto en coral, tres o cuatro líneas a la izquierda y, a la derecha, una ilustración tuya o una captura real con recuadro rojo. Sin cajas, sin tablas de consultoría, sin GIF.
- **Solo material real del repositorio.** Cada captura sale de un archivo que existe: `SKILL.md`, el informe de ejecución de hoy, el inventario, una ficha, el esquema, las señales de un vídeo, `mapa-temas.md`, `estilo.md`, la salida de las 11 pruebas y el texto de los prompts 04 y 05. Nada inventado. Las dos únicas capturas que no son del repo son el ejemplo «Ayuda con reuniones» frente a `decision-brief`, que es de tu artículo del 5 de julio.
- **Buenas prácticas con fuente.** Cómo se escribe la description (tu artículo), qué va en SKILL.md y qué en references (tu artículo + Harper), menos de 500 líneas (Harper), escribe lo que la IA no sabe y lo que no debe hacer (Harper), guarda el script que funcionó (vídeo Anthropic), tres peticiones para probar la activación (Harper), con y sin skill (tu artículo), diagnóstico proceso/contexto/regla/código (vídeo Anthropic), las cinco preguntas (tu artículo).

## Archivos

| Archivo | Qué es |
|---|---|
| `ConIA_bloque_tecnico.pptx` | 17 diapositivas nuevas, con guion, tiempo y fuente en las notas |
| `generar_bloque_tecnico.py` | Generador del PPTX |
| `recursos.py` | Genera las capturas en `capturas/` leyendo los archivos reales del repo. Si el repo cambia, se vuelve a ejecutar |
| `capturas/` | Las capturas (editor oscuro, recuadro rojo, chip con el nombre del archivo) |
| `ilustraciones/` | Tus ilustraciones extraídas de ConIA y de MujeresEnSEO a resolución completa |
| `render/` | Vista previa PNG de cada diapositiva, exportada con PowerPoint. Ahí Inter se sustituye por otra fuente; en Google Slides se ve con Inter |

Regenerar todo: `python ponencia/recursos.py && python ponencia/generar_bloque_tecnico.py`

## Montaje en la copia de Google Slides

Copia de trabajo: https://docs.google.com/presentation/d/16N2tKTRIzIYPmZ9eFss4xJSp8vtmSW3-VwjzkNr95gE/edit

Se conservan tuyas: 1–11 (incluido tu diagrama oscuro «02. Definir el proceso»), «// SKILLS // AGENTES // SCRIPTS» con la tríada, «Skill» con la caja de herramientas, «AGENTES», «Agente» con la máquina, y el cierre (Tools are great, Preguntas, Gracias). Se borran: «El proceso» (texto de SEO), «SKILLS», «RESULTADO» y «RECURSOS Y REFERENCIAS».

Orden final:

| # | Diapositiva | De quién | Tiempo |
|---|---|---|---|
| 1–11 | Introducción, método, objetivo, proceso | tuyas | 7:30 |
| 12 | Dónde usar IA y dónde no | nueva | 1:00 |
| 13 | … de la regla sale la arquitectura | nueva (texto de MujeresEnSEO) | 0:40 |
| 14 | // SKILLS // AGENTES // SCRIPTS + tríada | tuya | 0:30 |
| 15 | Skill (caja de herramientas) | tuya | 0:40 |
| 16 | Una skill no falla por el Markdown (description mala / buena) | nueva | 1:30 |
| 17 | La skill guarda el método (SKILL.md real) | nueva | 1:00 |
| 18 | Qué va dentro y qué va fuera (árbol real) | nueva | 1:15 |
| 19 | La IA lee solo lo que necesita (README real) | nueva | 1:00 |
| 20 | Script (tu ilustración de la prensa) | nueva con tu imagen | 1:00 |
| 21 | El script hace lo repetible (informe real: 55 newsletters) | nueva | 1:00 |
| 22 | Se prueba antes de usarse (11 pruebas reales) | nueva | 1:00 |
| 23 | AGENTES | tuya | 0:15 |
| 24 | Agente (máquina) | tuya | 0:45 |
| 25 | El modelo juzga, el script valida (ficha real) | nueva | 1:15 |
| 26 | El contrato entre etapas (esquema real) | nueva | 0:45 |
| 27 | Interés real: lo calcula el script (vídeo real, 150 vídeos) | nueva | 1:00 |
| 28 | El agente decide dentro de límites (cuatro condiciones, texto real) | nueva | 1:15 |
| 29 | El arnés: qué cuenta como terminado (prompt 05, texto real) | nueva | 1:30 |
| 30 | Arregla la skill, no la respuesta (estilo.md real) | nueva | 1:15 |
| 31 | El resultado, hoy (mapa-temas.md real) | nueva | 0:45 |
| 32 | Cinco preguntas antes de una skill | nueva | 1:00 |
| 33–35 | Tools are great · Preguntas · Gracias | tuyas | 0:45 |

Suma unos 29 minutos. Para entrar en 20 hay que elegir. Mi propuesta de recorte, en este orden: 26 (el contrato se explica en la 25), 19 (la carga progresiva cabe en la 18), 13 (ya lo dice la 12), 22 (las pruebas caben en la 21), y acortar la intro 1–11 a 6 minutos. Con eso quedan unos 21.

Pasos: Archivo → Importar diapositivas → Subir → `ConIA_bloque_tecnico.pptx`; selecciona todas, desmarca «Mantener el tema original»; colócalas según la tabla. Comprueba que la tipografía es Inter; para Consolas, Google Slides usará Courier New si no la tiene.

## Vocabulario definido en escena

| Término | Cómo se dice | Dónde |
|---|---|---|
| Tomar una decisión | Elegir entre opciones mirando la información y aplicando una regla que podemos escribir | 12 |
| Criterio | Esa regla escrita, con ejemplos de sí y de no | 12 |
| Sale siempre igual | En lugar de «determinista» | 12 |
| Skill | Carpeta con instrucciones: cuándo se usa, qué hace, qué no puede hacer | 15–18 |
| Script | Programa que fija una operación que no debería depender del modelo | 20 |
| Agente | Recibe el trabajo y decide dentro de límites | 24, 28 |
| Contrato | Lo que una etapa entrega a la siguiente, con los mismos campos | 26 |
| Arnés | Controla el entorno y qué cuenta como terminado | 29 |
| Evidencia | Una prueba fuera de la respuesta de la IA | 29 |

Fuera de escena: LLM, YAML, frontmatter, BM25, SHA-256, Glossa. «Tokens» aparece solo en tu diapositiva del script, como en MujeresEnSEO.
