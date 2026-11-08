# Mitwirken

Fehler und Controller-Wünsche über GitHub Issues melden. Bitte Modellnummer, Firmware, Verbindungsart, HA-Version, Studio-Version und gegebenenfalls Produkt-Key angeben. Bereinigte Diagnose reicht zunächst aus; keine Tokens, Passwörter oder vollständigen Telefon-Bugreports veröffentlichen.

## Lokale Prüfungen

```sh
python3 -m unittest discover -s tests -v
npm test
python3 -m compileall -q custom_components
python3 tools/build_release.py
```

Die Offline-Suite nutzt die Standardbibliothek. Native HA-Tests liegen in `tests_homeassistant/` und brauchen die Abhängigkeiten aus `requirements-test.txt` mit Python 3.14. Sie importieren die tatsächlichen HA-Module und simulieren Geräteantworten; reale Pumpen werden nicht kontaktiert.

Neue Controller benötigen eine belegte Produktdefinition und explizite Entitätsfreigaben. Tests sollten echte Paketpräfixe oder dokumentierte Antworten prüfen. In Dokumentation und PR zwischen Paketprüfung, simulierter HA-Laufzeit und echtem Hardwaretest unterscheiden. Keine Kompatibilität allein aus dem Marketingnamen ableiten.

## Pull Requests

Problem, neue Geräte-/Nutzerfunktion und durchgeführte Prüfungen beschreiben. Bei Protokolländerungen die Herkunft des Schemas, der Mitschnitte oder der Dokumentation nennen und Lizenzen erhalten. Keine beiläufigen Versions- oder Abhängigkeitsupdates.
