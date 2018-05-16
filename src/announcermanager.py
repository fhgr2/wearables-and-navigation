import logging
from logannouncer import LogAnnouncer

class AnnouncerManager():

    def __init__(self):
        pass
        self.__logger = logging.getLogger(__name__)
        self.__logger.info("LogAnnouncer.__init__() called")

        self.__announcers = []
        self.__announcers.append(LogAnnouncer())
        # TODO: add more announcers here

    def announce(self, thetype: int):
        for announcer in self.__announcers:
            announcer.announce(thetype)
