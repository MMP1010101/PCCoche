=== NOTA DE SINCRONIZACIÓN PARA CLAUDE (el del chat) ===

Estos cambios se hicieron DIRECTOS en el proyecto (en el PC de Markitos, vía Claude
Code) DESPUÉS de la última versión que montaste. Cuando regeneres código, INCORPÓRALOS
y NO los pises / no reintroduzcas los bugs ya arreglados. Todo está commiteado en
GitHub: https://github.com/MMP1010101/PCCoche

FIXES DE CÓDIGO (importantes, no revertir):
1. core/overlay.py -> cambio_marcha(self, nombre_modo, color=None):
   Ahora acepta un color OPCIONAL. main.py le pasa el color de la marcha porque el
   título es dinámico (Cap.8b) y no se puede resolver por nombre en 'marchas'. Si no
   se pasa color, se busca por nombre (compatibilidad). SIN esto, main.py peta con
   TypeError.
2. config_gui.py -> método _cargar_apps(self) restaurado:
   En la versión del Cap.8, tres líneas (self.apps = escanear_apps() + _render_historial
   + _render_lista) quedaron como CÓDIGO MUERTO tras el return de _buscar_atajos, y
   _cargar_apps no existía -> AttributeError al abrir la pizarra. Debe ser su propio
   método y llamarse desde __init__.

CONFIG (settings.json) añadida/ajustada a mano:
3. g29.ejes: acelerador 1, freno 2, embrague 3 (4 ejes; el volante es eje 0 sin usar).
4. filtro_apps.excluir: añadidos "configurar", "control panel", "panel de control".
5. catalogo_atajos: añadidos "mover_pantalla" (win+shift+left) y "dividir_pantalla"
   (win+left). Markitos decidió UNA sola versión (izquierda) de cada, NO duplicar
   izquierda/derecha.

BUG PENDIENTE (aún por arreglar, para un próximo capítulo):
- En modalidad ATAJOS, las tarjetas/huecos muestran un ICONO VIEJO de app (ej. el logo
  de VSCode en "Cambiar de ventana"). Se reutiliza un icono antiguo de la caché de apps
  en vez de dar a los atajos su propio icono/placeholder. Hay que arreglarlo.

IDEAS FUTURAS anotadas:
- Botones 0-3 con configuración propia por modalidad.
- Modalidad "Modelos de Claude".
- Modalidad IA: seleccionas texto -> la IA (API) lo lee y lo reescribe mejor.
- Abrir el configurador con un botón del G29 (pausar runtime, mismo botón guarda y cierra).
===
