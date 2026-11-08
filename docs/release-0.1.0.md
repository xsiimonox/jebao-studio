Jebao Studio 0.1.0 ist die erste öffentliche, experimentelle Version der Home-Assistant-Integration.

Enthalten sind lokale WLAN-Steuerung für bekannte Jebao-Aqua-Controllerprofile, optionale Cloud-Steuerung, native HA-Entitäten, deutsche Einrichtung, Diagnoseexporte und eine erweiterbare Produktprofilbasis. Der WLAN-Unterbau basiert auf dem MIT-lizenzierten Projekt von chrisc123; Lizenzen und Herkunft sind im Repository dokumentiert.

**Unterstützungsgrenzen:** DMP mit reinem Bluetooth ist derzeit ausschließlich für GATT-Diagnose vorbereitet und noch nicht steuerbar. Dosierpumpenprofile sind vorbereitet, ihre Steuerung ist gesperrt. Hardwaretests stehen aus. Nicht jeder Jebao-Controller wird unterstützt.

Installation über HACS als benutzerdefiniertes Repository: `https://github.com/xsiimonox/jebao-studio`, Kategorie Integration. Danach Home Assistant neu starten und Jebao Studio unter Geräte & Dienste hinzufügen. Alternativ das beigefügte ZIP im HA-Konfigurationsverzeichnis entpacken; enthalten ist bereits der Pfad `custom_components/jebao_studio/`.

Voraussetzung: Home Assistant Core 2026.10.1 oder neuer. Native HA-Tests prüfen Einrichtung, Entitäten, Service-Aufrufe und Entladen mit simulierten Geräten. Ein Hardwaretest ist damit nicht ersetzt.

- [Installation und Updates](https://github.com/xsiimonox/jebao-studio/blob/main/docs/installation.md)
- [Kompatibilität](https://github.com/xsiimonox/jebao-studio/blob/main/docs/compatibility.md)
- [DMP-Bluetooth-Diagnose](https://github.com/xsiimonox/jebao-studio/blob/main/docs/bluetooth.md)
