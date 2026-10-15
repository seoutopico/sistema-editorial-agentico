# Experimento: niveles de esfuerzo sobre una tarea editorial real

Escrito ANTES de ejecutar nada (2026-10-15).

## Tarea (idéntica en todas las ejecuciones)

Redactar una Substack Note a partir del artículo propio «He montado un pequeño equipo de IA para que mis aplicaciones no parezcan un Frankenstein» (2026-10-11), siguiendo `biblioteca/estilo.md` y la plantilla `notes.md` de adaptar-contenido (80–600 caracteres, enlace obligatorio como {{enlace}}, 0 hashtags).

## Diseño

- Niveles: low, medium, high, max (4 niveles).
- n = 2 ejecuciones por nivel (el vídeo hizo n=1; la variabilidad entre repeticiones es parte de lo que medimos).
- Mismo prompt literal en las 8; ningún dato de un nivel visible para otro.
- Métricas objetivas por ejecución: tokens consumidos y duración (del propio arnés).

## Criterios de calidad (puntuación 0–10, fijados antes de ver ningún resultado)

1. **Límites formales (0–2):** 80–600 caracteres, contiene {{enlace}}, 0 hashtags.
2. **Gancho (0–2):** la primera frase crea tensión o curiosidad concreta (no resumen plano).
3. **Voz (0–3):** primera persona experimental, lenguaje llano, sin hype ni tono de gurú; suena a la autora (contraste con estilo.md).
4. **Sustancia (0–2):** recoge la idea diferencial del artículo (sistema de diseño consultable + agente constructor y agente revisor), no una generalidad sobre IA.
5. **Cierre (0–1):** invita a leer o deja una pregunta/idea accionable, sin "léelo aquí" plano.

Evaluación a ciegas: las 8 notes se puntúan identificadas solo por un código aleatorio, sin saber nivel ni repetición, y el mapeo se revela después.

## Hipótesis previas (del vídeo, a contrastar)

- H1: más esfuerzo no implica mejor resultado (en el vídeo, Extra ganó a Max).
- H2: la diferencia de coste entre extremos será grande (12,9x en el vídeo) frente a una diferencia de calidad pequeña.
- H3 (nuestra): en tareas cortas de redacción, la variabilidad entre repeticiones del mismo nivel puede ser mayor que la diferencia entre niveles contiguos.
