# Jebao Studio 0.2.4

Diese Version entfernt die ZIP-Release-Konfiguration für HACS. Der direkte GitHub-Release-Download schlug auf der betroffenen Home-Assistant-Installation weiterhin fehl. HACS fällt nach dem automatisch erzeugten GitHub-Archiv auf die einzeln von `raw.githubusercontent.com` geladenen Integrationsdateien zurück; diese Dateien wurden für die Version 0.2.2 vollständig geprüft.

Die Controller-Meldungen `Keepalive ping failed` betreffen die Verbindung zu den beiden Pumpencontrollern und nicht den HACS-Download. Sie werden separat behandelt, sobald die Installation abgeschlossen ist.
