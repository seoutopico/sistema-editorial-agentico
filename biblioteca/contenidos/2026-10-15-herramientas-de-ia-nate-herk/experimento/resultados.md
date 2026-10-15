# Resultados del experimento — niveles de esfuerzo sobre una tarea editorial real

Fecha: 2026-10-15. Diseño y criterios fijados antes de ejecutar (ver `criterios.md`). Tarea: redactar la misma Substack Note (artículo del 2026-10-11) con `estilo.md` y la plantilla de notes. 4 niveles × 2 repeticiones, mismo prompt literal, evaluación a ciegas con mapeo revelado después.

## Métricas objetivas (del arnés)

| Nivel | Rep | Tokens | Duración | Calidad (0–10, a ciegas) |
|---|---|---|---|---|
| low | 1 | 58.113 | 17,5 s | 9,0 |
| low | 2 | 58.156 | 19,1 s | 8,5 |
| medium | 1 | 58.409 | 21,9 s | 9,5 |
| medium | 2 | 58.398 | 21,5 s | 9,5 |
| high | 1 | 58.950 | 28,4 s | 9,5 |
| high | 2 | 58.528 | 22,2 s | 9,5 |
| max | 1 | 65.432 | 97,8 s | 9,5 |
| max | 2 | 63.416 | 79,5 s | 9,5 |

(Calidad: límites formales 0–2, gancho 0–2, voz 0–3, sustancia 0–2, cierre 0–1. Las 8 cumplieron los límites formales y contienen {{enlace}} sin hashtags. El detalle por nota está en `ciegas/` y el mapeo en `mapeo-oculto.json`.)

## Hallazgos

1. **H1 confirmada (más esfuerzo ≠ mejor resultado):** de medium hacia arriba la calidad es plana (9,5 en las 6 ejecuciones). Max no aportó nada que high o medium no dieran.
2. **H2 matizada:** en el vídeo (tarea larga de edición, 1–2,5 h) el extremo costó 12,9× más. En nuestra tarea corta la diferencia de tokens fue mínima (+12 % max vs low) pero la de **tiempo** fue 4,6–5,6× (17–19 s vs 80–98 s). El coste del esfuerzo alto en tareas cortas se paga sobre todo en latencia, no en tokens.
3. **H3 parcialmente confirmada:** la variabilidad entre repeticiones del mismo nivel (p. ej. low: 9,0 vs 8,5; high: 28,4 s vs 22,2 s) es del orden de la diferencia entre niveles contiguos. Con n=1 (como el vídeo) cualquier ranking fino entre niveles vecinos es ruido.
4. **Dónde se diferenció low:** las dos únicas notas con algo que señalar salieron de low — una abrió con tesis abstracta en vez de escena vivida (menos gancho) y otra viró a segunda persona. Nada grave, pero es el único nivel donde la voz se resintió algo.
5. **Regla práctica derivada:** para piezas cortas de redacción con buen contexto (estilo + plantilla), medium basta y high es el tope útil; max solo paga en tareas largas de construcción/verificación, y aun así conviene medirlo (el vídeo mostró a Extra ganando a Max).

## Límites de este experimento

- Tarea corta y única (una Note); no extrapolable directamente a tareas de horas como las del vídeo.
- Evaluador único (aunque a ciegas y con criterios previos).
- Los tokens del arnés incluyen la lectura de contexto (artículo + estilo + plantilla), igual en todos los niveles, lo que comprime las diferencias relativas de tokens.
