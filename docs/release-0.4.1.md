# Jebao Studio 0.4.1

MLW-Controller verwenden `TimerON` für den Gerätezeitplan: `on` = Programm,
`off` = Manual. Die Betriebsart steht nun direkt auf der Pumpenkarte und lässt
sich dort umschalten. Gespeicherte Programme werden dabei nicht bearbeitet.

Bei aktivem Programm erscheint ein Hinweis mit einer Schaltfläche zum Wechsel
auf Manual. Manuelle Leistungs-/Frequenz- und Wellenmodusregler sind gesperrt,
solange der Controller das Geräteprogramm als aktiv meldet. Ein/Aus und
Fütterung bleiben bedienbar. Änderungen aus Jebao Aqua werden über die normalen
HA-Statusupdates sichtbar. Ohne verfügbaren TimerON-Status wird keine Betriebsart
erfunden; die Erkennung gilt für Controllerprofile mit diesem Attribut.

Gruppen erkennen erreichbare Pumpen im Programm-Modus und bieten das Umschalten
auf Manual gemeinsam an. Es findet kein automatischer Wechsel ohne Nutzeraktion
statt.

Außerhalb des Studios ist die Umschaltung weiterhin mit der vorhandenen
HA-Schalterentität „Gerätezeitplan“ möglich: Ausschalten für Manual,
Einschalten für Programm. Dadurch können auch Automationen die Betriebsart setzen.
