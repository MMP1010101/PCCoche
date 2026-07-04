"""
========================================
  WHEEL DECK · main.py
  PixelWorks / Emperador · Capitulos 1-8
========================================
Launcher del Logitech G29. App de terminal, segundo plano, consumo minimo.

- Cada marcha (boton 12-17) cambia de MODO (Idle, Flow, Drive, Turbo, Nitro, Apex).
- Al cambiar de marcha salta una notificacion toast de Windows con el nombre.
- Marcha atras (boton 18) cierra el programa.
- EMBRAGUE como AND: acelerador/freno solo actuan si el embrague esta pisado.
- Acelerador a fondo = SI · Freno a fondo = NO.
- Interruptores por modo: un boton ENCIENDE y otro APAGA (Modo 1: bot 0/1).

USO:
  uv pip install pygame winotify keyboard
  uv run main.py     (o:  python main.py)
"""

import json
import os
import time

from core.wheel import G29
from core.modes import GestorModos
from core.actions import Acciones
from core.notify import Notificador
from core.overlay import Overlay
from core.launcher import Launcher
from core.modalities import GestorModalidades
from core.shortcuts import Atajos
from core.model_switch import CambiadorModelo


RUTA_CONFIG = os.path.join(os.path.dirname(__file__), "config", "settings.json")


def cargar_config():
    with open(RUTA_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def log(texto):
    """Feedback limpio en terminal, con hora."""
    print(f"  {texto}")


def main():
    cfg = cargar_config()
    msg = cfg["mensajes"]

    wheel = G29(cfg)
    modos = GestorModos(cfg)
    acciones = Acciones(cfg, log)
    notificador = Notificador(cfg, log)
    overlay = Overlay(cfg, log)
    launcher = Launcher(cfg, log)
    modalidades = GestorModalidades(cfg, log)
    atajos = Atajos(cfg, log)
    cambiador_modelo = CambiadorModelo(cfg, log)
    gesto_activo = cfg.get("gesto_lanzar", {}).get("activo", True)

    botones_cara_ids = set(cfg.get("botones_cara", {}).get("ids", {}).keys())

    levas_cfg = cfg.get("levas", {})
    leva_sig = levas_cfg.get("siguiente", 4)
    leva_ant = levas_cfg.get("anterior", 5)

    print("=" * 46)
    print("  WHEEL DECK  ·  G29:", wheel.nombre)
    print("=" * 46)
    log(msg["arranque"])
    print("-" * 46)

    fps = cfg["g29"]["fps"]
    intervalo = 1.0 / fps

    # Estados previos para edge-detection (solo reaccionar a CAMBIOS).
    marchas_prev = set()
    si_prev = False
    no_prev = False
    lanzar_prev = False  # anti-repeticion del gesto de lanzar

    try:
        while True:
            inicio = time.perf_counter()
            wheel.refrescar()

            # --- 1. BOTONES recien pulsados (edge) ---
            pulsados = set(wheel.botones_pulsados())
            nuevos = pulsados - marchas_prev  # botones recien pulsados
            for b in nuevos:
                # ¿Es una LEVA? -> cambia de modalidad (ciclico) y avisa
                if b == leva_sig or b == leva_ant:
                    if b == leva_sig:
                        modalidades.siguiente()
                    else:
                        modalidades.anterior()
                    etiqueta = f"MODO: {modalidades.nombre_actual}"
                    log(f">> {etiqueta}")
                    overlay.cambio_marcha(etiqueta,
                                          esquina=overlay.esquina_modalidad)
                    continue

                info = modos.marcha_pulsada(b)
                if info:
                    # Es un boton de MARCHA -> cambia de modo o cierra
                    if modos.es_salida(info):
                        log(msg["salida"])
                        overlay.cerrar()
                        wheel.cerrar()
                        return
                    if modos.cambiar_a(info):
                        # Titulo DINAMICO segun modalidad y lo asignado.
                        # El color sigue siendo el de la marcha (gradiente).
                        titulo = modalidades.titulo_marcha(info["modo"])
                        color = info.get("color")
                        log(msg["cambio_modo"].format(nombre=titulo))
                        log(msg["modo_activo"].format(nombre=titulo))
                        notificador.cambio_marcha(titulo)
                        overlay.cambio_marcha(titulo, color=color,
                                              esquina=overlay.esquina_marcha)
                else:
                    # No es marcha ni leva. ¿Es un BOTON DE CARA (preset)?
                    if str(b) in botones_cara_ids:
                        info_preset = modalidades.cambiar_preset(b)
                        if info_preset is not None:
                            etiqueta = modalidades.etiqueta_preset(b)
                            log(f">> PRESET: {etiqueta}")
                            overlay.cambio_marcha(etiqueta,
                                                  esquina=overlay.esquina_modalidad)
            marchas_prev = pulsados

            # --- 2. EMBRAGUE como AND ---
            emb = wheel.embrague()
            and_ok = modos.embrague_activo(emb)

            # --- 3. SI / NO (solo si el embrague esta pisado) ---
            si_ahora = and_ok and modos.es_si(wheel.acelerador())
            no_ahora = and_ok and modos.es_no(wheel.freno())

            if si_ahora and not si_prev:
                acciones.confirmar_si()
            if no_ahora and not no_prev:
                acciones.cancelar_no()

            si_prev = si_ahora
            no_prev = no_ahora

            # --- 4. GESTO DE DISPARO (embrague + acelerador a la vez) ---
            # Segun la MODALIDAD activa: apps -> abre programa; atajos -> teclas.
            disparar_ahora = (
                gesto_activo
                and modos.modo_actual is not None
                and modos.modo_actual != "R"
                and modos.gesto_lanzar(emb, wheel.acelerador())
            )
            if disparar_ahora and not lanzar_prev:
                modal = modalidades.actual
                marchas = modalidades.marchas_preset_activo()
                asignacion = marchas.get(str(modos.modo_actual))
                if modal == "atajos":
                    clave = asignacion or ""
                    if clave:
                        atajos.ejecutar(clave)
                    else:
                        log("(esta marcha no tiene atajo asignado en este preset)")
                elif modal == "claude":
                    m = asignacion or {}
                    comando = m.get("comando", "") if isinstance(m, dict) else ""
                    nombre = m.get("nombre", "") if isinstance(m, dict) else ""
                    if comando:
                        cambiador_modelo.teclear(comando, nombre)
                    else:
                        log("(esta marcha no tiene modelo/comando en este preset)")
                else:
                    prog = asignacion or {}
                    destino = (prog.get("destino") or "").strip() if isinstance(prog, dict) else ""
                    if destino:
                        launcher.abrir_destino(destino)
                    else:
                        log("(esta marcha no tiene app asignada en este preset)")
            lanzar_prev = disparar_ahora

            # --- Dormir hasta el siguiente frame (bajo consumo de CPU) ---
            resto = intervalo - (time.perf_counter() - inicio)
            if resto > 0:
                time.sleep(resto)

    except KeyboardInterrupt:
        log("Cerrado con Ctrl+C.")
        wheel.cerrar()


if __name__ == "__main__":
    main()
