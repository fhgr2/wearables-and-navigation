from flask import Flask, request, abort, current_app

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'


@app.route("/router")
def myrouter():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    validate_coords(lat,lon)

    # alten prozess ggf. terminieren (wie speichert man dessen pid?)
    # neuen prozess starten
    # gute anleitung: https://stackoverflow.com/a/17809718
    # rtfm: https://docs.python.org/3/library/subprocess.html

    old_lat = get_lat()

    set_lat(lat)

    return "This is router. lat=" + str(lat) + " and lon=" + str(lon) + " and old_lat=" + str(old_lat)


def validate_coords(lat,lon):
    if lat<-90 or lat>90 or lon<-180 or lon>180:
        abort(400, "Invalid coordinates")


def get_lat():
    return getattr(current_app, 'lat', None)


def set_lat(lat):
    current_app.lat = lat

