=== PROMPT PARA CLAUDE — Capítulo 6: Cada marcha abre un programa (combo AND) ===

CONTEXTO: Wheel Deck (Python + G29 + pygame, segundo plano, Windows). Caps 1-5 ok.
MODELO GENERAL del proyecto: cada marcha abre un programa.

EJES (verificados Cap.5, 4 ejes):
- Eje 0 volante (sin usar) · Eje 1 acelerador · Eje 2 freno · Eje 3 embrague
- Botones 12-17 marchas · 18 = R (salir) · 0,1 interruptor Modo1 · 2,3 libres

PROGRAMAS POR MARCHA (nombres = programas, colores del gradiente igual):
- Modo1 Claude #4ade80 · Modo2 ChatGPT #a3e635 · Modo3 VSCode #facc15
- Modo4 Gemini #fb923c · Modo5 Kling #f87171 · Modo6 CapCut #ef4444

GESTO DE LANZAR (AND): marcha activa + embrague pisado (<0.44) + acelerador a
fondo (<=-0.72) los dos a la vez = abre el programa. Anti-repeticion: una vez
por gesto (hay que soltar y repetir).

COMO ABRE (decision de Claude, configurable en settings.json > programas):
- tipo "url" (Claude, ChatGPT, Gemini, Kling) -> navegador por defecto.
- tipo "app" (VSCode, CapCut) -> ruta del .exe (Markitos la rellena).
- destino vacio -> avisa y no abre, no pete.

Feedback: "Abriendo {nombre}... 🚀" en terminal.

PENDIENTE / A DECIDIR:
- Rutas .exe de VSCode y CapCut (las pone Markitos en settings.json).
- El gesto de lanzar comparte combo con el "SI" (embrague+acelerador): ahora el
  SI es placeholder y no molesta, pero decidir si se separan.

ESTADO: ✅ montado y probado (simulado). Falta que Markitos ponga rutas y pruebe.
===
