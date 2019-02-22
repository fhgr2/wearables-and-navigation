routing = {
    "poi_reached_threshold"         : 30,     # consider a poi reached, when distance is smaller than this value in meters
    "destination_reached_threshold" : 20,     # consider destination reached, when distance is smaller than this value in meters
    "wrong_way_threshold"           : 32,     # consider being on a wrong way when the distance is larger than this value in meters
    "bearings_tolerance"            : 100,    # in degress, see "bearings" at https://openrouteservice-py.readthedocs.io/en/latest/#module-openrouteservice.directions
    "allow_uturn"                   : "true", # allow routing engine to give uturn instruction
    "ors_routing_profile"           : "cycling-regular", # one of: cycling-regular, cycling-road, cycling-safe, cycling-mountain, cycling-tour, cycling-electric. In openrouteservice.org API version 4.7 do not use cycling-safe
    #"ors_routing_profile"           : "foot-walking", # foot-walking, foot-hiking
    "main_poll_interval"            : 1       # sleep this many seconds before fetching the current position again (may be a float)
}

vibration = {
    "impulsdauer" : 0.65, # Länge eines Impulses
    "nachpause"   : 0.1,  # Pause zwischen den einzelnen Impulsen
    "signalpause" : 1     # Pausenlänge in der Signalisierung
}

# enable/disable the different kind of announcers
announcers = {
    "log"   : True,
    "audio" : True,
    "vibra" : True
}

gpsd = {
    "ip"   : "127.0.0.1",
    "port" : 2947 # fake -> 55555 , real -> 2947
}
