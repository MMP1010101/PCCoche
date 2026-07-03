"""
core/switches.py
Interruptores por marcha/modo. Dentro de un modo, un boton ENCIENDE y otro
APAGA. Cada modo recuerda su propio estado ON/OFF por separado.
El embrague NO interviene aqui (los botones van sueltos).
"""


class Interruptores:
    def __init__(self, cfg, log):
        self.cfg = cfg
        self.log = log
        self.msg = cfg["mensajes"]
        self.defs = cfg.get("interruptores", {})
        # estado[modo] = True/False   (encendido/apagado)
        self.estado = {}

    def tiene(self, modo):
        """¿Este modo tiene interruptor configurado?"""
        return str(modo) in self.defs

    def _def(self, modo):
        return self.defs.get(str(modo))

    def esta_encendido(self, modo):
        return self.estado.get(str(modo), False)

    def procesar(self, modo, boton_num):
        """
        Recibe un boton recien pulsado y el modo actual.
        Si ese boton es el ON u OFF del modo, cambia el estado y avisa.
        Devuelve True si el boton correspondia a este interruptor.
        """
        d = self._def(modo)
        if not d:
            return False

        clave = str(modo)
        nombre = d.get("nombre", "interruptor")

        if boton_num == d["boton_on"]:
            if self.estado.get(clave, False):
                self.log(self.msg["int_ya_on"].format(nombre=nombre))
            else:
                self.estado[clave] = True
                self.log(self.msg["int_on"].format(nombre=nombre))
            return True

        if boton_num == d["boton_off"]:
            if not self.estado.get(clave, False):
                self.log(self.msg["int_ya_off"].format(nombre=nombre))
            else:
                self.estado[clave] = False
                self.log(self.msg["int_off"].format(nombre=nombre))
            return True

        return False
