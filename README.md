# Sistema editorial Think&Hack

Encuentra oportunidades de contenido, las investiga y las convierte en piezas para cada canal. El proceso tiene cinco fases: revisar lo publicado, encontrar oportunidades, investigar y desarrollar, adaptar y aprender.

## Cómo montarlo

Ejecuta los prompts de `prompts/` en orden, del 00 al 08, uno por sesión, en un agente de programación con acceso a archivos y terminal. Revisa el resultado de cada uno antes de pasar al siguiente. Cada prompt posterior actualizará su fila en la tabla de estado.

## Qué cambiar para tu publicación

- `proyecto.config.json`: publicación, línea editorial, canales de salida y parámetros de YouTube y de red.
- `biblioteca/youtube/canales.md`: canales de YouTube que quieres seguir.
- YouTube se consulta con `yt-dlp`, sin clave de API. No hace falta ningún `.env` para empezar.

## Estado

| Prompt | Skill que crea | Estado |
|---|---|---|
| `00-crear-estructura.md` | Ninguna; estructura y configuración | hecho |
| `01-crear-recuperar-newsletters.md` | `recuperar-newsletters` | hecho — `python .agents/skills/recuperar-newsletters/scripts/recuperar_newsletters.py` (primera prueba: añadir `--limite 5`) |
| `02-crear-analizar-biblioteca.md` | `analizar-biblioteca` | hecho — `python .agents/skills/analizar-biblioteca/scripts/analizar_biblioteca.py pendientes` y seguir el flujo de su SKILL.md |
| `03-crear-explorar-youtube.md` | `explorar-youtube` | hecho — `python .agents/skills/explorar-youtube/scripts/explorar_youtube.py recoger` y seguir el flujo de su SKILL.md. Solo necesita `yt-dlp` instalado (`pip install yt-dlp`), sin claves de API |
| `04-crear-detectar-oportunidades.md` | `detectar-oportunidades` | hecho — `python .agents/skills/detectar-oportunidades/scripts/detectar_oportunidades.py agrupar` y seguir el flujo de su SKILL.md. Lee las fichas externas de cualquier `biblioteca/<fuente>/`, sin depender de YouTube |
| `05-crear-investigar-tema.md` | `investigar-tema` | hecho — `python .agents/skills/investigar-tema/scripts/investigar_tema.py preparar <oportunidad_id>` con una oportunidad en `estado: aceptada` y seguir el flujo de su SKILL.md. La investigación queda en `biblioteca/contenidos/<id>/` pendiente de aprobación |
| `06-crear-redactar-contenido.md` | `redactar-contenido` | hecho — `python .agents/skills/redactar-contenido/scripts/redactar_contenido.py preparar <oportunidad_id>` con una investigación en `estado: aprobada` y seguir el flujo de su SKILL.md. El texto queda en `biblioteca/contenidos/<id>/principal.md` en borrador, con copia intacta en `principal.borrador.md` |
| `07-crear-adaptar-contenido.md` | `adaptar-contenido` | hecho — `python .agents/skills/adaptar-contenido/scripts/adaptar_contenido.py preparar <id>` con un `principal.md` en `estado: aprobado` y seguir el flujo de su SKILL.md. Las piezas quedan en `biblioteca/contenidos/<id>/piezas/<canal>.md` en borrador; tras publicar, `enlazar <id> <url>` sustituye `{{enlace}}`. Añadir un canal es crear `references/canales/<canal>.md` y añadirlo a `canales_salida` |
| `08-crear-registrar-resultado.md` | `registrar-resultado` | hecho — `python .agents/skills/registrar-resultado/scripts/registrar_resultado.py decisiones` y seguir el flujo de su SKILL.md. Tras publicar: `buscar-publicado <id>`, confirmar, `enlazar <id> <post_id>`, `diferencias <id>` y `guardar-reglas <archivo.json>` con las reglas que redacta el modelo |

## Uso cada semana

El orden es el de la sección 9 de `ARQUITECTURA.md`. Todos los comandos se ejecutan desde la raíz del proyecto.

1. **Actualizar lo publicado.**
   ```bash
   python .agents/skills/recuperar-newsletters/scripts/recuperar_newsletters.py
   python .agents/skills/analizar-biblioteca/scripts/analizar_biblioteca.py pendientes
   # rellenar las fichas pendientes con el modelo y guardarlas una a una:
   python .agents/skills/analizar-biblioteca/scripts/analizar_biblioteca.py guardar <id> <archivo.json>
   python .agents/skills/analizar-biblioteca/scripts/analizar_biblioteca.py mapa
   ```
2. **Generar propuestas.**
   ```bash
   python .agents/skills/explorar-youtube/scripts/explorar_youtube.py recoger
   # seguir el flujo del SKILL.md de explorar-youtube (señales, relevancia, candidatos, fichas)
   python .agents/skills/detectar-oportunidades/scripts/detectar_oportunidades.py agrupar
   python .agents/skills/detectar-oportunidades/scripts/detectar_oportunidades.py pendientes
   # evaluar cada paquete con el modelo y guardar:
   python .agents/skills/detectar-oportunidades/scripts/detectar_oportunidades.py guardar-evaluacion <archivo.json>
   python .agents/skills/detectar-oportunidades/scripts/detectar_oportunidades.py indice
   ```
3. **Decidir.** La persona marca una oportunidad como `aceptada` y las demás como `descartada`, con `motivo_estado`, en `biblioteca/oportunidades/<id>.md`.
4. **Investigar, redactar y adaptar.**
   ```bash
   python .agents/skills/investigar-tema/scripts/investigar_tema.py preparar <id>
   # la persona aprueba la investigación
   python .agents/skills/redactar-contenido/scripts/redactar_contenido.py preparar <id>
   python .agents/skills/redactar-contenido/scripts/redactar_contenido.py guardar <id> <archivo.md>
   # la persona edita principal.md y lo marca como aprobado
   python .agents/skills/adaptar-contenido/scripts/adaptar_contenido.py preparar <id>
   python .agents/skills/adaptar-contenido/scripts/adaptar_contenido.py guardar <id> <canal> <archivo.md>
   ```
5. **Tras publicar, registrar el resultado.**
   ```bash
   python .agents/skills/recuperar-newsletters/scripts/recuperar_newsletters.py   # incorpora el artículo nuevo
   python .agents/skills/registrar-resultado/scripts/registrar_resultado.py buscar-publicado <id>
   # confirmar con la persona el post propuesto
   python .agents/skills/registrar-resultado/scripts/registrar_resultado.py enlazar <id> <post_id>
   python .agents/skills/registrar-resultado/scripts/registrar_resultado.py diferencias <id>
   # el modelo redacta las reglas (references/instrucciones-reglas.md), la persona las revisa
   python .agents/skills/registrar-resultado/scripts/registrar_resultado.py guardar-reglas <archivo.json>
   python .agents/skills/registrar-resultado/scripts/registrar_resultado.py decisiones
   python .agents/skills/registrar-resultado/scripts/registrar_resultado.py metricas
   ```

Sin publicar nada, el mantenimiento semanal se reduce a `decisiones` y `metricas`.

Más detalle en [ARQUITECTURA.md](ARQUITECTURA.md).
