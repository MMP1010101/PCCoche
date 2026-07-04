"""
core/buttons.py
Los 4 botones configurables. Cada boton tiene una accion DISTINTA por modalidad:
- tipo "app"   -> abre esa app (reutiliza Launcher, valor = ruta/URL o clave)
- tipo "atajo" -> ejecuta ese atajo del catalogo (reutiliza Atajos, valor = clave)
- tipo "nada"  -> no hace nada
Facil de ampliar: anade mas 'tipo' aqui y en el configurador.

Los numeros de boton son configurables en settings.json > botones.ids
(VERIFICAR con tests/test.py).
"""


class Botones:
    def __init__(self, cfg, log, launcher, atajos):
        self.cfg = cfg
        self.log = log
        self.launcher = launcher
        self.atajos = atajos
        bcfg = cfg.get("botones", {})
        self.ids = set(bcfg.get("ids", []))
        self.acciones = bcfg.get("acciones", {})

    def es_boton_accion(self, n):
        return n in self.ids

    def ejecutar(self, boton_num, modalidad):
        """Ejecuta la accion del boton en la modalidad activa."""
        mapa = self.acciones.get(modalidad, {})
        acc = mapa.get(str(boton_num))
        if not acc:
            return False
        tipo = acc.get("tipo", "nada")
        valor = acc.get("valor", "")

        if tipo == "nada" or not valor:
            self.log(f"(boton {boton_num}: sin accion en modalidad {modalidad})")
            return False

        if tipo == "app":
            # valor puede ser una ruta/URL directa: la abrimos como programa suelto
            self.log(f">> Boton {boton_num}: abriendo app...")
            return self.launcher.abrir_destino(valor)

        if tipo == "atajo":
            self.log(f">> Boton {boton_num}: atajo {valor}")
            return self.atajos.ejecutar(valor)

        self.log(f"(boton {boton_num}: tipo '{tipo}' no soportado aun)")
        return False
