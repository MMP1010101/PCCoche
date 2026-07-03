=== PROMPT PARA CLAUDE — Capítulo 4: Overlay propio con gradiente (Tkinter) ===

CONTEXTO: Wheel Deck (launcher Python + Logitech G29 + pygame, segundo plano,
Windows). Caps 1-3 funcionan. El toast de Windows no deja poner color propio,
asi que montamos una notificacion PROPIA con color.

LO QUE QUIERO:
1. Overlay propio con Tkinter (viene con Python, no instala nada).
2. Ventanita sin bordes, siempre encima, en una esquina, con GRADIENTE por modo
   (color del modo -> negro) y el nombre grande (ej: "Apex").
3. Dura ~2s y se cierra sola, con fade.
4. Bajo consumo: se lanza como proceso APARTE que nace, muestra y muere. Entre
   avisos no hay ventana viva -> cero consumo. No bloquea la lectura del G29.
5. Un cambio nuevo reemplaza el overlay anterior (no se apilan).
6. Todo configurable en settings.json (esquina, tamano, duracion, fade, colores).
7. El toast nativo queda desactivado por config pero disponible.

COLORES (gradiente verde->rojo):
Idle #4ade80 · Flow #a3e635 · Drive #facc15 · Turbo #fb923c · Nitro #f87171 · Apex #ef4444

BUG ARREGLADO: el "_comentario" dentro de "marchas" en el JSON rompia la busqueda
de color; ahora se saltan las claves que no son dict.

ESTADO: ✅ montado. Pendiente que Markitos lo pruebe en su Windows con el G29.
===
