=== PROMPT PARA CLAUDE — Capítulo 9: Fix icono atajos + 4 botones + alertas por posición ===

>>> IMPORTANTE: lee antes prompts/SYNC_para_claude.md y RESPETA esos fixes locales
    (overlay.cambio_marcha con color opcional, config_gui._cargar_apps, atajos de
    pantalla). NO los pises ni reintroduzcas esos bugs.

CONTEXTO: Wheel Deck (launcher Python + Logitech G29 + pygame, segundo plano,
Windows). Caps 1-8b funcionan. Tres cosas en este capítulo.

--- 1) BUG: icono viejo en modalidad ATAJOS ---
En la pizarra (config_gui.py), en modalidad ATAJOS, las tarjetas/huecos muestran un
ICONO VIEJO de app (ej. el logo de VSCode en "Cambiar de ventana"). Se reutiliza un
icono cacheado de app en vez de dar a los atajos su propio icono. ARREGLAR:
- Los atajos NO deben usar iconos de apps. Dales su propio icono/placeholder (ej. un
  glifo o emoji por atajo, o un icono genérico de teclado bonito y coherente con la
  estética cabina). Que no quede ningún icono "heredado" de la app anterior.
- Revisar que al cambiar de modalidad Apps<->Atajos se limpian bien las tarjetas y no
  quedan iconos residuales.

--- 2) LOS 4 BOTONES con configuración propia (por modalidad) ---
Markitos quiere que 4 botones del volante tengan cada uno su acción configurable, y
DISTINTA según la modalidad activa (Apps / Atajos / futuras).
- Estructura en settings.json (ej: "botones" con la config por modalidad y por botón).
- Cada botón puede tener asignada una acción (para empezar: lanzar una app, ejecutar
  un atajo del catálogo, o nada). Reutiliza lo que ya existe (launcher, shortcuts,
  catalogo_atajos).
- Que sea fácil de ampliar (más acciones en el futuro).
PREGUNTAS ABIERTAS (Markitos las confirmará con tests/test.py, NO inventar):
- QUÉ 4 botones son (números exactos del G29). Nota previa del proyecto: botones 0 y 1
  los usa el interruptor del Modo1; 2 y 3 estaban libres. Markitos aún no ha fijado los
  4 definitivos. Deja los números CONFIGURABLES en settings.json y pon unos por defecto
  razonables, avisando de que hay que verificarlos.
- QUÉ hace cada botón en cada modalidad (aún por decidir). Monta el sistema/estructura
  y deja ejemplos, pero que sea todo configurable, sin hardcodear acciones concretas.

--- 3) ALERTAS (overlay) EN POSICIONES DISTINTAS según el evento ---
Markitos quiere que el aviso de cambio de MODALIDAD (levas) salga en una esquina y el
de cambio de MARCHA en otra. Confirmado que NO afecta al rendimiento (solo coordenadas).
- Cambio de MODALIDAD (leva) -> esquina ARRIBA-DERECHA (top-right).
- Cambio de MARCHA -> esquina ABAJO-DERECHA (bottom-right), como ahora.
- Configurable en settings.json (que overlay pueda recibir/usar una esquina por tipo de
  evento). Mantener el color del gradiente y todo lo del Cap.8b.
- Sin saturar: solo estas dos posiciones por ahora.

NO ROMPER: apps, atajos, títulos dinámicos, historial, filtro, interruptores, runtime
ligero en segundo plano.

NÚMEROS DEL G29:
- Ejes: 0 volante (sin usar) · 1 acelerador · 2 freno · 3 embrague
- Marchas H-shifter: botones 12-17 (Modos 1-6) · 18 = R (salir)
- Levas: 4 (siguiente modalidad) / 5 (anterior)
- Botones 0,1 interruptor Modo1 · 2,3 libres (los 4 botones a definir por Markitos)

ESTADO: ⏳ Por montar. Bug del icono = prioridad; 4 botones = framework configurable;
posiciones = arriba-der (levas) / abajo-der (marchas).
===
