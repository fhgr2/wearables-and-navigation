#!/bin/bash

# Attention: Umlauts in file names won't work, see e.g. https://github.com/gpsbabel/gpsbabel/issues/38

if [ "$#" -ne 2 ]; then
	echo "Syntax: $0 infile.gpx outfile.nmea"
	exit 1
fi

gpsbabel -i gpx -f $1 -x track,fix=3d -o nmea -F $2
