# Instrucciones para adaptar el contenido a los canales

Objetivo: convertir el principal aprobado en una pieza por canal. El
principal es el límite de lo que se puede afirmar; la plantilla del canal,
la forma de contarlo.

## Reglas

- **Cada pieza funciona por sí sola** para quien no ha leído la newsletter:
  no presupone contexto ni dice «como contaba en el artículo».
- **Solo afirmaciones del principal.** Nada de datos, cifras o conclusiones
  nuevas, aunque el modelo los «sepa». Si el principal matiza algo, la pieza
  no lo convierte en rotundo.
- **Voz:** se sigue `biblioteca/estilo.md` —incluida `## Reglas aprendidas`—
  y, además, el tono que pide la plantilla del canal.
- **Un ángulo por canal.** Cada canal elige el ángulo del principal que
  mejor le encaja; no se recorta el mismo texto para todos. Si LinkedIn
  desarrolla la prueba práctica, Notes puede quedarse con el dato más
  sorprendente.

## Enlaces

- La URL publicada normalmente no existe todavía: se escribe `{{enlace}}` y,
  tras publicar, `enlazar <id> <url>` lo sustituye en todas las piezas.
- No se enlazan artículos propios que no estén en el principal.

## Formato de entrega

- El archivo que recibe `guardar` es **solo el cuerpo de la pieza**, sin
  encabezado `---`: el encabezado (`canal`, `contenido`, `estado: borrador`,
  `fecha`) lo escribe el script.
- Si la plantilla declara `campos` (como `substack`), el cuerpo se organiza
  en una sección `## <campo>` por campo, en el orden de la plantilla.
- Los límites del encabezado de la plantilla (caracteres, enlace, hashtags)
  son obligatorios: el script no guarda una pieza que los incumpla.

## Después de guardar

Las piezas quedan **en borrador**. La persona las revisa, las edita si hace
falta y las marca como `aprobado` en el encabezado. Una pieza aprobada no se
regenera.
