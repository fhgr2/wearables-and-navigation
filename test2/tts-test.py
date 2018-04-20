#!/usr/bin/env python3

# sudo apt install python-espeak
# pip3 install pyttsx3

import pyttsx3;

def wait_for_say(text):
    engine = pyttsx3.init();
    engine.say(text);
    engine.runAndWait() ;

wait_for_say("I will speak this text")
