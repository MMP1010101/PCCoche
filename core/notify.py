"""
core/notify.py
Notificaciones toast de Windows al cambiar de marcha.
Usa winotify (ligera, Win10/11). Si no esta instalada o falla, NO rompe el
programa: simplemente no muestra toast y sigue el feedback por terminal.

Instalar:  uv pip install winotify
"""


class Notificador:
    def __init__(self, cfg, log):
        self.cfg = cfg
        self.log = log
        ncfg = cfg.get("notificaciones", {})
        self.activas = ncfg.get("activas", True)
        self.duracion = ncfg.get("duracion", 2)
        self.titulo = ncfg.get("titulo", "WHEEL DECK")
        self.app_id = ncfg.get("app_id", "Wheel Deck")

        self._Notification = None
        self._audio = None
        self._disponible = False

        if self.activas:
            self._intentar_cargar()

    def _intentar_cargar(self):
        try:
            from winotify import Notification, audio
            self._Notification = Notification
            self._audio = audio
            self._disponible = True
        except ImportError:
            self.log("(winotify no instalado: sin toast. uv pip install winotify)")
            self._disponible = False
        except Exception as e:
            self.log(f"(notificaciones off: {e})")
            self._disponible = False

    def cambio_marcha(self, nombre_modo):
        """Muestra un toast con SOLO el nombre del modo (ej: 'Apex')."""
        if not (self.activas and self._disponible):
            return
        try:
            # duration acepta 'short' (~5s) o 'long'. winotify no da segundos
            # exactos; 'short' es lo mas parecido a los 2s deseados. El "tag"
            # con el mismo valor hace que un toast nuevo reemplace al anterior
            # en vez de apilarse.
            toast = self._Notification(
                app_id=self.app_id,
                title=self.titulo,
                msg=nombre_modo,
                duration="short",
            )
            # Reemplazo del anterior: mismo tag/group -> Windows lo sustituye.
            try:
                toast.tag = "wheel-deck-modo"
                toast.group = "wheel-deck"
            except Exception:
                pass
            toast.show()
        except Exception as e:
            self.log(f"(fallo toast: {e})")
