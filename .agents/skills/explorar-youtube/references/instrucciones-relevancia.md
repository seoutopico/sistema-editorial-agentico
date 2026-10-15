# Instrucciones: clasificar la relevancia de los vídeos

Entrada: la salida JSON de `relevancia-pendiente` (vídeos con `id`, `canal`,
`titulo` y, a veces, `descripcion`; la `linea_editorial`; los `recursos` de la
publicación, con `fuera_de_alcance`; y la lista `temas_existentes`). Salida:
una lista JSON con un objeto por vídeo, todos en una sola respuesta:

```json
[
  { "id": "abc123", "relevante": true, "tema": "Agentes para automatizar la investigación", "motivo": "Una frase." }
]
```

## Criterios

- **Relevante** es lo que encaja con `linea_editorial.nicho` y tiene utilidad
  para `linea_editorial.audiencia`. El número de visualizaciones **no cuenta**
  en esta decisión: las señales ya se calculan aparte.
- **Fuera de alcance**: un vídeo cuyo **único ángulo** cae de lleno en
  `recursos.fuera_de_alcance` (por ejemplo, edición de vídeo o pruebas que
  exigen hardware caro) se marca `relevante: false` con el motivo
  "fuera de alcance: <qué>". Gastar subtítulos y ficha en él es desperdicio:
  caería igualmente en la evaluación posterior. Pero si además tiene un
  ángulo aprovechable en texto o en proceso (un flujo, un sistema, una
  lección trasladable a los formatos que la publicación domina), **sigue
  siendo relevante** por ese ángulo.
- **`tema`**: reutiliza uno de `temas_existentes` si encaja; crea uno nuevo
  solo si ninguno sirve. Los temas comparten vocabulario con las fichas
  propias de `analizar-biblioteca`: mismo idioma, misma granularidad
  (por ejemplo "Agentes para automatizar la investigación", no "IA").
  Un vídeo no relevante puede dejar `tema` en `null`.
- **`motivo`**: una frase.
- **Ambigüedad**: con título y descripción ambiguos, marca `relevante: true`
  con el motivo "requiere ver contenido". Es preferible revisar de más a
  perder una oportunidad. La regla de fuera de alcance solo se aplica cuando
  el único ángulo es claro; ante la duda, relevante.

Después, guarda la lista en un archivo y ejecuta
`guardar-relevancia <archivo.json>`. Si el script rechaza algún campo, corrige
el JSON y repite; el script no escribe nada hasta que todo es válido.
