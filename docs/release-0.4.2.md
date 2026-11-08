# Jebao Studio 0.4.2

Die schematische Vorschau verwendet jetzt die tatsächliche Richtung des
MLW-Frequenzparameters: kleine Werte = schnelle Wellen, große Werte = langsame
Wellen. Das gilt für Sinus und Puls. Die an den Controller gesendeten Werte
werden nicht invertiert; sie entsprechen weiterhin der Jebao-App. Ein Hinweis
am Regler erklärt die Richtung. Die Vorschau ist keine kalibrierte Hz-Messung.

Für lokale Flow-, Frequency- und Mode-Schreibbefehle gibt es maximal drei
Versuche mit neuen Sequenznummern. Volle ACK-Statusantworten werden geprüft.
Bei kurzen ACKs wird der Status abgefragt. Bei ausbleibender Bestätigung wird
nach einer kurzen Pause zurückgelesen, bevor erneut gesendet wird; ein verspätet
bestätigter Wert verhindert unnötige Wiederholungen. Nach drei erfolglosen
Versuchen bleibt ein Fehler sichtbar. Die Vorgänge bleiben je Controller
serialisiert. Ein/Aus und Fütterung werden nicht automatisch wiederholt.

Bei gemeldetem Programm-Modus bricht das lokale Backend manuelle Flow-,
Frequency- und Mode-Befehle mit einem Hinweis auf Manual ab. Es schaltet nicht
eigenmächtig die Betriebsart um. Cloud-Schreibbefehle verwenden weiterhin den
vorhandenen Cloud-Pfad.

Tests decken vorübergehende Ablehnung, verzögertes Readback, Programm-Modus und
die Richtung beider Wellenformen ab. Die Hardware-Akzeptanz ist vor Ort zu prüfen.
