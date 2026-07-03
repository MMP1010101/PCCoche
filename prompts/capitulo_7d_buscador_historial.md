=== PROMPT PARA CLAUDE — Capítulo 7d: Buscador primero + historial (pizarra) ===

CONTEXTO: Wheel Deck. La pizarra mostraba la lista completa de apps. Ahora:
buscador primero + historial de recientes.

LO MONTADO:
1. Buscador primero: al abrir NO hay listón. Buscador prominente arriba
   ("🔍 Escribe el nombre de tu app..."). Resultados aparecen al escribir
   (reusa app_scanner.buscar con el filtro del Cap.7c).
2. Historial: las apps ya asignadas se guardan como chips (con icono) arriba,
   para re-asignar sin buscar. Se arrastran igual que los resultados.
   - Persistido en settings.json > historial_apps { limite, items }.
   - Sin duplicados, recientes primero, limite 12.
   - Solo entran las que se ASIGNAN de verdad (no las buscadas).
3. Se mantiene todo: 6 huecos con color, drag & drop, iconos, vaciar hueco,
   "+ anadir web", filtro Cap.7c. Runtime intacto.
4. Estetica coherente (cabina oscura, chips redondeados).
5. Extra (pregunta abierta resuelta): boton "Ver todas" discreto por si se quiere
   el listón entero; por defecto oculto.

LIMITACION HONESTA: la GUI no se ejecuta en el entorno de Claude (sin pantalla).
Verificado: compila, y la logica de historial (duplicados, orden, limite) +
persistencia en settings.json funcionan. El look y el arrastre los prueba Markitos.

ESTADO: ✅ montado. Pendiente que Markitos lo vea en pantalla.
===
