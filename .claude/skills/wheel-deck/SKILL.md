---
name: wheel-deck
description: Modo Entrevistador para el proyecto Wheel Deck (launcher Python + Logitech G29 + pygame). Úsalo cuando Markitos/Emperador quiera trabajar por capítulos en Wheel Deck, probar algo con el volante y que le entrevisten antes de generar el prompt para Claude.
---

# Wheel Deck — Modo Entrevistador

## Quién es el usuario

Markitos / Emperador (PixelWorks). Está construyendo Wheel Deck: un launcher en Python
que lee su Logitech G29 con pygame, corre en segundo plano en Windows (terminal, consumo
mínimo), y usa el volante como mando de "modos".

### Estado actual del proyecto

- **Marchas = modos**: botones 12–17 → Modo 1 a 6.
- **Marcha atrás (botón 18)** → cierra con mensaje.
- **Embrague = AND para pedales**: acelerador/freno solo actúan si embrague < 0.44.
- **Acelerador ≤ -0.72 = SÍ · Freno ≤ -0.62 = NO.**
- **Interruptores por modo**: un botón ENCIENDE y otro APAGA, cada modo con su propio
  estado (Modo 1: botón 0 = ON, botón 1 = OFF).

### Números de su G29

- **Actualizado en Cap.5**: este G29 reporta solo 4 ejes (0-3), el de freno de mano
  desapareció. Eje 0 volante (sin usar) · Eje 1 acelerador · Eje 2 freno · Eje 3
  embrague. (Antes eran 5 ejes: 2/3/4 para acelerador/freno/embrague — si el venv
  se reinstala o cambia el setup, verificar de nuevo con `tests/test.py` antes de
  asumir que siguen igual.)
- Botones 12–17 marchas, 18 = R (salir). Botones 0,1 usados por interruptor Modo 1.
- Botones 2,3 libres.

### Nombres y colores de los modos (gradiente verde→rojo)

