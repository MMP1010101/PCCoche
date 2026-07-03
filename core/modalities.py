"""
core/modalities.py
Gestor de MODALIDADES (filosofias). Las levas del volante rotan entre ellas de
forma ciclica (del final vuelve al principio). Cada modalidad cambia lo que hacen
las 6 marchas: 'apps' abre programas, 'atajos' ejecuta atajos de teclado, etc.
"""


class GestorModalidades:
    def __init__(self, cfg, log):
        self.cfg = cfg
        self.log = log
        mods = cfg.get("modalidades", {})
        self.orden = mods.get("orden", ["apps"])
        self.defs = mods
        self.idx = 0  # empieza en la primera (apps)

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
