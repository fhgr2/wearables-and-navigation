import logging
from logannouncer import LogAnnouncer
from audioannouncer import AudioAnnouncer

class AnnouncerManager():

    def __init__(self):
        pass
        self.__logger = logging.getLogger(__name__)
        self.__logger.info("LogAnnouncer.__init__() called")

        self.__announcers = []
        self.__announcers.append(LogAnnouncer())
        self.__announcers.append(AudioAnnouncer())
        # TODO: add more announcers here

    def announce(self, announcement_information: dict):
        for announcer in self.__announcers:
            announcer.announce(announcement_information)
