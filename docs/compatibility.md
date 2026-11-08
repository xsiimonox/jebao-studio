# Produktprofile und Erweiterung

Der Treiber trennt Protokoll, Produktdefinition und HA-Entitäten. `models/<product_key>.json` definiert das Telegrammlayout. `models/device_configs.json` legt explizit fest, welche Attribute als Schalter, Zahlen, Auswahlfelder und Fehleranzeigen angeboten werden. Es gibt keine pauschale Freigabe für alle Modelle eines Marketingnamens.

MLW nutzt je nach Controllergeneration die lokalen Wavemaker-Profile `1d8c63eaccac4205b92c84d77d5a08fb`, `f0d844ab0d4947ac9527a286160bc705` oder die WLAN/BLE-Plattform `54114ccdac1e41c0bb17e222887c07ba`. Die genaue Zuordnung muss die Discovery liefern. Das Pro-Profil `50dbc92221fd4d33ae69a1fedd43b555` ist ebenfalls enthalten. Diese Keys sind keine Zusicherung, dass jede MLW-/DMP-Firmware dieselben Datenpunkte nutzt.

Weitere enthaltene Profile betreffen alte Wavemaker, Rückförderpumpen, einen LED-Typ und Dosierpumpen. DMP-Bluetooth wird ausdrücklich nicht anhand ähnlicher Modusnamen auf ein WLAN-Profil umgebogen. Die vorhandene Lichtplattform stammt aus dem Unterbau und ist kein Schwerpunkt der Studio-Oberfläche.

Bei unbekanntem Gerät:

1. Debug-Protokoll für `custom_components.jebao_studio` aktivieren und Einrichtung erneut versuchen.
2. Produkt-Key und Controller-Modell identifizieren. Debug-Logs vor dem Teilen prüfen: Sie enthalten unter anderem Geräteadressen, Kennungen und Statuswerte. Anmeldepakete und Cloud-Anmeldeantworten werden nicht als Rohdaten protokolliert.
3. Belegtes Produktschema und Transport bestimmen. Fremde oder unbekannte Controller bekommen keine geratenen Byte-Offets.
4. Passendes Profil mit expliziter Attributfreigabe ergänzen. Grenzwerte und Moduszuordnung gegen Schema und echte Antworten prüfen.
5. Statusdekodierung, Schreibtelegramme und Hardwareverhalten testen; Unterstützungsstatus dokumentieren.

## Dosierpumpen

Profile für mehrere WLAN-Dosiergenerationen sind bereits vorhanden. In dieser Version erzeugen sie keine Schalter, Zahlen- oder Auswahlentitäten und der Geräteadapter verweigert Dosier-Schreibbefehle. Status-/Fehler- und vorhandene Zeitplansensoren können erscheinen. Es gibt keine eigenen Dosierpläne, Kalibrierung oder manuelle Mengendosierung. Diese Funktionen benötigen pro Modell geprüfte Mengen-/Zeitkodierung und Hardwaretests.

## Netzwerk und Fehler

Broadcast-Discovery funktioniert gewöhnlich nur im selben Subnetz. Bei VLANs IP-Einrichtung verwenden und UDP 12414 sowie TCP 12416 gezielt erreichbar machen. Keine Routerports ins Internet öffnen. Ist das Produktprofil unbekannt, im HA-Protokoll nach `No device definition` suchen.

Bei geänderter IP sucht der Treiber die bekannte UID erneut. Eine DHCP-Reservierung bleibt sinnvoll. Cloud ist optional und keine automatische Ausweichroute; Zugangsdaten werden nur bei expliziter Einrichtung gespeichert. Diagnoseexporte der Integration enthalten keine Zugangsdaten, IPs, MACs oder UIDs.
