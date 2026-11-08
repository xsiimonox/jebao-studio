# Änderungen

## 0.2.2

- Versionsgebundener Import der Panel-Hilfsdatei verhindert eine leere Seite durch alte Browser-Module nach dem Update.
- Lokale Home-Assistant-Markenbilder unter `brand/icon.png` und `brand/logo.png` ergänzen die Integrationskachel, einschließlich dunkler und hochauflösender Fallbacks.
- Pumpenkarten erscheinen bereits vor Abschluss der optionalen Gruppen-Abfrage.
- Gruppen-Modusauswahl, Bearbeiten/Löschen und Bluetooth-Diagnose aus 0.2.0 wiederhergestellt.
- Neue Regressionstests reproduzieren den Modulfehler beim Upgrade und prüfen die echte HA-Bildauflösung.

## 0.2.1

- Pumpenkarten laden unabhängig von der Gruppen-API und bleiben auch bei einem verzögerten Home-Assistant-Neustart sichtbar.
- Das Logo wird relativ zum Panel-Modul geladen und erscheint damit zuverlässig in Home Assistant und der Vorschau.

## 0.2.0

- Neues Jebao-Studio-Logo und überarbeitete, auf Strömung ausgerichtete Oberfläche.
- Permanente Pumpengruppen direkt in der Studio-Seitenleiste erstellen, bearbeiten und löschen.
- Gemeinsame Ein/Aus-, Fütterungs-, Leistungs- und Modussteuerung für kompatible, erreichbare Pumpen.
- Übersicht mit Online-Pumpen, gespeicherten Gruppen und Fehlerstatus.

## 0.1.0

Erste öffentliche, experimentelle Version von Jebao Studio.

- Eigene authentifizierte HA-Seitenleiste mit Pumpen-, Dosierstatus- und Bluetooth-Ansicht.
- Lokale WLAN-Einrichtung über Suche oder IP; optionale Gizwits-Cloud-Verbindung.
- Native Schalter, Zahlen, Modusauswahl und Fehleranzeigen nach Produktprofil.
- 18 Produktdefinitionen aus dem MIT-lizenzierten Jebao-Aqua-Unterbau.
- DMP-Bluetooth-Einrichtung zur GATT-Diagnose. Noch keine DMP-Steuerung.
- Dosierpumpenprofile vorbereitet; Aktorsteuerung für Dosierer gesperrt.
- Deutsche Einrichtung, Diagnoseexport, Installations- und Protokolldokumentation.
- Regressionstests, Home-Assistant-Schnittstellentests und Installationspaket.

Hardwaretests stehen aus. Nicht alle Jebao-Controller werden unterstützt. Ein eigener Zeitplan-Editor ist noch nicht enthalten.
