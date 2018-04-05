# Notizen Wearables Projekt

## Benötigte Software installieren

```bash
sudo apt install python-gps
pip3 install gpsd-py3
```

## fake gpsd verwenden

### Daten aufbereiten

Anhand einer GPX-Datei sollen Fake-GPS Daten erstellt werden. Dazu muss die GPX-Datei ins NMEA-Format konvertiert werden:

   ./gpx2nmea.sh infile.gpx outfile.nmea 

### Signal einspeisen

    gpsfake -c 1 -P 55555 feldis-brambrueesch-2011-09-03-161919.nmea

### Signal abholen

    cgps localhost:55555
