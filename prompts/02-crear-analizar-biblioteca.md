Crea la skill `analizar-biblioteca`. Convierte los artículos descargados en fichas con esquema fijo y, a partir de ellas, genera el mapa de temas y la guía de estilo de la publicación. Responde a la pregunta "qué hemos tratado y desde qué perspectiva".

Es la segunda parte de la fase 1 de `ARQUITECTURA.md`. Léelo antes de empezar y respeta sus secciones 2, 4, 6, 8.1 y 10. Lee también `.agents/skills/recuperar-newsletters/SKILL.md` para conocer el formato de `inventario.json` y de los artículos. Si esa skill no existe, detente e indica que primero hay que ejecutar el prompt 01.

En este paso creas y validas la skill con artículos ficticios. **No analices la biblioteca real.**

## 1. Reparto entre script y modelo

| Lo hace el script (Python sin IA) | Lo hace el modelo |
|---|---|
| Detectar qué artículos necesitan ficha | Leer cada artículo y rellenar sus campos de juicio |
| Copiar los datos objetivos a la ficha | Extraer la guía de estilo |
| Validar y guardar cada ficha | |
| Generar `mapa-temas.md` | |
| Calcular las métricas de estilo | |

El modelo nunca escribe archivos de la biblioteca directamente. Entrega un JSON y el script lo valida y lo guarda.

## 2. Estructura

```text
.agents/skills/analizar-biblioteca/
├── SKILL.md
├── references/
│   ├── ficha-articulo.schema.json
│   └── instrucciones-ficha.md
└── scripts/
    ├── analizar_biblioteca.py
    └── test_analizar_biblioteca.py
```

**`SKILL.md`:**
- Empieza con un frontmatter con `name` y `description`. Úsala después de `recuperar-newsletters` o cuando haga falta saber qué se ha publicado.
- Describe el flujo paso a paso: `pendientes`, ficha por artículo, `guardar`, `mapa` y estilo.
- Es breve: los criterios para rellenar la ficha están en `references/instrucciones-ficha.md`.

## 3. La ficha

Usa el esquema de la sección 6 de `ARQUITECTURA.md` para los artículos propios. Añade un único campo, `basada_en` (`completo` o `extracto`), para saber si el análisis partió del texto íntegro.

**Campos que rellena el script** desde el inventario: `id`, `url`, `fecha`, `titulo`, `huella`, `basada_en` y `metricas_publicas`. El modelo no puede modificarlos; si su JSON los incluye, se ignoran.

**Campos que rellena el modelo**, con estos criterios, que se recogen en `references/instrucciones-ficha.md`:
- `tema`: el asunto principal, en pocas palabras. **Reutiliza un tema de la lista de existentes si encaja.** Solo crea uno nuevo si ninguno sirve, y lo indica.
- `subtemas`: de 1 a 5.
- `enfoque`: uno de `tutorial con prueba propia`, `opinión`, `caso`, `recopilación`, `explicación` o `entrevista`.
- `tesis`: una frase con la idea central, tal como la defiende el artículo.
- `entidades`: herramientas, empresas, personas o conceptos concretos que aparecen de forma relevante, con su nombre canónico.
- `nivel`: `inicial`, `intermedio` o `avanzado`.

**`ficha-articulo.schema.json`** define tipos, campos obligatorios y valores permitidos. El script valida contra él usando la biblioteca estándar: comprueba que estén los campos obligatorios, sus tipos y los valores permitidos. No añadas dependencias solo para validar.

## 4. Comandos del script

```text
python .agents/skills/analizar-biblioteca/scripts/analizar_biblioteca.py <comando>
```

**`pendientes`.** Lista en JSON los artículos que necesitan una ficha:
- Los que no tienen ficha.
- Los que tienen una ficha cuya huella no coincide con la del inventario.

Por cada artículo indica su ruta y el motivo. Incluye la **lista de temas existentes**, con su número de artículos, para que el modelo los reutilice. Si no hay pendientes, lo dice expresamente.

**`guardar <id> <archivo.json>`.**
1. Combina los campos de juicio del modelo con los datos objetivos del inventario.
2. Valida la ficha resultante.
3. La escribe de forma atómica en `biblioteca/substack/fichas/<id>.json`.

Si la validación falla, no escribe nada y explica qué campo falla.

