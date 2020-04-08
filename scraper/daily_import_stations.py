#!/usr/bin/env python3


import requests
import io
import psycopg2
from config.db import db as config_db

r = requests.get('https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/recent/KL_Tageswerte_Beschreibung_Stationen.txt', stream=True)

print(r)

if r.status_code == 200:

    f = r.iter_lines(decode_unicode=True)

    buffer = []

    is_first_line = True
    is_second_line = True

    for l in f:
        if l:
            if is_first_line:
                is_first_line = False
                continue
            if is_second_line:
                is_second_line = False
                continue

            l = str(l)

            b = {}

            print(l)

            b["station_id"], l = l.strip().split(" ", 1)
            b["station_id"] = str(b["station_id"])
            b["date_from"], l = l.strip().split(" ", 1)
            b["date_from"] = int(b["date_from"])
            b["date_to"], l = l.strip().split(" ", 1)
            b["date_to"] = int(b["date_to"])
            b["sea_level"], l = l.strip().split(" ", 1)
            b["sea_level"] = int(b["sea_level"])
            b["lat"], l = l.strip().split(" ", 1)
            b["lat"] = float(b["lat"])
            b["lon"], l = l.strip().split(" ", 1)
            b["lon"] = float(b["lon"])
            b["name"], l = l.strip().split("  ", 1)
            b["name"] = str(b["name"])
            b["state"] = l.strip()
            b["state"] = str(b["state"])

            if b["date_to"] >= 20200000:
                """
                Im OpenData Programm sind auch Stationen enthalten, die nicht mehr betrieben werden. Wir importieren nur Stationen, die in diesem Jahr schon Werte geliefert haben.
                """
                print(b["station_id"])
                print(b["date_from"])
                print(b["date_to"])
                print(b["sea_level"])
                print(b["lat"])
                print(b["lon"])
                print(b["name"])
                print(b["state"])
                print()

                buffer.append(b)
            else:
                print("ignore station " + str(b["station_id"]))
                print()

    print(buffer)

    conn = psycopg2.connect(config_db['uri'])
    cur = conn.cursor()

    for b in buffer:
        cur.execute("SELECT * FROM stations WHERE dwd_id LIKE %s;", [str(b["station_id"])])
        if cur.rowcount == 0:
            cur.execute("INSERT INTO stations (name, lat, lon, dwd_id, state, sea_level) VALUES (%s, %s, %s, %s, %s, %s);", [b["name"], b["lat"], b["lon"], b["station_id"], b["state"], b["sea_level"]])
        else:
            cur.execute("UPDATE stations SET name = %s, lat = %s, lon = %s, state = %s, sea_level = %s WHERE dwd_id LIKE %s", [b["name"], b["lat"], b["lon"], b["state"], b["sea_level"], b["station_id"]])

        conn.commit()

    cur.close()
    conn.close()
