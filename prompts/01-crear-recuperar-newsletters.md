Crea la skill `recuperar-newsletters`. Descarga todo lo publicado en una newsletter de Substack y lo mantiene actualizado en `biblioteca/substack/`, para que los pasos siguientes puedan analizar qué hemos tratado.

Es la fase 1 del sistema descrito en `ARQUITECTURA.md`. Léelo antes de empezar y respeta su estructura, en especial las secciones 2, 4, 8.1 y 10. Si `ARQUITECTURA.md` o `proyecto.config.json` no existen, detente e indica que primero hay que ejecutar `prompts/00-crear-estructura.md`.

En este paso creas y validas la skill con datos simulados. **No descargues la newsletter real.**

## 1. Estructura

```text
.agents/skills/recuperar-newsletters/
├── SKILL.md
└── scripts/
    ├── recuperar_newsletters.py
    └── test_recuperar_newsletters.py
```

Añade `references/` solo si necesitas guardar un esquema o plantilla.

`SKILL.md` empieza con un frontmatter con `name` y `description`. La descripción indica cuándo usar la skill: actualizar o revisar el histórico publicado. El cuerpo explica qué lee, qué escribe, el comando de ejecución, cómo interpretar el informe y los códigos de salida. Debe ser breve: lo que hace el script no se repite en el texto.

## 2. Entrada

El script lee `proyecto.config.json` desde la raíz del proyecto:
- `publicacion.substack`: URL de la publicación.
- `red.timeout_segundos`, `red.intentos` y `red.pausa_segundos`.

Todas las rutas son relativas a la raíz del proyecto. No hay valores de la publicación escritos en el código.

Opciones de línea de comandos:
- `--config <ruta>`: por defecto, `proyecto.config.json`.
- `--limite <n>`: procesa solo los n artículos más recientes, para hacer una primera prueba real corta.

## 3. Qué hace el script

Es Python sin IA. Usa la biblioteca estándar; si una dependencia es imprescindible, justifícala y añádela a `requirements.txt`.

**Recorrer el archivo completo.**
- Pide `GET <substack>/api/v1/archive?sort=new&offset=<n>&limit=12` avanzando `offset` hasta recibir una página vacía. El RSS no sirve, porque solo contiene lo reciente.
- Pon un tope de seguridad de páginas. Si se alcanza, o si una página falla tras los reintentos, la paginación queda como **incompleta** y se registra el motivo.

**Obtener cada artículo.**
- Pide `GET <substack>/api/v1/posts/<slug>`.
- Datos que se guardan: `id`, `slug`, `title`, `subtitle`, `post_date`, `canonical_url`, `audience`, `type` y las métricas públicas (reacciones, comentarios y restacks), con la fecha de captura.

**Clasificar el contenido.**
- `completo`: hay cuerpo íntegro.
- `extracto`: el artículo es de pago o el cuerpo está truncado.
- `error`: no se pudo obtener.

**Convertir a Markdown legible.** Usa `html.parser`. Conserva títulos, párrafos, listas, enlaces, citas, código e imágenes como enlaces.

**Huella.** Calcula el SHA-256 del Markdown normalizado del cuerpo.

**Guardar o actualizar.** El artículo se identifica siempre por su `id`, aunque cambie el slug.

| Situación | Qué se hace |
|---|---|
| Artículo nuevo | Se guarda. |
| Misma huella | No se reescribe el archivo; solo se actualizan las métricas y la fecha de comprobación. |
| Huella distinta y contenido completo | Se mueve la versión anterior a `historial/` y se guarda la nueva. |
| Extracto o error, y ya existe una copia completa | No se toca la copia; se registra la incidencia. |

**Escribir de forma segura.** Escribe en un archivo temporal y renómbralo. Una interrupción nunca deja un archivo a medias.

**Red.** Usa el timeout configurado y reintenta un número limitado de veces, con espera creciente, ante 429 y 5xx. Pausa entre peticiones. Un 404 en un artículo es un error de ese artículo, no de la ejecución.

## 4. Salidas

```text
biblioteca/substack/
├── articulos/<YYYY-MM-DD>-<slug>.md
├── INDICE.md
└── control/
    ├── inventario.json
    ├── originales/<id>.json
    ├── historial/<id>/<marca_temporal>.md
    └── ejecuciones/<run_id>.json
```

- **Artículo:** frontmatter YAML con `id`, `titulo`, `subtitulo`, `fecha`, `url`, `tipo`, `audiencia`, `estado` (`completo` o `extracto`) y `huella`; después, el cuerpo en Markdown.
- **`inventario.json`:** un registro por `id` con slug, título, fecha, url, archivo, estado, huella, métricas con fecha de captura, primera descarga, última comprobación y última modificación. Es lo que usará `analizar-biblioteca` para saber qué artículos necesitan una ficha nueva.
- **`originales/<id>.json`:** la última respuesta de la API de cada artículo, para comprobar su procedencia.
- **`INDICE.md`:** tabla generada con fecha, título, estado y enlace al archivo local, ordenada de más reciente a más antiguo.
- **`ejecuciones/<run_id>.json`:**
  - `run_id` en UTC con formato `YYYYMMDDTHHMMSSZ`.
  - Inicio y fin.
  - Páginas leídas y si la paginación terminó.
  - Contadores: nuevos, actualizados, sin cambios, extractos y errores.
  - La lista de cambios y errores con su motivo.

Al terminar, el script imprime un resumen de la ejecución. **Un fallo de consulta nunca se presenta como "sin novedades".**

Códigos de salida:
- `0`: todo correcto.
- `1`: terminó, pero con errores parciales o paginación incompleta.
- `2`: no pudo ejecutarse; por ejemplo, la configuración no es válida o el archivo de Substack es inaccesible.

## 5. Pruebas

Escríbelas con `unittest`. Inyecta la función de red en el script para usar respuestas simuladas y una carpeta temporal; nunca accedas a internet.

Deben comprobar que:
1. Una primera ejecución guarda los artículos, el inventario, el índice y el informe.
2. Repetir con los mismos datos no duplica artículos ni reescribe archivos sin cambios.
3. Un artículo modificado conserva su versión anterior en `historial/`.
4. Un extracto o un error no sustituye una copia completa existente.
5. La paginación sigue hasta la página vacía, y una página fallida deja la ejecución como incompleta con su motivo y código de salida 1.
6. Un cambio de slug con el mismo `id` no crea un artículo duplicado.
7. Las métricas se actualizan sin contar como cambio de contenido.
8. La conversión a Markdown conserva títulos, listas y enlaces.

Ejecuta las pruebas y muestra el resultado.

## 6. Documentación

- Actualiza en `README.md` la fila del prompt 01 a `hecho`, con el comando de ejecución.
- No modifiques `ARQUITECTURA.md`. Si encuentras algo que obliga a cambiar el diseño, indícalo al final como propuesta.

## 7. Entrega

Muestra:
- El árbol de la skill.
- El contenido de `SKILL.md`.
- El resultado de las pruebas.
- El comando para la primera descarga real corta (`--limite 5`) y el de la descarga completa.

Separa lo comprobado con datos simulados de lo que solo se sabrá con la ejecución real; por ejemplo, el formato exacto de las respuestas de Substack.
