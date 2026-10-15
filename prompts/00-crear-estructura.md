Crea la base de un sistema editorial que encuentra oportunidades de contenido, las investiga y las convierte en piezas para cada canal. Este es el primer prompt de una serie: los siguientes crearán una skill cada uno sobre esta base.

En este paso no crees skills, scripts ni carpetas de datos. Solo la estructura, la configuración y la documentación que los siguientes prompts van a respetar.

## 1. Documenta la arquitectura

Crea `ARQUITECTURA.md` con el contenido exacto del anexo de este prompt. Es el plano del sistema: estructura del repositorio, skills, esquemas de las fichas, cálculos y reglas para cada prompt. No lo resumas ni lo reinterpretes.

## 2. Crea la configuración

Crea `proyecto.config.json` con el ejemplo de la sección 5 del anexo. Son los valores de Think&Hack. Otra persona solo cambia este archivo y su lista de canales.

Crea `.env.example` solo con un comentario: no hace falta ninguna variable obligatoria (YouTube se consulta con `yt-dlp`, sin clave de API); las variables opcionales futuras se documentarán ahí.

Crea `requirements.txt` vacío, con un comentario que indique que cada skill añade aquí sus dependencias.

## 3. Crea la lista de canales

Crea `biblioteca/youtube/canales.md` con este contenido. Es una lista sencilla para que cada persona ponga los suyos:

```markdown
# Canales de YouTube

Un canal por línea. Sustitúyelos por los canales de tu nicho.

- https://www.youtube.com/@XavierMitjana
- https://www.youtube.com/@DotCSVLab
- https://www.youtube.com/@NateHerk
- https://www.youtube.com/@LiamOttley
- https://www.youtube.com/@NateBJones
```

No crees ninguna otra carpeta dentro de `biblioteca/`. La crea la skill que la llena.

## 4. Configura Git

Crea `.gitignore` para que:
- `.env` nunca se suba.
- Todo `biblioteca/` quede fuera, excepto `biblioteca/youtube/canales.md`.
- Se excluyan `__pycache__/` y `*.py[cod]`.

Si existe un repositorio Git, compruébalo con `git check-ignore -v` sobre `.env`, `biblioteca/youtube/canales.md` y una ruta inventada como `biblioteca/substack/articulos/prueba.md`. Si no existe, no lo inicialices; indica que la comprobación queda pendiente.

## 5. Escribe el README

Crea `README.md` breve, dirigido a quien quiere montar el sistema:

1. **Qué es:** una o dos frases y las cinco fases del proceso.
2. **Cómo montarlo:** ejecutar los prompts de `prompts/` en orden, uno por sesión, en un agente de programación con acceso a archivos y terminal. Revisar el resultado de cada uno antes de pasar al siguiente.
3. **Qué cambiar para tu publicación:** `proyecto.config.json`, `biblioteca/youtube/canales.md` y `.env`.
4. **Estado:** una tabla con los nueve prompts (00 a 08) de la sección 4 del anexo, la skill que crea cada uno y su estado. El 00 queda `hecho` y el resto `pendiente`. Cada prompt posterior actualizará su fila.
5. **Más detalle:** enlace a `ARQUITECTURA.md`.

No copies en el README lo que ya explica `ARQUITECTURA.md`.

## 6. Si el proyecto no está vacío

Inspecciona primero el directorio. No borres ni sobrescribas archivos que no estén en este prompt. Si encuentras configuraciones, listas de canales o documentación anteriores que se solapen con lo que creas, enuméralas al final con la propuesta de qué hacer con cada una, y espera confirmación.

## 7. Entrega

Al terminar, muestra:
- El árbol de archivos creado.
- El resultado de la comprobación de Git, o que queda pendiente.
- Los archivos anteriores que se solapan, si los hay.
- El siguiente paso: ejecutar `prompts/01-crear-recuperar-newsletters.md`.

## Anexo: contenido de ARQUITECTURA.md

````markdown
# Arquitectura del sistema editorial

> Define el sistema completo. Cada prompt de `prompts/` construye una parte de este diseño y no puede contradecirlo. Si el diseño cambia, se cambia primero este documento.

# Arquitectura del sistema editorial

