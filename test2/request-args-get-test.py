# https://teamtreehouse.com/community/what-does-requestargsget-return

from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/')
def index(name=""):
   # for example, try ?name=1.0
    name = request.args.get('name', type=float)
    print("name="+ str(name))
    return "You entered a query string of {}, and request.args.get returned it as a {}, of course!".format(name, type(name).__name__)

