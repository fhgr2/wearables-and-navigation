routing = {
    "poi_reached_threshold"         : 20, # consider a poi reached, when distance is smaller than this value in meters
    "destination_reached_threshold" : 20, # consider destination reached, when distance is smaller than this value in meters
    "wrong_way_threshold"           : 32  # consider being on a wrong way when the distance is larger than this value in meters
    # TODO: maybe use better logic which includes the current speed
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
