Crea la skill `investigar-tema`. Toma una oportunidad aceptada por la persona, busca fuentes fiables, verifica cada afirmación en la que se apoya y deja una investigación que sirva de base para redactar sin inventar.

Es la primera parte de la fase 3 de `ARQUITECTURA.md`. Léelo antes de empezar y respeta sus secciones 2, 4, 7, 8.5 y 10. Lee también el `SKILL.md` de `detectar-oportunidades` para conocer el formato de las oportunidades y sus evidencias. Si esa skill no existe, detente e indica que falta el prompt 04.

En este paso creas y validas la skill con una oportunidad ficticia. **No investigues ninguna oportunidad real.**

## 1. Reparto entre script y modelo

| Lo hace el script (Python sin IA) | Lo hace el modelo |
|---|---|
| Comprobar que la oportunidad está aceptada | Buscar fuentes en internet |
| Reunir las afirmaciones a verificar | Verificar cada afirmación |
| Validar y guardar las fuentes | Redactar la investigación |
| Comprobar que los enlaces responden | Revisarla de forma crítica |
| Validar que cada afirmación tiene estado y fuente | |

## 2. Estructura

```text
.agents/skills/investigar-tema/
├── SKILL.md
├── references/
│   ├── fuentes.schema.json
│   ├── plantilla-investigacion.md
│   ├── instrucciones-investigacion.md
│   └── instrucciones-verificador.md
└── scripts/
    ├── investigar_tema.py
    └── test_investigar_tema.py
```

Salidas, en la carpeta del contenido. El `<id>` es el de la oportunidad:

```text
biblioteca/contenidos/<id>/
├── afirmaciones.json      # Generado: lo que hay que verificar
├── fuentes.json           # Fuentes consultadas, validadas
├── investigacion.md       # Resultado, con estado de aprobación
└── revision.md            # Informe del verificador crítico
```

**`SKILL.md`:**
- Empieza con un frontmatter con `name` y `description`. Úsala cuando una oportunidad pase a `estado: aceptada`.
- Describe el flujo de la sección 5.
- Es breve: los criterios están en `references/`.

## 3. Comandos del script

```text
python .agents/skills/investigar-tema/scripts/investigar_tema.py <comando> <oportunidad_id>
```

### `preparar <id>`

1. Comprueba que `biblioteca/oportunidades/<id>.md` existe y tiene `estado: aceptada`. Si no, termina con código 2 explicando el estado actual.
2. Crea `biblioteca/contenidos/<id>/`.
3. Genera `afirmaciones.json` con:
   - Cada afirmación de las evidencias citadas en la oportunidad, sacada de las fichas externas, con su `id` estable (`a1`, `a2`…), su texto, su origen (`fuente:id@marca`) y su tipo.
   - Las afirmaciones que la sección "Qué hay que investigar o probar" de la oportunidad pide comprobar.
4. Devuelve en JSON la oportunidad, las afirmaciones, las fichas externas citadas y las rutas de los artículos propios relacionados.

**No sobrescribe una investigación existente.** Si ya hay una, lo indica.

### `guardar-fuentes <id> <archivo.json>`

Valida la lista de fuentes con `fuentes.schema.json`:

```json
[{
  "id": "f1",
  "url": "…",
  "titulo": "…",
  "autor_o_entidad": "…",
  "tipo": "oficial | repositorio | paper | datos | prensa | blog | vídeo",
  "fecha": "YYYY-MM-DD o null",
  "consultada": "YYYY-MM-DD",
  "respalda": ["a1"],
  "contradice": ["a3"],
  "nota": "Qué dice exactamente"
}]
```

- Los IDs deben ser únicos.
- Las afirmaciones citadas deben existir en `afirmaciones.json`.
- Al añadir fuentes, se conservan las ya guardadas.

### `comprobar-enlaces <id>`

- Pide cada URL con timeout y reintentos limitados.
- Registra en `fuentes.json` el código de respuesta y la fecha de la comprobación.
- Un enlace roto se informa; no se borra la fuente.

### `guardar-investigacion <id> <archivo.md>`

Valida y guarda `investigacion.md`.

1. **Encabezado, escrito por el script:** `oportunidad`, `estado: pendiente_aprobacion` y `fecha`.
2. **Secciones obligatorias,** las de `plantilla-investigacion.md`. Ninguna puede faltar.
3. **Tabla de verificación:** cada afirmación de `afirmaciones.json` aparece con un estado (`verificada`, `refutada` o `sin_confirmar`) y los IDs de fuentes que lo apoyan.
4. **Fuentes:**
   - Una afirmación `verificada` o `refutada` necesita al menos una fuente que no sea de tipo `vídeo`. El vídeo de origen no basta para verificarse a sí mismo.
   - Toda referencia `[f<n>]` del texto debe existir en `fuentes.json`.

Si falla una comprobación, no escribe nada y explica cuál.

**Nunca sobrescribe una investigación con `estado: aprobada`.** La aprobación la marca la persona cambiando el estado en el encabezado.

