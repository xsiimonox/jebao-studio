# Installation und Updates

Voraussetzung: Home Assistant Core **2026.10.1 oder neuer**. Eine Einrichtung der WLAN-Pumpen in Jebao Aqua muss bereits erfolgt sein. Home Assistant benötigt Zugriff auf UDP 12414 und TCP 12416 der Controller. Niemals diese Ports ins Internet weiterleiten.

## HACS

1. HACS → Menü → **Benutzerdefinierte Repositories** öffnen.
2. `https://github.com/xsiimonox/jebao-studio` eintragen, Kategorie **Integration**.
3. **Jebao Studio** herunterladen und Home Assistant neu starten.
4. **Einstellungen → Geräte & Dienste → Integration hinzufügen → Jebao Studio**.
5. **WLAN-Controller im Netzwerk suchen** oder die IP-Einrichtung wählen.
6. **Jebao Studio** in der Seitenleiste öffnen. Die Seitenleiste ist für Administratoren sichtbar.

Das Repository liefert `custom_components/jebao_studio` direkt aus. Der HACS-Standardkatalog ist nicht beantragt. Der nummerierte Release ist als experimentell dokumentiert und benötigt kein aktiviertes Beta-Repository.

## Manuell

Das ZIP aus [Releases](https://github.com/xsiimonox/jebao-studio/releases) herunterladen. Im Home-Assistant-Konfigurationsverzeichnis entpacken, sodass `/config/custom_components/jebao_studio/manifest.json` existiert. Keine zusätzliche Ebene wie `/config/custom_components/jebao-studio-0.1.0/custom_components/` anlegen. Danach HA neu starten und die Integration hinzufügen.

## Erste WLAN-Prüfung

Andere Integrationen für denselben Controller deaktivieren. Status und Modus zunächst mit dem Controller bzw. der App vergleichen. Eine einzelne Leistungsänderung innerhalb des erlaubten Wertebereichs ausführen und die Rückmeldung am Gerät prüfen. Die Integration sendet bei Einrichtung keine Leistungs- oder Modusänderung.

Der Gerätezeitplan-Schalter aktiviert einen bereits im Controller gespeicherten Plan; er ist kein eigener Planeditor. Verfügbare Modi und Grenzwerte stammen vom Produktprofil.

## DMP

Die Integration erneut hinzufügen und **Bluetooth-Diagnose** wählen. Der Eintrag dient ausschließlich der Vorbereitung des noch fehlenden BLE-Treibers. [Bluetooth-Anleitung](bluetooth.md).

## Updates

Vor Aktualisierungen HA-Backup erstellen. Über HACS aktualisieren oder den Integrationsordner durch die neue Release-Version ersetzen; anschließend HA neu starten. Konfigurierte Controller bleiben in Home Assistants Konfiguration gespeichert. Änderungen und Einschränkungen in den Release-Notizen beachten.

## Entfernen

Unter **Einstellungen → Geräte & Dienste** alle Jebao-Studio-Einträge entfernen. Danach die Integration in HACS entfernen oder den Ordner `custom_components/jebao_studio` löschen und HA neu starten. Das Entfernen löscht keine Programme im Pumpencontroller.
