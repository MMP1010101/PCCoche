=== PROMPT PARA CLAUDE — Capítulo 1: Motor principal + modos básicos ===

CONTEXTO: Wheel Deck (launcher Python + Logitech G29 + pygame, segundo plano,
Windows). Proyecto nuevo con uv + Python 3.12. Construimos el motor principal.

NÚMEROS DE MI G29:
- Eje 0: freno de mano (no se mueve, ignorar)
- Eje 2: acelerador → reposo +1.0, a fondo ~ -0.72
- Eje 3: freno      → reposo +1.0, a fondo ~ -0.62
- Eje 4: embrague   → AND, activo si valor < 0.44 (pisado)
- Botones 12–17: marchas → Modos 1–6
- Botón 18: marcha atrás R → cierra el programa
- Botones 0,1,2,3: reservados

LO QUE PROBÉ Y CÓMO FUE:
- test.py funciona perfecto con el G29.
- pygame instalado vía uv. Pedales van de +1.0 (reposo) a negativo (pisado).

LO QUE QUIERO CONSTRUIR:
1. main.py que arranque todo, segundo plano, consumo mínimo.
2. Lectura del G29 a 30fps.
3. Marchas (botón 12–17) cambian de modo.
4. Embrague como AND: acciones de pedal solo si embrague < 0.44.
5. Acelerador -0.72 = SÍ · Freno -0.62 = NO.
6. Feedback limpio en terminal.
7. Marcha atrás (18) cierra con mensaje.
8. Config en settings.json, nada hardcodeado.

ESTADO: ✅ HECHO y probado.
===