### `guardar-revision <id> <archivo.md>`

Guarda el informe del verificador en `revision.md`.

### Códigos de salida

- `0`: correcto.
- `1`: avisos, como enlaces rotos.
- `2`: no pudo ejecutarse o la validación falló.

Las escrituras son atómicas.

## 4. Plantilla de la investigación

`plantilla-investigacion.md` define estas secciones:

1. **Pregunta de investigación:** qué queremos responder, derivado de la oportunidad.
2. **Resumen:** lo que sabemos ahora, en cinco líneas como máximo.
3. **Verificación de afirmaciones:** tabla con afirmación, estado, fuentes y nota.
4. **Hallazgos nuevos:** lo que las fuentes aportan y no estaba en la evidencia de origen.
5. **Contradicciones y límites:** dónde no coinciden las fuentes y qué no se puede afirmar.
6. **Prueba práctica:** si hace falta probar algo nosotros, qué, cómo y qué resultado lo confirmaría. Si no hace falta, por qué.
7. **Ángulo propuesto:** cómo concretar la aportación de la oportunidad con lo investigado.
8. **Fuentes:** lista numerada con el formato `[f1] Título, autor o entidad, fecha, URL`.

## 5. Flujo que describe SKILL.md

1. `preparar`.
2. **Investigar.** El modelo busca fuentes en internet siguiendo `instrucciones-investigacion.md` y las guarda con `guardar-fuentes`, por tandas si hacen falta varias búsquedas. Después, `comprobar-enlaces`.
3. **Redactar.** El modelo escribe la investigación con la plantilla y la guarda con `guardar-investigacion`.
4. **Verificador crítico.** Se lanza un **subagente** con `instrucciones-verificador.md`.
   - Recibe solo `investigacion.md`, `fuentes.json` y `afirmaciones.json`, no la conversación.
   - Intenta refutar cada afirmación verificada y cada conclusión.
   - Su informe se guarda con `guardar-revision`.
   - Si encuentra errores, se corrige la investigación y se vuelve a guardar.
5. **Informar:** afirmaciones verificadas, refutadas y sin confirmar, enlaces rotos, hallazgos del verificador, y que la investigación queda **pendiente de aprobación** por la persona.

## 6. Criterios del modelo

**`instrucciones-investigacion.md`:**
- **Prioridad de fuentes:**
  1. Documentación oficial, repositorios, papers y datos originales.
  2. Prensa especializada.
  3. Blogs con autor identificable.
- **Afirmaciones sobre herramientas o productos:** se comprueban en su documentación o en su código, con su fecha.
- **Cada fuente:** se anota qué dice exactamente y qué afirmación respalda o contradice.
- **Lo que no se puede confirmar** queda `sin_confirmar`; no se fuerza.
- **Búsquedas:** se buscan fuentes que contradigan, no solo las que confirman.
- **Fecha de consulta:** se indica en cada fuente.

**`instrucciones-verificador.md`:**
- Por cada afirmación `verificada`, comprueba si la fuente dice realmente eso o solo algo parecido.
- Señala conclusiones que van más allá de las fuentes, fuentes desactualizadas y dependencias de una única fuente.
- Lista también lo que está bien fundamentado.
- Termina con un veredicto: `sin objeciones`, `objeciones menores` u `objeciones graves`, y la lista de correcciones.

## 7. Pruebas

Escríbelas con `unittest`, con una oportunidad, fichas y artículos ficticios en una carpeta temporal y la red simulada.

Deben comprobar que:
1. `preparar` rechaza una oportunidad que no está aceptada y no crea nada.
2. `preparar` extrae las afirmaciones de las evidencias con IDs estables y no sobrescribe una investigación existente.
3. `guardar-fuentes` rechaza IDs duplicados o afirmaciones inexistentes y conserva las fuentes anteriores al añadir nuevas.
4. `comprobar-enlaces` registra el código de respuesta y no borra una fuente con un enlace roto.
5. `guardar-investigacion` rechaza:
   - Secciones ausentes.
   - Una afirmación sin estado.
   - Una afirmación verificada solo con el vídeo de origen.
   - Una referencia `[f9]` inexistente.
6. `guardar-investigacion` nunca sobrescribe una investigación aprobada.

Ejecuta las pruebas y muestra el resultado.

Para comprobar las instrucciones del modelo, con la oportunidad ficticia y fuentes ficticias, redacta tú mismo una investigación breve con la plantilla y guárdala con el comando. No hagas búsquedas reales.

## 8. Documentación

- Actualiza en `README.md` la fila del prompt 05 a `hecho`.
- No modifiques `ARQUITECTURA.md`. Si algo obliga a cambiar el diseño, indícalo al final como propuesta.

## 9. Entrega

Muestra:
- El árbol de la skill.
- `SKILL.md`, la plantilla y las instrucciones.
- El resultado de las pruebas.
- La investigación de ejemplo.

Separa lo comprobado de lo que solo se verá con una investigación real.
