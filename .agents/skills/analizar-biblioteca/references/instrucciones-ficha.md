# Instrucciones para rellenar la ficha de un artículo

El modelo lee el artículo completo y entrega **un JSON con solo los campos de
juicio**. El script (`guardar`) lo combina con los datos objetivos del
inventario, lo valida contra `ficha-articulo.schema.json` y lo guarda. Si el
JSON incluye `id`, `url`, `fecha`, `titulo`, `huella`, `basada_en` o
`metricas_publicas`, el script los ignora.

## Campos de juicio

### `tema`
El asunto principal del artículo, en pocas palabras (p. ej. "Agentes para
automatizar la investigación").

**Reutiliza un tema de la lista de existentes si encaja.** El comando
`pendientes` incluye esa lista con su número de artículos. Solo crea un tema
nuevo si ninguno de los existentes sirve, y en ese caso indícalo expresamente
en tu informe ("tema nuevo: …"). Un tema por matiz distinto fragmenta el mapa
y lo vuelve inútil.

### `subtemas`
De 1 a 5 asuntos secundarios que el artículo trata de verdad, no palabras
clave decorativas.

**Reutiliza los subtemas existentes si encajan.** El comando `pendientes`
devuelve la lista con sus frecuencias. Un matiz nuevo por artículo ("agente
autónomo con objetivo medible" junto a "agente autónomo con objetivo real")
fragmenta el vocabulario y arruina el cruce léxico. Si `guardar` avisa de que
un subtema se parece a uno ya usado, decide: si es el mismo concepto, corrige
el JSON con el término existente y reguarda; si de verdad es distinto, el
aviso se ignora (la ficha ya quedó guardada).

### `enfoque`
Exactamente uno de estos valores:

- `tutorial con prueba propia` — enseña a hacer algo y muestra el proceso real.
- `opinión` — defiende una postura.
- `caso` — cuenta una experiencia o aplicación concreta.
- `recopilación` — reúne y compara recursos, herramientas o enlaces.
- `explicación` — aclara un concepto sin tutorial ni postura.
- `entrevista` — conversación con otra persona.

Si dudas entre dos, elige el que domina en extensión del texto.

### `tesis`
Una sola frase con la idea central **tal como la defiende el artículo**, no un
resumen neutro del tema. Mal: "El artículo habla de agentes". Bien: "Un agente
mal acotado produce más trabajo del que ahorra".

### `entidades`
Herramientas, empresas, personas o conceptos concretos que aparecen de forma
relevante (no una mención de pasada), con su **nombre canónico**: "Claude
Code", no "claude code" ni "el CLI de Claude". Usa la misma grafía que las
entidades existentes que devuelve `pendientes` para que las frecuencias del
mapa y el cruce léxico sean reales. Los avisos de `guardar` por entidades
casi-duplicadas se tratan igual que los de subtemas.

### `nivel`
- `inicial` — no presupone experiencia con el tema.
- `intermedio` — presupone manejo básico de las herramientas que cita.
- `avanzado` — presupone experiencia real y entra en detalles finos.

## Formato de entrega

Un archivo JSON con exactamente esta forma:

```json
{
  "tema": "Agentes para automatizar la investigación",
  "subtemas": ["diseño de prompts", "validación de fuentes"],
  "enfoque": "tutorial con prueba propia",
  "tesis": "Una frase con la idea central tal como la defiende el artículo.",
  "entidades": ["Claude Code", "n8n"],
  "nivel": "intermedio"
}
```

Guárdalo con:

```bash
python .agents/skills/analizar-biblioteca/scripts/analizar_biblioteca.py guardar <id> <archivo.json>
```

Si la validación falla, el script explica qué campo falla y no escribe nada:
corrige el JSON y vuelve a ejecutar `guardar`.
