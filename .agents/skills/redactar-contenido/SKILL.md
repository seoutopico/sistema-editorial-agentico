---
name: redactar-contenido
description: Escribe el contenido principal (la newsletter) a partir de una investigación aprobada y con la voz de biblioteca/estilo.md, y deja principal.md en borrador junto a una copia intacta en principal.borrador.md. Úsala cuando una investigación pase a `estado: aprobada`.
---

# redactar-contenido

Segunda parte de la fase 3 del sistema editorial (ver `ARQUITECTURA.md`,
secciones 2, 4, 7, 8.5 y 10). El script hace lo repetible (comprobar que la
investigación está aprobada, preparar el material, guardar el borrador
original intacto y comprobar citas, enlaces y longitud); el modelo solo el
juicio (escribir el texto con la voz de `estilo.md` y proponer títulos). El
texto **solo puede afirmar lo que está en la investigación**.

Los criterios del modelo están en `references/instrucciones-redaccion.md`.

## Qué lee

- `biblioteca/contenidos/<id>/investigacion.md` — aprobada por la persona.
- `biblioteca/contenidos/<id>/fuentes.json` — para las citas `[f<n>]`.
- `biblioteca/oportunidades/<id>.md` — la aportación y los relacionados.
- `biblioteca/estilo.md` — la voz, incluida `## Reglas aprendidas`.
- `biblioteca/substack/control/inventario.json` — URLs de artículos propios.

## Qué escribe

En `biblioteca/contenidos/<id>/`:

- `principal.md` — el texto que la persona revisa y edita.
- `principal.borrador.md` — copia idéntica del borrador del modelo; no se
  edita nunca. `registrar-resultado` la compara con lo publicado para
  convertir las diferencias en reglas de estilo.

## Flujo

Todos los comandos se ejecutan desde la raíz del proyecto:

```bash
python .agents/skills/redactar-contenido/scripts/redactar_contenido.py <comando> <id>
```

1. **`preparar <id>`.** El script comprueba que la investigación tiene
   `estado: aprobada` y devuelve en JSON las rutas del material, las métricas
   de estilo (calculadas con `analizar-biblioteca`) y los artículos propios
   relacionados con título y URL. Si falta `estilo.md`, avisa: conviene
   generarlo antes de redactar.
2. **Redactar.** El modelo lee la oportunidad, la investigación completa y
   `estilo.md` —incluida `## Reglas aprendidas`— y escribe el texto siguiendo
   `references/instrucciones-redaccion.md`, con el bloque inicial de títulos.
3. **`guardar <id> <archivo.md>`.** El script escribe el encabezado
   (`oportunidad`, `estado: borrador`, `fecha`, `titulos_alternativos`),
   comprueba citas, enlaces internos y longitud, y escribe `principal.md` y
   `principal.borrador.md` idénticos. Un `principal.md` con
   `estado: aprobado` no se toca; un borrador solo se sustituye con
   `--reemplazar`.
4. **Informar:** los avisos de las comprobaciones y que el texto queda **en
   borrador**. La persona lo edita en `principal.md` y lo marca como
   `aprobado` en el encabezado. Tras editar a mano, **`comprobar <id>`**
   repite las comprobaciones sin modificar nada.

Códigos de salida: `0` correcto, `1` avisos (p. ej. longitud fuera de rango),
`2` no pudo ejecutarse o la validación falló. Las escrituras son atómicas.

## Pruebas

```bash
python -m unittest discover .agents/skills/redactar-contenido/scripts -v
```

Usan una investigación, fuentes, estilo e inventario ficticios en una carpeta
temporal; nunca tocan `biblioteca/` ni la red.
