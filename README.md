# Sistema editorial Think&Hack

Encuentra oportunidades de contenido, las investiga y las convierte en piezas para cada canal. El proceso tiene cinco fases: revisar lo publicado, encontrar oportunidades, investigar y desarrollar, adaptar y aprender.

## Cómo montarlo

Ejecuta los prompts de `prompts/` en orden, del 00 al 08, uno por sesión, en un agente de programación con acceso a archivos y terminal. Revisa el resultado de cada uno antes de pasar al siguiente. Cada prompt posterior actualizará su fila en la tabla de estado.

## Qué cambiar para tu publicación

- `proyecto.config.json`: publicación, línea editorial, canales de salida y parámetros de YouTube y de red.
- `biblioteca/youtube/canales.md`: canales de YouTube que quieres seguir.
- `.env`: copia `.env.example` y añade tu `YOUTUBE_API_KEY` cuando vayas a consultar YouTube.

## Estado

| Prompt | Skill que crea | Estado |
|---|---|---|
| `00-crear-estructura.md` | Ninguna; estructura y configuración | hecho |
| `01-crear-recuperar-newsletters.md` | `recuperar-newsletters` | pendiente |
| `02-crear-analizar-biblioteca.md` | `analizar-biblioteca` | pendiente |
| `03-crear-explorar-youtube.md` | `explorar-youtube` | pendiente |
| `04-crear-detectar-oportunidades.md` | `detectar-oportunidades` | pendiente |
| `05-crear-investigar-tema.md` | `investigar-tema` | pendiente |
| `06-crear-redactar-contenido.md` | `redactar-contenido` | pendiente |
| `07-crear-adaptar-contenido.md` | `adaptar-contenido` | pendiente |
| `08-crear-registrar-resultado.md` | `registrar-resultado` | pendiente |

La skill anterior `recuperar-newsletters` sigue pendiente de adaptación a esta arquitectura.

Más detalle en [ARQUITECTURA.md](ARQUITECTURA.md).
