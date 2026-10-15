---
name: investigar-tema
description: Toma una oportunidad con estado aceptada, busca fuentes fiables en internet, verifica cada afirmación en la que se apoya y deja una investigación revisada en biblioteca/contenidos/<id>/, pendiente de aprobación. Úsala cuando una oportunidad pase a `estado: aceptada`.
---

# investigar-tema

Primera parte de la fase 3 del sistema editorial (ver `ARQUITECTURA.md`,
secciones 2, 4, 7, 8.5 y 10). El script hace lo repetible (comprobar que la
oportunidad está aceptada, reunir las afirmaciones a verificar, validar y
guardar fuentes, comprobar enlaces, validar que cada afirmación tiene estado
y fuente); el modelo solo el juicio (buscar fuentes en internet, verificar
cada afirmación, redactar la investigación y revisarla de forma crítica).

Los criterios del modelo están en `references/instrucciones-investigacion.md`,
`references/plantilla-investigacion.md` y
`references/instrucciones-verificador.md`; el esquema de las fuentes, en
`references/fuentes.schema.json`.

## Qué lee

- `biblioteca/oportunidades/<id>.md` — la oportunidad aceptada.
- `biblioteca/<fuente>/**/ficha.json` — las fichas externas de las evidencias.
- `biblioteca/substack/control/inventario.json` — rutas de los artículos
  propios relacionados.

## Qué escribe

En `biblioteca/contenidos/<id>/`: `afirmaciones.json`, `fuentes.json`,
`investigacion.md` (con `estado: pendiente_aprobacion`) y `revision.md`.

## Flujo

Todos los comandos se ejecutan desde la raíz del proyecto:

```bash
python .agents/skills/investigar-tema/scripts/investigar_tema.py <comando> <oportunidad_id>
```

1. **`preparar <id>`.** El script comprueba que la oportunidad está aceptada,
   crea `contenidos/<id>/`, genera `afirmaciones.json` y devuelve en JSON la
   oportunidad, las afirmaciones, las fichas citadas y las rutas de los
   artículos relacionados. No sobrescribe una investigación existente.
2. **Investigar.** El modelo busca fuentes en internet siguiendo
   `instrucciones-investigacion.md` y las guarda con
   **`guardar-fuentes <id> <archivo.json>`**, por tandas si hacen falta varias
   búsquedas. Después, **`comprobar-enlaces <id>`**.
3. **Redactar.** El modelo escribe la investigación con
   `plantilla-investigacion.md` y la guarda con
   **`guardar-investigacion <id> <archivo.md>`**: el script valida secciones,
   tabla de verificación y referencias, y escribe el encabezado.
4. **Verificador crítico.** Se lanza un **subagente** con
   `instrucciones-verificador.md`. Recibe solo `investigacion.md`,
   `fuentes.json` y `afirmaciones.json`, no la conversación, e intenta refutar
   cada afirmación verificada y cada conclusión. Su informe se guarda con
   **`guardar-revision <id> <archivo.md>`**. Si encuentra errores, se corrige
   la investigación y se vuelve a guardar.
5. **Informar:** afirmaciones verificadas, refutadas y sin confirmar, enlaces
   rotos, hallazgos del verificador, y que la investigación queda **pendiente
   de aprobación** por la persona (cambia `estado` en el encabezado de
   `investigacion.md`).

Códigos de salida: `0` correcto, `1` avisos (p. ej. enlaces rotos), `2` no
pudo ejecutarse o la validación falló. Las escrituras son atómicas y **nunca
se sobrescribe una investigación con `estado: aprobada`**.

## Pruebas

```bash
python -m unittest discover .agents/skills/investigar-tema/scripts -v
```

Usan una oportunidad, fichas y artículos ficticios en una carpeta temporal y
la red simulada; nunca tocan `biblioteca/` ni la red.
