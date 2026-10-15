# Instrucciones para investigar

Objetivo: verificar cada afirmación de `afirmaciones.json` en fuentes fiables
y reunir lo necesario para redactar sin inventar. La investigación es la base
del artículo: todo lo que después afirme la redacción tiene que estar aquí,
con su fuente.

## Prioridad de fuentes

1. **Documentación oficial, repositorios, papers y datos originales.** Es la
   fuente primaria: lo que dice quien lo hizo o lo midió.
2. **Prensa especializada.**
3. **Blogs con autor identificable.** Un blog anónimo o generado no vale como
   fuente.

## Cómo verificar

- **Afirmaciones sobre herramientas o productos:** se comprueban en su
  documentación o en su código, con su fecha. Las herramientas cambian rápido:
  una fuente de hace un año puede describir un producto que ya no existe así.
- **Cada fuente:** en el campo `nota` se anota **qué dice exactamente**, no una
  paráfrasis generosa, y en `respalda`/`contradice`, qué afirmaciones toca.
- **Lo que no se puede confirmar** queda `sin_confirmar`; no se fuerza un
  estado para que la tabla quede bonita.
- **Búsquedas:** se buscan también fuentes que **contradigan** cada afirmación,
  no solo las que confirman. Una afirmación sin intento de refutación no está
  verificada, está repetida.
- **Fecha de consulta:** se indica en cada fuente (`consultada`).
- El vídeo (u otra pieza) de origen se puede registrar como fuente de tipo
  `vídeo` para dejar constancia, pero **no cuenta** para verificar sus propias
  afirmaciones: hace falta al menos una fuente independiente de otro tipo.

## Mecánica

- Las fuentes se guardan por tandas con `guardar-fuentes`; el script conserva
  las anteriores, así que se puede buscar, guardar y seguir buscando.
- Después de la última tanda, `comprobar-enlaces` registra qué URLs responden.
  Un enlace roto no invalida la fuente, pero conviene buscar una copia o una
  alternativa antes de apoyarse solo en ella.
