=== PROMPT PARA CLAUDE — Capítulo 8b: Títulos dinámicos según modalidad ===

CONTEXTO: Wheel Deck. Bug: al meter una marcha el titulo mostraba siempre el
nombre fijo de settings.json (Claude, ChatGPT...), ignorando la modalidad y lo
asignado.

ARREGLO:
1. Metodo centralizado modalities.titulo_marcha(modo): devuelve el nombre a
   mostrar segun modalidad activa y lo asignado, con el numero de marcha delante.
   - APPS: "1 · Claude" o "6 · (sin app)".
   - ATAJOS: "1 · Captura de pantalla" o "2 · (sin atajo)".
2. main.py usa ese titulo dinamico para overlay + notificacion + terminal.
3. El overlay ahora acepta color opcional: el TEXTO es dinamico pero el COLOR
   sigue siendo el gradiente de la marcha (se lo pasa main.py). Sin romper el
   aviso de modalidad ("MODO: ATAJOS") que ya iba.
4. Logica centralizada en core/modalities.py (no repetida).

VERIFICADO (simulado): marchas en APPS y ATAJOS, asignadas y vacias, muestran
siempre el titulo correcto; el overlay recibe titulo dinamico + color de la marcha.

ESTADO: ✅ arreglado y probado.
===
