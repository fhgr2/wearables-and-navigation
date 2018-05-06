from abstractrouter import AbstractRouter
import logging
import openrouteservice
from openrouteservice.directions import directions, convert

class OrsRouter(AbstractRouter):

    def __init__(self, start_pos_bear: tuple, destination_pos: tuple):
        self.__logger = logging.getLogger(__name__)
        self.__logger.info("OrsRouter.__init__() called")
        self.__cur_pos_bear = start_pos_bear
        self.__client = openrouteservice.Client(key='***REMOVED***', retry_timeout=3600)
        self.__fetch_route(start_pos_bear, destination_pos)

    def update_pos(self, cur_pos_bear: tuple):
        # TODO: log-eintrag mit aktuellen koordinaten erstellen
        self.__logger.info("OrsRouter.update_pos() called with cur_pos_bear=" + str(cur_pos_bear))
        self.__cur_pos_bear = cur_pos_bear
        return False

    def __fetch_route(self, start_pos_bear: tuple, destination_pos: tuple):
        self.__logger.info("OrsRouter.__fetch_route() called")
        start_lat = start_pos_bear[0]
        start_lon = start_pos_bear[1]
        dest_lat  = destination_pos[0]
        dest_lon  = destination_pos[1]
        coords = ((start_lon,start_lat), (dest_lon,dest_lat))

        routes = directions(self.__client, coords, profile="cycling-safe", instructions="true", bearings=[[40,45]], continue_straight="true", optimized="false") # TODO: add further parameters, see https://openrouteservice-py.readthedocs.io/en/latest/#module-openrouteservice.directions

        print("routes=" + str(routes))
        print("geometry=" + str(convert.decode_polyline(routes['routes'][0]['geometry'])))
