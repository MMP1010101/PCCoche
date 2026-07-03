"""
core/wheel.py
Lectura del Logitech G29 con pygame. No necesita foco de ventana.
Normaliza los pedales y expone un estado simple para el resto del programa.
"""

import sys

try:
    import pygame
except ImportError:
    print("Falta pygame. Instala con:  uv pip install pygame")
    sys.exit(1)


class G29:
    def __init__(self, cfg):
        self.cfg = cfg
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            print("No veo el G29. Conectalo y comprueba que G HUB no lo bloquee.")
            sys.exit(1)

        self.js = pygame.joystick.Joystick(0)
        self.js.init()

        ejes = cfg["g29"]["ejes"]
        self.eje_acelerador = ejes["acelerador"]
        self.eje_freno = ejes["freno"]
        self.eje_embrague = ejes["embrague"]

    @property
    def nombre(self):
        return self.js.get_name()

    def refrescar(self):
        """Refresca el estado del mando. Llamar una vez por frame."""
        pygame.event.pump()

    # --- Pedales (valor crudo: +1.0 reposo, negativo pisado) ---
    def acelerador(self):
        return round(self.js.get_axis(self.eje_acelerador), 2)

    def freno(self):
        return round(self.js.get_axis(self.eje_freno), 2)

    def embrague(self):
        return round(self.js.get_axis(self.eje_embrague), 2)

    # --- Botones ---
    def boton(self, n):
        if 0 <= n < self.js.get_numbuttons():
            return bool(self.js.get_button(n))
        return False

    def botones_pulsados(self):
        return [i for i in range(self.js.get_numbuttons()) if self.js.get_button(i)]

    def cerrar(self):
        pygame.quit()
