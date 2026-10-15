---
id: 190999730
titulo: "Mi agente de IA se liaba cada mañana. Lo arreglé partiéndolo en dos."
subtitulo: "Subagentes, teams de agentes, y por qué la regla más vieja del management funciona igual con IA."
fecha: 2026-03-16
url: https://ainalluna.substack.com/p/subagentes-vs-agent-teams-claude-code
tipo: newsletter
audiencia: everyone
estado: completo
huella: 3cee4a962f06b120b9190200bff2a8bde53c44731b812b07b9e92965de0690fc
---

Soy Aina y esto es Think&Hack.

Tengo un sistema en Claude Code que me planifica el día Le digo “buenos días” y él recoge datos de mi vault de Obsidian, comprueba que toca publicar, revisa métricas, mira el inbox y me monta un dashboard visual. Un solo agente haciendo todo.

El formato me salía distinto cada mañana. O se comía secciones enteras, o metía datos en el sitio equivocado, o directamente ignoraba la plantilla. Le daba las instrucciones de recopilar datos Y las de formatear el dashboard en el mismo bloque. Y se perdía.

Hasta que lo partí en dos. Y funcionó.

[

![imagen](https://substackcdn.com/image/fetch/$s_!PBIa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F386cba01-6afc-4830-9697-209b4add3db1_1408x768.jpeg)

](https://substackcdn.com/image/fetch/$s_!PBIa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F386cba01-6afc-4830-9697-209b4add3db1_1408x768.jpeg)

### Cuando un agente hace demasiado, no falla. Se pierde.

Le estaba pidiendo a un solo agente que fuese analista y diseñador a la vez. Que recogiera datos de seis carpetas distintas, evaluara qué urgencia tenía cada cosa, decidiera qué mostrar y qué no, **y además** me lo presentara con callouts de Obsidian, embeds y formato visual perfecto.

Y ahí está el problema: **las instrucciones de datos competían con las de formato.** El contexto se saturaba. No es que el agente fuese incapaz. Es que le estaba pidiendo dos trabajos que requieren dos formas de pensar completamente distintas.

Todo correcto. Todo mal puesto.

**Le pregunté a Claude qué pasaba. Su respuesta fue directa:**

![imagen](https://substackcdn.com/image/fetch/$s_!PKLb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8fb459b3-2f19-4a1c-9a66-0438a96e9d12_929x135.png)

*El diagnóstico de Claude: instrucciones demasiado largas, el modelo pierde el formato.*

```
“Las instrucciones son muy largas y el modelo pierde el formato.” Claro como el agua.
```

Le propuse dividirlo mediante una orquestación de agentes. Y me devolvió esto:

[

![imagen](https://substackcdn.com/image/fetch/$s_!tXWN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52a8e6a8-dd88-4985-8788-bcb8fa3a635a_931x578.png)

](https://substackcdn.com/image/fetch/$s_!tXWN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52a8e6a8-dd88-4985-8788-bcb8fa3a635a_931x578.png)*La propuesta de Claude: dos subagentes en cadena. daily-planner para datos, home-builder para maquetación.*

Dos subagentes en cadena. Uno para datos, otro para maquetación Pero antes de implementarlo, necesitaba entender las opciones.

---

### Dos formas de dividir el trabajo: subagentes vs teams de agentes

Cuando empecé a investigar cómo dividirlo, descubrí que Claude Code tiene **dos formas de crear agentes especializados.** Y no son lo mismo.

**Subagentes.** Trabajan dentro de tu sesión Hacen una tarea específica, te devuelven el resultado y desaparecen. No hablan entre ellos. Solo reportan al agente principal. Como un becario al que le pides un informe: lo hace, te lo entrega, y ya.

[

![imagen](https://substackcdn.com/image/fetch/$s_!sCTR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe8b44b16-24c2-4902-9452-a712183c0a8d_799x715.png)

](https://substackcdn.com/image/fetch/$s_!sCTR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe8b44b16-24c2-4902-9452-a712183c0a8d_799x715.png)*Subagentes: Hacen el trabajo y reportan al agente principal. No se hablan entre ellos.*

**Teams de agentes.** Son instancias independientes de Claude Code que trabajan en paralelo. Tienen una lista de tareas compartida. Se envían mensajes entre ellos. Se coordinan solos. Como un equipo de proyecto donde cada persona tiene su rol y se comunican sin que tú estés en medio.

[

![imagen](https://substackcdn.com/image/fetch/$s_!b7Gz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd9126561-b9bb-49db-8e97-fc17e466bcc4_1052x703.png)

](https://substackcdn.com/image/fetch/$s_!b7Gz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd9126561-b9bb-49db-8e97-fc17e466bcc4_1052x703.png)*Teams de agentes: se coordinan solos a traves de una lista de tareas compartida. Se envian mensajes entre ellos.*

La diferencia visual es clara:

[

![imagen](https://substackcdn.com/image/fetch/$s_!kFRk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8d016633-cbc3-4e9f-84e2-6f327e7845d0_4245x1615.png)

](https://substackcdn.com/image/fetch/$s_!kFRk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8d016633-cbc3-4e9f-84e2-6f327e7845d0_4245x1615.png)*Subagentes vs Agent Teams. Fuente: Documentación oficial de Claude Code.*

La diferencia, en una tabla:

[

![imagen](https://substackcdn.com/image/fetch/$s_!06QY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9ba431e0-c888-4e36-89c3-38e5871fc31b_1082x426.png)

](https://substackcdn.com/image/fetch/$s_!06QY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9ba431e0-c888-4e36-89c3-38e5871fc31b_1082x426.png)

La pregunta clave no es cuál es mejor. Es: **¿Tus agentes necesitan hablar entre ellos o solo necesitan entregar un resultado?**

---

### Cómo lo resolví

Mi caso era claro. El agente de datos no necesita hablar con el de formato. Solo necesita pasarle un briefing. **Subagentes.**

**Lo dividí en dos:**

-

**Agente 1: daily-planner.** Recoge los datos. Revisa qué se ha publicado, qué falta, cómo van las métricas, qué hay en el inbox. Genera un briefing estructurado con secciones marcadas: NEWSLETTER, HOY, CALENDARIO, MÉTRICAS, INBOX, ACCIONES. Solo texto. Cero formato visual.

-

**Agente 2: home-builder.** Recibe ese briefing. Lee la plantilla de formato. Mapea cada sección a su callout de Obsidian. Escríbelo `_Home.md` con el formato visual completo. Solo maqueta. Cero recopilación de datos.

El flujo:

```
"buenos dias"
    |
    v
daily-planner (datos)
    |
    v
Briefing estructurado (texto plano)
    |
    v
home-builder (maquetacion)
    |
    v
_Home.md con formato perfecto en Obsidian

```

**Este es el resultado real. Cada mañana:**

[

![imagen](https://substackcdn.com/image/fetch/$s_!mghu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde0e03fd-bd5b-4a80-96ef-a8bfab24f023_695x357.png)

](https://substackcdn.com/image/fetch/$s_!mghu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde0e03fd-bd5b-4a80-96ef-a8bfab24f023_695x357.png)*“buenos días” ejecutándose en Claude Code. Dos agentes en cadena: primero datos, después maquetación.*

`daily-planner` Recopila todo en 2 minutos. `home-builder` Maqueta en 1 minuto. Formato consistente **cada mañana **Mismos datos. Mismo resultado visual. La diferencia no es que el agente sea mejor. Es que cada uno hace **una sola cosa.**

---

### Pruébalo tú.

La próxima vez que un agente te dé resultados inconsistentes, hazte esta pregunta: **¿le estoy pidiendo dos trabajos que requieren dos formas de pensar distintas?**

Si la respuesta es sí, pártelo. No necesitas teams ni arquitecturas complejas. Un subagente que recoge datos y otro que los presenta. O uno que investiga y otro que redacta. O uno que analiza y otro que ejecuta.

La misma regla que funciona con equipos humanos funciona con agentes: **especializar supera a generalizar.** Cada vez.

---

Le di a un solo agente demasiado trabajo y me quejé de que el resultado no era consistente. El agente no fallaba. Yo le estaba pidiendo mal.

**¿Te ha pasado algo parecido? ¿Has tenido que dividir un agente porque se perdía?**

**Comparte:** Reenvía esto a quien use agentes de IA y se queje de que los resultados son inconsistentes.
**Responde:** ¿Has tenido que partir un agente en dos? ¿Cómo lo resolviste?
**Suscríbete:** Si te han reenviado esto, [únete aquí](https://ainalluna.substack.com/).

***Cuéntamelo. Siempre leo todo.***

**Fuentes y links**

-

[Subagentes en Claude Code — Documentación oficial](https://code.claude.com/docs/en/sub-agents)

-

[Teams de agentes en Claude Code — Documentación oficial](https://code.claude.com/docs/en/agent-teams)

-

[Comparativa subagentes vs teams](https://code.claude.com/docs/en/agent-teams#compare-with-subagents)

---

![imagen](https://substackcdn.com/image/fetch/$s_!KYv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67c58daa-610b-4f97-9d9e-c7a7431183ba_80x80.webp)

**Recomienda Think&Hack**

Soy Aina. Responsable de IA generativa en Planeta.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
