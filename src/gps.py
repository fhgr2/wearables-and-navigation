import gpsd # pip3 install gpsd-py3
import logging
from tenacity import retry, wait_fixed, retry_if_result # pip3 install tenacity

class Gps():
    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel("DEBUG")

        self.__connect()

    @retry(wait=wait_fixed(0.5), retry=retry_if_result(lambda result: result.mode<3 or result.lon<5 or result.lon>11 or result.lat<45 or result.lat>48))
    def fetch(self):
        """
        Read new 3D position from gpsd and cache it
        """
        self.__packet = gpsd.get_current()
        return self.__packet # only used for the retry decorator, don't use this value
            
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

    @retry(wait=wait_fixed(0.5))
    def __connect(self):
        # TODO: logging
        self.__logger.debug("Going to connect to gpsd")

        # Connect to the local gpsd
        #gpsd.connect()

        # Connect somewhere else
        gpsd.connect(host="127.0.0.1", port=55555)
