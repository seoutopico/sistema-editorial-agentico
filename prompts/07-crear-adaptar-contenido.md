Crea la skill `adaptar-contenido`. Convierte el contenido principal aprobado en las piezas de cada canal de publicación configurado. Cada canal tiene su plantilla. Añadir un canal es añadir una plantilla y su nombre en la configuración, sin tocar código.

Es la fase 4 de `ARQUITECTURA.md`. Léelo antes de empezar y respeta sus secciones 2, 4, 5, 7, 8.5 y 10. Lee también el `SKILL.md` de `redactar-contenido` para conocer el formato de `principal.md`. Si no existe, detente e indica que falta el prompt 06.

En este paso creas y validas la skill con un contenido ficticio. **No adaptes ningún contenido real.**

## 1. Reparto entre script y modelo

| Lo hace el script (Python sin IA) | Lo hace el modelo |
|---|---|
| Comprobar que el principal está aprobado | Adaptar el contenido a cada canal |
| Saber qué canales hay que preparar | |
| Comprobar los límites de cada plantilla | |
| Guardar las piezas | |

## 2. Estructura

```text
.agents/skills/adaptar-contenido/
├── SKILL.md
├── references/
│   ├── instrucciones-adaptacion.md
│   └── canales/
│       ├── substack.md
│       ├── linkedin.md
│       └── notes.md
└── scripts/
    ├── adaptar_contenido.py
    └── test_adaptar_contenido.py
```

Salidas: `biblioteca/contenidos/<id>/piezas/<canal>.md`.

**`SKILL.md`:**
- Empieza con un frontmatter con `name` y `description`. Úsala cuando `principal.md` pase a `estado: aprobado`.
- Describe el flujo y cómo añadir un canal.
- Es breve.

## 3. Plantillas de canal

Cada archivo de `references/canales/<canal>.md` empieza con un encabezado de límites que el script lee:

```yaml
---
canal: linkedin
max_caracteres: 3000
min_caracteres: 600
enlace_obligatorio: true
max_hashtags: 3
---
```

Después del encabezado, en texto, vienen la estructura de la pieza, el tono, el formato y lo que hay que evitar.

Plantillas iniciales:
- **`substack.md`:** lo que acompaña a la newsletter, no el texto, que ya es el principal. Asunto del correo (≤ 60 caracteres), texto de vista previa (≤ 140) y subtítulo.
- **`linkedin.md`:** publicación propia, que no es un resumen de la newsletter. Arranca con la idea más útil para el lector, desarrolla un punto concreto y termina con el enlace.
- **`notes.md`:** nota corta de Substack Notes (≤ 600 caracteres) con una idea o un dato del contenido y el enlace.

## 4. Comandos del script

```text
python .agents/skills/adaptar-contenido/scripts/adaptar_contenido.py <comando> <id>
```

### `preparar <id>`

1. Comprueba que `principal.md` tiene `estado: aprobado`. Si no, termina con código 2.
2. Lee `canales_salida` de `proyecto.config.json`. Un canal sin plantilla es un error que indica qué archivo falta.
3. Devuelve en JSON:
   - La ruta del principal.
   - Por cada canal: su plantilla, sus límites y si ya tiene pieza.

### `guardar <id> <canal> <archivo.md>`

1. **Encabezado, escrito por el script:** `canal`, `contenido`, `estado: borrador` y `fecha`.
2. **Comprobaciones según los límites de la plantilla:**
   - Caracteres mínimos y máximos. En `substack`, los límites se aplican a cada campo.
   - Que haya enlace, si es obligatorio. Se usa `{{enlace}}` cuando la URL publicada todavía no existe.
   - Número de hashtags.
3. Si falla una comprobación, no escribe nada y lo explica.

**Nunca sobrescribe una pieza con `estado: aprobado`.** Una pieza en borrador solo se sustituye con `--reemplazar`.

### `comprobar <id>`

Revisa todas las piezas actuales, aunque estén editadas a mano, sin modificar nada.

### `enlazar <id> <url>`

Sustituye `{{enlace}}` por la URL publicada en todas las piezas del contenido.

### Códigos de salida

- `0`: correcto.
- `1`: avisos.
- `2`: no pudo ejecutarse o la validación falló.

Las escrituras son atómicas.

## 5. Flujo que describe SKILL.md

1. `preparar`.
2. Por cada canal sin pieza, el modelo lee el principal y la plantilla y escribe la pieza siguiendo `instrucciones-adaptacion.md`. Después, `guardar`.
3. **Informar:** piezas creadas y avisos. Las piezas quedan **en borrador** hasta que la persona las apruebe.
4. Tras publicar la newsletter, `enlazar` con su URL.

**Para añadir un canal:**
1. Crear `references/canales/<canal>.md` con su encabezado de límites.
2. Añadir el nombre del canal en `canales_salida`.

## 6. Criterios del modelo

**`instrucciones-adaptacion.md`:**
- Cada pieza funciona por sí sola para quien no ha leído la newsletter.
- Solo se usan afirmaciones que estén en el principal. No se añaden datos nuevos.
- Se sigue `biblioteca/estilo.md` y, además, el tono de la plantilla del canal.
- Cada canal elige el ángulo que mejor le encaja: no se recorta el mismo texto para todos.

## 7. Pruebas

Escríbelas con `unittest`, con un contenido ficticio aprobado y una configuración de prueba.

Deben comprobar que:
1. `preparar` rechaza un principal no aprobado y señala un canal configurado sin plantilla.
2. `guardar` aplica los límites leídos de la plantilla: longitud, enlace obligatorio y hashtags.
3. Un canal nuevo con su plantilla funciona sin cambiar el código. La prueba crea una plantilla `x.md` en la carpeta temporal.
4. `guardar` no sobrescribe una pieza aprobada, y sin `--reemplazar` no sustituye un borrador.
5. `enlazar` sustituye `{{enlace}}` en todas las piezas.
6. `comprobar` detecta una pieza editada a mano que supera el límite.

Ejecuta las pruebas y muestra el resultado.

Para comprobar las instrucciones, adapta tú mismo el principal ficticio a los tres canales y guarda las piezas con el comando.

## 8. Documentación

- Actualiza en `README.md` la fila del prompt 07 a `hecho`.
- No modifiques `ARQUITECTURA.md`. Si algo obliga a cambiar el diseño, indícalo al final como propuesta.

## 9. Entrega

Muestra:
- El árbol de la skill.
- `SKILL.md`, las plantillas y las instrucciones.
- El resultado de las pruebas.
- Las piezas de ejemplo.
