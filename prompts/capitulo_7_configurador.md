=== PROMPT PARA CLAUDE — Capítulo 7: Configurador + listador de apps ===

CONTEXTO: Wheel Deck (Python + G29 + pygame, segundo plano, Windows). Caps 1-6 ok.
Problema del Cap.6: había que meter la ruta del .exe a mano. Este cap lo resuelve.

VISION DEL PRODUCTO: dos ejecutables -> (1) CONFIGURADOR (solo config, no consume)
y (2) PRINCIPAL/runtime (lee G29 en segundo plano, ligero).

LO MONTADO EN ESTE CAP:
1. config.py = configurador de CONSOLA (menu de texto). Elegida consola por ser
   lo mas ligero y lo que mejor encaja con el Cap.8 (manejarlo con el G29).
2. core/app_scanner.py: escanea apps del PC leyendo los .lnk del Menu Inicio
   (usuario + sistema). Resuelve el .exe real con pywin32 si esta; si no, usa el
   .lnk (Windows lo abre igual).
3. Buscar por nombre (parcial, sin mayus/minus) y listar apps detectadas.
4. Asignar app o URL a cada marcha (1-6). Se guarda en settings.json > programas
   con el formato actual { nombre, tipo, destino }.
5. Busqueda pesada SOLO en config, una vez. El runtime (core/launcher.py) solo
   abre lo guardado, sin escanear -> bajo consumo intacto.

NO HECHO (siguientes caps, ya previsto en arquitectura):
- Cap.8: boton del G29 abre el config, PAUSA el runtime (soltar el G29 para no
  pisarse), manejar el config con el volante, y guardar+cerrar volviendo al runtime.
- Cap.9: modalidades por marcha (apps, atajos de teclado, aceptar/rechazar Claude,
  cambiar modelo, etc.).

NOTA WINDOWS: para resolucion fina del .exe -> uv pip install pywin32 (opcional).

ESTADO: ✅ montado y probado (escaneo, busqueda y guardado verificados).
===
