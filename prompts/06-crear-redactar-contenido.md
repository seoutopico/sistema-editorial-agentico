Crea la skill `redactar-contenido`. Escribe el contenido principal, la newsletter, a partir de una investigación aprobada y con la voz de la publicación. Solo puede afirmar lo que está en la investigación.

Es la segunda parte de la fase 3 de `ARQUITECTURA.md`. Léelo antes de empezar y respeta sus secciones 2, 4, 7, 8.5, 8.6 y 10. Lee también los `SKILL.md` de `analizar-biblioteca` (para `estilo.md` y las métricas de estilo) y de `investigar-tema` (para el formato de la investigación y las fuentes). Si alguna no existe, detente e indica qué prompt falta.

En este paso creas y validas la skill con una investigación ficticia. **No redactes ningún contenido real.**

## 1. Reparto entre script y modelo

| Lo hace el script (Python sin IA) | Lo hace el modelo |
|---|---|
| Comprobar que la investigación está aprobada | Escribir el texto con la voz de `estilo.md` |
| Preparar el material | Proponer títulos |
| Guardar el borrador original intacto | |
| Comprobar citas, enlaces y longitud | |

## 2. Estructura

```text
.agents/skills/redactar-contenido/
├── SKILL.md
├── references/
│   └── instrucciones-redaccion.md
└── scripts/
    ├── redactar_contenido.py
    └── test_redactar_contenido.py
```

Salidas, en `biblioteca/contenidos/<id>/`:

```text
principal.md            # Texto que la persona revisa y edita
principal.borrador.md   # Copia del borrador del modelo; no se edita nunca
```

`principal.borrador.md` existe para el aprendizaje. `registrar-resultado` compara lo que escribió el modelo con lo que finalmente se publicó y convierte las diferencias en reglas de estilo.

**`SKILL.md`:**
- Empieza con un frontmatter con `name` y `description`. Úsala cuando una investigación pase a `estado: aprobada`.
- Describe el flujo de la sección 4.
- Es breve.

## 3. Comandos del script

```text
python .agents/skills/redactar-contenido/scripts/redactar_contenido.py <comando> <id>
```

### `preparar <id>`

1. Comprueba que `biblioteca/contenidos/<id>/investigacion.md` tiene `estado: aprobada`. Si no, termina con código 2.
2. Devuelve en JSON:
   - Las rutas de la oportunidad, la investigación, `fuentes.json` y `biblioteca/estilo.md`.
   - Las métricas de estilo, calculadas con la skill `analizar-biblioteca`.
   - Los artículos propios relacionados en la oportunidad, con título y URL, para posibles enlaces internos.
3. Si `estilo.md` no existe, lo advierte y recomienda generarlo antes de redactar.

### `guardar <id> <archivo.md>`

1. **Encabezado, escrito por el script:** `oportunidad`, `estado: borrador`, `fecha` y `titulos_alternativos`, que se toman del archivo del modelo.
2. **Comprobaciones:**
   - Cada cita `[f<n>]` existe en `fuentes.json`.
   - No se cita una fuente que solo respalde afirmaciones `refutadas`.
   - Los enlaces a artículos propios apuntan a URLs del inventario.
   - La longitud en palabras está entre el 60 % y el 140 % de la mediana de los artículos propios. Si no, es un aviso, no un error.
3. Escribe `principal.md` y una copia idéntica en `principal.borrador.md`.

**Si `principal.md` ya existe con `estado: aprobado`, no lo toca.** Si existe como borrador, lo sustituye solo con `--reemplazar`; en ese caso `principal.borrador.md` pasa a ser el nuevo borrador.

### `comprobar <id>`

Repite las comprobaciones sobre el `principal.md` actual, que puede estar editado por la persona, y las informa sin modificar nada. Sirve después de editar a mano.

### Códigos de salida

- `0`: correcto.
- `1`: avisos.
- `2`: no pudo ejecutarse o la validación falló.

Las escrituras son atómicas.

## 4. Flujo que describe SKILL.md

1. `preparar`.
2. **Redactar.** El modelo lee la oportunidad, la investigación completa y `estilo.md`, incluida la sección `## Reglas aprendidas`, y escribe el texto siguiendo `instrucciones-redaccion.md`.
3. `guardar`.
4. **Informar:** avisos de las comprobaciones, y que el texto queda **en borrador**. La persona lo edita en `principal.md` y lo marca como `aprobado` en el encabezado.

## 5. Criterios del modelo

**`instrucciones-redaccion.md`:**
- **Lo que puede afirmar:** solo lo que está en la investigación.
  - Lo `verificado` se cita con `[f<n>]`.
  - Lo `sin_confirmar` solo aparece presentado como tal.
  - Lo `refutado` solo aparece para desmentirlo.
- **Estilo:** se siguen `estilo.md` y sus reglas aprendidas, que tienen prioridad sobre las preferencias generales del modelo.
- **Aportación:** el texto desarrolla la aportación y el ángulo propuesto en la investigación. Si incluye una prueba práctica, la explica tal como se hizo, con lo que funcionó y lo que no. Nunca se inventa un resultado que no esté documentado.
- **Enlaces internos:** se enlaza a los artículos propios relacionados cuando aportan contexto.
- **Títulos:** se entrega el título elegido y dos alternativos en un bloque inicial que el script lee.
- **Fuentes:** el texto termina con una sección de fuentes con el formato de la investigación.

## 6. Pruebas

Escríbelas con `unittest`, con un contenido ficticio en una carpeta temporal: oportunidad, investigación, fuentes, `estilo.md` e inventario.

Deben comprobar que:
1. `preparar` rechaza una investigación no aprobada.
2. `guardar` rechaza una cita `[f9]` inexistente y un enlace interno que no está en el inventario.
3. `guardar` avisa de una longitud fuera de rango sin rechazar el texto.
4. `guardar` crea `principal.md` y `principal.borrador.md` idénticos.
5. `guardar` no toca un `principal.md` aprobado, y sin `--reemplazar` no sustituye un borrador.
6. `comprobar` detecta un error introducido al editar a mano y no modifica nada.

Ejecuta las pruebas y muestra el resultado.

Para comprobar las instrucciones, con la investigación ficticia, redacta tú mismo un texto breve siguiendo `instrucciones-redaccion.md` y guárdalo con el comando.

## 7. Documentación

- Actualiza en `README.md` la fila del prompt 06 a `hecho`.
- No modifiques `ARQUITECTURA.md`. Si algo obliga a cambiar el diseño, indícalo al final como propuesta.

## 8. Entrega

Muestra:
- El árbol de la skill.
- `SKILL.md` y las instrucciones.
- El resultado de las pruebas.
- El texto de ejemplo.

Separa lo comprobado de lo que solo se verá con un contenido real.
