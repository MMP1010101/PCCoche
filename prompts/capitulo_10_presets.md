=== PROMPT PARA CLAUDE — Capítulo 10: Presets por botón de cara (2 niveles) ===

CONTEXTO: montado sobre la version REAL de Markitos (subida por zip), no sobre la
copia desincronizada de Claude. Respetados los fixes del SYNC (overlay color
opcional, _cargar_apps como metodo propio, ejes 1/2/3, atajos mover/dividir pantalla).

SISTEMA DE 2 NIVELES:
- Nivel 1 MODALIDAD (levas 4/5): apps, atajos. Ya existia.
- Nivel 2 PRESET (botones de cara 0-3 = ✕□○△): dentro de cada modalidad, cada
  boton de cara es una sub-config de las 6 marchas. El preset activo se recuerda
  POR modalidad.

CAMBIOS:
1. settings.json MIGRADO sin perder datos: modalidades.apps.presets y
   modalidades.atajos.presets con claves "0".."3" {simbolo,nombre,marchas}. Las
   apps de 'programas' y los 'atajos_marcha' actuales pasaron al preset △ Normal
   (bid 3, preset_por_defecto). Se eliminaron programas/botones/interruptores/
   atajos_marcha (respaldo en settings.json.bak_cap9).
   Nuevo: botones_cara { ids:{0:✕,1:□,2:○,3:△}, preset_por_defecto:"3" }.
2. core/modalities.py: gestor de presets. cambiar_preset(bid), preset_activo por
   modalidad, marchas_preset_activo(), etiqueta_preset ("△ Normal"),
   titulo_marcha ahora lee del preset activo (Cap.8b preservado).
3. main.py: botones de cara cambian preset (overlay top-right "△ Normal"). El
   disparo (embrague+acelerador) lee del preset activo (apps -> abrir_destino,
   atajos -> ejecutar). Quitado el interruptor viejo (0/1). Salida sigue en R (18).
4. config_gui.py: selector de modalidad (Apps/Atajos) + selector de PRESET (4
   botones ✕□○△, el activo resaltado) + "✎ Renombrar". Drag&drop, buscador,
   historial, iconos y glifos de atajos (Cap.9) preservados; ahora escriben en el
   preset en edicion. Fix _cargar_apps intacto.
5. core/switches.py y core/buttons.py quedan HUERFANOS (ya no se importan). No
   molestan; se pueden borrar en limpieza futura.

VERIFICADO (simulado): presets independientes (asignar en uno no toca otro),
disparo lee del preset activo en apps y atajos, cambio de preset por boton de cara,
runtime arranca con la config real migrada (chatGPT/VSCode/CapCut/captura...).

PENDIENTE MARKITOS (verificar con tests/test.py):
- Numeros de los 4 botones de cara (ahora ✕=0,□=1,○=2,△=3 en botones_cara.ids).
- La parte visual del selector de presets (verla en pantalla).

ESTADO: ✅ montado y probado (simulado). Migracion sin perdida de datos.
===
