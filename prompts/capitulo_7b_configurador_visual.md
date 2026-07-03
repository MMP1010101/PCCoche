=== PROMPT PARA CLAUDE — Capítulo 7b: Configurador VISUAL (pizarra drag & drop con iconos) ===

>>> RECOMENDADO HACERLO CON CLAUDE OPUS 4.8 (interfaz bonita = merece el mejor modelo).

CONTEXTO: Wheel Deck (launcher Python + Logitech G29 + pygame, segundo plano,
Windows). Caps 1-7 funcionan. En el Cap.7 se hizo un configurador de CONSOLA
(config.py + core/app_scanner.py) que escanea las apps del Menú Inicio y las asigna
a cada marcha en settings.json. PROBLEMA: la consola no es nada visual y a Markitos
le cuesta entenderla. Queremos un configurador GRÁFICO y MUY BONITO.

ESTO ES LO MÁS IMPORTANTE DEL CAPÍTULO: la interfaz gráfica tiene que ser MUY
ATRACTIVA, moderna y clara. Nada del Tkinter clásico feo. Usa algo bonito de verdad
(recomendado: CustomTkinter, con esquinas redondeadas, modo oscuro, tipografía
cuidada, y los colores del gradiente de cada marcha como acento). Que dé gusto usarla.

METÁFORA DE MARKITOS (la "pizarra"):
- Una pizarra con 6 HUEQUECILLOS, uno por marcha (Modo 1-6). En cada hueco se ve qué
  app tiene asignada (con su ICONO y nombre) o "vacío" si no tiene.
- A un lado, una LISTA/BUSCADOR de las apps detectadas del PC, cada una con su ICONO.
- Markitos ARRASTRA una app desde la lista y la SUELTA en el hueco de la marcha que
  quiera (drag & drop, estilo pizarra de verdad). Al soltarla, queda asignada.

LO QUE QUIERO EN ESTE CAPÍTULO:
1. Configurador gráfico (nuevo, ej: config_gui.py o reemplazar config.py; reutiliza
   la lógica de core/app_scanner.py para escanear/buscar, no la repitas).
2. Los 6 huequecillos con el COLOR del gradiente de cada marcha:
   Modo1 Claude #4ade80 · Modo2 ChatGPT #a3e635 · Modo3 VSCode #facc15 ·
   Modo4 Gemini #fb923c · Modo5 Kling #f87171 · Modo6 CapCut #ef4444
3. Lista/buscador de apps CON ICONOS: extrae el icono real de cada app (del .exe o
   .lnk) y muéstralo en la lista y en el hueco. Usa pywin32 (ya instalado) + Pillow
   para sacar el icono. Cachea los iconos para que vaya fluido. Si una app no da
   icono, pon un placeholder bonito.
4. DRAG & DROP: arrastrar app de la lista -> soltar en un hueco de marcha -> se asigna
   y se GUARDA en settings.json (sección "programas", formato { nombre, tipo, destino },
   puedes añadir "icono" con la ruta cacheada si ayuda).
5. Buscador por nombre en la lista (filtra según escribes), reutilizando app_scanner.buscar.
6. También poder asignar una URL (web) a una marcha (Claude, ChatGPT, Gemini, Kling van
   por navegador). Un botoncito tipo "añadir web" con un icono genérico bonito.
7. Poder VACIAR un hueco (quitar la asignación) de forma fácil.
8. SOLO configuración: NO lanza las apps, NO corre en segundo plano, NO toca el G29.
9. El runtime (main.py / core/launcher.py) sigue igual: abre lo que quede guardado en
   settings.json. No lo rompas.

DEPENDENCIAS (Markitos usa uv, venv en la raíz):
- customtkinter, pillow (pywin32 ya está). Deja claro el comando:
  uv pip install customtkinter pillow
- Que si falta una dependencia, avise claro en vez de petar feo.

NO HACER TODAVÍA (próximos capítulos):
- Cap.7c: asignar también con CLIC (app -> clic en hueco), además del drag & drop.
- Cap.8: abrir el configurador con un BOTÓN del G29, pausar el runtime (soltar el
  volante para no pisarse) y que el mismo botón guarde y cierre.
- Cap.9: MODALIDADES por marcha (apps, atajos, aceptar cosas de Claude, cambiar de
  modelo, etc.).

PREGUNTAS ABIERTAS:
- Si el config.py de consola se conserva como alternativa o se reemplaza por el gráfico
  (a Markitos le vale reemplazarlo; decide tú lo más limpio).

ESTADO: ⏳ Por montar. Prioridad: que quede MUY bonito.
===