> Define el sistema completo. Cada prompt de `prompts/` construye una parte de este diseño y no puede contradecirlo. Si el diseño cambia, se cambia primero este documento.

## 1. Objetivo

Crear contenido para una publicación a partir de **oportunidades reales**:

1. **Revisar lo publicado.** Qué temas hemos tratado y desde qué perspectiva.
2. **Encontrar oportunidades.** Temas relevantes que todavía no hemos desarrollado.
3. **Investigar y desarrollar.** Contrastar fuentes y construir un contenido principal sólido.
4. **Adaptar.** Preparar las piezas de cada canal.
5. **Aprender.** Incorporar lo publicado, las decisiones y las correcciones para la siguiente vez.

El sistema se monta **ejecutando los prompts de `prompts/` en orden, en una carpeta vacía**. Ningún prompt depende de repositorios ni de skills ya hechas. Cada uno especifica lo que construye, y otra persona lo adapta cambiando la configuración y su lista de canales.

## 2. Principios

- **Script para lo repetible, modelo para el juicio.** Descargar, limpiar, calcular métricas, buscar coincidencias y generar índices son operaciones deterministas: las hace Python sin IA. El modelo solo interpreta: resume, clasifica, compara y argumenta.
- **Fichas con esquema fijo.** Todo lo que analiza el modelo se guarda como ficha JSON con campos definidos. La salida es siempre comparable y no hay que volver a leer el original.
- **Caché por huella.** Cada pieza se identifica por su ID y la huella de su contenido. Solo se vuelve a analizar lo nuevo o lo que ha cambiado.
- **Un error nunca destruye datos válidos** ni se presenta como "sin novedades".
- **La persona decide.** El sistema propone y justifica. Elegir oportunidad, aprobar la investigación y aprobar el texto son decisiones humanas.
- **Escalar es añadir, no modificar.** Una fuente nueva o un paso nuevo es una carpeta y una skill nuevas que respetan los contratos de este documento.

## 3. Proceso completo

```text
                     proyecto.config.json + biblioteca/youtube/canales.md
                                         │
 ┌─ 1. REVISAR LO PUBLICADO ─────────────┼──────────────────────────────────┐
 │  recuperar-newsletters  (script)      │                                  │
 │     Substack ──► substack/articulos/  │                                  │
 │  analizar-biblioteca  (modelo+script) │                                  │
 │     artículos ──► substack/fichas/ ──► mapa-temas.md · estilo.md         │
 └──────────────────────────────────────────────────────────────────────────┘
                                         │
 ┌─ 2. ENCONTRAR OPORTUNIDADES ──────────┼──────────────────────────────────┐
 │  explorar-youtube  (script+modelo)    │                                  │
 │     canales ──► vídeos + señales ──► candidatos ──► subtítulos ──► fichas│
 │  detectar-oportunidades  (script+modelo)                                 │
 │     fichas externas × fichas propias × decisiones ──► oportunidades/     │
 └──────────────────────────────────────────────────────────────────────────┘
                                         │
                      ◆ La persona elige una oportunidad
                                         │
 ┌─ 3. INVESTIGAR Y DESARROLLAR ─────────┼──────────────────────────────────┐
 │  investigar-tema  (modelo + web)  ──► contenidos/<id>/investigacion.md   │
 │                      ◆ La persona aprueba la investigación               │
 │  redactar-contenido  (modelo)     ──► contenidos/<id>/principal.md       │
 │                      ◆ La persona corrige y aprueba                      │
 └──────────────────────────────────────────────────────────────────────────┘
                                         │
 ┌─ 4. ADAPTAR ──────────────────────────┼──────────────────────────────────┐
 │  adaptar-contenido  (modelo)      ──► contenidos/<id>/piezas/<canal>.md  │
 └──────────────────────────────────────────────────────────────────────────┘
                                         │
 ┌─ 5. APRENDER ─────────────────────────┼──────────────────────────────────┐
 │  registrar-resultado  (script+modelo)                                    │
 │     enlaza lo publicado, guarda métricas, decisiones y correcciones      │
 │     ──► decisiones.md · estilo.md · vuelve a ejecutar el paso 1          │
 └──────────────────────────────────────────────────────────────────────────┘
```

## 4. Estructura del repositorio

