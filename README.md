# DWD Scraper
Importiert Messdaten aus dem OpenData Programm des DWD in eine Datenbank.

## Quellen
Der Datenbestand von Wetter stammt vollständig aus dem Open-Data Programm des Deutschen Wetterdienstes. Dort laden wir regelmäßig direkt die Messergebnisse herunter und pflegen diese in unser System ein. Nach und nach aktualisiert der DWD einige Messergenisse duch Fehlerkorrekturverfahren. Auch diese pflegen wir im Laufe der Zeit nach.

Alles zu diesem Datensatz findet sich unter https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/recent/

Dieses Projekt benutzt die selben Bezeichner, wie die Datensätze selber. Eine Dokumentation der Bezichner findet sich unter https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/recent/BESCHREIBUNG_obsgermany_climate_daily_kl_recent_de.pdf

## Datenbank
Als Datenbank wird PostgreSQL verwendet und das Datenbankschema liegt unter `sql/wetter.sql`.

Zugangsdaten für die Datenbank müssen unter `scraper/config/db.py` abgelegt werden, das entsprechende Format ist unter `scraper/config/db.py.example` hinterlegt.

## Scraper
Als erstes müssen die Stationen importiert werden.
```
./scraper/daily_import_stations.py
```

Anschließend können darauf die Messergebnisse für die importierten Stationen eingelesen werden.
```
./scraper/daily_import_climate.py
```
