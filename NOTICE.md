# Herkunft und Änderungen

Jebao Studio enthält abgeleiteten Code aus:

- https://github.com/chrisc123/jebao_aqua-homeassistant
- Stand: `76f98ea0746af2fb3beb53c99ca439cd6f252e7a`
- Lizenz: MIT, Copyright (c) 2024–2026 Chris Cole (chrisc123) and contributors.
- Übernommen: HA-Plattformen, Konfigurations-/Optionsfluss, Gizwits-LAN- und Cloud-Treiber, Produktdefinitionen, englische/spanische Übersetzungen und ursprüngliche Tests.
- Änderungen: Domain/Name, Studio-Seitenleiste, authentifizierter Gerätekatalog, deutsche Einrichtung und zentrale Entitätsnamen, Bluetooth-GATT-Diagnose, Dosiersteuerungssperre, Konfigurations-Nachladen bei neuen Geräten, getrennte LAN-/Cloud-Einträge, eindeutige Befehlssequenzen, Begrenzung der TCP-Paketlänge, Produkt-Key-Prüfung, strengere Zahlenvalidierung, Diagnoseexport, Tests und Paketbau.

Die vollständige Lizenz liegt in `LICENSE` und in der ausgelieferten Integration. Studio-Erweiterungen werden ebenfalls unter MIT bereitgestellt. Keine offizielle Jebao-Software; keine Mitautorenschaft oder Wartung durch die ursprünglichen Autoren behauptet.

Die zwei binären Testfixtures `tests/fixtures/switchon_*.bin` stammen unverändert aus:

- https://github.com/markosharknz1/ha-jebao-pumps
- Verzeichnis `fixtures/captured_writes/`
- MIT, Copyright (c) 2026 markosharknz1; vollständiger Text: `licenses/capture-fixtures-MIT.txt`.
- Herkunft laut Referenzprojekt: offizielle App-Logcat-Ausgaben, abgeschnittene Telegramme. Nur der sichtbare Payload-Präfix wird geprüft; keine vollständige Hardwarevalidierung.
