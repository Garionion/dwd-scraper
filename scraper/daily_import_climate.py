#! /usr/bin/env python3

import psycopg2
import requests
import io
import zipfile
import datetime
from config.db import db as config_db

def cleanup_value(v):
    if int(v) == -999:
        return None

    return v

conn = psycopg2.connect(config_db["uri"])
cur = conn.cursor()

cur.execute("SELECT min(dwd_last_update) FROM stations;")
last_date = cur.fetchall()[0][0]
print(last_date)

if not last_date is None:
    cur.execute("SELECT id, name, lat, lon, dwd_id, dwd_last_update FROM stations WHERE dwd_last_update = %s LIMIT 1;", [last_date])
else:
    cur.execute("SELECT id, name, lat, lon, dwd_id, dwd_last_update FROM stations WHERE dwd_last_update IS NULL LIMIT 1;")
last_station = cur.fetchone()
print(last_station)

curr_station_id = last_station[0]
curr_station_dwd_id = last_station[4]

print(curr_station_dwd_id)
r = requests.get('https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/recent/tageswerte_KL_' + str(curr_station_dwd_id) + '_akt.zip', stream=True)
print(r.url)
if r.status_code == 200:
    zip = zipfile.ZipFile(io.BytesIO(r.content))
    files = zip.namelist()
    print(files)
    files_climate = [f for f in files if f.startswith("produkt_klima_")]
    print(files_climate)


    buffer = []

    is_first_line = True

    for line in zip.open(files_climate[0]):
        l = line.decode('utf-8').strip()
        if is_first_line:
            is_first_line = False
            continue

        b = {}

        b["dwd_id"], l = l.strip().split(";", 1)
        b["dwd_id"] = str(b["dwd_id"])
        b["date"], l = l.strip().split(";", 1)
        b["date"] = str(b["date"])
        b["date"] = datetime.date(int(b["date"][0:4]), int(b["date"][4:6]), int(b["date"][6:8]))
        b["qn_3"], l = l.strip().split(";", 1)
        b["qn_3"] = cleanup_value(int(b["qn_3"]))
        b["fx"], l = l.strip().split(";", 1)
        b["fx"] = cleanup_value(float(b["fx"]))
        b["fm"], l = l.strip().split(";", 1)
        b["fm"] = cleanup_value(float(b["fm"]))
        b["qn_4"], l = l.strip().split(";", 1)
        b["qn_4"] = cleanup_value(int(b["qn_4"]))
        b["rsk"], l = l.strip().split(";", 1)
        b["rsk"] = cleanup_value(float(b["rsk"]))
        b["rskf"], l = l.strip().split(";", 1)
        b["rskf"] = cleanup_value(int(b["rskf"]))
        b["sdk"], l = l.strip().split(";", 1)
        b["sdk"] = cleanup_value(float(b["sdk"]))
        b["shk_tag"], l = l.strip().split(";", 1)
        b["shk_tag"] = cleanup_value(float(b["shk_tag"]))
        b["nm"], l = l.strip().split(";", 1)
        b["nm"] = cleanup_value(float(b["nm"]))
        b["vpm"], l = l.strip().split(";", 1)
        b["vpm"] = cleanup_value(float(b["vpm"]))
        b["pm"], l = l.strip().split(";", 1)
        b["pm"] = cleanup_value(float(b["pm"]))
        b["tmk"], l = l.strip().split(";", 1)
        b["tmk"] = cleanup_value(float(b["tmk"]))
        b["upm"], l = l.strip().split(";", 1)
        b["upm"] = cleanup_value(float(b["upm"]))
        b["txk"], l = l.strip().split(";", 1)
        b["txk"] = cleanup_value(float(b["txk"]))
        b["tnk"], l = l.strip().split(";", 1)
        b["tnk"] = cleanup_value(float(b["tnk"]))
        b["tgk"], l = l.strip().split(";", 1)
        b["tgk"] = cleanup_value(float(b["tgk"]))

        #print(b)
        print(curr_station_id, b["date"].isoformat())

        cur.execute("SELECT id FROM climate WHERE station = %s AND date = %s; ", [curr_station_id, b["date"].isoformat()])
        if cur.rowcount == 0:
            cur.execute("INSERT INTO climate (station, date, qn_3, fx, fm, qn_4, rsk, rskf, sdk, shk_tag, nm, vpm, pm, tmk, upm, txk, tnk, tgk) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
            [curr_station_id, b["date"].isoformat(), b["qn_3"], b["fx"], b["fm"], b["qn_4"], b["rsk"], b["rskf"], b["sdk"], b["shk_tag"], b["nm"], b["vpm"], b["pm"], b["tmk"], b["upm"], b["txk"], b["tnk"], b["tgk"]])
            print("imported")
        else:
            print("ignored")

cur.execute("UPDATE stations SET dwd_last_update = %s WHERE id = %s;", [datetime.datetime.today().isoformat(), curr_station_id])
conn.commit()


cur.close()
conn.close()
