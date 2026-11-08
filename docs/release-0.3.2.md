# Jebao Studio 0.3.2

Der Gizwits-Payload-Builder erhält jetzt die zuletzt empfangenen Nachbarwerte
im Steuerblock, statt sie mit Nullen zu überschreiben. Flags wählen weiterhin
nur die ausdrücklich geänderten Attribute aus. Zahlen und Enum-Indizes werden
vor dem Socket-Schreibzugriff gegen das Produktprofil geprüft.

Eine vollständige ACK-Statusantwort wird übernommen und mit dem Sollwert
verglichen. Bestätigt der Controller den Wert nicht, meldet der Dienst einen
Fehler; das optimistische Entity-Update verdeckt diese Antwort nicht mehr.

MLW-Profil: W1=0, W2=1, Else=2, Konstant=3 in Bits 5–6 des
Big-Endian-Bitfelds. Leistung liegt an Statusoffset 2, Frequenz an Offset 3.
Fütterung verwendet FeedSwitch, nicht einen zusätzlichen Mode-Enumwert.
Der vorhandene Frame verwendet Magic, variable Länge, Flag, Kommando und
Payload; eine zusätzliche Prüfsumme ist durch die vorhandenen Mitschnitte
nicht belegt.

Validiert mit 30 Python-, 7 Panel- und 9 Home-Assistant-Tests einschließlich
Socket-/ACK-Simulation. Die reale Akzeptanz von Leistungs- und Modusbefehlen
ist weiterhin durch einen Test am Controller zu bestätigen. Vorhandene
offizielle Mitschnitte decken nur Ein/Aus ab.
