"""
core/modalities.py
Sistema de DOS NIVELES:
- NIVEL 1 MODALIDAD (levas 4/5): apps, atajos, ... -> ciclico.
- NIVEL 2 PRESET (botones de cara 0-3 = X cuadrado circulo triangulo): dentro de
  una modalidad, cada boton de cara es una sub-config distinta de las 6 marchas.

Cada modalidad guarda sus 4 presets en cfg['modalidades'][modalidad]['presets'],
con claves "0".."3" (id del boton de cara). El preset activo se recuerda POR
modalidad, asi al cambiar de modalidad cada una mantiene su ultimo preset.
"""


class GestorModalidades:
    def __init__(self, cfg, log):
        self.cfg = cfg
        self.log = log
        mods = cfg.get("modalidades", {})
        self.orden = mods.get("orden", ["apps"])
        self.defs = mods
        self.idx = 0

        por_defecto = cfg.get("botones_cara", {}).get("preset_por_defecto", "3")
        self._preset_activo = {m: por_defecto for m in self.orden}

    # ---------- Modalidad (nivel 1) ----------
    @property
    def actual(self):
        return self.orden[self.idx]

    @property
    def nombre_actual(self):
        d = self.defs.get(self.actual, {})
        return d.get("nombre", self.actual.upper())

    def siguiente(self):
        self.idx = (self.idx + 1) % len(self.orden)
        return self.actual

    def anterior(self):
        self.idx = (self.idx - 1) % len(self.orden)
        return self.actual

    def config_de(self, clave=None):
        return self.defs.get(clave or self.actual, {})

    # ---------- Preset (nivel 2) ----------
    def preset_activo(self, modalidad=None):
        modalidad = modalidad or self.actual
        return self._preset_activo.get(modalidad, "3")

    def _presets_de(self, modalidad=None):
        return self.config_de(modalidad).get("presets", {})

    def cambiar_preset(self, boton_id):
        bid = str(boton_id)
        presets = self._presets_de()
        if bid not in presets:
            return None
        self._preset_activo[self.actual] = bid
        return presets[bid]

    def preset_info(self, boton_id=None, modalidad=None):
        bid = str(boton_id) if boton_id is not None else self.preset_activo(modalidad)
        return self._presets_de(modalidad).get(bid, {})

    def marchas_preset_activo(self, modalidad=None):
        modalidad = modalidad or self.actual
        info = self.preset_info(self.preset_activo(modalidad), modalidad)
        return info.get("marchas", {})

    def etiqueta_preset(self, boton_id=None, modalidad=None):
        info = self.preset_info(boton_id, modalidad)
        sim = info.get("simbolo", "")
        nom = info.get("nombre", "")
        return f"{sim} {nom}".strip()

    # ---------- Titulo dinamico de marcha (Cap.8b) leyendo del preset ----------
    def titulo_marcha(self, modo):
        marchas = self.marchas_preset_activo()
        if self.actual == "atajos":
            clave = marchas.get(str(modo), "")
            cat = self.cfg.get("catalogo_atajos", {}).get(clave, {})
            if clave and cat:
                return f"{modo} \u00b7 {cat.get('nombre', clave)}"
            return f"{modo} \u00b7 (sin atajo)"
        else:
            prog = marchas.get(str(modo), {}) or {}
            destino = prog.get("destino", "")
            nombre = prog.get("nombre", "")
            if destino and nombre:
                return f"{modo} \u00b7 {nombre}"
            return f"{modo} \u00b7 (sin app)"
