#!/usr/bin/env python3

# pip3 install gpsd-py3
import gpsd

# Connect to the local gpsd
#gpsd.connect()

# Connect somewhere else
gpsd.connect(host="127.0.0.1", port=55555)

# Get gps position
packet = gpsd.get_current()

# See the inline docs for GpsResponse for the available data: https://github.com/MartijnBraam/gpsd-py3/blob/master/DOCS.md
print("position()=" + str(packet.position()))
print("track=" + str(packet.track))
