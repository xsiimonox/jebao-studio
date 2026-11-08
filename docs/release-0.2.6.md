# Jebao Studio 0.2.6

Behebt den Schreibstatus für WLAN-Strömungspumpen: Die Antwort auf einen erfolgreichen 0x93/0x94-Controllerbefehl enthält den resultierenden Gerätestatus. Dieser wurde zuvor verworfen. Home Assistant zeigte dadurch weiter den alten Wert an, bis ein späterer Statusabruf eintraf.

Leistung, Modus und Schalter übernehmen jetzt den vom Controller bestätigten Wert sofort. Die neue Prüfung simuliert eine Leistungsänderung und stellt sicher, dass der Status an die Home-Assistant-Entitäten weitergegeben wird.
