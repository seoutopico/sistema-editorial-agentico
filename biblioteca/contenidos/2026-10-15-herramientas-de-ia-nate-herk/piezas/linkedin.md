---
canal: linkedin
contenido: 2026-10-15-herramientas-de-ia-nate-herk
estado: borrador
fecha: 2026-10-15
---
Pagar más razonamiento a la IA no me compró mejor texto. Y esta vez no es una impresión: lo medí.

Se repite mucho que subir el nivel de esfuerzo de la IA mejora el resultado. Yo misma lo había hecho alguna vez por intuición, sin medir nada. Esta semana dejé de opinar y monté el experimento en mi terreno: una tarea editorial real de mi sistema.

El método, antes que los resultados:

— Escribí los criterios de calidad antes de ejecutar nada, para no puntuar a favor de mi hipótesis.

— Lancé el mismo prompt literal en cuatro niveles de esfuerzo (low, medium, high y max), dos veces por nivel.

— Puntué las ocho salidas a ciegas, sin saber de qué nivel salía cada una.

Resultado: de medium hacia arriba, con mi rúbrica no detecté diferencias de calidad. Seis de las ocho ejecuciones empataron. Los tokens apenas se movieron (un +11-13 % entre extremos). Lo único que se disparó fue la espera: max tardó entre 4,2 y 5,6 veces más que low.

Y el detalle que casi nadie mira: medium no es solo la recomendación de Anthropic, es el valor por defecto del modelo. Te colocan abajo de serie. Eso es una decisión de producto, no una nota al pie.

Mi regla práctica, con todos los límites de un experimento pequeño: medium por defecto, high como tope en piezas cortas, y xhigh o max solo cuando hayas medido una mejora. Antes de pagar más esfuerzo, escribe tus criterios, ejecuta al menos dos veces por nivel y puntúa a ciegas. Es menos épico que una demo espectacular, pero es lo que convierte una impresión en un dato.

En la newsletter cuento el experimento completo, con la tabla de resultados y lo que dice la documentación oficial de Anthropic: {{enlace}}
