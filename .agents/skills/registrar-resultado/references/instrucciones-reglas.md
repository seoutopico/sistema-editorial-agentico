# Cómo convertir las diferencias en reglas de estilo

El comando `diferencias <oportunidad_id>` devuelve los párrafos que la
persona eliminó, añadió o modificó al editar el borrador del modelo. Estas
instrucciones dicen cómo convertir esos cambios en reglas para
`## Reglas aprendidas` de `biblioteca/estilo.md`.

## Qué es una regla

Una regla es algo que **se aplicaría a cualquier texto futuro**. Por ejemplo:

- «No abrir con una pregunta retórica.»
- «Explicar el porqué antes del cómo.»
- «Cerrar con lo que se probó, no con una promesa.»

**No es una regla** una corrección puntual de este texto:

- Un dato actualizado o corregido.
- Una errata o un cambio de nombre propio.
- Un párrafo eliminado porque ese tema sobraba aquí.

Si un cambio no generaliza, no produce regla. Ninguna regla es mejor que una
regla inventada.

## Cada regla

- Se apoya en **uno o varios cambios reales** del diff, con su ejemplo antes
  y después tomados del texto (recortados si son largos, sin alterarlos).
- Se formula en positivo o negativo, en una frase, sin condiciones vagas.
- Lleva el formato que espera `guardar-reglas`:

```json
[{
  "regla": "No abrir con una pregunta retórica.",
  "ejemplo_antes": "¿Te imaginas no volver a buscar fuentes a mano?",
  "ejemplo_despues": "Los agentes pueden encargarse de la investigación previa.",
  "origen": "<oportunidad_id>"
}]
```

## Cuántas

Como máximo **cinco por contenido**. Es mejor pocas y claras: si hay más de
cinco candidatas, quedarse con las que se apoyan en más de un cambio o en el
cambio más claro.

## Contradicciones

Antes de proponer, leer las reglas ya existentes en `## Reglas aprendidas`.
Si una regla nueva **contradice una existente**, no se añaden las dos: se
señala la contradicción a la persona (regla existente, regla candidata y los
ejemplos de cada una) y decide ella. Solo se guarda lo que la persona
confirme.

## Flujo

1. Ejecutar `diferencias <oportunidad_id>` y leer también
   `## Reglas aprendidas` de `biblioteca/estilo.md`.
2. Redactar las reglas candidatas con estos criterios.
3. Enseñarlas a la persona: regla, ejemplos y de qué cambios salen.
4. Guardar las confirmadas en un JSON y ejecutar
   `guardar-reglas <archivo.json>`. El script descarta las repetidas y lo
   informa; las contradicciones las detecta el modelo en el paso 1, no el
   script.
