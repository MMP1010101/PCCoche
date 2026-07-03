"""
========================================
  WHEEL DECK · config_gui.py
  Configurador VISUAL (pizarra) · Cap.7b
========================================
Pizarra con 6 huecos (una por marcha) y una lista de apps del PC con iconos.
Arrastra una app de la lista y sueltala en el hueco de la marcha -> asignada y
guardada en config/settings.json.

SOLO configuracion: no lanza apps, no toca el G29, no corre en segundo plano.

Requiere:  uv pip install customtkinter pillow      (pywin32 ya instalado)

USO:  uv run config_gui.py   (o:  python config_gui.py)
"""

import os
import sys
import json

# --- Dependencias con aviso claro si faltan ---
try:
    import customtkinter as ctk
except ImportError:
    print("Falta customtkinter. Instala con:  uv pip install customtkinter pillow")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("Falta Pillow. Instala con:  uv pip install pillow")
    sys.exit(1)

from core.app_scanner import escanear_apps, buscar
from core.icon_extractor import extraer_icono


RUTA_CONFIG = os.path.join(os.path.dirname(__file__), "config", "settings.json")

# Colores del gradiente por marcha (los del proyecto)
COLOR_MARCHA = {
    1: "#4ade80", 2: "#a3e635", 3: "#facc15",
    4: "#fb923c", 5: "#f87171", 6: "#ef4444",
}

# Paleta "cabina" oscura
BG        = "#0e0f13"
PANEL     = "#16181e"
PANEL_2   = "#1d2028"
TXT       = "#e8eaed"
TXT_DIM   = "#8b909c"
PLACE     = "#2a2e38"


