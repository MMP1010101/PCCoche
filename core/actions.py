"""
core/actions.py
Acciones que dispara el Wheel Deck. De momento solo SI/NO por pedales.
Los botones 0,1,2,3 quedan como preguntas abiertas (capitulos futuros).
"""


class Acciones:
    def __init__(self, cfg, log):
        self.cfg = cfg
        self.log = log
        self.msg = cfg["mensajes"]

    def confirmar_si(self):
        """Acelerador a fondo con embrague pisado."""
        self.log(self.msg["si"])
        # TODO (capitulo futuro): aqui va lo que hace el SI segun el modo activo.

    def cancelar_no(self):
        """Freno a fondo con embrague pisado."""
        self.log(self.msg["no"])
        # TODO (capitulo futuro): aqui va lo que hace el NO segun el modo activo.

    def boton_libre(self, n, modo_actual):
        """Botones 0,1,2,3: reservados. De momento solo avisan."""
        self.log(f"(boton {n} libre - sin accion aun, modo {modo_actual})")
        # TODO (capitulo futuro): accion por boton dependiente del modo.
