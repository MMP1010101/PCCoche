"""
core/icon_extractor.py
Extrae el icono real de una app (.exe o .lnk) en Windows y lo cachea como PNG
en config/icon_cache/. Usa pywin32 + Pillow. Si algo falla, devuelve None y el
configurador pondra un placeholder.

Solo se usa en el CONFIGURADOR (nunca en el runtime), asi que su coste no afecta
al consumo del programa principal.
"""

import os
import hashlib


CACHE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "config", "icon_cache",
)


def _clave(ruta):
    return hashlib.md5(ruta.encode("utf-8")).hexdigest()[:16]


def _cache_path(ruta):
    os.makedirs(CACHE_DIR, exist_ok=True)
    return os.path.join(CACHE_DIR, _clave(ruta) + ".png")


def extraer_icono(ruta, tam=48):
    """
    Devuelve la ruta a un PNG del icono de 'ruta' (cacheado), o None si no se pudo.
    Acepta .exe, .lnk o cualquier archivo con icono asociado en Windows.
    """
    if not ruta or not os.path.exists(ruta):
        return None

    destino_png = _cache_path(ruta)
    if os.path.exists(destino_png):
        return destino_png  # ya cacheado

    if os.name != "nt":
        return None  # extraccion de iconos solo en Windows

    try:
        # Si es un .lnk, resolvemos primero el .exe destino
        objetivo = ruta
        if ruta.lower().endswith(".lnk"):
            try:
                import win32com.client
                shell = win32com.client.Dispatch("WScript.Shell")
                tgt = shell.CreateShortcut(ruta).TargetPath
                if tgt and os.path.exists(tgt):
                    objetivo = tgt
            except Exception:
                pass

        import win32ui
        import win32gui
        import win32con
        import win32api
        from PIL import Image

        # Extrae el handle del icono grande
        grandes, pequenos = win32gui.ExtractIconEx(objetivo, 0)
        if not grandes:
            if pequenos:
                win32gui.DestroyIcon(pequenos[0])
            return None
        hicon = grandes[0]
        # liberar los demas
        for h in grandes[1:] + pequenos:
            win32gui.DestroyIcon(h)

        ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_x)
        hdc_mem = hdc.CreateCompatibleDC()
        hdc_mem.SelectObject(hbmp)
        hdc_mem.DrawIcon((0, 0), hicon)
        win32gui.DestroyIcon(hicon)

        bmpinfo = hbmp.GetInfo()
        bmpstr = hbmp.GetBitmapBits(True)
        img = Image.frombuffer(
            "RGBA", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]),
            bmpstr, "raw", "BGRA", 0, 1,
        )
        img = img.resize((tam, tam), Image.LANCZOS)
        img.save(destino_png)
        return destino_png
    except Exception:
        return None
