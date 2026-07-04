=== PROMPT PARA CLAUDE — Capítulo 10: Presets por botón de cara (2 niveles) ===

>>> RECOMENDADO: Opus 4.8 alto + razonamiento (reestructura settings; NO romper nada).
>>> LEE ANTES prompts/SYNC_para_claude.md y respeta esos fixes (sobre todo el bug
    REINCIDENTE de config_gui._cargar_apps: debe ser su propio metodo, NO codigo muerto).

CONTEXTO: Wheel Deck (launcher Python + Logitech G29 + pygame, segundo plano, Windows).
Caps 1-9 funcionan. Ahora: los 4 BOTONES DE CARA del volante = PRESETS (sub-configs).

IDEA DE MARKITOS (sistema de 2 niveles):
- NIVEL 1 = MODALIDAD (ya existe, se cambia con las levas 4/5): Apps, Atajos, ...
- NIVEL 2 = PRESET (NUEVO, se cambia con los botones de cara): dentro de una modalidad,
  cada boton de cara es una sub-configuracion distinta de las 6 marchas.
- Botones de cara (estilo PlayStation, MOSTRAR con su SIMBOLO en overlay/configurador):
  - ✕ (equis)     = boton 0
  - □ (cuadrado)  = boton 1
  - ○ (circulo)   = boton 2
  - △ (triangulo) = boton 3
  (VERIFICAR numeros con tests/test.py; dejar configurables en settings.json.)

EJEMPLO que dio Markitos (modalidad Apps):
  ✕ = apps moviles · △ = normal · ○ = para videos · □ = (otra que quiera)
Al pulsar un simbolo, las 6 marchas cambian a las asignaciones de ESE preset. Lo mismo
dentro de Atajos y futuras modalidades (cada modalidad tiene sus 4 presets).

REQUISITOS:
1. Los nombres de los 4 presets son LIBRES y se definen POR MODALIDAD (en Apps pueden ser
   moviles/normal/videos/..., en Atajos otros). Editables por Markitos a su gusto.
2. Cada preset guarda las asignaciones de las 6 marchas de esa modalidad:
   - En Apps: 6 apps (formato actual { nombre, tipo, destino }).
   - En Atajos: 6 atajos (clave del catalogo_atajos).
3. Pulsar un boton de cara cambia el PRESET ACTIVO de la modalidad actual. El overlay
   avisa mostrando el simbolo + nombre del preset (ej. "△ Normal"). Usa la posicion de
   overlay que encaje (puedes reusar esquina_modalidad o una nueva configurable).
4. Las 6 marchas (botones 12-17) actuan segun (modalidad activa, preset activo). El gesto
   de disparo (embrague+acelerador) y los titulos dinamicos del Cap.8b siguen igual, pero
   leyendo del preset activo.
5. MIGRAR lo que ya hay sin perder nada: las asignaciones actuales de "programas" y de
   modalidades.atajos.atajos_marcha deben pasar a ser el preset por DEFECTO (ej. el
   "normal"/△) de su modalidad. Nada de datos perdidos.
6. EL CONFIGURADOR (pizarra): que se pueda elegir QUE modalidad y QUE preset estas
   editando (un selector de preset con los 4 simbolos ✕□○△ + su nombre editable), y
   asignar las 6 marchas de ESE preset. Mantener drag&drop, buscador, historial, iconos,
   glifos de atajos (Cap.9) y el fix _cargar_apps.
7. Esto REEMPLAZA/REDEFINE el sistema de "botones" del Cap.9 (core/buttons.py + seccion
   'botones'): los botones de cara ahora CAMBIAN DE PRESET, no ejecutan una accion suelta.
   Reconcilia core/buttons.py con este nuevo rol (o sustituyelo por un gestor de presets).
8. QUITAR el interruptor viejo del Modo1 (usaba botones 0 y 1): ya no aplica, porque 0 y 1
   ahora son botones de cara (presets). La salida sigue siendo la marcha atras (boton 18).
9. Todo configurable en settings.json, estructura limpia y ampliable (mas presets/
   modalidades en el futuro). No romper: overlay, runtime ligero, filtro, historial.

NUMEROS DEL G29:
- Ejes: 0 volante (sin usar) · 1 acelerador · 2 freno · 3 embrague
- Marchas H-shifter: 12-17 (Modos 1-6) · 18 = R (salir/apagar)
- Levas (modalidad): 4 siguiente / 5 anterior
- Botones de cara (presets): ✕=0 · □=1 · ○=2 · △=3

ESTADO: ⏳ Por montar. Es estructural: cuidado con no romper lo existente y migrar datos.
===
