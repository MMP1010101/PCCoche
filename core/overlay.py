"""
core/overlay.py
Lanza la ventana de overlay (core/overlay_window.py) como un PROCESO APARTE,
sin bloquear el bucle de lectura del G29. Cada aviso = un proceso que nace,
muestra la tarjeta 'duracion' segundos y muere. Entre avisos: cero consumo.

Si hay un overlay anterior aun visible al cambiar de marcha, lo mata antes
para que el nuevo lo reemplace (no se apilan).
"""

import os
import sys
import subprocess


class Overlay:
    def __init__(self, cfg, log):
        self.cfg = cfg
        self.log = log
        o = cfg.get("overlay", {})
        self.activo = o.get("activo", True)
        self.duracion = o.get("duracion", 2.0)
        self.esquina = o.get("esquina", "bottom-right")
        self.esquina_marcha = o.get("esquina_marcha", self.esquina)
        self.esquina_modalidad = o.get("esquina_modalidad", "top-right")
        self.margen = o.get("margen", 24)
        self.ancho = o.get("ancho", 320)
        self.alto = o.get("alto", 110)
        self.fade = o.get("fade", True)
        self.color_texto = o.get("color_texto", "#ffffff")

        self.marchas = cfg.get("marchas", {})
        self._proc = None  # proceso del overlay activo

        # Carpeta raiz del proyecto (para lanzar con -m core.overlay_window)
        self._raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def _color_de(self, nombre_modo):
        for _, info in self.marchas.items():
            if not isinstance(info, dict):
                continue  # salta el "_comentario" y cualquier no-dict
            if info.get("nombre") == nombre_modo:
                return info.get("color", "#4ade80")
        return "#4ade80"

    def cambio_marcha(self, nombre_modo, color=None, esquina=None):
        if not self.activo:
            return
        if color is None:
            color = self._color_de(nombre_modo)
        esq = esquina or self.esquina

        # Mata el overlay anterior si sigue vivo (reemplazo, no apilar)
        if self._proc and self._proc.poll() is None:
            try:
                self._proc.terminate()
            except Exception:
                pass

        args = [
            sys.executable, "-m", "core.overlay_window",
            nombre_modo, color, str(self.duracion), esq,
            str(self.margen), str(self.ancho), str(self.alto),
            "1" if self.fade else "0", self.color_texto,
        ]
        try:
            # cwd = raiz para que 'core.overlay_window' se resuelva.
            # Sin ventana de consola extra en Windows.
            flags = 0
            if os.name == "nt":
                flags = subprocess.CREATE_NO_WINDOW
            self._proc = subprocess.Popen(args, cwd=self._raiz, creationflags=flags)
        except Exception as e:
            self.log(f"(overlay no lanzado: {e})")

    def cerrar(self):
        if self._proc and self._proc.poll() is None:
            try:
                self._proc.terminate()
            except Exception:
                pass
