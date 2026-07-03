# 🏁 WHEEL DECK — Capítulos 1 + 2

Launcher del Logitech G29. App de terminal, segundo plano, consumo mínimo.

## Qué hace ya
- **Marchas = modos**: botón 12→Modo 1, 13→2, 14→3, 15→4, 16→5, 17→6.
- **Marcha atrás (botón 18)** → cierra con mensaje.
- **Embrague = AND** para los pedales: acelerador/freno solo actúan si el
  embrague está pisado (valor < 0.44).
- **Acelerador ≤ -0.72** = SÍ · **Freno ≤ -0.62** = NO.
- **Interruptores por modo (Cap.2)**: dentro de un modo, un botón ENCIENDE y
  otro APAGA. En el Modo 1: botón 0 = ON, botón 1 = OFF (ejemplo de prueba en
  terminal). Cada modo recuerda su propio estado. El embrague NO interviene aquí.

## Cómo ejecutarlo
```bash
cd wheel-deck
uv pip install pygame
uv run main.py
```

## Config sin tocar código  (config/settings.json)
- `interruptores`: añade más modos con su `boton_on` y `boton_off`.
- Ejes, umbrales, marchas y mensajes: todo ahí.

## Estructura
```
wheel-deck/
├── main.py
├── config/settings.json
├── core/
│   ├── wheel.py      lectura del G29
│   ├── modes.py      marchas + embrague AND (pedales)
│   ├── switches.py   interruptores ON/OFF por modo  (Cap.2)
│   └── actions.py    SÍ/NO + huecos futuros
├── modes/  logs/  tests/test.py
```

## Preguntas abiertas (capítulos futuros)
- Botones 2 y 3: sin acción aún.
- Interruptores para los modos 2–6 (ahora solo Modo 1 de ejemplo).
- Qué encienden/apagan de verdad los botones (app, sistema, etc.).
- Volante girando: sin uso aún.
- Overlay en pantalla fuera de la terminal.
