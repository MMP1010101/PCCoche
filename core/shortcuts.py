"""
core/shortcuts.py
Ejecuta atajos de teclado SEGUROS del catalogo. Usa la libreria 'keyboard'.
Solo dispara lo que este en 'catalogo_atajos' de settings.json (nunca atajos
destructivos). Si 'keyboard' no esta instalada, avisa y no rompe el programa.

Instalar:  uv pip install keyboard
Nota: en Windows 'keyboard' puede requerir ejecutar como administrador para
algunos atajos con la tecla Win (ej: captura win+shift+s).
"""


class Atajos:
    def __init__(self, cfg, log):
        self.cfg = cfg
        self.log = log
        self.catalogo = cfg.get("catalogo_atajos", {})
        self._keyboard = None
        self._disponible = False
        self._cargar()

    def _cargar(self):
        try:
            import keyboard
            self._keyboard = keyboard
            self._disponible = True
        except ImportError:
            self.log("(atajos off: falta 'keyboard'. uv pip install keyboard)")
        except Exception as e:
            self.log(f"(atajos off: {e})")

    def disponible(self):
        return self._disponible

    def ejecutar(self, clave_atajo):
        """Dispara el atajo con esa clave del catalogo. Devuelve True si lo hizo."""
        item = self.catalogo.get(clave_atajo)
        if not item:
            self.log(f"(atajo '{clave_atajo}' no esta en el catalogo)")
            return False

        nombre = item.get("nombre", clave_atajo)
        teclas = item.get("teclas", "")
        if not teclas:
            self.log(f"({nombre}: sin teclas definidas)")
            return False

        if not self._disponible:
            self.log(f"(no puedo ejecutar {nombre}: falta 'keyboard')")
            return False

        try:
            self.log(f">> Atajo: {nombre} ({teclas})")
            # send() pulsa la combinacion completa y la suelta.
            self._keyboard.send(teclas)
            return True
        except Exception as e:
            self.log(f"(fallo atajo {nombre}: {e})")
            return False
