from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route("/router")
def router():
    lat = request.args.get("lat", "")
    lon = request.args.get("lon", "")
    return "This is router. lat=" + lat + " and lon=" + lon