```text
.
├── README.md                     # Qué es, cómo montarlo y cómo usarlo cada semana
├── ARQUITECTURA.md               # Este documento: estructura, contratos y cálculos
├── proyecto.config.json          # Lo que cambia cada persona (sin secretos)
├── .env.example                  # Variables de entorno opcionales; ninguna es obligatoria
├── requirements.txt              # Dependencias Python de todas las skills
├── .gitignore
├── prompts/                      # Un prompt por pieza, ejecutados en orden
│   ├── 00-crear-estructura.md
│   ├── 01-crear-recuperar-newsletters.md
│   ├── 02-crear-analizar-biblioteca.md
│   ├── 03-crear-explorar-youtube.md
│   ├── 04-crear-detectar-oportunidades.md
│   ├── 05-crear-investigar-tema.md
│   ├── 06-crear-redactar-contenido.md
│   ├── 07-crear-adaptar-contenido.md
│   └── 08-crear-registrar-resultado.md
├── .agents/skills/
│   └── <skill>/
│       ├── SKILL.md              # Cuándo usarla, qué lee, qué escribe, cómo se ejecuta
│       ├── scripts/              # Python sin IA y sus pruebas
│       └── references/           # Esquemas de fichas y plantillas de salida
└── biblioteca/                   # Memoria del sistema
    ├── substack/                 # Fuente propia
    │   ├── articulos/<fecha>-<slug>.md
    │   ├── fichas/<post_id>.json
    │   ├── control/              # inventario.json, originales/, historial/, ejecuciones/
    │   └── INDICE.md
    ├── youtube/                  # Fuente externa
    │   ├── canales.md            # Lista editable de canales
    │   ├── videos/<video_id>/    # meta.json, subtitulos.vtt, transcripcion.md, ficha.json
    │   └── control/              # ejecuciones/<run_id>.json, metricas.jsonl
    ├── mapa-temas.md             # Qué hemos tratado, cuándo y desde qué enfoque
    ├── estilo.md                 # Voz de la publicación y correcciones aprendidas
    ├── oportunidades/
    │   ├── <fecha>-<slug>.md     # Una por oportunidad; su estado lo cambia la persona
    │   ├── INDICE.md             # Generado: orden de prioridad
    │   └── control/              # grupos.json, evaluaciones/<grupo_id>.json
    ├── contenidos/<id>/          # Un contenido por oportunidad aceptada
    │   ├── afirmaciones.json · fuentes.json · investigacion.md · revision.md
    │   ├── principal.md · principal.borrador.md   # Editado por la persona · original del modelo
    │   ├── piezas/<canal>.md
    │   └── resultado.json        # Artículo publicado, métricas y reglas derivadas
    └── decisiones.md             # Generado: aceptadas, descartadas, publicadas y motivos
```

**Para añadir una fuente** (newsletters ajenas, Reddit, blogs) se crea `biblioteca/<fuente>/` y una skill `explorar-<fuente>` que produzca **fichas externas con el mismo esquema** que YouTube (sección 6). `detectar-oportunidades` lee todas las fichas externas sin cambiar su código.

**Git.** Se comparte el sistema: prompts, skills, configuración, `canales.md` y la documentación. `biblioteca/` queda fuera de Git, excepto `youtube/canales.md`, porque contiene datos descargados y trabajo editorial propio. Las claves van en `.env`, que nunca se sube.

## 5. Configuración

`proyecto.config.json` es lo único que otra persona necesita cambiar, junto con `canales.md`:

```json
{
  "publicacion": {
    "nombre": "Think&Hack",
    "substack": "https://ainalluna.substack.com",
    "idioma": "es"
  },
  "linea_editorial": {
    "nicho": "IA aplicada al trabajo: procesos, agentes, automatización y creación de contenido",
    "audiencia": "Profesionales que quieren aplicar IA en su trabajo diario",
    "aportacion": "Probar las cosas y explicar el proceso real, con lo que funciona y lo que no"
  },
  "canales_salida": ["substack", "linkedin", "notes"],
  "recursos": {
    "herramientas": ["ChatGPT Plus (Codex, Projects, Work)", "Claude (Claude Code, Cowork)", "n8n", "Obsidian", "Substack", "WordPress"],
    "hardware": "PC Windows de consumo, sin GPU para modelos locales grandes",
    "formatos_que_domina": ["texto y capturas", "procesos y sistemas con agentes", "datos y hojas de cálculo"],
    "fuera_de_alcance": ["edición y producción de vídeo", "pruebas que exijan hardware caro o infraestructura propia"]
  },
  "youtube": {
    "videos_por_canal": 30,
    "ventana_dias": 60,
    "duracion_minima_segundos": 180,
    "candidatos_por_ejecucion": 10,
    "idiomas_subtitulos": ["es", "en"]
  },
  "red": { "timeout_segundos": 30, "intentos": 3, "pausa_segundos": 0.5 }
}
```

