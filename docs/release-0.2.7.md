# Jebao Studio 0.2.7

## Strömung auf einen Blick

Die Oberfläche für WLAN-Strömungspumpen wurde vollständig neu gestaltet:

- Grafisches Wellenbild pro Pumpe, das Intensität und Frequenz abbildet.
- Eigene Regler für Strömungsintensität und Wellenfrequenz.
- Klarer Wellenmodus-Selektor mit lesbaren deutschen Bezeichnungen.
- Status, Verbindung, Fütterungspause und Ein/Aus direkt auf der Pumpenkarte.

## Gruppensteuerung

Pumpen können als Strömungsgruppe zusammengefasst werden. Intensität, Frequenz,
Wellenmodus sowie Ein/Aus werden dann als synchroner Befehl an alle erreichbaren
Gruppenmitglieder gesendet.

Bluetooth-/DMP-Controller bleiben bewusst in einer getrennten Diagnoseansicht,
bis ihr Steuerprotokoll verifiziert ist.
