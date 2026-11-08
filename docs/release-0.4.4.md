# Jebao Studio 0.4.4

## Gruppen zuverlässig anlegen

Gruppennamen und Checkbox-Auswahl liegen jetzt in einem eigenen Entwurf.
Home-Assistant-Statusupdates können dadurch keine ausgewählten Pumpen mehr
abwählen. Bearbeiten kopiert die Gruppe, sodass Abbrechen gespeicherte Namen
und Mitglieder nicht verändert. Speicherfehler behalten den Entwurf; erneutes
Speichern bleibt möglich. Leere Gruppen werden verständlich abgefangen.
Eingerichtete Offline-Pumpen bleiben als Mitglieder wählbar und gespeichert;
nicht gestartete Einträge ohne Laufzeitprofil sind weiterhin gesperrt.

## Mobile Seitenleistenansicht

Vier gleich breite Navigationselemente, größere Checkboxen und Touchflächen,
angepasste Karten und Zusammenfassung, umbruchfähige Gerätenamen und
16-Pixel-Zahleneingaben für Mobilgeräte. Bildschirmränder und Safe Areas werden
berücksichtigt. Die HA-Seitenleiste öffnet weiterhin die normale Menüschaltfläche.

## Prüfung

Automatisierte Panel-, Python- und Home-Assistant-Tests sowie Browserabläufe
mit Beispieldaten: Gruppen erstellen/bearbeiten/abbrechen/löschen, Statusupdates
während Auswahl, simuliertes fehlgeschlagenes Speichern und Wiederholen,
Pflichtfeldprüfung, Leistungs-/Frequenzeingabe, Wellenmodus, Manual/Programm,
Fütterung und Gruppenbefehle. Layoutprüfung bei 320, 360, 390, 430, 768 und
1280 Pixeln. Das prüft die Anwendung mit simulierten Controllerantworten,
nicht die tatsächliche Funkverbindung oder die iOS-Tastatur auf Hardware.
