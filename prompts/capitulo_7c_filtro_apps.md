=== PROMPT PARA CLAUDE — Capítulo 7c: Filtrar apps peligrosas/basura del escáner ===

CONTEXTO: Wheel Deck. El escaner (core/app_scanner.py) listaba desinstaladores,
ayudas y utilidades de sistema. Este cap los oculta.

LO MONTADO:
1. Filtro en escanear_apps() -> beneficia a la pizarra y al config de consola.
2. Se ocultan: desinstaladores (uninstall, unins000...), ayudas/docs (.chm, .txt,
   help, readme, release notes...), instaladores (setup, installer), utilidades de
   sistema (regedit, registry, services, driver, odbc...) y todo lo que este en
   \Windows\System32, \SysWOW64, \WinSxS.
3. Se salvan SIEMPRE (lista blanca): cmd/command prompt, powershell, terminal,
   bloc de notas, calculadora, paint, explorador... ("hasta el cmd es bueno").
4. Configurable en settings.json > filtro_apps: excluir, excluir_ext,
   excluir_rutas, permitir_siempre. Valores por defecto sensatos.
5. Filtro por nombre Y por ruta, sin mayus/minus, robusto con barras \ y /.
6. Runtime, drag & drop, iconos: intactos. Solo se recorta lo que muestra el escaner.

FIX durante el montaje: normalizacion de barras (\ vs /) para que el filtro de
rutas de sistema funcione igual en cualquier formato.

AGRESIVIDAD: peca de limpio. Si falta una app, se anade a permitir_siempre en
settings.json sin tocar codigo.

ESTADO: ✅ montado y probado (12/12 casos: oculta basura, salva apps buenas y cmd).
===
