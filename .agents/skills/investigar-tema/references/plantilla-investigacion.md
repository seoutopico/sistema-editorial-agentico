# Plantilla de la investigación

El modelo redacta solo el cuerpo: el encabezado YAML (`oportunidad`,
`estado: pendiente_aprobacion`, `fecha`) lo escribe el script al guardar.
El cuerpo debe tener estas ocho secciones, en este orden y ninguna vacía.
`guardar-investigacion` las comprueba antes de escribir nada.

Las referencias a fuentes se citan en el texto como `[f1]` y deben existir en
`fuentes.json`. En las celdas de la tabla no se usa el carácter `|`.

```markdown
## Pregunta de investigación

Qué queremos responder, derivado de la oportunidad. Una o dos frases.

## Resumen

Lo que sabemos ahora, en cinco líneas como máximo.

## Verificación de afirmaciones

Una fila por cada afirmación de `afirmaciones.json`, con su estado
(`verificada`, `refutada` o `sin_confirmar`) y las fuentes que lo apoyan.
Una afirmación `verificada` o `refutada` necesita al menos una fuente que no
sea de tipo `vídeo`: el vídeo de origen no basta para verificarse a sí mismo.

| ID | Afirmación | Estado | Fuentes | Nota |
|---|---|---|---|---|
| a1 | Texto resumido de la afirmación | verificada | f1, f2 | Qué dicen las fuentes |
| a2 | … | sin_confirmar | — | Por qué no se pudo confirmar |

## Hallazgos nuevos

Lo que las fuentes aportan y no estaba en la evidencia de origen, con sus
referencias `[f<n>]`.

## Contradicciones y límites

Dónde no coinciden las fuentes y qué no se puede afirmar.

## Prueba práctica

Si hace falta probar algo nosotros: qué, cómo y qué resultado lo confirmaría.
Si no hace falta, por qué.

## Ángulo propuesto

Cómo concretar la aportación de la oportunidad con lo investigado.

## Fuentes

Lista numerada con el formato `[f1] Título, autor o entidad, fecha, URL`.

[f1] Título, Autor o entidad, 2026-01-15, https://…
[f2] …
```
