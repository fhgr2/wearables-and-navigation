from flask import Flask, request, abort
from flask_voluptuous import expect, Schema, Required, All, Range, ALLOW_EXTRA
from voluptuous import *
import functools
import ast
from functools import update_wrapper

app = Flask(__name__)

# inspired by:
# - http://mitsuhiko.pocoo.org/flaskfun.pdf, p.43
# - https://github.com/ludusrusso/flask_voluptuous/blob/master/flask_voluptuous.py

def myexpect(schema):
    def decorator(f):
        #@functools.wraps(f)
        def wrapper(*args, **kargs):
            print("schema="+str(schema))
            args_original = request.args.to_dict()
            # TODO: read request.args item-by-item, with correct type from schema
            args_candidate = {}
#            for k,v in ast.literal_eval(str(schema)).items(): # schema is not a dict. maybe use https://stackoverflow.com/a/48828621 instead?
#                print("k=", k)
#                args_candidate[k] = request.args.get(k, type=v)
            print("args_candidate=" + str(args_candidate))
            print("args_original=" + str(args_original))
            print("args_filtered" + str(schema(args_original)))
            try:
                args_filtered = schema(args_candidate)
                kargs.update(args_filtered)
            except Invalid as e:
                abort(406, str(e))
            #kargs["args"] = args_filtered
            return f(*args, **kargs)
        return update_wrapper(wrapper, f)
    return decorator

@app.route('/')
def index():
    return 'Hello, World!'

@app.route("/router")
@myexpect(Schema({
    #"lat": All(float, Range(min=-90, max=90)),
    #'lat': All(str,str),
    #'lon': All(str,str),
    'lat': float,
    'lon': float,
    #"lon": All(int, Range(min=-180, max=180)),
    #Required("lat"): All(int, Range(min=-90, max=90)),
    #Required("lon"): All(int, Range(min=-180, max=180)),
}, extra=REMOVE_EXTRA))
def myrouter(lat: float, lon: float):
    print("type(lat)=" + str(type(lat)))
    print("request=" + str(request))
    print("request.args=" + str(getattr(request,"args")))
    print("request.json=" + str(request.get_json()))
    #print("schema(req)=" + schema(request.args.to_dict()))
    lat = request.args.get("lat", "")
    lon = request.args.get("lon", "")
    #validate_router_params(request.args)
    return "This is router. lat=" + lat + " and lon=" + lon

def validate_router_params(params):
    print(params)
    schema = Schema({
        Required("lat"): All(int, Range(min=-90, max=90)),
        Required("lon"): All(int, Range(min=-180, max=180)),
    }, extra=ALLOW_EXTRA)
    schema(params)



