=== PROMPT PARA CLAUDE — Capítulo 11: Modalidad "Claude" (cambiar de modelo) ===

>>> LEE ANTES prompts/SYNC_para_claude.md y respeta los fixes/estructura actual.
>>> Recomendado: Opus 4.8 alto (nueva modalidad + toca configurador; no romper nada).

CONTEXTO: Wheel Deck (launcher Python + Logitech G29 + pygame, segundo plano, Windows).
Caps 1-10 funcionan. Sistema de 2 niveles: leva = modalidad, botones de cara = preset,
marchas = 6 huecos del preset. Modalidades actuales: apps, atajos. Ahora AÑADIMOS una
tercera modalidad: "claude".

IDEA: en la modalidad CLAUDE, cada marcha CAMBIA EL MODELO de Claude escribiendo su
comando en la ventana de Claude que Markitos tenga enfocada. O sea: la marcha TECLEA
el comando (tipo "/model <id>") y pulsa Enter, usando la libreria 'keyboard' que ya
esta (igual que la modalidad Atajos).

MAPEADO POR DEFECTO (6 marchas = 6 modelos; editable luego):
- Marcha 1: Sonnet 5                    -> /model claude-sonnet-5
- Marcha 2: Opus 4.8 normal             -> /model claude-opus-4-8
- Marcha 3: Opus 4.8 alto               -> (ver nota abajo)
- Marcha 4: Opus 4.8 alto + razonamiento-> (ver nota abajo)
- Marcha 5: Opus 4.8 extra              -> (ver nota abajo)
- Marcha 6: Fable                       -> /model claude-fable-5
NOTA: el nivel de esfuerzo (normal/alto/extra/razonamiento) puede NO cambiarse con el
mismo comando que el modelo. Por eso cada marcha debe guardar un TEXTO/COMANDO LIBRE que
se teclea tal cual (Markitos pondra el comando exacto que use su Claude para cada uno).
Deja el mapeo por defecto como ejemplo, pero que el comando de cada marcha sea EDITABLE.

REQUISITOS:
1. Nueva modalidad "claude" en settings.json > modalidades (anadir a 'orden' y su bloque).
   Igual que apps/atajos, con sus 4 PRESETS (✕□○△) y sus 6 marchas. En esta modalidad,
   cada marcha guarda: { nombre, comando } (el texto a teclear, ej "/model claude-opus-4-8").
2. Al disparar una marcha en modalidad Claude (mismo gesto que las demas: marcha +
   embrague + acelerador, o como encaje), Wheel Deck TECLEA el comando y pulsa Enter en
   la ventana enfocada, usando keyboard.write + keyboard.press("enter") (con una pequena
   pausa si hace falta para que el texto entre bien). Con manejo de errores.
3. Un CATALOGO editable de comandos de modelo en settings.json (tipo "catalogo_modelos"
   o dentro de la modalidad), para elegirlos en la pizarra sin escribirlos a mano cada vez.
   Incluye por defecto los IDs conocidos: claude-sonnet-5, claude-opus-4-8, claude-fable-5,
   claude-haiku-4-5-20251001. Los de esfuerzo (alto/extra/razonamiento) los dejara Markitos.
4. CONFIGURADOR (pizarra): el selector de modalidad ahora tiene Apps / Atajos / Claude.
   En modalidad Claude, se asignan comandos a las 6 marchas (elegir del catalogo o escribir
   uno propio), con su icono/glifo propio (ej. 🤖) para no heredar iconos de apps.
5. Titulos dinamicos (Cap.8b) y overlay: en modalidad Claude el titulo muestra el nombre
   del modelo de esa marcha (ej "1 · Sonnet 5" o "3 · (sin modelo)"). Icono/glifo 🤖.
6. IMPORTANTE seguridad: esto solo teclea texto en la ventana enfocada. Que quede claro
   que el usuario debe tener la ventana de Claude enfocada al disparar. No hace nada raro
   ni peligroso.
7. No romper NADA: apps, atajos, presets (Cap.10), levas, overlay, historial, filtro,
   runtime ligero. Estructura limpia y ampliable.

NUMEROS DEL G29 (sin cambios):
- Ejes: 0 volante · 1 acelerador · 2 freno · 3 embrague
- Marchas 12-17 (Modos 1-6) · 18 = R (salir)
- Levas: 4 siguiente modalidad / 5 anterior · Botones de cara (presets): ✕=0 □=1 ○=2 △=3

PREGUNTA ABIERTA:
- Comandos exactos para los niveles de esfuerzo (Opus alto / alto+razonamiento / extra):
  los pondra Markitos en settings.json cuando sepa el comando que usa su Claude.

ESTADO: ⏳ Por montar.
===
