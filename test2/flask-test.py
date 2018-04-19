from flask import Flask, request, abort, current_app
import subprocess

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

    old_proc = get_proc()
    old_pid = None
    if old_proc != None and old_proc.poll() == None: # poll() == None means process is still alive
        old_pid = str(old_proc.pid)
        old_proc.terminate() # send SIGTERM
        try:
            returncode = old_proc.wait(timeout=3) # wait for SIGTERM taking effect
        except subprocess.TimeoutExpired: # if SIGTERM wasn't successful
            old_proc.kill()

    proc = subprocess.Popen(["./announcer-test.py", "myarg"])
    set_proc(proc)

    return "This is router.<br>lat=" + str(lat) + "<br> lon=" + str(lon) + "<br> old_proc=" + str(old_proc) + "<br> proc=" + str(proc) + "<br> pid=" + str(proc.pid) + "<br> old_pid=" + str(old_pid)


def validate_coords(lat,lon):
    if lat<-90 or lat>90 or lon<-180 or lon>180:
        abort(400, "Invalid coordinates")


def get_proc():
    return getattr(current_app, 'proc', None)

def set_proc(proc):
    current_app.proc = proc
