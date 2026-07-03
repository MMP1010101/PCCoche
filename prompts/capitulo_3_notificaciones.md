=== PROMPT PARA CLAUDE — Capítulo 3: Feedback visual con notificaciones Windows ===

CONTEXTO: Wheel Deck (launcher Python + Logitech G29 + pygame, segundo plano,
Windows). Motor (Cap.1) e interruptores (Cap.2) ya funcionan. Añadimos toast de
Windows al cambiar de marcha.

NÚMEROS DE MI G29:
- Eje 0 mano (ignorar) · Eje 2 acelerador · Eje 3 freno · Eje 4 embrague
- Botones 12-17 marchas · 18 = R (salir) · Botones 0,1 interruptor Modo 1

NOMBRES DE LOS MODOS (gradiente verde->rojo):
- 12 Idle (#4ade80) · 13 Flow (#a3e635) · 14 Drive (#facc15)
- 15 Turbo (#fb923c) · 16 Nitro (#f87171) · 17 Apex (#ef4444)

LO QUE PROBÉ Y CÓMO FUE:
- Todos los inputs funcionan (marchas, embrague, acelerador, freno, interruptores).

LO QUE QUIERO AÑADIR:
1. Al cambiar de marcha, toast de Windows (esquina inf. derecha).
2. Muestra SOLO el nombre del modo (ej: "Apex").
3. Dura ~2s y desaparece sola; un cambio nuevo reemplaza al anterior.
4. Colores por modo en settings.json (gradiente verde->rojo).
5. Nombres y config editables en settings.json.

DECISIÓN DE CLAUDE:
- Librería: winotify (la más ligera para Win10/11). Con manejo de errores para
  que si no está instalada el programa no pete.

ESTADO: ✅ HECHO y probado (simulado).
===
