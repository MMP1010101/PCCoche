"""
core/overlay_window.py
Ventana de notificacion PROPIA con Tkinter. Se ejecuta como proceso aparte:

    python -m core.overlay_window "Apex" "#ef4444" 2.0 bottom-right 24 320 110 1 #ffffff

Dibuja una tarjeta sin bordes, siempre encima, con un gradiente vertical del
color del modo hacia negro, el nombre del modo grande, y se cierra sola tras
'duracion' segundos (con fade opcional). Tkinter viene con Python: no instala nada.

Se lanza y muere en cada aviso -> entre avisos no consume nada.
"""

import sys
import tkinter as tk


def _hex_a_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _mezcla(c1, c2, t):
    """Interpola entre dos colores RGB. t=0 -> c1, t=1 -> c2."""
    return tuple(round(a + (b - a) * t) for a, b in zip(c1, c2))


def _rgb_a_hex(rgb):
    return "#%02x%02x%02x" % rgb


def mostrar(nombre, color, duracion, esquina, margen, ancho, alto, fade, color_texto):
    root = tk.Tk()
    root.overrideredirect(True)        # sin barra de titulo ni bordes
    root.attributes("-topmost", True)  # siempre encima
    try:
        root.attributes("-alpha", 0.0 if fade else 1.0)
    except tk.TclError:
        pass

    # Posicion segun esquina
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    if "right" in esquina:
        x = sw - ancho - margen
    else:
        x = margen
    if "bottom" in esquina:
        y = sh - alto - margen - 40   # 40px extra por la barra de tareas
    else:
        y = margen
    root.geometry(f"{ancho}x{alto}+{x}+{y}")

    # Gradiente vertical: color del modo -> negro
    canvas = tk.Canvas(root, width=ancho, height=alto, highlightthickness=0, bd=0)
    canvas.pack(fill="both", expand=True)
    c_top = _hex_a_rgb(color)
    c_bot = (18, 18, 18)
    for i in range(alto):
        t = i / max(1, alto - 1)
        canvas.create_line(0, i, ancho, i, fill=_rgb_a_hex(_mezcla(c_top, c_bot, t)))

    # Barra de acento arriba (el color puro del modo)
    canvas.create_rectangle(0, 0, ancho, 5, fill=color, outline=color)

    # Textos
    canvas.create_text(20, alto // 2 - 8, anchor="w", text=nombre,
                       fill=color_texto, font=("Segoe UI", 26, "bold"))
    canvas.create_text(20, alto - 22, anchor="w", text="WHEEL DECK",
                       fill=color_texto, font=("Segoe UI", 9))

    # --- Animacion de aparecer/desaparecer (fade) y auto-cierre ---
    pasos_fade = 12
    dur_ms = int(duracion * 1000)

    def fade_in(paso=0):
        if not fade:
            root.after(dur_ms, fade_out)
            return
        a = min(1.0, paso / pasos_fade)
        try:
            root.attributes("-alpha", a)
        except tk.TclError:
            pass
        if paso < pasos_fade:
            root.after(15, lambda: fade_in(paso + 1))
        else:
            root.after(dur_ms, fade_out)

    def fade_out(paso=0):
        if not fade:
            root.destroy()
            return
        a = max(0.0, 1.0 - paso / pasos_fade)
        try:
            root.attributes("-alpha", a)
        except tk.TclError:
            pass
        if paso < pasos_fade:
            root.after(15, lambda: fade_out(paso + 1))
        else:
            root.destroy()

    root.after(0, fade_in)
    root.mainloop()


if __name__ == "__main__":
    # args: nombre color duracion esquina margen ancho alto fade color_texto
    a = sys.argv[1:]
    mostrar(
        nombre=a[0],
        color=a[1],
        duracion=float(a[2]),
        esquina=a[3],
        margen=int(a[4]),
        ancho=int(a[5]),
        alto=int(a[6]),
        fade=bool(int(a[7])),
        color_texto=a[8],
    )
