# Jebao Studio 0.2.2

Behebt einen reproduzierten Startfehler bei zwischengespeicherter `model.js` aus der Version vor der Gruppensteuerung: Das neue Panel importiert Funktionen, die in der alten Browserkopie fehlen. Die Hilfsdatei erhält jetzt eine eigene Versions-URL. In diesem Fall konnte 0.2.1 die leere Seite nicht beheben.

Die Integrationskachel erhält lokale Markenbilder im von Home Assistant unterstützten `brand`-Ordner. Die bisherige PNG-Datei im Panel-Verzeichnis konnte diesen Zweck nicht erfüllen.

Pumpenkarten erscheinen unabhängig vom Abschluss der Gruppen-Abfrage. Modusauswahl in Gruppen, Gruppen löschen und Bluetooth-Diagnose sind wieder enthalten.

Nach dem Update Home Assistant vollständig neu starten und den geöffneten Browser-Tab einmal neu laden. Es müssen keine Geräte oder Gruppen gelöscht werden. Falls das Panel weiterhin leer ist, werden Browser-Fehler und Home-Assistant-Protokolle zur weiteren Diagnose benötigt.
