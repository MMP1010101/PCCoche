=== PROMPT PARA CLAUDE — Capítulo 8: Modalidades por leva (Apps / Atajos) ===

CONTEXTO: Wheel Deck. Salto grande: MODALIDADES ("filosofias"). Las levas del
volante rotan entre modalidades (ciclico) y cada una cambia lo que hacen las 6 marchas.

LO MONTADO:
1. Esqueleto de modalidades (core/modalities.py): levas rotan ciclico. Config en
   settings.json > modalidades { orden:[apps,atajos], ... }. Facil anadir mas.
   Levas configurables en settings.json > levas { siguiente:4, anterior:5 }
   (VERIFICAR con tests/test.py; ajustar si el G29 da otros numeros).
2. Modalidad APPS: la de siempre (marchas abren 'programas'). Runtime intacto.
3. Modalidad ATAJOS (core/shortcuts.py): las marchas ejecutan atajos de teclado
   con la libreria 'keyboard'. Catalogo de 15 atajos SEGUROS (copiar, pegar,
   cortar, deshacer, rehacer, sel. todo, guardar, buscar, CAPTURA win+shift+s,
   alt+tab, nueva/cerrar pestana, zoom, escritorio). CERO peligrosos (ni delete,
   ni apagar, ni alt+f4).
4. Configurador (pizarra): selector Apps/Atajos arriba. En Atajos el buscador
   filtra el catalogo seguro y se asignan a las marchas igual que las apps
   (arrastrar). Se guardan en modalidades.atajos.atajos_marcha.
5. Overlay avisa la modalidad al cambiar con la leva ("MODO: ATAJOS").
6. Nada roto: apps, overlay, interruptores, filtro, historial, runtime ligero.

DECISIONES (preguntas abiertas):
- Gesto en Atajos = MISMO que apps (marcha + embrague + acelerador), por coherencia.
- Libreria: 'keyboard' (ligera para Windows). uv pip install keyboard. Aviso si
  falta. Nota: win+shift+s puede requerir ejecutar como admin.

VERIFICADO (simulado): levas rotan ciclico, atajos disparan en modo ATAJOS, apps
en modo APPS, catalogo sin peligrosos, asignacion y busqueda OK. La parte visual
del selector la prueba Markitos en pantalla.

PARA MAS ADELANTE (no en este cap): botones 0-3 con config propia por modalidad;
modalidad "Modelos de Claude"; abrir configurador con boton del G29.

ESTADO: ✅ montado y probado (simulado).
===
