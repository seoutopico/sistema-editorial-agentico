---
name: analizar-biblioteca
description: Convierte los artículos descargados de Substack en fichas JSON con esquema fijo y genera biblioteca/mapa-temas.md y biblioteca/estilo.md. Úsala después de recuperar-newsletters o cuando haga falta saber qué se ha publicado y desde qué perspectiva.
---

# analizar-biblioteca

Segunda parte de la fase 1 del sistema editorial (ver `ARQUITECTURA.md`,
secciones 2, 4, 6 y 8.1). El script hace lo repetible (detectar pendientes,
validar, guardar, agregar); el modelo solo el juicio (leer cada artículo y
rellenar los campos de la ficha, extraer la guía de estilo). El modelo nunca
escribe archivos de la biblioteca: entrega un JSON y el script lo valida y lo
guarda.

Los criterios para rellenar la ficha están en
`references/instrucciones-ficha.md`; el esquema, en
`references/ficha-articulo.schema.json`.

## Qué lee

- `biblioteca/substack/control/inventario.json` (lo escribe `recuperar-newsletters`).
- `biblioteca/substack/articulos/*.md` (el texto completo de cada artículo).
- `biblioteca/substack/fichas/*.json` (las fichas ya existentes).

## Qué escribe

- `biblioteca/substack/fichas/<id>.json` — una ficha por artículo.
- `biblioteca/mapa-temas.md` — qué hemos tratado, cuándo y desde qué enfoque.
- `biblioteca/estilo.md` — voz de la publicación; la sección `## Reglas
  aprendidas` nunca se pierde al regenerar.

## Flujo

Todos los comandos se ejecutan desde la raíz del proyecto:

```bash
python .agents/skills/analizar-biblioteca/scripts/analizar_biblioteca.py <comando>
```

1. **`pendientes`.** Lista en JSON los artículos sin ficha o con huella
   cambiada, con su motivo, y las listas de temas, subtemas y entidades
   existentes con su número de artículos, ordenadas por frecuencia. Si no hay
   pendientes, ir al paso 4.
2. **Ficha por artículo.** Leer cada artículo pendiente completo y redactar el
   JSON con los campos de juicio siguiendo `instrucciones-ficha.md`,
   reutilizando los temas, subtemas y entidades existentes cuando encajen. Con
   muchos pendientes, avanzar por tandas de 10 y guardar después de cada
   artículo: una interrupción no pierde el trabajo hecho.
3. **`guardar <id> <archivo.json>`** por cada artículo. El script combina el
   juicio con los datos objetivos del inventario, valida contra el esquema y
   escribe de forma atómica. Si falla la validación, explica qué campo falla y
   no escribe nada: corregir y repetir. Si un subtema o entidad se parece a
   uno ya usado (similitud difusa ≥ 0.85 tras normalizar minúsculas y
   tildes), **avisa con el término existente sugerido pero guarda igualmente**
   (salida 0 con avisos): revisar cada aviso y, si el término existente es el
   mismo concepto, corregir el JSON y reguardar. Una coincidencia exacta tras
   normalizar no avisa: es reutilización correcta.
4. **`mapa`.** Regenera `biblioteca/mapa-temas.md` con salida determinista:
   temas con fechas, enfoques y entidades; temas sin tocar en 6 meses;
   entidades globales; y artículos sin ficha si los hay.
5. **Estilo** (solo si `biblioteca/estilo.md` no existe o la persona lo pide).
   - Ejecutar `metricas-estilo` (JSON con longitudes, secciones, listas,
     citas, imágenes y frases, calculado solo sobre artículos completos).
   - Leer los 8 artículos completos más recientes.
   - Escribir la guía con estas secciones: tono y voz, estructura habitual,
     aperturas y cierres, recursos frecuentes, lo que se evita y
     `## Reglas aprendidas`. Cada afirmación se apoya en ejemplos reales de
     esos artículos.
   - Guardarla con **`guardar-estilo <archivo.md>`**, que conserva intacta la
     sección `## Reglas aprendidas` existente (la alimenta
     `registrar-resultado`).
6. **Informar:** fichas creadas, actualizadas y fallidas; temas nuevos
   creados; avisos de vocabulario pendientes de decisión; y si el mapa está
   completo.

## Limpieza periódica del vocabulario

**`vocabulario`** imprime en JSON los temas, subtemas y entidades del corpus
(término, frecuencia y artículos, por frecuencia descendente) y una sección
`sospechosos` con los pares casi-duplicados detectados con la misma similitud
difusa. Ejecutarlo de vez en cuando (o cuando se acumulen avisos de `guardar`)
y unificar los pares que sean el mismo concepto corrigiendo las fichas
afectadas y reguardándolas. Ojo con los falsos positivos: nombres cortos con
versiones ("GPT-5.1" vs "GPT-5.2") se parecen pero son entidades distintas.

## Pruebas

```bash
python -m unittest discover .agents/skills/analizar-biblioteca/scripts -v
```

Usan una biblioteca ficticia en una carpeta temporal; nunca tocan
`biblioteca/` ni la red.