`linea_editorial` es la referencia con la que el modelo decide qué es relevante y qué podemos aportar. `recursos` acota la aportación: qué herramientas, hardware y formatos tiene la persona; una aportación que no puede ejecutarse con esos recursos no es una oportunidad.

## 6. Datos: las fichas

Las fichas son el contrato entre pasos. Sus esquemas se guardan en `references/` de la skill que las crea, y los scripts validan cada ficha antes de guardarla.

**Ficha de artículo propio** (`substack/fichas/<post_id>.json`):

```json
{
  "id": "…", "url": "…", "fecha": "…", "titulo": "…", "huella": "sha256…",
  "tema": "Agentes para automatizar la investigación",
  "subtemas": ["…"],
  "enfoque": "tutorial con prueba propia | opinión | caso | recopilación | explicación | entrevista",
  "tesis": "Una frase con la idea central",
  "entidades": ["Claude Code", "n8n"],
  "nivel": "inicial | intermedio | avanzado",
  "metricas_publicas": { "reacciones": 0, "comentarios": 0, "restacks": 0 }
}
```

**Ficha externa** (`youtube/videos/<id>/ficha.json`), con el mismo esquema para cualquier fuente:

```json
{
  "id": "…", "fuente": "youtube", "url": "…", "autor": "…", "fecha": "…", "huella": "…",
  "tema": "…",
  "tesis": "…",
  "afirmaciones": [
    { "texto": "…", "marca": "12:34", "tipo": "dato | demostración | opinión" }
  ],
  "entidades": ["…"],
  "demuestra": "Lo que el vídeo enseña funcionando",
  "promete_sin_demostrar": "Lo que afirma sin enseñarlo",
  "preguntas_abiertas": ["…"],
  "avisos_transcripcion": ["Punto confuso del audio, si lo hay (opcional)"],
  "senales": { "multiplo_mediana": 3.1, "interaccion": 0.042, "dias": 21 }
}
```

## 7. Skills

| # | Skill | Script (sin IA) | Modelo | Lee | Escribe |
|---|---|---|---|---|---|
| 1 | `recuperar-newsletters` | Recorre el archivo público de Substack, descarga, compara huellas y versiona | — | config | `substack/articulos`, `control`, `INDICE.md` |
| 2 | `analizar-biblioteca` | Detecta artículos sin ficha o cambiados; agrega las fichas en el mapa | Rellena la ficha de cada artículo; extrae el estilo | artículos | `substack/fichas`, `mapa-temas.md`, `estilo.md` |
| 3 | `explorar-youtube` | Lista los canales con `yt-dlp`, calcula señales, descarga y limpia subtítulos | Clasifica relevancia por título; rellena la ficha de cada candidato | `canales.md`, config | `youtube/videos`, `youtube/control` |
| 4 | `detectar-oportunidades` | Busca artículos y descartes parecidos a cada ficha; agrupa temas repetidos | Decide la cobertura, la aportación y redacta la propuesta | fichas externas y propias, `decisiones.md` | `oportunidades/` |
| 5 | `investigar-tema` | Guarda fuentes y comprueba enlaces | Busca fuentes primarias y verifica afirmaciones | oportunidad aceptada | `contenidos/<id>/investigacion.md` |
| 6 | `redactar-contenido` | — | Escribe con la voz de `estilo.md` | investigación, `estilo.md` | `contenidos/<id>/principal.md` |
| 7 | `adaptar-contenido` | Comprueba longitudes por canal | Adapta usando las plantillas de cada canal | principal, config | `contenidos/<id>/piezas/` |
| 8 | `registrar-resultado` | Enlaza lo publicado, guarda métricas y genera `decisiones.md` | Resume las correcciones como reglas de estilo | estados, diferencias entre borrador y publicado | `decisiones.md`, `estilo.md` |

