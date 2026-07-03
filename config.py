"""
========================================
  WHEEL DECK · config.py  (CONFIGURADOR)
  PixelWorks / Emperador · Capitulo 7
========================================
Herramienta SOLO de configuracion. Escanea las apps del PC, deja buscarlas por
nombre y asignar una a cada marcha (Modo 1-6). Guarda todo en config/settings.json
(seccion "programas"). NO lanza apps, NO corre en segundo plano.

Interfaz: consola (menu de texto). Es lo mas ligero y lo que mejor encaja con el
Cap.8 (manejarlo con el G29). Si se quiere GUI luego, se cambia sin tocar la
logica de busqueda (core/app_scanner.py).

USO:
  uv run config.py     (o:  python config.py)
"""

import os
import json

from core.app_scanner import escanear_apps, buscar


RUTA_CONFIG = os.path.join(os.path.dirname(__file__), "config", "settings.json")


def cargar():
    with open(RUTA_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar(cfg):
    with open(RUTA_CONFIG, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def nombre_marcha(cfg, modo):
    for _, info in cfg["marchas"].items():
        if isinstance(info, dict) and info.get("modo") == modo:
            return info.get("nombre", f"Modo {modo}")
    return f"Modo {modo}"


def mostrar_estado(cfg):
    print("\n=== ASIGNACION ACTUAL POR MARCHA ===")
    programas = cfg.get("programas", {})
    for modo in range(1, 7):
        p = programas.get(str(modo), {})
        nombre = p.get("nombre", nombre_marcha(cfg, modo))
        tipo = p.get("tipo", "-")
        destino = p.get("destino", "") or "(sin asignar)"
        print(f"  Marcha {modo} · {nombre:8} [{tipo}] -> {destino}")
    print("=" * 38)


def asignar_app_a_marcha(cfg, apps):
    modo = pedir_modo()
    if modo is None:
        return
    print("\nEscribe parte del nombre de la app (ej: capcut, code, chrome):")
    texto = input("  buscar> ").strip()
    encontradas = buscar(apps, texto)
    if not encontradas:
        print("  No hay coincidencias. Prueba con otra palabra.")
        return
    print("\n  Coincidencias:")
    for i, a in enumerate(encontradas[:20], 1):
        print(f"    {i}. {a['nombre']}")
    sel = input("  Elige numero (enter para cancelar): ").strip()
    if not sel.isdigit():
        return
    idx = int(sel) - 1
    if not (0 <= idx < len(encontradas[:20])):
        print("  Numero fuera de rango.")
        return
    app = encontradas[idx]
    cfg.setdefault("programas", {})[str(modo)] = {
        "nombre": app["nombre"],
        "tipo": "app",
        "destino": app["destino"],
    }
    guardar(cfg)
    print(f"  ✅ Marcha {modo} -> {app['nombre']}  (guardado)")


def asignar_url_a_marcha(cfg):
    modo = pedir_modo()
    if modo is None:
        return
    nombre = input("  Nombre a mostrar (ej: Claude): ").strip() or f"Modo {modo}"
    url = input("  URL (ej: https://claude.ai): ").strip()
    if not url:
        print("  URL vacia, cancelado.")
        return
    cfg.setdefault("programas", {})[str(modo)] = {
        "nombre": nombre,
        "tipo": "url",
        "destino": url,
    }
    guardar(cfg)
    print(f"  ✅ Marcha {modo} -> {nombre} ({url})  (guardado)")


def pedir_modo():
    sel = input("  ¿Que marcha configuras? (1-6): ").strip()
    if sel.isdigit() and 1 <= int(sel) <= 6:
        return int(sel)
    print("  Marcha invalida.")
    return None


def listar_apps(apps):
    print(f"\n=== {len(apps)} APPS DETECTADAS (primeras 40) ===")
    for a in apps[:40]:
        print(f"  · {a['nombre']}")
    if len(apps) > 40:
        print(f"  ... y {len(apps) - 40} mas. Usa la busqueda por nombre.")
    print("=" * 38)


def menu():
    cfg = cargar()
    print("=" * 46)
    print("  WHEEL DECK · CONFIGURADOR")
    print("=" * 46)
    print("Escaneando apps del PC (esto solo se hace aqui)...")
    apps = escanear_apps()
    print(f"  {len(apps)} apps encontradas.")

    while True:
        mostrar_estado(cfg)
        print("\nOpciones:")
        print("  1) Asignar una APP a una marcha (buscar por nombre)")
        print("  2) Asignar una URL (web) a una marcha")
        print("  3) Listar apps detectadas")
        print("  4) Re-escanear apps")
        print("  0) Guardar y salir")
        op = input("  > ").strip()

        if op == "1":
            asignar_app_a_marcha(cfg, apps)
        elif op == "2":
            asignar_url_a_marcha(cfg)
        elif op == "3":
            listar_apps(apps)
        elif op == "4":
            apps = escanear_apps()
            print(f"  Re-escaneadas: {len(apps)} apps.")
        elif op == "0":
            guardar(cfg)
            print("  ✅ Guardado en settings.json. Hasta luego, Emperador. 🏁")
            break
        else:
            print("  Opcion no valida.")


if __name__ == "__main__":
    menu()
