#!/bin/bash

export FLASK_APP=flask-app.py
export FLASK_DEBUG=1 # automatically reload changes from files
python3 -m flask run