**Agentes.** Se usan solo cuando aislar el contexto compensa:
- Analizar varios vídeos en paralelo, con un subagente por vídeo que devuelve solo su ficha.
- Revisar la investigación con un verificador crítico que intenta refutar cada afirmación.

El resto lo hace la sesión principal invocando skills.

## 8. Cómo se calculan las cosas

### 8.1 Revisar lo publicado

- **Recuperación:** `GET <substack>/api/v1/archive?sort=new&offset=N&limit=12` hasta agotar el archivo; después `GET /api/v1/posts/<slug>` para obtener el contenido completo. La huella es el SHA-256 del texto limpio.
- **Análisis:** solo se analizan los artículos sin ficha o cuya huella ha cambiado.
- **Mapa de temas:** un script agrupa las fichas por tema. Por cada tema muestra el número de artículos, la primera y la última fecha, los enfoques usados y las entidades. Así se ve qué hemos tratado, cuándo y desde qué perspectiva, y qué temas llevan tiempo sin tocarse.

### 8.2 Explorar YouTube

1. **Recogida** con `yt-dlp`, sin clave de API ni cuota:
   - `yt-dlp --flat-playlist -J --extractor-args "youtubetab:approximate_date" <url-del-canal>/videos` devuelve en una sola llamada los vídeos recientes del canal con id, título, visualizaciones, duración y fecha aproximada. Se toman los N configurados.
   - Los metadatos completos (fecha exacta, likes, comentarios, descripción) se obtienen con `yt-dlp -J <url-del-vídeo>` solo para los candidatos, que son pocos.
2. **Señales** por vídeo, calculadas sobre su propio canal:
   - **Múltiplo de la mediana** = visualizaciones / mediana del canal (solo vídeos de formato largo). Corrige el tamaño del canal: 50.000 visitas son mucho en un canal pequeño y poco en uno grande.
   - **Interacción** = (likes + comentarios) / visualizaciones. Se calcula al obtener los metadatos completos de los candidatos; hasta entonces es `null`.
   - Los vídeos de menos de 7 días se marcan como *señal incompleta* y no entran en la mediana.
   - **Interés:** alto si el múltiplo es ≥ 2; medio si está entre 1 y 2; bajo si es < 1.
3. **Relevancia:** el modelo clasifica en un solo lote los títulos (y la descripción cuando está disponible) de la ejecución frente a `linea_editorial`. Devuelve `relevante: sí/no` y un `tema` corto. Es barato porque no lee transcripciones.
4. **Candidatos:** vídeos relevantes, de formato largo, dentro de la ventana y con interés medio o alto, o con un tema que aparece en 2 o más canales. Se ordenan por interés y se toman los K configurados.
5. **Contenido:** `yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs es,en` descarga los subtítulos. Un script elimina las líneas que los subtítulos automáticos repiten y conserva las marcas de tiempo en `transcripcion.md`. Si no hay subtítulos, se indica en la ficha; nunca se inventa el contenido.
6. **Ficha del vídeo:** el modelo lee la transcripción y rellena la ficha externa. Distingue lo que **demuestra** de lo que **promete sin demostrar**. Si el vídeo ya tiene ficha, no se vuelve a leer: una actualización de visualizaciones no cambia el contenido.

### 8.3 Detectar oportunidades

1. **Cruce con lo publicado (script):** compara cada ficha externa con todas las fichas propias mediante BM25 sobre tema, tesis y entidades. Es Python puro y no necesita embeddings ni servicios. Selecciona los 5 artículos más parecidos y los descartes anteriores parecidos.
2. **Agrupación (script):** reúne las fichas externas con el mismo tema y entidades. Un tema que aparece en varios canales es tendencia, no un caso aislado.
3. **Juicio (modelo):** lee la ficha externa y el **texto completo** de los artículos parecidos, no solo sus fichas, y decide:
   - **Cobertura:** `nuevo`, `ampliación` (lo tratamos, pero hay un ángulo distinto) o `cubierto`.
   - **Aportación:** qué podemos añadir nosotros: una prueba propia, el caso en español, una crítica a lo que promete sin demostrar, el proceso paso a paso o la conexión con un artículo anterior.
   - **Descartes:** si se parece a algo descartado, solo se propone con una razón nueva y explícita.

