# DWD Scraper
Importiert Messdaten aus dem OpenData Programm des DWD in eine Datenbank.

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
