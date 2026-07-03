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


def _cargar_filtro():
    """Lee la seccion filtro_apps de settings.json. Si no esta, sin filtro."""
    ruta = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "config", "settings.json",
    )
    try:
        import json
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f).get("filtro_apps", {})
    except Exception:
        return {}


def _permitida(nombre, destino, filtro):
    """Decide si una app pasa el filtro. True = se muestra."""
    n = nombre.lower()
    # Normaliza barras: asi el filtro de rutas funciona con \ (Windows) y / igual
    d = (destino or "").lower().replace("\\", "/")

    # Lista blanca: si el nombre coincide, se salva siempre.
    for ok in filtro.get("permitir_siempre", []):
        if ok.lower() in n:
            return True

    # Extensiones fuera (mira el destino)
    for ext in filtro.get("excluir_ext", []):
        if d.endswith(ext.lower()):
            return False

    # Rutas de sistema fuera (normaliza el patron tambien)
    for r in filtro.get("excluir_rutas", []):
        if r.lower().replace("\\", "/") in d:
            return False

    # Patrones prohibidos en nombre o ruta
    for pat in filtro.get("excluir", []):
        p = pat.lower()
        if p in n or p in d:
            return False

    return True


def escanear_apps(aplicar_filtro=True):
    """
    Devuelve lista de dicts: {"nombre": str, "destino": str}
    ordenada por nombre. En Windows lee los .lnk del Menu Inicio.
    Si aplicar_filtro, oculta desinstaladores, ayudas y utilidades de sistema
    segun la seccion 'filtro_apps' de settings.json (con lista blanca).
    """
    apps = {}
    if os.name == "nt":
        for carpeta in _carpetas_menu_inicio():
            patron = os.path.join(carpeta, "**", "*.lnk")
            for lnk in glob.glob(patron, recursive=True):
                nombre = os.path.splitext(os.path.basename(lnk))[0]
                if nombre not in apps:
                    apps[nombre] = _resolver_lnk(lnk)
    else:
        for base in ["/usr/share/applications",
                     os.path.expanduser("~/.local/share/applications")]:
            if os.path.isdir(base):
                for dsk in glob.glob(os.path.join(base, "*.desktop")):
                    nombre = os.path.splitext(os.path.basename(dsk))[0]
                    apps.setdefault(nombre, dsk)

    lista = [{"nombre": n, "destino": d} for n, d in apps.items()]

    if aplicar_filtro:
        filtro = _cargar_filtro()
        if filtro:
            lista = [a for a in lista
                     if _permitida(a["nombre"], a["destino"], filtro)]

    return sorted(lista, key=lambda a: a["nombre"].lower())


def buscar(apps, texto):
    """Busqueda parcial, sin mayus/minus. Devuelve las que contienen 'texto'."""
    t = texto.strip().lower()
    if not t:
        return []
    return [a for a in apps if t in a["nombre"].lower()]
