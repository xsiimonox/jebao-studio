# DMP-Bluetooth-Diagnose

DMP mit reinem Bluetooth verwendet nicht automatisch das WLAN-Gizwits-Protokoll. Ein vorhandenes Wavemaker-Datenpunktschema verrät noch keine BLE-Authentifizierung, Paketstruktur, UUIDs oder Prüfsummen. Version 0.1.0 besitzt **keinen DMP-Steuerungstreiber** und sendet keine geratenen Steuertelegramme.

## Schnittstellen erfassen

1. In HA Bluetooth einrichten; bei ESPHome muss der Proxy aktive Verbindungen unterstützen und einen freien Verbindungsslot haben.
2. Jebao Aqua schließen, damit die App den Controller nicht belegt. Den Controller eingeschaltet lassen.
3. Jebao Studio hinzufügen → **Bluetooth-Diagnose**. Nur den eigenen DMP-Controller auswählen. Da der eindeutige Jebao-Advertising-Fingerabdruck noch unbekannt ist, enthält die Auswahl auch andere sichtbare BLE-Geräte. Bei Unklarheit die Adresse mit einem BLE-Scanner wie nRF Connect abgleichen.
4. Studio → **Bluetooth / DMP** → **Bluetooth-Schnittstellen auslesen**.
5. Die JSON-Datei enthält Service-UUIDs und Characteristic-UUIDs mit Eigenschaften. Das Auslesen verbindet sich vorübergehend mit dem Controller und fragt nur die GATT-Struktur ab. Es schreibt keine Characteristic-Werte und startet keine Pumpenbefehle.

Bluetooth-Adressen können unter macOS als UUID erscheinen. Für die Einrichtung in HA die von **HA** erkannte Adresse verwenden. Das Diagnosegerät erscheint im Studio, nicht als steuerbare HA-Pumpe.

## Steuerbefehle erfassen

Benötigt werden anschließend genaue DMP-Modellnummer/Firmware sowie ein Bluetooth-Mitschnitt aus der Jebao Aqua App. Bei Android lässt sich über die Entwickleroptionen ein **Bluetooth-HCI-Snoop-Protokoll** aufzeichnen und über einen Bugreport exportieren. Verfügbarkeit und Export hängen vom Telefon ab. Eine Alternative ist eine gezielte App-/SDK-Protokollanalyse.

Für den Mitschnitt jeweils Zeit und Aktion notieren: Verbindung herstellen, Ausgangswert ablesen, einmal Leistung ändern, Modus ändern und danach zum Ausgangswert zurückkehren. Keine zusätzlichen Veränderungen am Aquarium nur für die Aufzeichnung durchführen.

HCI- und Bugreport-Dateien können andere Bluetooth-Geräte, Kontodaten und persönliche Informationen enthalten. Für die Analyse nur den zu Jebao gehörenden Ausschnitt weitergeben. Ein GATT-JSON allein reicht normalerweise nicht für einen verifizierten Steuertreiber.

## Nächste Implementierung

Aus den Belegen werden UUID-Zuordnung, Authentifizierung, variable Datenpunktkodierung, Statusabfrage und bestätigte Schreibbefehle abgeleitet. Danach folgen Pakettests und ein kontrollierter Hardwaretest. Erst dann werden BLE-Entitäten und Automationen freigegeben.
