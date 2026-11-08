# Jebao Studio 0.3.3

Neben jedem Leistungs- und Frequenzslider steht ein direkt bearbeitbares
Zahlenfeld. Slider und Zahlenfeld bleiben synchron. Loslassen, Enter oder
Verlassen des Zahlenfelds senden die Änderung einmal; ungültige Eingaben
werden vor dem Senden abgefangen.

Statusupdates zeichnen die Oberfläche während Eingaben und Schreibbefehlen
nicht neu. Ein gesendeter Sollwert bleibt bis zum Abgleich bzw. für maximal
fünf Sekunden gespeichert. Danach wird wieder der gemeldete Pumpenwert
angezeigt. Controllerfehler bleiben sichtbar. Gilt auch für Pumpengruppen.
