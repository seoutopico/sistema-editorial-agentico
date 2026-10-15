# Instrucciones para redactar el contenido principal

Objetivo: escribir la newsletter a partir de la investigación aprobada, con la
voz de la publicación. La investigación es el límite de lo que se puede
afirmar; el estilo, la forma de decirlo.

## Formato de entrega

El archivo que recibe `guardar` empieza con un bloque que el script lee:

```markdown
---
titulo: El título elegido
titulos_alternativos: [Primer alternativo, Segundo alternativo]
---
El texto completo en Markdown…

## Fuentes

[f1] Título, autor o entidad, fecha, URL
```

- El script convierte `titulo` en el `# Título` inicial y guarda los dos
  alternativos en el encabezado de `principal.md`. No usar comas dentro de
  los títulos alternativos: el bloque es una lista separada por comas.
- El texto termina con una sección `## Fuentes` con el mismo formato que la
  investigación, solo con las fuentes citadas en el texto.

## Lo que puede afirmar

Solo lo que está en la investigación:

- Lo **verificado** se afirma y se cita con `[f<n>]`, con fuentes que existen
  en `fuentes.json`.
- Lo **sin confirmar** solo aparece presentado como tal («no hemos podido
  confirmarlo», «la fuente lo afirma sin datos»), nunca como un hecho.
- Lo **refutado** solo aparece para desmentirlo, citando la fuente que lo
  refuta. No se cita como apoyo una fuente que solo respalda afirmaciones
  refutadas.
- Nada de datos, cifras o conclusiones que no estén en la investigación,
  aunque el modelo los «sepa».

## Estilo

- Se siguen `estilo.md` y su sección `## Reglas aprendidas`. Las reglas
  aprendidas **tienen prioridad** sobre las preferencias generales del modelo
  y sobre el resto de la guía si chocan.
- La longitud de referencia es la mediana de los artículos propios (la da
  `preparar`); el script avisa fuera del rango 60 %–140 %.

## Aportación

- El texto desarrolla la aportación y el ángulo propuesto en la investigación
  (`## Ángulo propuesto`), no un resumen genérico del tema.
- Si incluye una prueba práctica, se explica **tal como se hizo**, con lo que
  funcionó y lo que no. Nunca se inventa un resultado que no esté documentado
  en la investigación.

## Enlaces internos

- Se enlaza a los artículos propios relacionados (los da `preparar`, con
  título y URL) cuando aportan contexto, con su URL exacta del inventario.
- No se enlaza a artículos propios que no estén en el inventario.

## Títulos

- Se entrega el título elegido y dos alternativos en el bloque inicial.
- Los tres responden al contenido real del texto, no a una promesa que el
  texto no cumple.
