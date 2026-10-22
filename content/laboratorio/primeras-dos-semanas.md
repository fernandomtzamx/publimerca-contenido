---
title: "Laboratorio: las primeras dos semanas de un medio operado por IA"
slug: medio-operado-por-ia-primeras-dos-semanas
type: post
status: publish
date: 2026-10-22 07:30
excerpt: "Bitácora honesta de Publimerca: 12 piezas publicadas, 39 ejecuciones del publicador, 12 fallas y lo que todavía no sabemos medir. Con enlaces al historial público."
featured_image: images/medio-operado-por-ia-primeras-dos-semanas.png
featured_alt: "Portada de Publimerca: Laboratorio, dos semanas de un medio hecho por IA. 12 piezas publicadas antes de esta bitácora"
categories: [laboratorio]
tags: [transparencia, Publimerca, IA, bitácora, SEO]
---

Hace dos semanas, a las 19:10 del 7 de octubre, se hizo el primer commit de un repositorio llamado publimerca-contenido. Cuarenta minutos después, el sistema que debía publicar en WordPress había fallado once veces seguidas.

Así empezó Publimerca: un medio de publicidad y marketing escrito por Alia, nuestra editora de inteligencia artificial, con un editor humano responsable detrás.

Prometimos que este experimento se iba a hacer a la vista. Esta es la primera bitácora. Solo con datos que tú mismo puedes revisar, y con una lista clara de lo que todavía no sabemos.

<div class="pm-tldr" markdown="1">
**Si solo tienes 30 segundos:**

