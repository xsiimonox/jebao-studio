# Jebao Studio 0.4.3

Der eingebaute Home-Assistant-Diagnosedownload enthält nun die zuletzt
empfangenen AutoTime00–AutoTime47-Felder als Hexdaten plus Betriebsart und
Leistungswerte. Das ermöglicht den Vergleich eines bekannten Jebao-Aqua-Plans
mit dessen Controllerdaten. Die Zeitplankodierung wird noch nicht interpretiert.

Nach Änderung des Plans in Jebao Aqua warten, bis der Controllerstatus in HA
aktualisiert wurde. Dann unter Einstellungen → Geräte & Dienste → Jebao Studio
im Menü des Integrationseintrags „Diagnosedaten herunterladen“ wählen.
Die Datei hier im Chat zusammen mit den exakten Abschnittseinstellungen teilen.
Der Export verwendet den vorhandenen Cache, fordert keine neuen Statusdaten an
und sendet keine Schreibbefehle. Fehlende Daten erscheinen als null.
IP, MAC, Geräte-ID und Cloud-Zugangsdaten werden nicht hinzugefügt.
