from flask import Flask, request, abort, current_app, render_template
import subprocess
import signal
import sys
import os

app = Flask(__name__)

#Prevent cache problems
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 10000

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/router", methods=["GET", "POST"])
def myrouter():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    validate_coords(lat,lon)

    kill_process()
    proc = subprocess.Popen(["./main.py", "--lat", str(lat), "--lon", str(lon)])
    set_proc(proc)

    return "This is router.<br>lat=" + str(lat) + "<br> lon=" + str(lon)

def validate_coords(lat,lon):
    if lat<-90 or lat>90 or lon<-180 or lon>180:
        abort(400, "Invalid coordinates")


@app.route("/kill", methods=["GET", "POST"])
def graphic_kill():
    kill_process()
    return "Killed process"

@app.route("/shutdown", methods=["GET", "POST"])
def raspberry_shutdown():
    kill_process()  # first kill process before shutdown
    shutdown_raspberry()
    return "Killed process and Shutdown"

def shutdown_raspberry():
    os.system('sudo shutdown -h now')

def kill_process():
    # https://stackoverflow.com/a/17809718
    # https://docs.python.org/3/library/subprocess.html

    p = get_proc()

    old_pid = None
    if p != None and p.poll() == None: # poll() == None means process is still alive
        old_pid = str(p.pid)
        p.terminate() # send SIGTERM
        try:
            returncode = p.wait(timeout=3) # wait for SIGTERM taking effect
        except subprocess.TimeoutExpired: # if SIGTERM wasn't successful
            p.kill() # send SIGKILL


def get_proc():
    with app.app_context():
        return getattr(current_app, 'proc', None)

def set_proc(proc):
    current_app.proc = proc

def handle_signals(signum, frame):
    print("Received signal " + str(signum) + ". Going to stop routing process...")
    kill_process()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_signals)
signal.signal(signal.SIGTERM, handle_signals)
