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
ACCENT    = "#4ade80"


# Glifo (emoji) por atajo, para que cada uno tenga su icono propio y no herede
# el de una app. Fallback: teclado.
GLIFO_ATAJO = {
    "copiar": "📋", "pegar": "📌", "cortar": "✂", "deshacer": "↩",
    "rehacer": "↪", "seleccionar_todo": "🔲", "guardar": "💾",
    "buscar": "🔍", "captura": "📸", "cambiar_ventana": "🪟",
    "nueva_pestana": "➕", "cerrar_pestana": "✖", "zoom_mas": "🔎",
    "zoom_menos": "🔍", "escritorio": "🖥",
}


def glifo_de_atajo(clave):
    return GLIFO_ATAJO.get(clave, "⌨")


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
        self._ver_todas = False   # modo "ver todas" desactivado por defecto
        self._modo_config = "apps"  # que modalidad estoy configurando
        self._preset_config = self.cfg.get("botones_cara", {}).get(
            "preset_por_defecto", "3")  # que preset estoy editando

        self._construir()
        self._cargar_apps()

    # ---------- Acceso al preset en edicion ----------
    def _marchas_preset(self):
        """Dict de las 6 marchas del preset+modalidad que estoy editando."""
        pr = self.cfg["modalidades"][self._modo_config].get("presets", {})
        return pr.get(self._preset_config, {}).get("marchas", {})

    def _preset_actual_info(self):
        pr = self.cfg["modalidades"][self._modo_config].get("presets", {})
        return pr.get(self._preset_config, {})

    # ---------- Historial ----------
    def _historial(self):
        return self.cfg.get("historial_apps", {}).get("items", [])

    def _limite_historial(self):
        return self.cfg.get("historial_apps", {}).get("limite", 12)

    def _add_historial(self, app):
        """Mete una app asignada al principio del historial, sin duplicados."""
        h = self.cfg.setdefault("historial_apps", {"limite": 12, "items": []})
        items = h.setdefault("items", [])
        # quita duplicado por destino
        items = [x for x in items if x.get("destino") != app.get("destino")]
        items.insert(0, {
            "nombre": app["nombre"],
            "tipo": app.get("tipo", "app"),
            "destino": app["destino"],
        })
        h["items"] = items[:h.get("limite", 12)]

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

        # Selector de modalidad a configurar: Apps / Atajos / Claude
        self.sel_modo = ctk.CTkSegmentedButton(
            head, values=["Apps", "Atajos", "Claude"],
            command=self._cambiar_modo_config,
            font=("Segoe UI", 13, "bold"))
        self.sel_modo.set("Apps")
        self.sel_modo.pack(side="right", pady=(4, 0))

        # Selector de PRESET (los 4 botones de cara ✕ □ ○ △)
        presets_row = ctk.CTkFrame(cont, fg_color=BG)
        presets_row.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(presets_row, text="Preset:", font=("Segoe UI", 13),
                     text_color=TXT_DIM).pack(side="left", padx=(2, 8))
        self._btn_presets = {}
        for bid in ["0", "1", "2", "3"]:
            info = self._preset_info_de(bid)
            b = ctk.CTkButton(
                presets_row, width=90, height=34, corner_radius=10,
                text=f"{info.get('simbolo','?')} {info.get('nombre','')}",
                font=("Segoe UI", 13, "bold"),
                fg_color=PANEL_2, hover_color=PLACE, text_color=TXT,
                command=lambda x=bid: self._cambiar_preset_config(x))
            b.pack(side="left", padx=3)
            self._btn_presets[bid] = b
        # boton para renombrar el preset actual
        ctk.CTkButton(presets_row, text="✎ Renombrar", width=110, height=34,
                      corner_radius=10, fg_color=PANEL, hover_color=PLACE,
                      text_color=TXT_DIM, font=("Segoe UI", 12),
                      command=self._renombrar_preset).pack(side="left", padx=(10, 0))

        cuerpo = ctk.CTkFrame(cont, fg_color=BG)
        cuerpo.pack(fill="both", expand=True)

        # Panel izquierdo: historial + buscador + resultados
        izq = ctk.CTkFrame(cuerpo, fg_color=PANEL, corner_radius=16, width=320)
        izq.pack(side="left", fill="y", padx=(0, 16))
        izq.pack_propagate(False)

        # -- Historial (chips de apps ya asignadas) --
        self.lbl_hist = ctk.CTkLabel(izq, text="Recientes",
                                     font=("Segoe UI", 13, "bold"),
                                     text_color=TXT_DIM)
        self.lbl_hist.pack(anchor="w", padx=16, pady=(16, 6))
        self.cont_hist = ctk.CTkFrame(izq, fg_color=PANEL)
        self.cont_hist.pack(fill="x", padx=12)

        # -- Buscador prominente --
        self.buscador = ctk.CTkEntry(
            izq, placeholder_text="🔍  Escribe el nombre de tu app...",
            height=44, corner_radius=12, fg_color=PANEL_2, border_width=0,
            font=("Segoe UI", 14))
        self.buscador.pack(fill="x", padx=16, pady=(14, 6))
        self.buscador.bind("<KeyRelease>", lambda e: self._filtrar())

        # -- Resultados de busqueda (vacio al inicio) --
        self.lista = ctk.CTkScrollableFrame(izq, fg_color=PANEL, corner_radius=0)
        self.lista.pack(fill="both", expand=True, padx=8, pady=(6, 6))

        # -- Pie: ver todas + anadir web --
        pie = ctk.CTkFrame(izq, fg_color=PANEL)
        pie.pack(fill="x", padx=16, pady=(0, 16))
        self.btn_todas = ctk.CTkButton(
            pie, text="Ver todas", height=34, corner_radius=10,
            fg_color=PANEL_2, hover_color=PLACE, text_color=TXT_DIM,
            font=("Segoe UI", 12), command=self._toggle_todas)
        self.btn_todas.pack(fill="x", pady=(0, 8))
        ctk.CTkButton(pie, text="+ Anadir web (URL)", height=40,
                      corner_radius=10, fg_color=PANEL_2, hover_color=PLACE,
                      text_color=TXT, command=self._dialogo_web).pack(fill="x")

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

    def _cambiar_modo_config(self, valor):
        if valor == "Atajos":
            self._modo_config = "atajos"
        elif valor == "Claude":
            self._modo_config = "claude"
        else:
            self._modo_config = "apps"
        self.buscador.delete(0, "end")
        self._ver_todas = False
        if self._modo_config == "atajos":
            self.buscador.configure(
                placeholder_text="🔍  Busca un atajo (copiar, captura...)")
            self._render_lista(self._catalogo_atajos_lista())
        elif self._modo_config == "claude":
            self.buscador.configure(
                placeholder_text="🤖  Busca un modelo (sonnet, opus, fable...)")
            self._render_lista(self._catalogo_modelos_lista())
        else:
            self.buscador.configure(
                placeholder_text="🔍  Escribe el nombre de tu app...")
            self._render_lista([])
        self._render_historial()
        self._refrescar_botones_preset()
        for m in range(1, 7):
            self._refrescar_hueco(m)

    def _preset_info_de(self, bid):
        pr = self.cfg["modalidades"][self._modo_config].get("presets", {})
        return pr.get(bid, {})

    def _cambiar_preset_config(self, bid):
        self._preset_config = bid
        self._refrescar_botones_preset()
        for m in range(1, 7):
            self._refrescar_hueco(m)

    def _refrescar_botones_preset(self):
        """Actualiza los textos de los 4 botones de preset y resalta el activo."""
        for bid, btn in self._btn_presets.items():
            info = self._preset_info_de(bid)
            btn.configure(text=f"{info.get('simbolo','?')} {info.get('nombre','')}")
            if bid == self._preset_config:
                btn.configure(fg_color=ACCENT, text_color="#0e0f13")
            else:
                btn.configure(fg_color=PANEL_2, text_color=TXT)

    def _renombrar_preset(self):
        dlg = ctk.CTkToplevel(self)
        dlg.title("Renombrar preset")
        dlg.geometry("340x160")
        dlg.configure(fg_color=PANEL)
        dlg.transient(self)
        dlg.grab_set()
        info = self._preset_actual_info()
        ctk.CTkLabel(dlg, text=f"Nuevo nombre para {info.get('simbolo','')}",
                     font=("Segoe UI", 14, "bold"), text_color=TXT).pack(pady=(18, 10))
        e = ctk.CTkEntry(dlg, height=36)
        e.insert(0, info.get("nombre", ""))
        e.pack(fill="x", padx=20)

        def ok():
            nuevo = e.get().strip()
            if nuevo:
                self.cfg["modalidades"][self._modo_config]["presets"][
                    self._preset_config]["nombre"] = nuevo
                guardar(self.cfg)
                self._refrescar_botones_preset()
            dlg.destroy()
        ctk.CTkButton(dlg, text="Guardar", height=38, command=ok).pack(
            fill="x", padx=20, pady=(14, 0))

    def _catalogo_atajos_lista(self):
        cat = self.cfg.get("catalogo_atajos", {})
        out = []
        for clave, item in cat.items():
            if isinstance(item, dict) and "teclas" in item:
                out.append({"nombre": item.get("nombre", clave),
                            "tipo": "atajo", "destino": clave,
                            "teclas": item.get("teclas", "")})
        return sorted(out, key=lambda a: a["nombre"].lower())

    def _buscar_atajos(self, texto):
        t = texto.strip().lower()
        return [a for a in self._catalogo_atajos_lista()
                if t in a["nombre"].lower() or t in a["destino"].lower()]

    def _catalogo_modelos_lista(self):
        cat = self.cfg.get("catalogo_modelos", {})
        out = []
        for clave, item in cat.items():
            if isinstance(item, dict) and "nombre" in item:
                out.append({"nombre": item.get("nombre", clave),
                            "tipo": "modelo", "destino": clave,
                            "comando": item.get("comando", "")})
        return sorted(out, key=lambda a: a["nombre"].lower())

    def _buscar_modelos(self, texto):
        t = texto.strip().lower()
        return [a for a in self._catalogo_modelos_lista()
                if t in a["nombre"].lower() or t in a.get("comando", "").lower()]

    def _cargar_apps(self):
        self.apps = escanear_apps()
        self._render_historial()
        self._render_lista([])  # al inicio, sin listón: solo historial + buscador

    def _filtrar(self):
        t = self.buscador.get()
        if self._modo_config == "atajos":
            self._render_lista(self._buscar_atajos(t) if t.strip()
                               else self._catalogo_atajos_lista())
            return
        if self._modo_config == "claude":
            self._render_lista(self._buscar_modelos(t) if t.strip()
                               else self._catalogo_modelos_lista())
            return
        if t.strip():
            self._ver_todas = False
            self._render_lista(buscar(self.apps, t))
        else:
            self._render_lista(self.apps if self._ver_todas else [])

    def _toggle_todas(self):
        self._ver_todas = not self._ver_todas
        self.btn_todas.configure(text="Ocultar" if self._ver_todas else "Ver todas")
        self._render_lista(self.apps if self._ver_todas else [])

    def _render_historial(self):
        for w in self.cont_hist.winfo_children():
            w.destroy()
        hist = self._historial()
        if not hist:
            self.lbl_hist.configure(text="Recientes  ·  aun no hay, asigna una app")
            return
        self.lbl_hist.configure(text="Recientes")
        # chips en rejilla de 2 columnas
        for i, app in enumerate(hist):
            chip = ctk.CTkFrame(self.cont_hist, fg_color=PANEL_2, corner_radius=10)
            chip.grid(row=i // 2, column=i % 2, padx=4, pady=4, sticky="ew")
            self.cont_hist.grid_columnconfigure(i % 2, weight=1)
            png = extraer_icono(app["destino"]) if app.get("tipo") == "app" else None
            cim = self._ctk_img(png, 22)
            ic = ctk.CTkLabel(chip, text="" if cim else "🌐", image=cim,
                              width=26, text_color=TXT_DIM)
            ic.pack(side="left", padx=(8, 4), pady=6)
            lbl = ctk.CTkLabel(chip, text=app["nombre"][:14], font=("Segoe UI", 12),
                               text_color=TXT, anchor="w")
            lbl.pack(side="left", fill="x", expand=True, padx=(0, 6))
            for w in (chip, ic, lbl):
                w.bind("<Button-1>", lambda e, a=app: self._empezar_arrastre(a, e))
                w.bind("<B1-Motion>", self._mover_arrastre)
                w.bind("<ButtonRelease-1>", self._soltar_arrastre)

    def _render_lista(self, apps):
        for w in self.lista.winfo_children():
            w.destroy()
        for app in apps[:80]:
            self._fila_app(app)

    def _fila_app(self, app):
        fila = ctk.CTkFrame(self.lista, fg_color=PANEL_2, corner_radius=10)
        fila.pack(fill="x", pady=4, padx=4)

        es_atajo = app.get("tipo") == "atajo"
        es_modelo = app.get("tipo") == "modelo"
        if es_atajo:
            ic = ctk.CTkLabel(fila, text=glifo_de_atajo(app.get("destino", "")),
                              width=32, font=("Segoe UI", 18), text_color=TXT_DIM)
            ic.pack(side="left", padx=(10, 8), pady=8)
            texto = f"{app['nombre']}   {app.get('teclas','')}"
            lbl = ctk.CTkLabel(fila, text=texto, font=("Segoe UI", 13),
                               text_color=TXT, anchor="w")
        elif es_modelo:
            ic = ctk.CTkLabel(fila, text="🤖", width=32, font=("Segoe UI", 18),
                              text_color=TXT_DIM)
            ic.pack(side="left", padx=(10, 8), pady=8)
            cmd = app.get("comando", "") or "(sin comando, editalo)"
            lbl = ctk.CTkLabel(fila, text=f"{app['nombre']}   {cmd}",
                               font=("Segoe UI", 13), text_color=TXT, anchor="w")
        else:
            png = extraer_icono(app["destino"])
            cim = self._ctk_img(png, 28)
            ic = ctk.CTkLabel(fila, text="" if cim else "▦", image=cim,
                              width=32, text_color=TXT_DIM)
            ic.pack(side="left", padx=(10, 8), pady=8)
            lbl = ctk.CTkLabel(fila, text=app["nombre"], font=("Segoe UI", 13),
                               text_color=TXT, anchor="w")
        lbl.pack(side="left", fill="x", expand=True)

        # Arrastre manual: guardo la app/atajo y muevo un fantasma
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

    # ---------- Asignar / vaciar / guardar (sobre el PRESET en edicion) ----------
    def _asignar(self, modo, app):
        marchas = self._marchas_preset()
        if self._modo_config == "atajos" or app.get("tipo") == "atajo":
            marchas[str(modo)] = app["destino"]  # clave del catalogo
            guardar(self.cfg)
            self._refrescar_hueco(modo)
            return
        if self._modo_config == "claude" or app.get("tipo") == "modelo":
            marchas[str(modo)] = {
                "nombre": app["nombre"],
                "comando": app.get("comando", ""),
            }
            guardar(self.cfg)
            self._refrescar_hueco(modo)
            return
        entrada = {
            "nombre": app["nombre"],
            "tipo": app.get("tipo", "app"),
            "destino": app["destino"],
        }
        marchas[str(modo)] = entrada
        self._add_historial(entrada)
        guardar(self.cfg)
        self._refrescar_hueco(modo)
        self._render_historial()

    def _vaciar(self, modo):
        marchas = self._marchas_preset()
        if self._modo_config == "atajos":
            marchas[str(modo)] = ""
        elif self._modo_config == "claude":
            marchas[str(modo)] = {"nombre": "", "comando": ""}
        else:
            marchas[str(modo)] = {"nombre": "", "tipo": "app", "destino": ""}
        guardar(self.cfg)
        self._refrescar_hueco(modo)

    def _refrescar_hueco(self, modo):
        h = self.huecos[modo]
        marchas = self._marchas_preset()
        if self._modo_config == "atajos":
            clave = marchas.get(str(modo), "")
            cat = self.cfg.get("catalogo_atajos", {}).get(clave, {})
            # image="" limpia de verdad cualquier icono de app heredado (fix Cap.9)
            h["icono"].configure(image="", text=glifo_de_atajo(clave) if clave else "")
            if clave and cat:
                h["texto"].configure(
                    text=f"{cat.get('nombre', clave)}\n{cat.get('teclas','')}",
                    text_color=TXT)
            else:
                h["texto"].configure(text="vacio  ·  arrastra un atajo aqui",
                                     text_color=TXT_DIM)
            return
        if self._modo_config == "claude":
            m = marchas.get(str(modo), {}) or {}
            nombre = m.get("nombre", "")
            comando = m.get("comando", "")
            h["icono"].configure(image="", text="🤖" if nombre else "")
            if nombre:
                cmd_txt = comando if comando else "(sin comando, editalo)"
                h["texto"].configure(text=f"{nombre}\n{cmd_txt}", text_color=TXT)
            else:
                h["texto"].configure(text="vacio  ·  arrastra un modelo aqui",
                                     text_color=TXT_DIM)
            return
        prog = marchas.get(str(modo), {}) or {}
        destino = prog.get("destino", "")
        nombre = prog.get("nombre", "")
        if destino:
            png = extraer_icono(destino) if prog.get("tipo") == "app" else None
            cim = self._ctk_img(png, 40)
            h["icono"].configure(image=cim if cim else "", text="" if cim else "🌐")
            tipo_txt = "web" if prog.get("tipo") == "url" else "app"
            h["texto"].configure(text=f"{nombre}\n{tipo_txt}", text_color=TXT)
        else:
            h["icono"].configure(image="", text="")
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
            entrada = {
                "nombre": n.get().strip() or f"Modo {modo}",
                "tipo": "url", "destino": url,
            }
            self._marchas_preset()[str(modo)] = entrada
            self._add_historial(entrada)
            guardar(self.cfg)
            self._refrescar_hueco(modo)
            self._render_historial()
            dlg.destroy()

        ctk.CTkButton(dlg, text="Guardar", height=40, command=ok).pack(
            fill="x", padx=20, pady=(14, 0))


if __name__ == "__main__":
    app = Pizarra()
    app.mainloop()
