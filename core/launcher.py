"""
core/launcher.py
Abre el programa asignado a cada marcha/modo.
- tipo "url": abre en el navegador por defecto.
- tipo "app": ejecuta la ruta/comando del ejecutable.
Todo viene de settings.json (seccion "programas"), nada hardcodeado.
"""

import os
import sys
import webbrowser
import subprocess


class Launcher:
    def __init__(self, cfg, log):
        self.cfg = cfg
        self.log = log
        self.msg = cfg["mensajes"]
        self.programas = cfg.get("programas", {})

    def _prog_de_modo(self, modo):
        return self.programas.get(str(modo))

    def lanzar(self, modo):
        """Abre el programa del modo dado. Devuelve True si lo intento."""
        prog = self._prog_de_modo(modo)
        if not prog:
            self.log(self.msg["sin_marcha_lanzar"])
            return False

        nombre = prog.get("nombre", f"modo {modo}")
        tipo = prog.get("tipo", "url")
        destino = (prog.get("destino") or "").strip()

        if not destino:
            self.log(self.msg["sin_destino"].format(nombre=nombre))
            return False

        self.log(self.msg["abriendo"].format(nombre=nombre))
        try:
            if tipo == "url":
                webbrowser.open(destino)
            else:
                self._abrir_app(destino)
            return True
        except Exception as e:
            self.log(self.msg["fallo_abrir"].format(nombre=nombre, error=e))
            return False

    def _abrir_app(self, ruta):
        """Ejecuta una app de escritorio segun el SO."""
        if os.name == "nt":
            # Windows: os.startfile respeta asociaciones y no bloquea.
            os.startfile(ruta)  # noqa (solo existe en Windows)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", ruta])
        else:
            subprocess.Popen([ruta])
