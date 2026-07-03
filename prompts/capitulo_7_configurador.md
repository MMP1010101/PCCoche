=== PROMPT PARA CLAUDE — Capítulo 7: Configurador + listador de apps (abrir por nombre) ===

CONTEXTO: Wheel Deck (launcher Python + Logitech G29 + pygame, segundo plano,
Windows). Caps 1-6 funcionan. En el Cap.6 cada marcha abre un programa, pero el
problema es que hay que meter la RUTA EXACTA del .exe a mano en settings.json, y
normalmente no sabes dónde está el ejecutable. Esto no escala.

EJES (verificados Cap.5, 4 ejes):
- Eje 0 volante (sin usar) · Eje 1 acelerador · Eje 2 freno · Eje 3 embrague
- Botones 12-17 marchas · 18 = R (salir) · 0,1 interruptor Modo1 · 2,3 libres

OBJETIVO DEL PRODUCTO FINAL (visión, para que orientes la arquitectura):
- Habrá DOS ejecutables: (1) el CONFIGURADOR y (2) el programa PRINCIPAL (runtime
  que lee el G29 en segundo plano, consumo mínimo).
- El configurador es SOLO configuración: busca apps y guarda en settings.json.
  NO lanza las apps, NO corre en segundo plano, no debe consumir recursos cuando
  no se usa.

LO QUE QUIERO EN ESTE CAPÍTULO (solo el configurador + listador):
1. Una herramienta de configuración aparte (ej: config.py / configurador, que en el
   futuro será su propio .exe). De momento se lanza a mano; la integración con un
   botón del G29 es el SIGUIENTE capítulo (Cap.8), no lo hagas aún.
2. LISTADOR DE APPS: que escanee las apps instaladas del PC (lo normal en Windows:
   accesos directos .lnk del Menú Inicio, tanto de usuario como de sistema) y las
   liste por NOMBRE amigable. Así Markitos ve qué apps hay sin saber rutas.
3. BUSCAR POR NOMBRE: Markitos escribe el nombre (ej "CapCut") y el configurador lo
   busca/matchea entre las apps detectadas (búsqueda parcial, sin distinguir
   mayúsculas). Muestra coincidencias.
4. Al elegir una app para una marcha, el configurador RESUELVE su destino real (la
   ruta del .lnk o del .exe que encuentre) y lo GUARDA en settings.json, en la
   sección "programas" que ya existe. Idea clave para el bajo consumo: la búsqueda
   pesada se hace UNA VEZ aquí, en config; el runtime luego solo abre lo guardado,
   sin escanear nada.
5. El runtime (core/launcher.py del Cap.6) debe seguir funcionando: abre lo que haya
   guardado en settings.json (tipo "url" -> navegador; tipo "app" -> el destino
   resuelto). Si una marcha no tiene destino configurado, avisa y no abre, no pete.
6. Que el configurador permita asignar app a cada una de las 6 marchas (modos 1-6),
   y también dejar tipo "url" con una URL a mano (para Claude, ChatGPT, Gemini,
   Kling que van por web).
7. Todo lo que se configura se persiste en settings.json (no en otro sitio raro).

NO HACER TODAVÍA (próximos capítulos, no en este):
- Cap.8: que un BOTÓN del G29 abra el configurador, pause el runtime, el configurador
  también se maneje con el G29, y el mismo botón GUARDE y CIERRE volviendo al runtime.
  (Detalle técnico ya previsto: cuando se abra el config, el principal debe SOLTAR/
  pausar el G29 para no pisarse, y retomarlo al cerrar. No lo montes aún, solo tenlo
  en mente para no cerrar puertas en la arquitectura.)
- Cap.9: MODALIDADES por marcha (cada marcha = un tipo distinto: apps, atajos de
  teclado, aceptar/rechazar cosas de Claude, cambiar modelo de Claude, etc.).

PREGUNTAS ABIERTAS:
- Interfaz del configurador: ¿consola simple (menú de texto) o ventanita Tkinter?
  Markitos no lo ha decidido; elige la más sencilla y ligera y coméntalo, se puede
  cambiar. (Tkinter ya se usa para el overlay, así que está disponible.)
- Formato de guardado en "programas": mantener el actual { nombre, tipo, destino }.

ESTADO: ⏳ Por montar.
===
