=== PROMPT PARA CLAUDE — Capítulo 9: Fix icono atajos + 4 botones + alertas por posición ===

RESPETADOS los fixes locales del SYNC (overlay color opcional, config_gui buscador+
historial, atajos captura). No se pisaron.

1) BUG ICONO ATAJOS (arreglado):
   - Causa: en CustomTkinter image=None no limpia el icono anterior -> heredaba el
     de la app (ej VSCode en "Cambiar de ventana").
   - Fix: image="" limpia de verdad. Ademas cada atajo tiene su GLIFO propio
     (📋 copiar, 📸 captura, ✂ cortar...) con fallback ⌨. Web usa 🌐.
   - Al cambiar Apps<->Atajos las tarjetas se refrescan sin residuos.

2) 4 BOTONES configurables por modalidad (framework):
   - settings.json > botones { ids:[2,3,6,7] (VERIFICAR con test.py), acciones:{
     apps:{...}, atajos:{...} } }. Cada accion {tipo: app|atajo|nada, valor}.
   - core/buttons.py ejecuta la accion segun modalidad activa. Reutiliza launcher
     (nuevo abrir_destino) y shortcuts. Facil anadir tipos.
   - Numeros por defecto 2,3,6,7 -> Markitos los confirma con test.py y los cambia
     en settings.json.

3) ALERTAS por posicion:
   - Cambio de MODALIDAD (leva) -> top-right. Cambio de MARCHA -> bottom-right.
   - Configurable: overlay.esquina_modalidad / esquina_marcha en settings.json.
   - Mantiene color de gradiente y titulos dinamicos del Cap.8b.

VERIFICADO (simulado): iconos sin herencia, botones distintos por modalidad
(nada en apps, copiar/pegar en atajos), esquinas correctas. Runtime intacto.

PENDIENTE MARKITOS: fijar los 4 botones definitivos con test.py; decidir que hace
cada uno por modalidad (todo configurable, sin hardcodear).

ESTADO: ✅ montado y probado (simulado). GUI: iconos los ve Markitos en pantalla.
===