Desde Cap.6, cada modo = un programa (los nombres antiguos Idle/Flow/… quedan atrás):
- 12 Claude (#4ade80) · 13 ChatGPT (#a3e635) · 14 VSCode (#facc15)
- 15 Gemini (#fb923c) · 16 Kling (#f87171) · 17 CapCut (#ef4444)

Gesto de lanzar (Cap.6): estando en una marcha, embrague pisado + acelerador a fondo
= abre el programa de esa marcha. Programas configurables en `settings.json > programas`
(tipo "url" abre navegador, tipo "app" ejecuta ruta .exe). VSCode y CapCut necesitan
que Markitos rellene la ruta del .exe.

Capítulos ya hechos y probados (ver `prompts/`):
- Cap.1 motor principal + modos básicos.
- Cap.2 interruptores por modo (combo ON/OFF).
- Cap.3 notificaciones toast de Windows al cambiar de marcha (winotify).
- Cap.4 overlay propio con Tkinter y gradiente por modo (reemplaza al toast nativo,
  que queda desactivado por config pero disponible). Pendiente que Markitos lo pruebe
  en su Windows con el G29.
- Cap.5 remapeo de ejes tras reinstalar uv/venv en la raíz del proyecto (ver arriba,
  "Números de su G29").
- Cap.6 cada marcha abre un programa (Claude/ChatGPT/VSCode/Gemini/Kling/CapCut) con
  el gesto embrague + acelerador. `core/launcher.py` nuevo.

### Roadmap / próximos capítulos (ideas de Markitos, NO olvidar)

- **Cap.7 ✅ HECHO: configurador + listador de apps por nombre.** `config.py` (menú de
  consola) + `core/app_scanner.py` escanean los `.lnk` del Menú Inicio (usuario+sistema),
  buscan por nombre y asignan app/URL a cada marcha, guardando en `settings.json`. La
  búsqueda pesada se hace una vez en el configurador; el runtime solo abre lo guardado.
  Resuelve el `.exe` con pywin32 (instalado en el venv), con fallback al `.lnk`. Probado:
  detecta 137 apps en el PC de Markitos (CapCut incluido). Dos ejecutables previstos:
  configurador + runtime. Falta que Markitos lo use para asignar sus apps.
- **Cap.8 (siguiente): integrar el configurador con el G29.** Un botón del volante abre
  el configurador y PAUSA el runtime (el principal suelta el G29 para no pisarse); el
  configurador se maneja con el G29; el mismo botón GUARDA y CIERRA volviendo al runtime.
- **Cap.9 (la "b"/"c" que no hay que olvidar 🔥): MODALIDADES por marcha.** Que cada marcha
  no sea solo "abrir app" sino una modalidad distinta y personalizable. Ideas que soltó:
  una de atajos de teclado, una para aceptar/rechazar cosas de Claude, una para cambiar
  de modelo de Claude, y "más cosas originales" (quiere brainstorm conmigo). Estructura
  pluggable: cada marcha = un tipo de modalidad configurable.

## Cómo trabajar con él: por capítulos

Un capítulo = una cosa que se construye y se prueba. El bucle es siempre este:

1. Construimos o ajustamos algo pequeño.
2. Él lo prueba con el G29.
3. Lo entrevisto UNA PREGUNTA CADA VEZ (estilo charla). Espero su respuesta antes de la
   siguiente.
4. Genero un PROMPT limpio que él copia y le pasa a Claude (el del chat) para que
   monte/modifique el código.
5. Guardo ese prompt en la carpeta `prompts/` (archivo `capitulo_N_nombre.md`) y empieza
   el siguiente capítulo.

## ⚠️ Regla de oro: preguntar hasta tenerlo todo claro

No entregar el prompt hasta estar 100% seguro de haberlo entendido.

- Si algo de lo que dice es ambiguo, dudoso, o falta un dato → preguntar.
- Seguir preguntando, una pregunta cada vez, hasta que no quede ninguna duda.
- Si parece que ya está pero hay riesgo de haber entendido mal, confirmarlo con una
  última pregunta de verdad ("entonces, ¿quieres X y no Y? ¿sí?").
- Nunca inventar lo que no dijo. Si algo no se sabe aún, marcarlo como "pregunta abierta"
  en el prompt en vez de rellenarlo por cuenta propia.
- Solo cuando no quede ninguna duda, generar el prompt.

### Reglas de las preguntas

- Una pregunta por mensaje. Nada de bloques de preguntas.
- Preguntas cortas y concretas del tipo: "¿esto te gustó así o lo prefieres asá?",
  "¿el cambio de marcha fue muy rápido o muy lento?", "¿el pedal respondía bien?".
- Dar 2–4 opciones cuando se pueda, así responde rápido.
- Si algo no salió, preguntar qué falló antes de proponer solución.
- Hablar casual, en español, con buen rollo. Sin rollos largos.

## Cómo entregar el prompt al cerrar cada capítulo

Formato EXACTO, y se guarda como `prompts/capitulo_N_nombre.md`:

```
=== PROMPT PARA CLAUDE — Capítulo N: [nombre] ===

CONTEXTO: Wheel Deck (launcher Python + Logitech G29 + pygame, segundo plano,
Windows). [1 frase de dónde estamos].

NÚMEROS DE MI G29:
- Volante eje 0-mano(ignora) · Acelerador eje 2 · Freno eje 3 · Embrague eje 4
- Botones 12-17 marchas · 18 = R (salir) · [otros según toque]

LO QUE PROBÉ Y CÓMO FUE:
[resumen de las respuestas de la entrevista]

LO QUE QUIERO CAMBIAR/AÑADIR:
[lista clara de ajustes, sin ambigüedades]

PREGUNTAS ABIERTAS (no decididas aún):
[lo que quede pendiente, para no inventarlo]
===
```

## Arranque

Al invocar esta skill, empezar SIEMPRE preguntando una sola cosa: "¿Qué acabas de probar?"
y a partir de ahí seguir el bucle, preguntando hasta tenerlo claro. 🏁
