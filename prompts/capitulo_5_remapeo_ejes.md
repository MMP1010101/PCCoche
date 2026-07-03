=== PROMPT PARA CLAUDE — Capítulo 5: Remapeo de ejes del G29 (venv reinstalado) ===

CONTEXTO: Wheel Deck (launcher Python + Logitech G29 + pygame, segundo plano,
Windows). Caps 1-4 funcionan (motor, interruptores, notificaciones, overlay). Se
tuvo que reinstalar uv y recrear el venv en la raíz del proyecto (antes vivía,
por error, en una subcarpeta `wheel-deck/` que se borró sin querer junto con un
scaffold vacío). Al volver a correr `main.py` petó con "pygame.error: Invalid
joystick axis" porque el eje del embrague (4) ya no existe.

NÚMEROS DE MI G29 (NUEVOS, verificados con tests/test.py):
- El G29 ahora reporta solo 4 ejes (0-3), antes eran 5. El eje de freno de mano
  desapareció.
- Eje 0: volante (sin usar por ahora)
- Eje 1: acelerador
- Eje 2: freno
- Eje 3: embrague
- Botones 12-17 marchas · 18 = R (salir) · Botones 0,1 interruptor Modo 1 (sin cambios)

LO QUE PROBÉ Y CÓMO FUE:
- tests/test.py detecta el G29 bien: "Ejes: 4 | Botones: 25 | Hats: 1".
- Mapeé cada eje moviendo volante y pedales uno a uno: volante=0, acelerador=1,
  freno=2, embrague=3.
- Ya actualicé `config/settings.json` → `g29.ejes` con estos valores nuevos
  (acelerador:1, freno:2, embrague:3) y un comentario explicando el porqué.
  Es solo dato de config, no debería requerir tocar código.

LO QUE QUIERO CAMBIAR/AÑADIR:
1. Confirmar que `core/wheel.py` no tiene ningún número de eje hardcodeado (todo
   debe salir de `settings.json`, ya lo hacía así en el Cap.1, solo verificar).
2. Confirmar que los umbrales de `acelerador_si` (-0.72), `freno_no` (-0.62) y
   `embrague_and` (0.44) siguen siendo válidos con este remapeo (son valores de
   recorrido del pedal, no dependen del índice del eje, pero verificar por si
   acaso el pedal físico cambió de comportamiento).
3. Si por lo que sea el eje 0 (volante) se llega a leer en algún sitio, que no
   rompa nada — de momento sigue sin usarse.

PREGUNTAS ABIERTAS (no decididas aún):
- Si en el futuro el G29 vuelve a reportar 5 ejes (freno de mano detectado de
  nuevo), habría que re-mapear otra vez. No hay solución automática todavía,
  se sigue confiando en `tests/test.py` para verificar.

ESTADO: ✅ Config actualizada y aplicada. Pendiente confirmar en Claude que
core/wheel.py no necesita cambios de código, solo iba a datos de settings.json.
===
