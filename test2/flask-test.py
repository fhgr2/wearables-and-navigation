from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route("/router")
def myrouter():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    validate_coords(lat,lon)
    return "This is router. lat=" + str(lat) + " and lon=" + str(lon)

def validate_coords(lat,lon):
    if lat<-90 or lat>90 or lon<-180 or lon>180:
        abort(400, "Invalid coordinates")



