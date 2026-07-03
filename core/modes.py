"""
core/modes.py
Logica de modos (marchas) y del embrague como AND gate.
"""


class GestorModos:
    def __init__(self, cfg):
        self.cfg = cfg
        self.marchas = cfg["marchas"]
        self.embrague_umbral = cfg["g29"]["embrague_and"]["umbral"]
        self.acel_umbral = cfg["g29"]["acelerador_si"]["umbral"]
        self.freno_umbral = cfg["g29"]["freno_no"]["umbral"]

        self.modo_actual = None          # numero de modo activo (1..6) o None
        self.nombre_actual = "sin marcha"

    # --- Embrague como AND: pisado (valor por debajo del umbral) = activo ---
    def embrague_activo(self, valor_embrague):
        return valor_embrague < self.embrague_umbral

    # --- SI / NO por pedales (solo cuentan como pisado hasta el umbral) ---
    def es_si(self, valor_acelerador):
        return valor_acelerador <= self.acel_umbral

    def es_no(self, valor_freno):
        return valor_freno <= self.freno_umbral

    def gesto_lanzar(self, valor_embrague, valor_acelerador):
        """Gesto AND para lanzar: embrague pisado Y acelerador a fondo."""
        return self.embrague_activo(valor_embrague) and self.es_si(valor_acelerador)

    # --- Cambio de marcha ---
    def marcha_pulsada(self, boton_num):
        """Devuelve info de la marcha si ese boton es una marcha, si no None."""
        return self.marchas.get(str(boton_num))

    def cambiar_a(self, info_marcha):
        """Aplica un cambio de modo. Devuelve True si cambio de verdad."""
        modo = info_marcha["modo"]
        if modo == self.modo_actual:
            return False
        self.modo_actual = modo
        self.nombre_actual = info_marcha["nombre"]
        return True

    def es_salida(self, info_marcha):
        return info_marcha["modo"] == "R"
