from abstractannouncer import AbstractAnnouncer
import logging
import pyttsx3; # sudo apt install python-espeak ; pip3 install pyttsx3

class AudioAnnouncer(AbstractAnnouncer):

    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.__logger.info("AudioAnnouncer.__init__() called")
        super(AudioAnnouncer, self).__init__()
        self.__engine = pyttsx3.init();
        self.__engine.setProperty('rate', 130)

    def __say(self, text):
        self.__engine.say(text + " I repeat. " + text);
        self.__engine.runAndWait();

    def left(self, exit_number):
        self.__say("Turn left.")

    def right(self, exit_number):
        self.__say("Turn right.")

    def sharp_left(self, exit_number):
        self.__say("Turn sharp left.")

    def sharp_right(self, exit_number):
        self.__say("Turn sharp right.")

    def slight_left(self, exit_number):
        self.__say("Turn slightly left.")

    def slight_right(self, exit_number):
        self.__say("Turn slightly right.")

    def continue_way(self, exit_number):
        self.__say("Continue straight.")

    def enter_roundabout(self, exit_number):
        self.__say("Enter roundabout and use exit number.")

    def exit_roundabout(self, exit_number):
        self.__say("Leave roundabout and use exit number.")

    def uturn(self, exit_number):
        self.__say("Make a you turn.")

    def arrival(self, exit_number):
        self.__say("You have arrived at your destination.")

    def departure(self, exit_number):
        self.__say("Start your journey.")

    def unknown(self, exit_number):
        self.__say("Unknown message.")

