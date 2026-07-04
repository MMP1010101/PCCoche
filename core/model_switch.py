"""
core/model_switch.py
Modalidad CLAUDE: teclea el comando de una marcha (ej "/model claude-opus-4-8")
y pulsa Enter en la ventana que el usuario tenga ENFOCADA. Usa 'keyboard'.

SEGURIDAD: esto solo escribe texto en la ventana activa. El usuario debe tener
la ventana de Claude enfocada al disparar. No hace nada mas.

Instalar:  uv pip install keyboard
"""

import time


class CambiadorModelo:
    def __init__(self, cfg, log):
        self.cfg = cfg
        self.log = log
        self._keyboard = None
        self._disponible = False
        self._cargar()

    def _cargar(self):
        try:
            import keyboard
            self._keyboard = keyboard
            self._disponible = True
        except ImportError:
            self.log("(modalidad Claude off: falta 'keyboard'. uv pip install keyboard)")
        except Exception as e:
            self.log(f"(modalidad Claude off: {e})")

    def disponible(self):
        return self._disponible

    def teclear(self, comando, nombre=""):
        """Escribe 'comando' y pulsa Enter en la ventana enfocada."""
        comando = (comando or "").strip()
        if not comando:
            self.log(f"({nombre or 'esta marcha'}: sin comando definido)")
            return False
        if not self._disponible:
            self.log(f"(no puedo teclear {nombre}: falta 'keyboard')")
            return False
        try:
            etq = nombre or comando
            self.log(f">> Claude: {etq}  (tecleando '{comando}')")
            # pequena pausa para asegurar que la ventana recibe el foco del texto
            time.sleep(0.05)
            self._keyboard.write(comando, delay=0.01)
            time.sleep(0.05)
            self._keyboard.press_and_release("enter")
            return True
        except Exception as e:
            self.log(f"(fallo al teclear {nombre}: {e})")
            return False
