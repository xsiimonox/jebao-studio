# Jebao Studio 0.4.0

## Bedienung am Becken

Unter „Fütterung & Controller“ auf der Pumpenkarte stehen unterstützte
Funktionen bereit: Fütterungsdauer in Minuten, Fütterung starten/beenden,
Controller-Zeitplan ein-/ausschalten und Kopplung unabhängig/Master/Slave.
Aktive Fehler werden auf der Karte angezeigt. Bei aktivem Zeitplan oder
Slave-Betrieb erklärt die Oberfläche, warum manuelle Werte überschrieben
werden können. Diese Einstellungen werden nicht automatisch geändert.

Die Dauer verwendet den Timer des Controllers; es läuft kein Browser-Timer,
der nach dem Schließen des Studios verloren gehen könnte.

## Behobene Fehler

- Attributkennungen aus der Entity-Registry ersetzen unzuverlässige
  Namenserkennung. Leistung, Modus, Kopplung und Fütterungsdauer bleiben
  auch nach Umbenennen korrekt zugeordnet.
- Gruppen prüfen Bereiche, Schritte und Optionen sämtlicher Zielgeräte
  vor dem Senden und melden Erfolge, Fehler und übersprungene Geräte.
- Gemischte Gruppenmodi werden explizit angezeigt; wählbar sind nur
  gemeinsame Modi. Unterschiede bei der Leistung bleiben erkennbar.
- Befehle je lokalem Controller werden nacheinander ausgeführt, damit
  parallele Änderungen nicht denselben veralteten Steuerblock verwenden.
- Gleiche Namen neuer Gruppen überschreiben keine bestehende Gruppe.
- Geerbte numerische Moduszuordnungen werden als Mapping erhalten.
- Fehlgeschlagene Eingaben lassen sich mit demselben Sollwert erneut senden.

Wellenbilder sind schematisch. Prozentwerte sind eingestellte Leistung,
keine gemessene Durchflussmenge. Gruppen senden einzelne Befehle; daraus
folgt keine phasengenaue Synchronisierung der Pumpen.

## Prüfung

Automatisierte Python-, Panel- und Home-Assistant-Tests sowie Browserprüfung
auf Desktop und Mobilgerät mit Beispieldaten. Browserprüfung umfasst
Zahleneingabe, Gruppenbefehle, gemischte Modi, Zeitplan und Fütterungsende.
Das ist kein Hardwaretest der MLW-/DMP-Controller. Ungeklärte Akzeptanz von
Leistungs-/Modusbefehlen erfordert weiterhin eine Controllerantwort.

Lokale Vorschau: `python3 -m http.server 8766 --bind 127.0.0.1`, dann
`node tools/browser-check.cjs` mit installiertem Playwright ausführen.
