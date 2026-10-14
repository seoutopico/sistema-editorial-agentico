# Handoff: sistema editorial Think&Hack

Fecha: 2026-10-14. Proyecto: `C:\Users\uatb8a\Repositorios\conia` (no es repositorio Git todavía).

## 1. Qué se está construyendo

Un proceso agéntico para crear contenido de Think&Hack (https://ainalluna.substack.com) a partir de **oportunidades reales**:

1. **Revisar lo publicado:** qué temas se han tratado y desde qué perspectiva.
2. **Encontrar oportunidades:** temas relevantes todavía no desarrollados.
3. **Investigar y desarrollar:** contrastar fuentes y escribir un contenido principal sólido.
4. **Adaptar:** preparar las piezas para cada canal.
5. **Aprender:** usar lo publicado, lo que funcionó, los descartes y las correcciones la próxima vez.

**Entregable:** una serie de prompts (`prompts/00…08`) que cualquiera puede ejecutar en orden, en una carpeta vacía, para montar el sistema. Cada prompt **crea** una skill. Además servirá para una presentación y se compartirá en Git.

## 2. Cómo quiere trabajar la usuaria

- **Los prompts piden construir, no copiar.** Nunca deben depender de sus repos de demo, como `seoutopico/newsletters-a-notes-work` o `seoutopico/claude_skills/youtube-channel-research`. Un prompt que dice "usa", "adapta" o "revisa como referencia" una skill existente está mal. Ese error se repitió varias veces en la sesión anterior y es lo que más la frustró.
- **Diseño antes que código.** Pensar el proceso entero como lo haría un ingeniero y no crear carpetas o archivos sobre la marcha.
- **Simplificar es pensar mejor, no quitar.** Estructura sencilla y escalable.
- **Ciclo de cada prompt:** redactar, revisarlo con ella, guardarlo y ejecutarlo. No adelantar pasos.
- **Directo y sin dar la razón por sistema.** Explicar qué se va a hacer y cómo, y hacerlo bien.
- **Scripts deterministas y plantillas fijas** para ahorrar tokens y obtener siempre la misma salida.
- Responder en español.

## 3. Decisiones tomadas

El plano completo está en **`ARQUITECTURA.md`**, que es la fuente de verdad. Lo esencial:

- **Tres piezas:**
  - `prompts/`: un prompt por skill.
  - `.agents/skills/<skill>/`: `SKILL.md`, `scripts/` y `references/`.
  - `biblioteca/`: memoria central, con una carpeta por fuente.
- **Ocho skills:**
  1. `recuperar-newsletters`
  2. `analizar-biblioteca`
  3. `explorar-youtube`
  4. `detectar-oportunidades`
  5. `investigar-tema`
  6. `redactar-contenido`
  7. `adaptar-contenido`
  8. `registrar-resultado`
- **Script para lo repetible, modelo para el juicio.** Los análisis se guardan como **fichas JSON con esquema fijo**, que son el contrato entre pasos, con caché por huella.
- **Escalar:** una fuente nueva es otra carpeta `biblioteca/<fuente>/` más una skill `explorar-<fuente>` que produce fichas externas con el mismo esquema.
- **YouTube:**
  - Datos y métricas con YouTube Data API v3.
  - Señal de interés: visualizaciones / mediana del propio canal; alto si es ≥ 2.
  - Relevancia: el modelo clasifica todos los títulos en un lote.
  - Contenido: subtítulos con `yt-dlp`.
  - Ficha por vídeo: distingue lo que demuestra de lo que promete sin demostrar.
- **Cruce con lo publicado:**
  - Un script hace BM25 en Python puro para encontrar los artículos y descartes parecidos.
  - El modelo lee el texto completo de esos artículos y decide si el tema es `nuevo`, una `ampliación` o está `cubierto`.
- **Oportunidad:** debe cumplir cuatro condiciones a la vez: interés real, encaje con la línea editorial, que no esté cubierta y una aportación concreta nuestra. No hay puntuación única: los criterios quedan visibles y decide la persona.
- **Puntos de control humanos:** elegir la oportunidad, aprobar la investigación y aprobar el texto.
- **Configuración:**
  - `proyecto.config.json`: publicación, línea editorial, canales de salida, parámetros de YouTube y de red.
  - `biblioteca/youtube/canales.md`: lista simple de URLs.
  - Claves en `.env`.
- **Git:** se excluye todo `biblioteca/` salvo `youtube/canales.md`.

## 4. Estado de los archivos

Repositorio: **https://github.com/seoutopico/sistema-editorial-agentico** (privado).

| Archivo | Estado |
|---|---|
| `ARQUITECTURA.md` | Plano completo y aprobado. Es la fuente de verdad. |
| `prompts/00-crear-estructura.md` | **Ejecutado y validado** por la usuaria en otra sesión. Crea la base e incluye `ARQUITECTURA.md` íntegro como anexo. |
| `prompts/01` … `08` | **Escritos.** Cada uno crea una skill como especificación autónoma, sin repos de demo. |
| `README.md`, `.gitignore`, `proyecto.config.json`, `.env.example`, `requirements.txt`, `biblioteca/youtube/canales.md` | Creados por el prompt 00. |
| `.agents/skills/recuperar-newsletters/` | **Sin verificar.** Un subagente estaba ejecutando el prompt 01 cuando se subió el repositorio; puede estar a medias o ser la versión antigua. **Hay que volver a ejecutar el prompt 01.** |
| `HANDOFF.md` | Este documento. |

**Importante:** si cambia `ARQUITECTURA.md`, hay que regenerar el anexo del prompt 00. El prompt se construye concatenando la cabecera, que va hasta la línea `## Anexo: contenido de ARQUITECTURA.md` y el bloque ````markdown que la sigue, con el contenido de `ARQUITECTURA.md`, y cerrando con ````.

## 5. Siguientes pasos

La usuaria pidió **"construye todo ya y al acabar sube todo a mi cuenta git seoutopico"**. El método acordado es este:

1. **Ejecutar los prompts 01 a 08 en orden, cada uno en un subagente nuevo y sin contexto previo,** dentro de la raíz del repositorio. Así se prueba que cada prompt basta por sí solo.
   - Mensaje para el subagente: "Ejecuta tal cual el prompt `prompts/0X-….md` en este proyecto. No busques repositorios externos ni descargues datos reales. Devuelve el árbol, el resultado real de las pruebas, las ambigüedades del prompt y las propuestas de diseño."
   - En el 01: la skill antigua `recuperar-newsletters` se sustituye entera; la usuaria lo ha autorizado.
2. **Revisar cada informe antes de lanzar el siguiente.** Si el prompt tenía huecos, se corrige el prompt, no solo el código, y se registra en este documento.
3. **Al final:** ejecutar todas las pruebas (`python -m unittest discover -s .agents/skills -p "test_*.py"`, o las de cada skill), actualizar el README, hacer commit y push.
4. **Después,** cuando la usuaria lo decida, primera ejecución real: `recuperar-newsletters --limite 5`.

## 6. Cómo continuar en otro PC

```text
gh auth login                      # Entrar con la cuenta seoutopico
gh repo clone seoutopico/sistema-editorial-agentico
cd sistema-editorial-agentico
pip install -r requirements.txt    # Cuando las skills añadan dependencias
claude
```

En Claude Code: "Lee HANDOFF.md y ARQUITECTURA.md y continúa desde el paso 5."

## 7. Fuera de alcance por ahora

- No ejecutar descargas reales de Substack ni de YouTube hasta que la skill correspondiente esté validada.
- No hace falta `YOUTUBE_API_KEY` hasta ejecutar `explorar-youtube` de verdad. Se pone en `.env`, que nunca se sube.
