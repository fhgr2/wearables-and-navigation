from abstractannouncer import AbstractAnnouncer
import logging

class LogAnnouncer(AbstractAnnouncer):

    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.__logger.info("LogAnnouncer.__init__() called")
        super(LogAnnouncer, self).__init__()

    def left(self, exit_number):
        self.__logger.info("LogAnnouncer.left() called")

    def right(self, exit_number):
        self.__logger.info("LogAnnouncer.right() called")

    def sharp_left(self, exit_number):
        self.__logger.info("LogAnnouncer.sharp_left() called")

    def sharp_right(self, exit_number):
        self.__logger.info("LogAnnouncer.sharp_right() called")

    def slight_left(self, exit_number):
        self.__logger.info("LogAnnouncer.slight_left() called")

    def slight_right(self, exit_number):
        self.__logger.info("LogAnnouncer.slight_right() called")

    def continue_way(self, exit_number):
        self.__logger.info("LogAnnouncer.continue_way() called")

    def enter_roundabout(self, exit_number):
        self.__logger.info("LogAnnouncer.enter_roundabout() called with exit_number=" + str(exit_number))

    def exit_roundabout(self, exit_number):
        self.__logger.info("LogAnnouncer.exit_roundabout() called with exit_number=" + str(exit_number))

    def uturn(self, exit_number):
        self.__logger.info("LogAnnouncer.uturn() called")

    def arrival(self, exit_number):
        self.__logger.info("LogAnnouncer.arrival() called")

    def departure(self, exit_number):
        self.__logger.info("LogAnnouncer.departure() called")

    def unknown(self, exit_number):
        self.__logger.info("LogAnnouncer.unknown() called, exit_number=" + str(exit_number))

