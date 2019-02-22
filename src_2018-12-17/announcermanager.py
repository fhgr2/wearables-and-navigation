import logging
from logannouncer import LogAnnouncer
from audioannouncer import AudioAnnouncer
from vibraannouncer import VibraAnnouncer
import config

class AnnouncerManager():

    def __init__(self):
        pass
        self.__logger = logging.getLogger(__name__)
        self.__logger.info("LogAnnouncer.__init__() called")

        self.__announcers = []

        if config.announcers['log']:
            self.__announcers.append(LogAnnouncer())

        if config.announcers['audio']:
            self.__announcers.append(AudioAnnouncer())

        if config.announcers['vibra']:
            self.__announcers.append(VibraAnnouncer())

        # add more announcers here

    def announce(self, announcement_information: dict):
        for announcer in self.__announcers:
            announcer.announce(announcement_information)
