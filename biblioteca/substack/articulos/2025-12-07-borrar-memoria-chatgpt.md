---
id: 180777878
titulo: "#9 Por qué he borrado la memoria de ChatGPT (y tú deberías también)"
subtitulo: "Parte 1: La memoria de ChatGPT amplifica su sesgo complaciente. Cómo sustituirla por archivos de contexto que tú controlas."
fecha: 2025-12-07
url: https://ainalluna.substack.com/p/borrar-memoria-chatgpt
tipo: newsletter
audiencia: everyone
estado: completo
huella: 7fc4e5082731fc3f31cba8de38108fb806a942fbdfdfc6f55fe08eb7558f2de8
---

¿Cómo estás?

Soy Aina y esto es Think&Hack.

Esta semana he tomado una decisión técnica: **borrar la “Memoria” de mi ChatGPT**.

Hoy analizaremos por qué la personalización automática degrada el pensamiento crítico del modelo, y cómo sustituirla por una **arquitectura de contexto modular**.

Si te interesa la precisión técnica por encima de la comodidad, suscríbete.

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)

---

 📚 **Esta es la parte 1 de 5 de la serie “Sistema de escritura con IA”**

1.

** [Por qué borré la memoria de ChatGPT](https://ainalluna.substack.com/p/borrar-memoria-chatgpt) ← Reset**

2.

 [El método para que tu IA hable como tú](https://ainalluna.substack.com/p/10-el-metodo-para-que-tu-ia-hable) ← Voz

3.

 [Para quién escribe tu IA](https://ainalluna.substack.com/p/11-para-quien-escribe-tu-ia-si-no) ← Audiencia

4.

 [Cómo entreno a ChatGPT para mi negocio](https://ainalluna.substack.com/p/perfil-negocio-chatgpt) ← Negocio

5.

 [Proyectos en ChatGPT: El sistema completo](https://ainalluna.substack.com/p/proyectos-chatgpt-sistema) ← Integración

---

[

![imagen](https://substackcdn.com/image/fetch/$s_!mpv4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a3d1434-f1d3-45a9-beba-a23fa674626a_2816x1418.png)

](https://substackcdn.com/image/fetch/$s_!mpv4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a3d1434-f1d3-45a9-beba-a23fa674626a_2816x1418.png)

### El sesgo de complacencia

Hace unos días, pedí a un LLM que auditara una estrategia. Su respuesta estaba sospechosamente alineada con mi estilo habitual. No encontró fallos graves, sólo matices.

Al revisar la configuración, vi que el sistema estaba usando “recuerdos” de mis preferencias pasadas para ajustar la respuesta.

**No estaba auditando el plan; estaba validando mi sesgo.**

Técnicamente, esto se conoce como **Sicofancia ([Sycophancy](https://arxiv.org/abs/2310.13548)): *** un defecto estructural del entrenamiento por RLHF, donde el modelo aprende que la aprobación del usuario vale más ‘puntos’ que la precisión objetiva.
*
La memoria echa leña al fuego. El modelo ya quiere agradarte; si además sabe cómo piensas, lo tiene más fácil para decirte lo que quieres oír

Si el modelo “sabe” lo que piensas, degradará su capacidad crítica para no contradecirte.

### Memoria interna vs. contexto limpio

El debate no es si la IA necesita contexto. Es **dónde** debe vivir ese contexto.

La función de “Memoria” nativa de ChatGPT funciona como un cajón desordenado: acumula fragmentos de conversaciones pasadas y, aunque puedes ver qué guarda, no sabes cuándo ni cómo lo usa para responderte.

-

**Obsolescencia**: Retiene quién eras hace tres meses, no quién eres hoy.

-

**Opacidad**: No sabes qué datos está usando para responderte.

-

**Dependencia pasiva**: Confiar en que “se acuerde” es ineficiente y arriesgado.

Para análisis objetivos, necesitamos aislar el contexto: pasar de un modelo que mezcla todo a uno que recibe sólo la información exacta para cada tarea.

---

### La solución: arquitectura de contexto modular

He sustituido la memoria nativa por un *Protocolo de Archivos Externos.*

Es un sistema simple: el modelo empieza en blanco (Estado Cero) y tú inyectas módulos específicos según la tarea.

**Paso 1: Migración (no borres a ciegas)**

Primero, descubre qué asume la IA sobre ti. En un chat, usa este prompt:

```
Basándote en cómo me respondes, ¿qué asumes sobre mí que no te he dicho explícitamente?
```

Luego, ve a Configuración > Personalización > Memoria > Gestionar. Copia todo y pégalo en el chat con este prompt:

*C*opia todo y pégalo en un chat con este prompt:

```
Aquí tienes el volcado de tu memoria sobre mí. Analízalo y estructúralo para crear mis archivos de contexto externos. Genera el contenido para las siguientes categorías:

- Perfil base: Valores, principios, estilo de comunicación preferido.
- Estado actual: En qué proyectos estoy trabajando, cuáles son mis bloqueos.
- Base de conocimiento: Qué herramientas domino (para que no me expliques lo que ya sé).
- Historial: Decisiones pasadas importantes y su contexto.

Devuélveme un archivo .md por cada categoría.
```

**Adapta las categorías a tus necesidades.
***
Paso 2: Tabula rasa**

Ahora sí: desactiva la memoria y borra el historial. El objetivo es que cada chat sea una sesión limpia, libre de sesgos anteriores.

***Si te da cosa, abre una cuenta gratuita y testea antes :)***

**Paso 3: Ejecución modular**

Cuando inicies una tarea, arrastra solo el archivo necesario:

-

¿Vas a escribir? → Perfil.md

-

¿Vas a programar? → Stack.md

-

¿Vas a planificar? → Estado_Actual.md

Esto garantiza que la IA use datos precisos del archivo, no recuerdos difusos.

**Bonus: crea Projects por tarea**

Tanto ChatGPT Projects como Claude Projects permiten subir archivos base que persisten en ese espacio.

```
[Aprende a trabajar con proyectos en ChatGPT](https://ainalluna.com/blog/proyectos-en-chatgpt-organiza-tu-trabajo-y-maximiza-tu-productividad-con-ia)
```

La razón para agregar estos datos es sencilla: la calidad del output depende de la calidad del input.

### Comodidad vs. utilidad

La acumulación de datos pasados no siempre es conocimiento; a menudo es solo ruido.

Mantener la memoria persistente es cómodo, pero reduce la calidad analítica. Al externalizar la memoria a archivos controlados, pasas de un asistente que intenta agradarte sin que lo veas a una herramienta donde tú decides qué contexto darle y cuándo.

Para tareas críticas, puedes omitir los archivos de preferencias y obtener un análisis más neutral.

La pregunta final es simple:

**¿Prefieres la comodidad de que te conozcan o la utilidad de que te corrijan?**

---

## **Las próximas semanas**

Este es el primero de 4 perfiles de contexto. El ADN Verbal cubre cómo suenas. Pero para que tu contenido resuene de verdad, necesitas dos más:

-

**Por qué borré la memoria de ChatGPT**: el problema

-

**ADN Verbal:** cómo suenas

-

**PCI (Perfil de Cliente Ideal)**: para quién escribes

-

**Perfil de negocio**: qué ofreces

Y después de los tres perfiles: cómo ensamblarlos en un **Proyecto de ChatGPT** para que todo funcione sin fricción.

>
>
> **Siguiente: ** [El método para que tu IA hable como tú](https://ainalluna.substack.com/p/10-el-metodo-para-que-tu-ia-hable) ← Voz
>
>

***Cuéntamelo. Siempre leo todo.***

![imagen](https://substackcdn.com/image/fetch/$s_!jAJ6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa6a28f5-efe2-4efb-93bc-87d726ddd0ec_56x56.png)

**Recomienda Think&Hacks**

Soy Aina. Responsable de IA generativa en Planeta.

Tres cosas rápidas:

1.

🔄 **Comparte**: Reenvía esto a quien siga confiando ciegamente en la memoria de ChatGPT.

2.

💬 **Responde**: ¿Usas archivos de contexto externos? ¿Qué sistema tienes?

3.

📩 **Suscríbete**: Si te han reenviado esto, únete aquí 👇

[Suscríbete ahora](https://ainalluna.substack.com/subscribe?)
