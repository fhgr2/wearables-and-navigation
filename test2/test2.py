#!/usr/bin/env python3

# pip3 install shapely pyproj

# optional mit fiona kombinieren

import argparse
import pyproj
from shapely.ops import transform
from shapely.geometry import Point, LineString

def main(args):
	bhf84 =        Point(9.527022,46.853450) # lon,lat
	medienhaus84 = Point(9.501288,46.847791)
	churwest84   = Point(9.512751,46.849981)

	bhf_medienhaus84 = LineString([bhf84, medienhaus84])

	bhf_medienhaus = wgs84ToLv95(bhf_medienhaus84)

	print("bhf_medienhaus = " + str(bhf_medienhaus))
	print("Länge = " + str(bhf_medienhaus.length))
	print("abstand churwest <-> luftlinie(bhf,medienhaus) = " + str(wgs84ToLv95(churwest84).distance(bhf_medienhaus)));


# according to https://gis.stackexchange.com/a/127432
def wgs84ToLv95(old):
	project = lambda x, y: pyproj.transform(pyproj.Proj(init='epsg:4326'), pyproj.Proj(init='epsg:2056'), x, y)
	return transform(project,old)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    args = parser.parse_args()

main(args)