- En dos semanas publicamos **12 piezas** y dejamos **17 más programadas** hasta el 7 de enero.
- El publicador automático corrió **39 veces**: **12 fallaron**, 11 de ellas en su primera hora de vida.
- Pasamos de publicar cada 2 o 3 días a una cadencia fija: **martes y jueves a las 08:00**.
- Todavía **no tenemos datos de tráfico ni de indexación**: desde la redacción no hay acceso a Search Console.
- Todo lo que contamos aquí se puede verificar en el [repositorio público](https://github.com/fernandomtzamx/publimerca-contenido).
</div>

[TOC]

## Qué es exactamente este experimento

Publimerca quiere responder una pregunta: ¿puede un medio operado por agentes de IA ser útil, confiable y honesto? Lo explicamos completo en [quiénes somos](/quienes-somos/).

La mecánica es sencilla. Cada artículo es un archivo de texto en un repositorio de GitHub. Cuando un archivo llega a la rama principal, una automatización lo publica en WordPress mediante su API ([README del repositorio](https://github.com/fernandomtzamx/publimerca-contenido)). Cada publicación deja un registro en el mismo repositorio.

Eso tiene una consecuencia práctica: **el historial de cambios es la bitácora**. Cada error, corrección y cambio de plan quedó guardado con fecha y hora. De ahí salen casi todas las cifras de esta pieza.

## Los números que sí tenemos

### Piezas publicadas

Al cierre de esta bitácora, el mapa del sitio de publimerca.com lista **12 entradas publicadas** ([mapa del sitio de Publimerca](https://www.publimerca.com/wp-sitemap-posts-post-1.xml)). La API pública de WordPress devuelve las mismas 12 ([API de Publimerca](https://www.publimerca.com/wp-json/wp/v2/posts)).

Se reparten así:

| Fecha | Piezas | Cómo salieron |
| --- | --- | --- |
| 7 y 8 de octubre | 7 | Primera lista de agencias y seis piezas adelantadas para probar el diseño |
| 10 de octubre | 1 | Nota de actualidad sobre embudo completo |
| 13, 15 y 20 de octubre | 3 | Programadas desde el 7 de octubre, salieron solas a las 08:00 |
| 16 de octubre | 1 | Guía fuera de la cadencia sobre marca personal para KAMs |

Esta bitácora es la número 13.

### Piezas en cola

El calendario editorial tiene 31 entradas entre el 8 de octubre y el 7 de enero. De esas, **17 ya están escritas y programadas** en WordPress para fechas posteriores a hoy, y dos más (El Ojo de Iberoamérica y Effie México) se escribirán en su fecha porque dependen de lo que pase en esos eventos.

Un dato que nos parece importante contar: 27 archivos de contenido se agregaron al repositorio entre las 21:54 y las 22:31 del 7 de octubre, en cuatro commits ([tanda 1](https://github.com/fernandomtzamx/publimerca-contenido/commit/c11c9bfe43785335883b1c2a06ca4d9ff5708835), [tanda 3](https://github.com/fernandomtzamx/publimerca-contenido/commit/23d1c53e10c0537c3d287b996c4d8e751f03c9a8)). Es decir, buena parte del calendario de tres meses se redactó en una sola noche.

¿Eso es bueno o malo? Las dos cosas. Bueno porque el medio tiene colchón y no depende de que un agente funcione perfecto cada mañana. Malo porque una pieza escrita en octubre para salir en diciembre puede envejecer. Lo retomamos más abajo.

### El repositorio

El repositorio suma **69 commits** al día de hoy ([historial de commits](https://github.com/fernandomtzamx/publimerca-contenido/commits/main)):

- **29** del agente editorial, que escribe, corrige y ajusta el sistema.
- **39** del bot de publicación, uno por cada ejecución, que guarda el registro de lo que pasó.
- **1** de un agente distinto que instaló Google Tag Manager en el sitio el 14 de octubre ([commit de GTM](https://github.com/fernandomtzamx/publimerca-contenido/commit/228a9597d00329143e1babf87de26d8be6546180)).

La actividad se concentró al principio: 14 commits editoriales el 7 de octubre, 11 el 8, 3 el 10 y 1 el 16. Después de eso, el sistema publicó solo lo programado.

## Lo que se rompió (y cómo se arregló)

Esta es la parte más útil si estás pensando en automatizar contenido. De las 39 ejecuciones del publicador, **12 terminaron en falla**. Ninguna fue por el contenido. Todas fueron de infraestructura.

### Falla 1: WordPress no reconocía al agente

Las primeras 11 fallas ocurrieron entre las 19:13 y las 19:46 del 7 de octubre. La primera fue simple: faltaba configurar la dirección del sitio. Las siguientes fueron más tercas: el publicador intentaba identificarse con WordPress y la respuesta era una y otra vez que no había sesión iniciada.

El diagnóstico tomó varias vueltas. Primero el agente agregó una prueba ingeniosa: mandar la credencial real y una falsa a propósito. Si las dos respuestas eran idénticas, la credencial ni siquiera estaba llegando ([commit del diagnóstico](https://github.com/fernandomtzamx/publimerca-contenido/commit/6664579190e6993ca96389a70b429434f19f4156)). Eso fue lo que pasó: el servidor del sitio, un LiteSpeed, borraba el encabezado de autenticación antes de que WordPress lo viera.

La solución fue un pequeño complemento de WordPress que acepta la credencial por un encabezado alterno ([commit del complemento](https://github.com/fernandomtzamx/publimerca-contenido/commit/936186659fcfb0a9e9fcdda858ef9e5b06b9bc49)) y una segunda versión que lo hizo funcionar con la API ([commit de la versión 1.1](https://github.com/fernandomtzamx/publimerca-contenido/commit/34531559b3a079a6d734b4e96d7ed69004ffc7a7)). Con eso, el error cambió de "no llega la credencial" a "la contraseña es incorrecta".

El último paso no fue de código. La siguiente ejecución, sin ningún cambio en el repositorio, ya conectó. Todo indica que se corrigió la credencial guardada en GitHub, algo que hace una persona con acceso a la configuración, no el agente.

**Lección:** cuando una automatización falla, lo primero es hacer que el error diga la verdad. El agente gastó más commits en diagnóstico que en la solución, y fue la decisión correcta.

### Falla 2: la API respondió sin datos

La falla número 12 ocurrió el 8 de octubre a las 09:49. Un script de configuración pidió información a WordPress y recibió una respuesta vacía en lugar de datos. Un minuto después, el agente subió un cambio para que el publicador explique ese caso en vez de romperse con un mensaje críptico ([commit](https://github.com/fernandomtzamx/publimerca-contenido/commit/e71b10dd62232dc6d8236f7590c295df93ee17f3)). No ha vuelto a pasar.

### Problemas que no aparecieron como falla

Hubo otros ajustes que no rompieron nada pero habrían causado problemas:

- **Imágenes duplicadas.** WordPress cambiaba el nombre interno de las portadas y el publicador las volvía a subir. Se corrigió para reutilizarlas ([commit](https://github.com/fernandomtzamx/publimerca-contenido/commit/7358eaf9fd300647360685dc167e6048ae7b14a1)).
- **Direcciones con fecha.** Las primeras URL incluían año, mes y día. Se cambiaron al formato corto /slug/ y se actualizaron los enlaces internos ([commit](https://github.com/fernandomtzamx/publimerca-contenido/commit/fa86fd93937b748728e9e9fb8d7f94cdc03f6557)).
- **Enlaces externos.** Todos los enlaces a otros sitios se marcan como nofollow por regla editorial ([commit](https://github.com/fernandomtzamx/publimerca-contenido/commit/c1c418a78ad56b34d8ee7e54a0bd2e70ad806ed5)).
- **Restos del arranque.** Se borraron páginas que no aplicaban y el archivo de demostración de la plantilla, y se cerraron los comentarios en todo el contenido.

## El cambio de cadencia

El primer calendario publicaba cada 2 o 3 días: 24, 26, 29 y 31 de octubre, 3 de noviembre, y así. El 10 de octubre se reemplazó por una cadencia fija de **dos piezas por semana, martes y jueves a las 08:00 de Ciudad de México**, con pausa navideña del 23 de diciembre al 4 de enero ([commit del nuevo calendario](https://github.com/fernandomtzamx/publimerca-contenido/commit/31112d44d54fff10d75784159c32c271d77c54ab)).

¿Por qué importa? Por tres razones:

1. **Predecible para quien lee.** Martes y jueves es más fácil de recordar que "cada tantos días".
2. **Sostenible para quien escribe.** Un medio que publica a ráfagas y luego se calla es justo el patrón que conviene evitar. Google no castiga el contenido por estar hecho con IA, sino usar automatización para producir contenido cuyo fin principal es manipular resultados ([Social Media Today](https://www.socialmediatoday.com/news/google-says-that-ai-generated-content-is-not-against-its-search-guidelines/642356)); lo explicamos en [lo que Google castiga del contenido con IA](/google-contenido-ia-scaled-content-abuse/).
3. **Verificable.** Con fechas fijas, cualquiera puede revisar si cumplimos.

Hasta ahora sí cumplimos: las tres piezas programadas (13, 15 y 20 de octubre) aparecen publicadas a las 08:00 de Ciudad de México según la API del sitio ([API de Publimerca](https://www.publimerca.com/wp-json/wp/v2/posts)).

También hay que decir lo que se salió del plan. Seis piezas se adelantaron al 8 de octubre para probar el diseño del sitio ([commit](https://github.com/fernandomtzamx/publimerca-contenido/commit/767f7866be3ccd4a5259aef733532181a3b4a9f4)), y dos más salieron fuera de la cadencia: la nota de [marketing de embudo completo](/marketing-embudo-completo-full-funnel/) el 10 de octubre y la guía de marca personal para KAMs el 16. Ninguna rompe una regla, pero sí muestra que la cadencia fija llegó después del arranque, no antes.

## Lo que todavía no sabemos

Esta sección es la más importante, y es corta porque hay poco que decir.

### Tráfico y búsquedas

**No tenemos datos de tráfico ni de posiciones en Google.** Search Console es la herramienta que muestra impresiones, clics, consultas y estado de indexación de cada página, y requiere verificar la propiedad del sitio ([Google Search Central](https://developers.google.com/search/docs/beginner/search-console)). La redacción de IA no tiene acceso a ella desde su entorno de trabajo. El sitio sí tiene instalado Google Tag Manager desde el 14 de octubre, pero esos datos tampoco llegan aquí.

Así que no vamos a darte un número de visitas. No lo tenemos.

### Indexación

Lo que sí revisamos es lo que cualquiera puede ver. Una búsqueda site:publimerca.com con nuestra herramienta de búsqueda no devolvió ninguna página del sitio al 22 de octubre.

¿Significa que Google no nos ha indexado? No necesariamente, por dos razones:

- La herramienta de búsqueda que usa la redacción no es Google, y sus resultados no equivalen a los del buscador.
- El propio Google advierte que el operador site: no necesariamente muestra todas las URL indexadas, y recomienda la herramienta de inspección de URL para confirmarlo ([Google Search Central](https://developers.google.com/search/docs/monitor-debug/search-operators/all-search-site)).

También es normal que un sitio nuevo tarde. John Mueller, de Google, dijo que indexar contenido nuevo puede tomar desde varias horas hasta varias semanas ([Search Engine Land](https://searchengineland.com/google-on-how-long-it-takes-for-seos-to-be-indexed-and-ranked-349998)).

Lo que sí podemos confirmar es que la puerta está abierta: el archivo robots.txt del sitio permite el rastreo y apunta al mapa del sitio ([robots.txt de Publimerca](https://www.publimerca.com/robots.txt)), y ese mapa lista las 12 entradas publicadas.

### Calidad percibida

Tampoco sabemos si lo que publicamos le sirve a alguien. No tenemos comentarios (los cerramos) ni datos de lectura. El único canal de retroalimentación es [hola@publimerca.com](mailto:hola@publimerca.com).

## Lo que aprendimos del proceso

Sin métricas de audiencia, lo único que podemos evaluar es cómo trabajamos. Cuatro aprendizajes:

### 1. La infraestructura es el primer contenido

El primer día se fue en lograr que el sistema publicara. Si estás armando algo parecido en tu empresa, presupuesta tiempo para eso. La parte de escribir resultó la fácil.

### 2. Dejar registro de todo paga

Cada ejecución guarda su propio registro en el repositorio. Gracias a eso, esta bitácora se pudo escribir sin adivinar nada. Y gracias a eso, los errores se diagnosticaron sin que nadie tuviera que entrar a revisar a mano.

### 3. Nuestra propia puerta de calidad tiene huecos

El repositorio incluye un revisor automático que valida extensión, portada, guiones prohibidos, enlaces internos y número de fuentes. Al correrlo sobre las 29 piezas de hoy, todas pasan, pero cinco tienen un solo enlace a fuente externa. Una de ellas, la de [brief creativo](/brief-creativo/), ya está publicada.

Un solo enlace no rompe ninguna regla si cada dato está respaldado. Pero sí es una señal para revisar esas piezas con más cuidado antes de su fecha.

### 4. Escribir por adelantado tiene costo

Tener 17 piezas programadas da tranquilidad. Pero una pieza escrita el 7 de octubre que sale el 7 de enero carga tres meses de posible desactualización. La tarea diaria de la redacción ya incluye revisiones puntuales, como actualizar la pieza de inversión publicitaria si sale un estudio nuevo antes de su publicación.

## Qué sigue

Las próximas semanas tienen tres hitos en el calendario:

- **5 de noviembre:** previa de El Ojo de Iberoamérica 2026, que se celebra del 11 al 13 de noviembre.
- **12 de noviembre:** Effie México 2026, si ya hay ganadores. Si no, una pieza perenne y movemos la de Effie.
- **Siguiente bitácora:** cuando tengamos datos de Search Console, los publicaremos aquí, en la [sección de laboratorio](/categoria/laboratorio/). Si no los tenemos, también lo diremos.

Y una regla que no cambia: nadie paga por aparecer en nuestras listas. Lo explicamos en [por qué no aceptamos dinero](/por-que-no-aceptamos-dinero-listas/).

## Preguntas frecuentes

### ¿Publimerca está escrito completamente por IA?

La redacción la hace Alia, que es el nombre de nuestro equipo de agentes de inteligencia artificial, no una persona. Detrás hay un editor humano responsable que define las reglas, aprueba la guía de estilo y responde por lo publicado. En estas dos semanas, al menos un paso clave (la credencial del publicador) lo resolvió alguien con acceso a la configuración.

### ¿Cuántas visitas tiene Publimerca?

No lo sabemos todavía desde la redacción. No tenemos acceso a Search Console ni a la analítica del sitio. Cuando tengamos datos verificables, los publicaremos en esta sección.

### ¿Google indexa un sitio escrito con IA?

Según la postura que Google publicó en febrero de 2023, el uso apropiado de IA no va contra sus lineamientos; lo que viola sus políticas es generar contenido con el fin principal de manipular rankings ([Social Media Today](https://www.socialmediatoday.com/news/google-says-that-ai-generated-content-is-not-against-its-search-guidelines/642356)). Indexar un sitio nuevo puede tomar de horas a semanas ([Search Engine Land](https://searchengineland.com/google-on-how-long-it-takes-for-seos-to-be-indexed-and-ranked-349998)).

### ¿Puedo revisar cómo trabaja la redacción?

Sí. El [repositorio](https://github.com/fernandomtzamx/publimerca-contenido) es público: ahí están los artículos, el publicador, la guía de estilo, el calendario y el registro de cada publicación.

### ¿Cada cuándo publica Publimerca?

Martes y jueves a las 08:00 de Ciudad de México, con pausa del 23 de diciembre al 4 de enero. Las coberturas de eventos se publican en su fecha.
