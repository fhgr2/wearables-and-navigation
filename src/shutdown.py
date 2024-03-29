#!/usr/bin/python3
# shutdown/reboot Raspberry Pi mittels Taste

import RPi.GPIO as GPIO
import subprocess, time, sys, syslog, os

# GPIO-Port, an dem die Taste gegen GND angeschlossen ist
# GPIO 21, Pin 40 (GND waere daneben auf Pin 30)
PORT = 21

# Schwelle fuer Shutdown (in Sekunden), wird die Taste kuerzer
# gedruckt, erfolgt ein Reboot
T_SHUT = 3

# Entprellzeit fuer die Taste
T_PRELL = 0.05

uid = os.getuid()
if uid > 0:
  print ("Programm benoetigt root-Rechte!")
  syslog.syslog('shutdown.py nicht gestartet');
  sys.exit(0)

# GPIO initialisieren, BMC-Pinnummer, Pullup-Widerstand
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PORT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Zeitdauer des Tastendrucks
duration = 0

# Interrupt-Routine fuer die Taste
def buttonISR(pin):
  global duration

  if not (GPIO.input(pin)):
    # Taste gedrueckt
    if duration == 0:
      duration = time.time()
  else:
    # Taste losgelassen
    if duration > 0:
      elapsed = (time.time() - duration)
      duration = 0
      if elapsed >= T_SHUT:
        syslog.syslog('Shutdown: System halted');
        subprocess.call(['shutdown', '-h', 'now'], shell=False) 
      elif elapsed >= T_PRELL:
        syslog.syslog('Shutdown: System rebooted');
        subprocess.call(['shutdown', '-r', 'now'], shell=False) 

# Interrupt fuer die Taste einschalten
GPIO.add_event_detect(PORT, GPIO.BOTH, callback=buttonISR)

syslog.syslog('Shutdown.py started');
while True:
  try:
    time.sleep(300)
  except KeyboardInterrupt:
    syslog.syslog('Shutdown terminated (Keyboard)');
    print ("Bye")
    sys.exit(0)
