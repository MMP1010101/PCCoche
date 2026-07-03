=== PROMPT PARA CLAUDE — Capítulo 7b: Configurador VISUAL (pizarra drag & drop) ===

CONTEXTO: Wheel Deck. El config de consola (Cap.7) no era visual. Ahora pizarra
grafica bonita con CustomTkinter.

LO MONTADO:
1. config_gui.py: pizarra con 6 huecos (uno por marcha) + lista/buscador de apps.
2. Cada hueco con el color de su marcha (gradiente verde->rojo) como acento.
3. Iconos reales de las apps (core/icon_extractor.py, pywin32 + Pillow, cacheados
   en config/icon_cache/). Placeholder si una app no da icono.
4. Drag & drop MANUAL (CustomTkinter no trae dnd nativo): clic-arrastrar-soltar
   sobre el hueco. Al soltar, asigna y guarda en settings.json.
5. Buscador que filtra segun escribes (reusa app_scanner.buscar).
6. Boton "+ Anadir web" para asignar URL a una marcha.
7. Boton ✕ en cada hueco para vaciarlo.
8. Solo config: no lanza apps, no toca G29, no corre en segundo plano.
9. Reutiliza core/app_scanner.py (no duplica logica). Runtime intacto.

DEPENDENCIAS:  uv pip install customtkinter pillow   (pywin32 ya estaba).
Si falta una, avisa claro y no pete.

DECISIONES:
- Look: paleta "cabina" oscura, no un dark-mode generico; el gradiente por marcha
  es la firma visual (justificado por el proyecto).
- Se conservan LOS DOS configuradores: el visual (principal) y el de consola
  (respaldo por si CustomTkinter da guerra).

LIMITACION HONESTA: la GUI no se pudo ejecutar en el entorno de Claude (sin
pantalla). Verificado: compila, avisa bien si faltan deps, y la logica de
asignar/vaciar/guardar persiste en settings.json. El aspecto visual final y el
drag & drop fino los prueba Markitos en su Windows.

NO HECHO: Cap.7c (asignar con clic), Cap.8 (abrir config con boton G29 + pausar
runtime), Cap.9 (modalidades por marcha).

ESTADO: ✅ montado. Prioridad era que quede MUY bonito. Pendiente que Markitos lo
vea en pantalla y ajustemos el look si hace falta.
===
