import gpsd # pip3 install gpsd-py3
import logging
from tenacity import retry, wait_fixed, retry_if_result, retry_if_exception_type # pip3 install tenacity
from shapely.geometry import Point, LineString
import config

class Gps():
    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel("DEBUG")

        self.__connect()

    @retry(wait=wait_fixed(0.5), retry=(retry_if_result(lambda packet: packet.mode<3 or packet.lon<5 or packet.lon>11 or packet.lat<45 or packet.lat>48) | retry_if_exception_type()))
    def fetch(self):
        """
        Read new 3D position from gpsd and cache it
        """
        self.__packet = gpsd.get_current()
        return self.__packet # only used for the retry decorator, don't use this value
            
    def fetch_get_pos_bearing(self):
        #self.__logger.info("mv, bei fetch_get_pos_bearing") # MV
        #self.__logger.info("mv, self: " + str(self)) # MV
        self.fetch()
        #self.__logger.info("mv, nach self.fetch") # MV
        #self.__logger.info("mv, Aufruf: self.get_pos_bearing()") # MV
        return self.get_pos_bearing()

    def get_pos_bearing(self):
        """
        Return cached position and bearing
        """
        #self.__logger.info("mv, In get_pos_bearing(self)") # MV
        packet = self.__packet
        
        self.__logger.debug("self.__packet=" + str(packet))
        self.__logger.debug("self.__packet.position()=" + str(packet.position()))
        self.__logger.debug("self.__packet.track=" + str(packet.track))

        # See the inline docs for GpsResponse for the available data: https://github.com/MartijnBraam/gpsd-py3/blob/master/DOCS.md
        return (Point(packet.lon,packet.lat), self.__packet.track)

    @retry(wait=wait_fixed(0.5))
    def __connect(self):
        self.__logger.info("Going to connect to gpsd, ip=" + config.gpsd['ip'] + " port=" + str(config.gpsd['port']))
        gpsd.connect(host=config.gpsd['ip'], port=config.gpsd['port'])