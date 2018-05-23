from flask import Flask, request, abort, current_app
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World! To start routing call something like: http://127.0.0.1:5000/router?lat=46.85449&lon=9.52864'


@app.route("/router")
def myrouter():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    validate_coords(lat,lon)

    kill_process(get_proc())
    proc = subprocess.Popen(["./main.py", "--lat", str(lat), "--lon", str(lon)])
    set_proc(proc)

    return "This is router.<br>lat=" + str(lat) + "<br> lon=" + str(lon)

def validate_coords(lat,lon):
    if lat<-90 or lat>90 or lon<-180 or lon>180:
        abort(400, "Invalid coordinates")

def kill_process(p):
    # https://stackoverflow.com/a/17809718
    # https://docs.python.org/3/library/subprocess.html

    old_pid = None
    if p != None and p.poll() == None: # poll() == None means process is still alive
        old_pid = str(p.pid)
        p.terminate() # send SIGTERM
        try:
            returncode = p.wait(timeout=3) # wait for SIGTERM taking effect
        except subprocess.TimeoutExpired: # if SIGTERM wasn't successful
            p.kill() # send SIGKILL


def get_proc():
    return getattr(current_app, 'proc', None)

def set_proc(proc):
    current_app.proc = proc