def cargar():
    with open(RUTA_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar(cfg):
    with open(RUTA_CONFIG, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


class Pizarra(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.cfg = cargar()
        self.title("Wheel Deck · Pizarra de marchas")
        self.geometry("980x640")
        self.configure(fg_color=BG)
        ctk.set_appearance_mode("dark")

        self._img_cache = {}      # ruta_png -> CTkImage
        self._arrastrando = None  # app en curso de arrastre
        self._fantasma = None     # etiqueta flotante durante el arrastre

        self._construir()
        self._cargar_apps()

    # ---------- UI ----------
    def _construir(self):
        cont = ctk.CTkFrame(self, fg_color=BG)
        cont.pack(fill="both", expand=True, padx=18, pady=18)

        # Cabecera
        head = ctk.CTkFrame(cont, fg_color=BG)
        head.pack(fill="x", pady=(0, 14))
        ctk.CTkLabel(head, text="PIZARRA DE MARCHAS",
                     font=("Segoe UI Black", 26, "bold"),
                     text_color=TXT).pack(side="left")
        ctk.CTkLabel(head, text="  arrastra una app a su marcha",
                     font=("Segoe UI", 13), text_color=TXT_DIM).pack(
            side="left", padx=(10, 0), pady=(8, 0))

        cuerpo = ctk.CTkFrame(cont, fg_color=BG)
        cuerpo.pack(fill="both", expand=True)

        # Panel izquierdo: lista/buscador de apps
        izq = ctk.CTkFrame(cuerpo, fg_color=PANEL, corner_radius=16, width=320)
        izq.pack(side="left", fill="y", padx=(0, 16))
        izq.pack_propagate(False)

        ctk.CTkLabel(izq, text="Apps del PC", font=("Segoe UI", 15, "bold"),
                     text_color=TXT).pack(anchor="w", padx=16, pady=(16, 8))

        self.buscador = ctk.CTkEntry(izq, placeholder_text="Buscar app...",
                                     height=38, corner_radius=10,
                                     fg_color=PANEL_2, border_width=0)
        self.buscador.pack(fill="x", padx=16)
        self.buscador.bind("<KeyRelease>", lambda e: self._filtrar())

        self.lista = ctk.CTkScrollableFrame(izq, fg_color=PANEL,
                                            corner_radius=0)
        self.lista.pack(fill="both", expand=True, padx=8, pady=12)

        # Boton anadir web
        ctk.CTkButton(izq, text="+ Anadir web (URL)", height=40,
                      corner_radius=10, fg_color=PANEL_2, hover_color=PLACE,
                      text_color=TXT, command=self._dialogo_web).pack(
            fill="x", padx=16, pady=(0, 16))

        # Panel derecho: los 6 huecos
        der = ctk.CTkFrame(cuerpo, fg_color=BG)
        der.pack(side="left", fill="both", expand=True)

        self.huecos = {}
        for modo in range(1, 7):
            self._crear_hueco(der, modo)

    def _crear_hueco(self, parent, modo):
        fila = modo - 1
        col = 0
        # rejilla 2 columnas x 3 filas
        r, c = divmod(fila, 2)
        color = COLOR_MARCHA[modo]

        card = ctk.CTkFrame(parent, fg_color=PANEL, corner_radius=16)
        card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
        parent.grid_columnconfigure(c, weight=1)
        parent.grid_rowconfigure(r, weight=1)

        # Barra de color de la marcha
        barra = ctk.CTkFrame(card, fg_color=color, corner_radius=8, height=6)
        barra.pack(fill="x", padx=14, pady=(14, 8))

        cab = ctk.CTkFrame(card, fg_color=PANEL)
        cab.pack(fill="x", padx=14)
        ctk.CTkLabel(cab, text=f"MARCHA {modo}", font=("Segoe UI", 12, "bold"),
                     text_color=color).pack(side="left")
        ctk.CTkButton(cab, text="✕", width=26, height=26, corner_radius=8,
                      fg_color=PANEL_2, hover_color="#3a2020", text_color=TXT_DIM,
                      command=lambda m=modo: self._vaciar(m)).pack(side="right")

        # Zona de destino (donde se suelta)
        zona = ctk.CTkFrame(card, fg_color=PANEL_2, corner_radius=12,
                            height=90)
        zona.pack(fill="both", expand=True, padx=14, pady=14)
        zona.pack_propagate(False)

        icono = ctk.CTkLabel(zona, text="", width=48)
        icono.pack(side="left", padx=12)
        texto = ctk.CTkLabel(zona, text="vacio", font=("Segoe UI", 14),
                             text_color=TXT_DIM, anchor="w", justify="left")
        texto.pack(side="left", fill="x", expand=True)

        self.huecos[modo] = {"zona": zona, "icono": icono, "texto": texto,
                             "color": color, "card": card}
        self._refrescar_hueco(modo)

    # ---------- Datos / apps ----------
    def _ctk_img(self, ruta_png, tam=40):
        if not ruta_png:
            return None
        if ruta_png in self._img_cache:
            return self._img_cache[ruta_png]
        try:
            im = Image.open(ruta_png)
            cim = ctk.CTkImage(light_image=im, dark_image=im, size=(tam, tam))
            self._img_cache[ruta_png] = cim
            return cim
        except Exception:
            return None

    def _cargar_apps(self):
        self.apps = escanear_apps()
        self._render_lista(self.apps)

    def _filtrar(self):
        t = self.buscador.get()
        self._render_lista(buscar(self.apps, t) if t.strip() else self.apps)

    def _render_lista(self, apps):
        for w in self.lista.winfo_children():
            w.destroy()
        for app in apps[:80]:
            self._fila_app(app)

    def _fila_app(self, app):
        fila = ctk.CTkFrame(self.lista, fg_color=PANEL_2, corner_radius=10)
        fila.pack(fill="x", pady=4, padx=4)

        png = extraer_icono(app["destino"])
        cim = self._ctk_img(png, 28)
        ic = ctk.CTkLabel(fila, text="" if cim else "▦", image=cim,
                          width=32, text_color=TXT_DIM)
        ic.pack(side="left", padx=(10, 8), pady=8)
        lbl = ctk.CTkLabel(fila, text=app["nombre"], font=("Segoe UI", 13),
                           text_color=TXT, anchor="w")
        lbl.pack(side="left", fill="x", expand=True)

        # Arrastre manual: guardo la app y muevo un fantasma
        for w in (fila, ic, lbl):
            w.bind("<Button-1>", lambda e, a=app: self._empezar_arrastre(a, e))
            w.bind("<B1-Motion>", self._mover_arrastre)
            w.bind("<ButtonRelease-1>", self._soltar_arrastre)

    # ---------- Drag & drop manual ----------
    def _empezar_arrastre(self, app, e):
        self._arrastrando = app
        if self._fantasma:
            self._fantasma.destroy()
        self._fantasma = ctk.CTkLabel(self, text=f"  {app['nombre']}  ",
                                      font=("Segoe UI", 12, "bold"),
                                      fg_color=PANEL_2, text_color=TXT,
                                      corner_radius=8)
        self._fantasma.place(x=e.x_root - self.winfo_rootx(),
                             y=e.y_root - self.winfo_rooty())

    def _mover_arrastre(self, e):
        if self._fantasma:
            self._fantasma.place(x=e.x_root - self.winfo_rootx() + 8,
                                 y=e.y_root - self.winfo_rooty() + 8)

    def _soltar_arrastre(self, e):
        if self._fantasma:
            self._fantasma.destroy()
            self._fantasma = None
        if not self._arrastrando:
            return
        modo = self._hueco_bajo_cursor(e.x_root, e.y_root)
        if modo:
            self._asignar(modo, self._arrastrando)
        self._arrastrando = None

    def _hueco_bajo_cursor(self, xr, yr):
        for modo, h in self.huecos.items():
            z = h["zona"]
            x0 = z.winfo_rootx(); y0 = z.winfo_rooty()
            x1 = x0 + z.winfo_width(); y1 = y0 + z.winfo_height()
            if x0 <= xr <= x1 and y0 <= yr <= y1:
                return modo
        return None

    # ---------- Asignar / vaciar / guardar ----------
    def _asignar(self, modo, app):
        self.cfg.setdefault("programas", {})[str(modo)] = {
            "nombre": app["nombre"],
            "tipo": "app",
            "destino": app["destino"],
        }
        guardar(self.cfg)
        self._refrescar_hueco(modo)

    def _vaciar(self, modo):
        progs = self.cfg.setdefault("programas", {})
        if str(modo) in progs:
            progs[str(modo)]["destino"] = ""
            guardar(self.cfg)
        self._refrescar_hueco(modo)

    def _refrescar_hueco(self, modo):
        h = self.huecos[modo]
        prog = self.cfg.get("programas", {}).get(str(modo), {})
        destino = prog.get("destino", "")
        nombre = prog.get("nombre", "")
        if destino:
            png = extraer_icono(destino) if prog.get("tipo") == "app" else None
            cim = self._ctk_img(png, 40)
            h["icono"].configure(image=cim, text="" if cim else "▦")
            tipo_txt = "web" if prog.get("tipo") == "url" else "app"
            h["texto"].configure(text=f"{nombre}\n{tipo_txt}", text_color=TXT)
        else:
            h["icono"].configure(image=None, text="")
            h["texto"].configure(text="vacio  ·  arrastra una app aqui",
                                 text_color=TXT_DIM)

    def _dialogo_web(self):
        dlg = ctk.CTkToplevel(self)
        dlg.title("Anadir web")
        dlg.geometry("360x260")
        dlg.configure(fg_color=PANEL)
        dlg.transient(self)
        dlg.grab_set()

        ctk.CTkLabel(dlg, text="Anadir una web a una marcha",
                     font=("Segoe UI", 15, "bold"), text_color=TXT).pack(
            pady=(18, 12))
        m = ctk.CTkEntry(dlg, placeholder_text="Marcha (1-6)", height=36)
        m.pack(fill="x", padx=20, pady=6)
        n = ctk.CTkEntry(dlg, placeholder_text="Nombre (ej: Claude)", height=36)
        n.pack(fill="x", padx=20, pady=6)
        u = ctk.CTkEntry(dlg, placeholder_text="URL (https://...)", height=36)
        u.pack(fill="x", padx=20, pady=6)

        def ok():
            if not m.get().isdigit() or not (1 <= int(m.get()) <= 6):
                return
            url = u.get().strip()
            if not url:
                return
            modo = int(m.get())
            self.cfg.setdefault("programas", {})[str(modo)] = {
                "nombre": n.get().strip() or f"Modo {modo}",
                "tipo": "url", "destino": url,
            }
            guardar(self.cfg)
            self._refrescar_hueco(modo)
            dlg.destroy()

        ctk.CTkButton(dlg, text="Guardar", height=40, command=ok).pack(
            fill="x", padx=20, pady=(14, 0))


if __name__ == "__main__":
    app = Pizarra()
    app.mainloop()
