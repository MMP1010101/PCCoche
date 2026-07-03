"""
core/app_scanner.py
Escanea las apps instaladas en Windows leyendo los accesos directos (.lnk) del
Menu Inicio (de usuario y de sistema). Devuelve una lista de apps con nombre
amigable y la ruta del .lnk (o del .exe destino si se puede resolver).

Esta busqueda "pesada" se hace SOLO en el configurador, una vez. El runtime no
escanea nada: solo abre lo que quedo guardado en settings.json.

Multiplataforma-friendly: en Linux/Mac devuelve lista vacia o .desktop basicos,
para que el configurador se pueda probar fuera de Windows sin petar.
"""

import os
import glob


# Carpetas tipicas del Menu Inicio en Windows
def _carpetas_menu_inicio():
    carpetas = []
    appdata = os.environ.get("APPDATA", "")
    programdata = os.environ.get("PROGRAMDATA", "")
    if appdata:
        carpetas.append(os.path.join(appdata, "Microsoft", "Windows",
                                     "Start Menu", "Programs"))
    if programdata:
        carpetas.append(os.path.join(programdata, "Microsoft", "Windows",
                                     "Start Menu", "Programs"))
    return [c for c in carpetas if os.path.isdir(c)]


def _resolver_lnk(ruta_lnk):
    """
    Intenta sacar el .exe real al que apunta un .lnk.
    Usa pywin32 si esta; si no, devuelve el propio .lnk (Windows lo sabe abrir).
    """
    try:
        import win32com.client  # parte de pywin32
        shell = win32com.client.Dispatch("WScript.Shell")
        acceso = shell.CreateShortcut(ruta_lnk)
        destino = acceso.TargetPath
        if destino and os.path.exists(destino):
            return destino
    except Exception:
        pass
    return ruta_lnk  # fallback: abrir el propio acceso directo funciona igual


def escanear_apps():
    """
    Devuelve lista de dicts: {"nombre": str, "destino": str}
    ordenada por nombre. En Windows lee los .lnk del Menu Inicio.
    """
    apps = {}
    if os.name == "nt":
        for carpeta in _carpetas_menu_inicio():
            patron = os.path.join(carpeta, "**", "*.lnk")
            for lnk in glob.glob(patron, recursive=True):
                nombre = os.path.splitext(os.path.basename(lnk))[0]
                # Evita duplicados por nombre (usuario + sistema)
                if nombre not in apps:
                    apps[nombre] = _resolver_lnk(lnk)
    else:
        # Linux: intenta leer .desktop basicos (best-effort, para pruebas)
        for base in ["/usr/share/applications",
                     os.path.expanduser("~/.local/share/applications")]:
            if os.path.isdir(base):
                for dsk in glob.glob(os.path.join(base, "*.desktop")):
                    nombre = os.path.splitext(os.path.basename(dsk))[0]
                    apps.setdefault(nombre, dsk)

    return sorted(
        [{"nombre": n, "destino": d} for n, d in apps.items()],
        key=lambda a: a["nombre"].lower(),
    )


def buscar(apps, texto):
    """Busqueda parcial, sin mayus/minus. Devuelve las que contienen 'texto'."""
    t = texto.strip().lower()
    if not t:
        return []
    return [a for a in apps if t in a["nombre"].lower()]
