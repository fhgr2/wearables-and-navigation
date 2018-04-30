import gpsd # pip3 install gpsd-py3
import logging
from retrying import retry # pip3 install retrying

class Gps():
    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel("DEBUG")

        self.__connect()

    @retry(wait_fixed=500)
    def fetch(self):
        """
        Read new position from gpsd and cache it
        """
        self.__packet = gpsd.get_current()
        
    def fetch_get_pos_bearing(self):
        self.fetch()
        return self.get_pos_bearing()


    def get_pos_bearing(self):
        """
        Return cached position and bearing
        """

        self.__logger.debug("self.__packet=" + str(self.__packet))
        self.__logger.debug("self.__packet.position()=" + str(self.__packet.position()))
        self.__logger.debug("self.__packet.track=" + str(self.__packet.track))

        # See the inline docs for GpsResponse for the available data: https://github.com/MartijnBraam/gpsd-py3/blob/master/DOCS.md
        return self.__packet.position() + (self.__packet.track,)
        

    @retry(wait_fixed=500)
    def __connect(self):
        # TODO: logging
        self.__logger.debug("Going to connect to gpsd")

        # Connect to the local gpsd
        #gpsd.connect()

        # Connect somewhere else
        gpsd.connect(host="127.0.0.1", port=55555)
