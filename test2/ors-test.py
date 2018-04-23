#!/usr/bin/env python3

import openrouteservice
from openrouteservice.directions import directions
from openrouteservice.directions import convert

coords = ((9.52864,46.85449),(9.50131,46.84811))

client = openrouteservice.Client(key='***REMOVED***')
routes = directions(client, coords, profile="cycling-safe", instructions="true", bearings=[[40,45]], continue_straight="true", optimized="false") # TODO: add further parameters, see https://openrouteservice-py.readthedocs.io/en/latest/#module-openrouteservice.directions

print("routes=" + str(routes))
print("geometry=" + str(convert.decode_polyline(routes['routes'][0]['geometry'])))