**`mapa`.** Regenera `biblioteca/mapa-temas.md` a partir de todas las fichas:
- **Por cada tema:** número de artículos, primera y última fecha, enfoques usados, entidades más frecuentes y la lista de artículos con su enlace.
- **Temas sin tocar en los últimos 6 meses.**
- **Entidades más frecuentes** en toda la biblioteca.
- **Artículos sin ficha,** si los hay, para que el mapa no parezca completo cuando no lo es.

La salida es determinista: los mismos datos siempre producen el mismo archivo, con orden estable. Indica la fecha de generación y el número de fichas usadas.

**`metricas-estilo`.** Calcula sobre los artículos completos:
- Longitud media y mediana en palabras.
- Número medio de secciones.
- Uso de listas, citas e imágenes.
- Longitud media de las frases.

Lo devuelve en JSON para que el modelo lo use al escribir la guía de estilo.

**`guardar-estilo <archivo.md>`.** Escribe `biblioteca/estilo.md` **conservando intacta la sección `## Reglas aprendidas`** si ya existe. Esa sección la alimenta `registrar-resultado` con las correcciones de la persona y nunca se pierde al regenerar el estilo.

## 5. Flujo que describe SKILL.md

1. Ejecutar `pendientes`. Si no hay ninguno, ir al paso 4.
2. Leer cada artículo pendiente completo y redactar el JSON con los campos de juicio, siguiendo `instrucciones-ficha.md`. Con muchos pendientes, avanzar por tandas de 10 y ejecutar `guardar` después de cada artículo. Así una interrupción no pierde el trabajo hecho.
3. Ejecutar `guardar` por cada artículo y corregir los que no superen la validación.
4. Ejecutar `mapa`.
5. **Estilo.** Se genera si `estilo.md` no existe o si la persona lo pide.
   - Leer `metricas-estilo` y los 8 artículos completos más recientes.
   - Escribir la guía con estas secciones: tono y voz, estructura habitual, aperturas y cierres, recursos frecuentes, lo que se evita y `## Reglas aprendidas`.
   - Cada afirmación de la guía se apoya en ejemplos reales de esos artículos.
   - Guardarla con `guardar-estilo`.
6. **Informar:** fichas creadas, actualizadas y fallidas; temas nuevos creados; y si el mapa está completo.

## 6. Pruebas

Escríbelas con `unittest`, sobre una biblioteca ficticia en una carpeta temporal. La biblioteca de prueba tiene un inventario y 4 artículos: uno sin ficha, uno con ficha al día, uno con huella cambiada y uno que es un extracto.

Deben comprobar que:
1. `pendientes` detecta exactamente el artículo sin ficha y el de huella cambiada, con su motivo, y devuelve los temas existentes.
2. `guardar` rechaza fichas con campos obligatorios ausentes, tipos incorrectos o un `enfoque` no permitido, y en ese caso no escribe nada.
3. `guardar` impone los datos objetivos del inventario aunque el JSON del modelo traiga otros valores.
4. `basada_en` refleja si el artículo es un extracto.
5. `mapa` agrupa por tema, calcula fechas y frecuencias, señala artículos sin ficha y produce un archivo idéntico en dos ejecuciones con los mismos datos.
6. `guardar-estilo` conserva la sección `## Reglas aprendidas` existente.
7. `metricas-estilo` ignora los extractos.

Ejecuta las pruebas y muestra el resultado.

Para comprobar las instrucciones del modelo, rellena tú mismo la ficha de uno de los artículos ficticios siguiendo `instrucciones-ficha.md`, guárdala con `guardar` y muestra el resultado. Este ejemplo vive en la carpeta temporal de pruebas, nunca en `biblioteca/`.

## 7. Documentación

- Actualiza en `README.md` la fila del prompt 02 a `hecho`.
- No modifiques `ARQUITECTURA.md`. Si algo obliga a cambiar el diseño, indícalo al final como propuesta.

## 8. Entrega

Muestra:
- El árbol de la skill.
- `SKILL.md` e `instrucciones-ficha.md`.
- El resultado de las pruebas y la ficha de ejemplo.
- Cómo ejecutar el análisis real una vez descargada la newsletter.

Separa lo comprobado con datos ficticios de lo que solo se verá con la biblioteca real; por ejemplo, si la lista de temas queda bien agrupada.
