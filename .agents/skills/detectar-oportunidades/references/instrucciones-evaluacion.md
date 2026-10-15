# Cómo redactar la evaluación de un grupo

Entrada: un paquete del comando `pendientes`. Salida: un JSON que cumple
`evaluacion.schema.json`. Antes de redactarla, **lee el texto completo de los
artículos parecidos** (campo `ruta_texto` de cada uno), no solo sus fichas.
Las cuatro condiciones las aplica el script; tu trabajo es rellenar los campos
de juicio con honestidad: descartar bien también es un buen resultado.

## `cobertura`

Se decide leyendo nuestros artículos, no por el parecido BM25:

- `cubierto`: ya defendimos lo mismo con un enfoque equivalente.
- `ampliación`: tratamos el tema, pero falta un ángulo, un caso o una
  actualización relevante.
- `nuevo`: no lo hemos tratado.

En `que_hemos_publicado` resume qué cubren ya nuestros artículos; en
`diferencia`, qué no cubren.

## `aportacion`

Concreta y comprobable, por ejemplo: una prueba propia del flujo, el caso en
español, contrastar lo que el vídeo promete sin demostrar o el proceso paso a
paso. Si no hay ninguna, es `null`: **repetir lo que dice el vídeo no es
aportar.**

Además debe ser **ejecutable por la autora con sus recursos**: lee la sección
`recursos` de `proyecto.config.json` (herramientas, hardware, formatos que
domina, fuera de alcance). Una aportación que exige vídeo, hardware que no
tiene o un terreno que no es el suyo **no es una aportación: es un deseo**.
En ese caso busca el ángulo que sí pueda probar con lo que tiene (por ejemplo,
la misma idea aplicada a texto, procesos o su propio sistema editorial) o deja
`aportacion` en `null`. La prueba debe poder hacerse en una semana de trabajo
real, no en un proyecto aparte.

## `encaje`

Frente a `linea_editorial.nicho` y `linea_editorial.aportacion` del paquete:
¿es nuestro nicho y podemos tratarlo como lo hacemos nosotros (probar y contar
el proceso real)? `true` o `false`, con el porqué en `motivo` (una frase).

## Descartes anteriores

Si en `oportunidades_parecidas` hay una **descartada**, lee su motivo. Solo se
vuelve a proponer si algo ha cambiado desde aquel descarte (una versión nueva,
una demostración que antes no existía, un cambio de precio…), y se explica en
`razon_nueva`. Si nada ha cambiado, deja `razon_nueva` en `null`. Pon su id en
`parecida_a`. Si la parecida está en estado `propuesta`, `aceptada` o
`publicada`, ponla igualmente en `parecida_a`: el script no creará un
duplicado e indicará cómo añadirle las evidencias nuevas.

## `articulos_comparados`

Lista los IDs de **todos** los artículos del paquete: el script rechaza la
evaluación si falta alguno. Así queda constancia de con qué se comparó.

## Fuentes

Las afirmaciones se citan con su evidencia (`fuente:id@marca`). No añadas
información que no esté en las fichas o en los artículos.
