#!/bin/bash

export FLASK_APP=flask-app.py
export FLASK_DEBUG=0 # automatically reload changes from files
python3 -m flask run