### 8.4 Qué es una oportunidad

Un tema es oportunidad solo si cumple **las cuatro condiciones**:

| Condición | Cómo se comprueba |
|---|---|
| **Interés real** | Interés medio o alto, o presencia en 2 o más canales. Lo calcula un script. |
| **Encaja con la línea editorial** | Clasificación de relevancia frente a la configuración. |
| **No está cubierto** | Cobertura `nuevo` o `ampliación` tras leer los artículos parecidos. |
| **Podemos aportar algo** | Una aportación concreta, comprobable y **ejecutable con los `recursos` de la configuración** (herramientas, hardware, formatos). Sin aportación es copiar; con una aportación que la persona no puede ejecutar, es un deseo. |

**Orden de prioridad:** interés, después número de canales y después cobertura (`nuevo` antes que `ampliación`). No se calcula una puntuación única: cada criterio queda visible y la persona decide.

**Archivo** `oportunidades/<fecha>-<slug>.md`:

```markdown
---
id: 2026-10-20-agentes-investigacion
estado: propuesta            # propuesta | aceptada | descartada | publicada
motivo_estado: ""
interes: alto
canales: 3
cobertura: ampliación
evidencias: [yt:abc123@12:34, yt:def456@03:10]
relacionados: [substack:987654]
---
## La oportunidad
## Por qué ahora (evidencias)
## Qué hemos publicado y qué falta
## Qué aportaríamos
## Qué hay que investigar o probar
## Riesgos
```

El **estado** en el encabezado es la fuente de verdad. La persona lo cambia y `registrar-resultado` lo recopila en `decisiones.md`.

### 8.5 Investigar, redactar y adaptar

- **Investigación:**
  - Fuentes primarias: documentación oficial, repositorios, artículos técnicos y datos.
  - Cada afirmación de la oportunidad queda como `verificada`, `refutada` o `sin confirmar`, con su fuente.
  - Plan de la prueba práctica cuando haga falta.
- **Redacción:** usa la investigación aprobada y `estilo.md`. No puede introducir afirmaciones que no estén en la investigación.
- **Adaptación:** cada canal tiene una plantilla en `references/` con longitud, estructura y tono. Un script comprueba que se respetan los límites.

### 8.6 Aprender

- Al publicar, `recuperar-newsletters` incorpora el artículo y `analizar-biblioteca` crea su ficha. La oportunidad pasa a `publicada` y queda enlazada al artículo.
- **Métricas:** reacciones, comentarios y restacks públicos de Substack, con fecha de captura. Son una señal débil; si la persona exporta sus estadísticas privadas, se añaden como CSV.
- **Correcciones:** se compara el borrador aprobado con lo publicado. Los cambios se resumen como reglas en `estilo.md`, por ejemplo "no abrir con una pregunta retórica".
- **Descartes:** sus motivos se consultan en el siguiente cruce de oportunidades.

## 9. Uso cada semana

1. `recuperar-newsletters` y `analizar-biblioteca`: actualizar lo publicado.
2. `explorar-youtube` y `detectar-oportunidades`: generar propuestas.
3. La persona marca una oportunidad como aceptada y las demás como descartadas, con motivo.
4. `investigar-tema`, revisión, `redactar-contenido`, revisión y `adaptar-contenido`.
5. Tras publicar, `registrar-resultado`.

## 10. Reglas para cada prompt

Cada prompt de `prompts/`:

- Pide **crear** su skill con la estructura de la sección 4 y respeta los contratos de las secciones 6 y 8. No referencia repositorios de terceros como solución.
- Especifica entradas, salidas, el esquema de sus fichas y qué parte es script y qué parte es modelo.
- Incluye pruebas con **datos simulados**: repetir sin duplicar, conservar datos ante errores y validar los esquemas.
- No ejecuta descargas reales y separa lo comprobado de lo pendiente.
- Actualiza el README con lo que deja construido.
````
