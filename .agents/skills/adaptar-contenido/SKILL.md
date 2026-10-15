---
name: adaptar-contenido
description: Convierte el contenido principal aprobado en las piezas de cada canal configurado (substack, linkedin, notes…) usando la plantilla de cada canal, y las deja en borrador en biblioteca/contenidos/<id>/piezas/. Úsala cuando principal.md pase a `estado: aprobado`.
---

# adaptar-contenido

Fase 4 del sistema editorial (ver `ARQUITECTURA.md`, secciones 2, 4, 5, 7,
8.5 y 10). El script hace lo repetible (comprobar que el principal está
aprobado, saber qué canales hay que preparar, comprobar los límites de cada
plantilla y guardar las piezas); el modelo solo el juicio (adaptar el
contenido a cada canal). Los criterios del modelo están en
`references/instrucciones-adaptacion.md` y cada canal tiene su plantilla en
`references/canales/<canal>.md`, con sus límites en el encabezado.

## Qué lee

- `biblioteca/contenidos/<id>/principal.md` — aprobado por la persona.
- `biblioteca/estilo.md` — la voz, incluida `## Reglas aprendidas`.
- `proyecto.config.json` — la lista `canales_salida`.
- `references/canales/<canal>.md` — plantilla y límites de cada canal.

## Qué escribe

- `biblioteca/contenidos/<id>/piezas/<canal>.md` — una pieza por canal, con
  encabezado `canal`, `contenido`, `estado: borrador` y `fecha` escrito por
  el script.

## Flujo

Todos los comandos se ejecutan desde la raíz del proyecto:

```bash
python .agents/skills/adaptar-contenido/scripts/adaptar_contenido.py <comando> <id>
```

1. **`preparar <id>`.** Comprueba que `principal.md` tiene
   `estado: aprobado` y devuelve en JSON la ruta del principal y, por cada
   canal de `canales_salida`, su plantilla, sus límites y si ya tiene pieza.
   Un canal configurado sin plantilla es un error que indica qué archivo falta.
2. **Adaptar.** Por cada canal sin pieza, el modelo lee el principal y la
   plantilla del canal y escribe la pieza siguiendo
   `references/instrucciones-adaptacion.md` (solo el cuerpo, sin encabezado;
   `{{enlace}}` donde irá la URL publicada). Después,
   **`guardar <id> <canal> <archivo.md>`**: el script escribe el encabezado,
   comprueba los límites de la plantilla y guarda la pieza. Una pieza
   aprobada no se sobrescribe nunca; un borrador, solo con `--reemplazar`.
3. **Informar:** piezas creadas y avisos. Las piezas quedan **en borrador**
   hasta que la persona las apruebe en el encabezado. Tras editar a mano,
   **`comprobar <id>`** revisa todas las piezas sin modificar nada.
4. Tras publicar la newsletter, **`enlazar <id> <url>`** sustituye
   `{{enlace}}` por la URL publicada en todas las piezas.

Códigos de salida: `0` correcto, `1` avisos, `2` no pudo ejecutarse o la
validación falló. Las escrituras son atómicas.

## Para añadir un canal

1. Crear `references/canales/<canal>.md` con su encabezado de límites
   (`max_caracteres`, `min_caracteres`, `enlace_obligatorio`, `max_hashtags`
   y, si la pieza tiene campos, `campos` con `max_caracteres_<campo>`).
2. Añadir el nombre del canal en `canales_salida` de `proyecto.config.json`.

Sin tocar código.

## Pruebas

```bash
python -m unittest discover .agents/skills/adaptar-contenido/scripts -v
```

Usan un principal ficticio aprobado, una configuración y plantillas en una
carpeta temporal; nunca tocan `biblioteca/` ni la red.
