---
id: 2026-10-14-contenido-y-curacion-con-ia
estado: descartada
motivo_estado: "La autora no trabaja vídeo ni es su terreno; aportación no ejecutable con sus recursos (decisión de Aina, 2026-10-14)"
tema: Contenido y curación con IA
grupo_id: contenido-y-curacion-con-ia
interes: alto
canales: 1
cobertura: nuevo
evidencias: [youtube:j906Pf7n7Sg@00:01, youtube:j906Pf7n7Sg@02:06, youtube:j906Pf7n7Sg@00:33, youtube:j906Pf7n7Sg@04:11, youtube:j906Pf7n7Sg@08:58, youtube:j906Pf7n7Sg@10:00, youtube:j906Pf7n7Sg@13:45, youtube:j906Pf7n7Sg@16:19, youtube:j906Pf7n7Sg@19:56, youtube:j906Pf7n7Sg@22:32, youtube:j906Pf7n7Sg@24:06, youtube:j906Pf7n7Sg@13:14, youtube:j906Pf7n7Sg@23:03]
relacionados: [substack:183130708, substack:186168347, substack:195602355, substack:214284185, substack:217631531]
---
## La oportunidad

Los modelos de lenguaje acaban de dar el salto a la creación audiovisual: animación, pixel art, motion graphics y juegos generados programáticamente, con Claude Opus 5.5 a la cabeza. No hemos publicado nada sobre esto y el vídeo que lo demuestra deja sin responder justo lo que nuestra audiencia necesita saber para usarlo en su trabajo: prompts completos, coste, tasa de fallo y mecanismo de integración.

## Por qué ahora (evidencias)

Un vídeo de Dot CSV Lab del 2026-09-24 con interés alto (múltiplo 3,98 sobre la mediana del canal). Las capacidades audiovisuales habrían recorrido su fase exponencial en los dos últimos meses (youtube:j906Pf7n7Sg@04:11) y el salto es demostrable: una animación pixel art de una red neuronal que entrena un MLP real con MNIST para ser fiel al proceso (youtube:j906Pf7n7Sg@10:00), un juego one shot con pixel art puro, niveles y música reactiva donde GPT-6 Astra solo logra algo normalito con el mismo prompt (youtube:j906Pf7n7Sg@13:45), animaciones sincronizadas con audio que superan el flujo anterior del autor con ChatGPT (youtube:j906Pf7n7Sg@19:56) y una escena reconstruida dentro de After Effects con el 90-95% del trabajo hecho (youtube:j906Pf7n7Sg@22:32). El propio autor avisa de que no basta con pedir "hazme una animación": hay que condicionar con referencias de estilo (youtube:j906Pf7n7Sg@08:58).

## Qué hemos publicado y qué falta

Hemos cubierto agentes que construyen apps e interfaces propias ([El contenido me lo das tú](biblioteca/substack/articulos/2026-09-06-el-contenido-me-lo-das-tu-como-consumirlo.md)), sistemas de escritura portables entre agentes ([Codex en ChatGPT Plus](biblioteca/substack/articulos/2026-04-27-codex-chatgpt-plus-incluido.md)), prompting limpio para GPT-5.2 ([Guía prompting GPT-5.2](biblioteca/substack/articulos/2026-01-11-14-guia-prompting-gpt-52-lo-que-cambio.md)), reutilizar archivo vía API ([ChatGPT + WordPress](biblioteca/substack/articulos/2026-02-02-chatgpt-wordpress-calendario-editorial.md)) y convertir tutoriales en skills ([Adiós a los GPT personalizados](biblioteca/substack/articulos/2026-10-04-como-crear-skill-chatgpt-work.md)). Falta por completo la creación audiovisual con modelos de lenguaje: animación, pixel art y motion graphics generados programáticamente. De hecho, en el artículo de Astra reconocimos que la edición de vídeo con IA nos salía floja sin criterio experto: este salto toca directamente esa carencia.

## Qué aportaríamos

Probar nosotras el flujo que el vídeo enseña pero no documenta: generar una animación explicativa real para la propia newsletter con Opus 5.5 (y el mismo prompt en GPT-6 Astra como contraste), publicando los prompts completos, los intentos descartados, el tiempo y el consumo de cuota por generación. El vídeo solo enseña los resultados buenos; nuestra pieza contaría el proceso real con lo que funciona y lo que no, en español y aplicado a contenido de trabajo, no a demos espectaculares.

## Qué hay que investigar o probar

- Cuánto cuestan en tiempo y cuota estas generaciones y qué plan hace falta para trabajar así a diario (el vídeo menciona 40-50 minutos por animación sin medir coste).
- Cómo se integra Claude con After Effects en la práctica (youtube:j906Pf7n7Sg@22:32 lo demuestra pero no enseña el mecanismo: ¿MCP, scripting, agente?).
- Qué tasa de fallo real hay: cuántos intentos se descartan y cómo se depura un resultado malo.
- Cuánto pesa la referencia de estilo frente al modelo (youtube:j906Pf7n7Sg@08:58): repetir el mismo prompt con y sin referencias.
- Si la ventaja de Opus 5.5 sobre Astra se mantiene en nuestro caso de uso con el mismo prompt (youtube:j906Pf7n7Sg@13:45).

## Riesgos

El vídeo promete sin demostrar que la técnica funcione igual en Unity o Blender (solo enseña After Effects) y que las mejoras de cuota se noten de verdad. El marco de las sigmoides por dominio es un modelo mental sin datos. Es un tema de ciclo corto: la comparativa Opus 5.5 vs Astra puede quedar obsoleta con el siguiente lanzamiento, así que la pieza debe anclarse en el proceso y los costes, no en qué modelo gana. Trabajar así requiere planes de pago y las generaciones largas pueden agotar cuotas.
