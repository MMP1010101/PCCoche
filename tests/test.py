"""
========================================
  G29 TESTER  ·  PixelWorks / Emperador
========================================
Descubre qué número tiene cada boton y eje de TU Logitech G29.

QUE HACE:
  - Muestra en tiempo real: volante, pedales (acelerador/freno/embrague),
    todos los botones y los paddles.
  - Corre en segundo plano: puedes minimizar la consola, sigue leyendo.
  - APAGADO: pulsa el boton que uses como "marcha atras" (R) y se cierra
    con un mensaje.

COMO USARLO:
  1) Instala Python 3 (python.org) y marca "Add to PATH".
  2) En la terminal:  pip install pygame
  3) Conecta el G29, ejecuta:  python g29_tester.py
  4) Mueve TODO y apunta los numeros que van saliendo.

IMPORTANTE (pedales del G29):
  En reposo un pedal marca ~+1.0 y pisado ~-1.0 (van al reves).
  Aqui lo normalizo a 0.0 (suelto) .. 1.0 (a fondo) para que se lea facil.
"""

import sys
import time

try:
    import pygame
except ImportError:
    print("Falta pygame. Instalalo con:  pip install pygame")
    sys.exit(1)

# ---------------------------------------------------------------
# CONFIG: cambia esto cuando sepas que boton usas como marcha atras
# Con el tester puesto, mira que numero sale al pulsar tu boton "R"
# y ponlo aqui. De momento -1 = desactivado (no apaga por boton).
BOTON_APAGADO = -1     # ej: 5  (el numero que veas para tu boton R)
# ---------------------------------------------------------------


def normaliza_pedal(valor_bruto):
    """G29: reposo +1.0, a fondo -1.0  ->  devuelve 0.0 .. 1.0"""
    return round((1.0 - valor_bruto) / 2.0, 2)


def main():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No veo ningun mando. Conecta el G29 y vuelve a ejecutar.")
        print("(Comprueba tambien que Logitech G HUB no lo tenga bloqueado)")
        sys.exit(1)

    js = pygame.joystick.Joystick(0)
    js.init()

    print("=" * 50)
    print("  G29 DETECTADO:", js.get_name())
    print("  Ejes:", js.get_numaxes(), " | Botones:", js.get_numbuttons(),
          " | Hats:", js.get_numhats())
    print("=" * 50)
    print("Mueve el volante, pisa pedales y pulsa botones.")
    print("Apunta los numeros. Ctrl+C para salir.")
    if BOTON_APAGADO >= 0:
        print(f"Apagado configurado en boton {BOTON_APAGADO} (marcha R).")
    print("-" * 50)

    reloj = pygame.time.Clock()

    # Para pedales: guardamos el ultimo eje "conocido" y detectamos cual es cual.
    # En el G29 tipico:  eje 0 = volante, 1 = acelerador, 2 = freno, 3 = embrague.
    # Pero varia, por eso el tester te ensena TODOS los ejes.

    try:
        while True:
            pygame.event.pump()  # refresca el estado del mando (no necesita foco)

            # --- VOLANTE Y PEDALES (ejes) ---
            ejes = [round(js.get_axis(i), 2) for i in range(js.get_numaxes())]

            # --- BOTONES pulsados ahora mismo ---
            pulsados = [i for i in range(js.get_numbuttons()) if js.get_button(i)]

            # --- HAT / cruceta (si tiene) ---
            hats = [js.get_hat(i) for i in range(js.get_numhats())]

            # Linea de estado en vivo (se reescribe sola)
            estado = f"EJES {ejes}  |  BOTONES {pulsados}"
            if hats:
                estado += f"  |  HAT {hats}"
            print(estado.ljust(90), end="\r")

            # --- APAGADO por boton R ---
            if BOTON_APAGADO >= 0 and js.get_button(BOTON_APAGADO):
                print("\n" + "=" * 50)
                print("  MARCHA ATRAS · APAGANDO WHEEL DECK")
                print("  Nos vemos, Emperador. 🏁")
                print("=" * 50)
                break

            reloj.tick(30)  # 30 lecturas por segundo, suave y ligero

    except KeyboardInterrupt:
        print("\nSaliendo (Ctrl+C).")
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
