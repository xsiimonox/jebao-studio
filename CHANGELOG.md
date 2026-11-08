# Änderungen

## 0.4.3

- HA-Diagnosedownload enthält die gecachten AutoTime-Zeitplanfelder als Hexdaten zur Protokollanalyse; keine Schreibbefehle oder Gerätekennungen.

## 0.4.2

- Wellenvorschau korrigiert: höhere Frequenz-Controllerwerte bedeuten langsamere Wellen.
- Leistung, Frequenz und Modus werden bei fehlender Bestätigung begrenzt wiederholt und zurückgelesen.
- Programm-Modus verhindert manuelle Reglerbefehle auch im lokalen Backend.

## 0.4.1

- Programm-/Manual-Betriebsart sichtbar auf der Pumpenkarte und direkt umschaltbar.
- Programm-Modus wird erkannt; Hinweis und Schutz der manuellen Regler verhindern widersprüchliche Bedienung.
- Gruppen erkennen Pumpen mit aktivem Geräteprogramm und bieten gemeinsame Umschaltung auf Manual.

## 0.4.0

- Stabile Attributzuordnung auch bei umbenannten oder übersetzten Entitäten.
- Fütterungsdauer, Fütterung beenden, Zeitplan, Kopplung und aktive Pumpenfehler im Studio.
- Gruppen prüfen jeden Controller vorab; gemischte Modi, Leistungsbereiche und Teilerfolge werden angezeigt.
- Schreibzugriffe je WLAN-Controller serialisiert; Fehler bei gleichnamigen Gruppen und geerbten Auswahlprofilen behoben.
- Browserprüfung für Desktop und Mobilgeräte inklusive echter UI-Interaktionen mit Beispieldaten.

## 0.3.3

- Slider und direkte Zahleneingabe für Leistung/Frequenz bei Einzelpumpen und Gruppen.
- Laufende Eingaben und Schreibbefehle werden gegen Neuzeichnen durch Statusupdates geschützt.
- Ausstehende Sollwerte bleiben kurz sichtbar, bevor der Controllerstatus wieder maßgeblich wird.

## 0.3.2

- Gizwits-Steuerblock erhält Nachbarwerte; vollständige ACK-Antworten werden auf den angeforderten Wert geprüft.
- Ungültige Zahlen und Moduswerte werden vor dem Senden abgelehnt.

## 0.3.1

- Leistungs- und Modusentitäten aktualisieren ihre Home-Assistant-Anzeige nach bestätigtem LAN-Befehl sofort.

## 0.3.0

- Vollständig überarbeitete, nativeartige Studio-Oberfläche mit ruhigem Wellen-Dashboard, großen Bedienelementen und klarer Gruppenansicht.

## 0.2.10

- Behebt MLW-Leistungs-, Frequenz- und Modusbefehle durch den kompakten Jebao-Steuerblock.

## 0.2.9

- Im Modus „Konstant“ wird keine Wellenfrequenz mehr angezeigt oder gesendet.

## 0.2.8

- Pumpenkarten laden unabhängig von einer langsamen oder fehlgeschlagenen Gruppenabfrage.

## 0.2.7

- Neue Strömungsoberfläche mit Live-Wellenbild für Intensität und Frequenz.
- Direkte Steuerung von Leistung, Frequenz und Wellenmodus pro Pumpe sowie synchron für Pumpengruppen.

## 0.2.6

- Übernimmt den Status aus der Controller-Antwort nach Schreibbefehlen für Leistung, Modus und Schalter.
- Verhindert, dass Home Assistant den vorherigen Wert nach einer bestätigten Änderung erneut anzeigt.

## 0.2.5

- Gespeicherte Controller bleiben bei fehlender Laufzeiteinrichtung im Studio sichtbar.
- Direkte Links zur Pumpensuche und zur Verwaltung bestehender Einträge im Panel.

## 0.2.4

- Der Release-ZIP-Download ist entfernt: Die HACS-Installation nutzt wieder die einzeln erreichbaren Repository-Dateien.
- Damit umgeht sie den Fehler beim Weiterleiten von GitHubs Release-Download auf der betroffenen Home-Assistant-Installation.

## 0.2.3

- HACS verwendet ein explizites, fertig gepacktes ZIP-Release anstelle der automatischen GitHub-Repository-Archive, deren Download mit HTTP 502/504 scheiterte.
- Getrennte Pakete für HACS (Integration im ZIP-Hauptverzeichnis) und manuelle Installation (`custom_components/jebao_studio/`).
- Installation beider Archive wird durch einen Extraktionstest auf identischen Inhalt geprüft.

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
