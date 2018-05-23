#!/usr/bin/env python3

import time
import signal
import sys
import openrouteservice # pip3 install openrouteservice

def handle_signals(signum, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, handle_signals)
signal.signal(signal.SIGTERM, handle_signals)



while True:
    time.sleep(10.1)
