# Notizen Wearables Projekt

## fake gpsd verwenden

### Daten aufbereiten

Anhand einer GPX-Datei sollen Fake-GPS Daten erstellt werden. Dazu muss die GPX-Datei ins NMEA-Format konvertiert werden:

   ./gpx2nmea.sh infile.gpx outfile.nmea 

### Signal einspeisen

    gpsfake -c 1 -P 55555 feldis-brambrueesch-2011-09-03-161919.nmea

### Signal abholen

    cgps localhost:55555

bzw.

    read-gpsd.py
   

## Flask

Flask ist ein in Python geschriebenes Webframework. Den eingebauten Webserver können wir wie folgt starten:

Für die Entwicklung:


```bash
export FLASK_APP=flask-test.py
export FLASK_DEBUG=1 # automatically reload changes from files
python3 -m flask run
```

Für den Betrieb:


```bash
export FLASK_APP=flask-test.py
python3 -m flask run --host=0.0.0.0
```

### Links

- Über background tasks: https://stackoverflow.com/questions/22615475/flask-application-with-background-threads/39008301
- requests.args.get gibt immer Strings zurück: https://teamtreehouse.com/community/what-does-requestargsget-return

