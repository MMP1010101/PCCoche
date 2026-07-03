=== PROMPT PARA CLAUDE — Capítulo 2: Interruptores por modo (combo ON/OFF) ===

CONTEXTO: Wheel Deck (launcher Python + Logitech G29 + pygame, segundo plano,
Windows). El motor del Cap.1 ya funciona. Añadimos combos por marcha.

NÚMEROS DE MI G29:
- Acelerador eje 2 · Freno eje 3 · Embrague eje 4 · Eje 0 mano (ignorar)
- Botones 12–17 marchas · 18 = R (salir)
- Botón 0 = ON · Botón 1 = OFF (interruptor del Modo 1) · Botones 2,3 libres

LO QUE PROBÉ Y CÓMO FUE:
- Cap.1 funciona: marchas cambian de modo, embrague AND, SÍ/NO, salida por R.

LO QUE QUIERO AÑADIR:
1. Combo POR MARCHA: dentro de un modo, un botón ENCIENDE y otro APAGA.
2. En el Modo 1: botón 0 = ON, botón 1 = OFF, ejemplo de prueba que escribe el
   estado en terminal.
3. Cada modo recuerda su propio estado ON/OFF por separado.
4. El embrague NO interviene en los botones (van sueltos).
5. Todo configurable en settings.json (sección "interruptores").

PREGUNTAS ABIERTAS (no decididas aún):
- Qué encienden/apagan de verdad los botones (app, sistema, etc.).
- Interruptores para los modos 2–6.
- Botones 2 y 3.
- Volante girando.
- Overlay en pantalla fuera de la terminal.

ESTADO: ✅ HECHO y probado.
===
