=== PROMPT PARA CLAUDE — Capítulo 11: Modalidad "Claude" (cambiar de modelo) ===

CONTEXTO: sobre la version real (Cap.10 presets). Respetados fixes del SYNC.
Tercera modalidad "claude": cada marcha TECLEA un comando (ej /model ...) + Enter
en la ventana enfocada, con la libreria keyboard (write + enter).

CAMBIOS:
1. settings.json: modalidad 'claude' en orden [apps,atajos,claude], con 4 presets
   (✕□○△) y 6 marchas {nombre, comando}. Preset △ Normal con mapeo por defecto:
   m1 Sonnet5, m2 Opus4.8, m3 Opus4.8 alto (comando vacio), m4 Opus alto+razon
   (vacio), m5 Opus extra (vacio), m6 Fable5. Nuevo catalogo_modelos editable
   (sonnet5, opus48, fable5, haiku45 + los de esfuerzo con comando vacio).
2. core/model_switch.py: teclea comando + Enter (keyboard.write/press_and_release)
   con pausa y manejo de errores. Aviso si falta keyboard.
3. main.py: disparo en modalidad claude teclea el comando de la marcha del preset
   activo. Marcha sin comando -> avisa, no hace nada.
4. modalities.titulo_marcha: modo claude muestra "1 · Sonnet 5" o "3 · (sin modelo)".
5. config_gui.py: selector Apps/Atajos/Claude. En Claude, catalogo de modelos
   buscable con glifo 🤖, se asignan a las marchas (arrastrar). Guarda {nombre,
   comando}. Preservados presets (Cap.10), fix iconos (Cap.9), _cargar_apps.

SEGURIDAD: solo teclea texto en la ventana enfocada. El usuario debe tener la
ventana de Claude enfocada al disparar. Nada peligroso.

VERIFICADO (simulado): teclea /model claude-sonnet-5 y claude-fable-5 + Enter,
marcha sin comando no hace nada, ciclo de 3 modalidades OK, catalogo/busqueda/
asignacion en la pizarra correctos.

PENDIENTE MARKITOS: comandos exactos de los niveles de esfuerzo (Opus alto /
alto+razonamiento / extra) en catalogo_modelos y en las marchas del preset.

ESTADO: ✅ montado y probado (simulado).
===
