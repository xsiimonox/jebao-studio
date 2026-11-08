# Jebao Studio 0.2.3

HACS lädt jetzt die fertig gepackte Release-Datei `jebao_studio.zip`. Damit entfällt die automatische GitHub-Archiv-Erzeugung über `/archive/refs/tags/…` und der Ausweichversuch über `/archive/refs/heads/…`. Für diese Archiv-Downloads wurden HTTP 502 und 504 gemeldet.

Das HACS-Paket enthält `manifest.json` direkt im ZIP-Hauptverzeichnis. HACS entpackt es in den Integrationsordner. Für die manuelle Installation bleibt separat `jebao-studio-0.2.3.zip` mit dem Pfad `custom_components/jebao_studio/` verfügbar. Beide Pakete enthalten denselben Integrationsstand inklusive der Panel- und Icon-Korrekturen aus 0.2.2.

In HACS die Repository-Informationen aktualisieren, 0.2.3 herunterladen und Home Assistant neu starten. Ein GitHub-Netzwerkproblem kann weiterhin auch den direkten Release-Dateidownload beeinträchtigen; in diesem Fall ist der neue Fehlertext für die Diagnose erforderlich.
