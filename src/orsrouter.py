from abstractrouter import AbstractRouter
import logging
import openrouteservice # TODO: wie installieren?
from openrouteservice.directions import directions, convert
import pprint # only for debugging
import pyproj
from shapely.ops import transform
from shapely.geometry import Point, LineString
import config
#from orsrouter import Pois
from geometryhelper import GeometryHelper

class OrsRouter(AbstractRouter):

    def __init__(self, start: Point, start_bear: float, destination: Point):
        # logging
        self.__logger = logging.getLogger(__name__)
        self.__logger.info("OrsRouter.__init__() called")

        # value initialization
        self.__cur = start
        self.__cur_bear = start_bear
        self.__destination = destination
        self.__client = openrouteservice.Client(key='***REMOVED***', retry_timeout=3600)
        self.__fetch_ls84_pois(start, start_bear, destination) # TODO: use cur values?

    def update_pos_wrapped(self, pos_bear):
        return self.update_pos(pos_bear[0], pos_bear[1])

    def update_pos(self, cur: Point, cur_bear: float):
        self.__logger.info("OrsRouter.update_pos() called with cur=" + str(cur) + " cur_bear=" + str(cur_bear))
        self.__cur = cur
        self.__cur_bear = cur_bear
        return self.__is_destination_reached()

    def __is_destination_reached(self):
        distance = GeometryHelper.get_distance(self.__cur, self.__destination)
        self.__logger.info("OrsRouter.__is_destination_reached() called with distance=" + str(distance) + " and __destination_reached_threshold=" + str(config.routing['destination_reached_threshold']))
        return distance < config.routing['destination_reached_threshold']

    def __fetch_ls84_pois(self, start: Point, start_bear: float, destination: Point):
        """
        Fetch
            1. a linestring containing all points of the route and
            2. an array of points where a change of direction happens
        """
        self.__logger.info("OrsRouter.__fetch_ls84_pois() called")

        route = self.__fetch_route(start, start_bear, destination)

        coordinates = convert.decode_polyline(route['geometry'])['coordinates']
        #print("coordinates=" + str(coordinates))

        self.__linestring84 = self.__coords2ls84(coordinates) # all coordinates

        self.__pois = Pois(route, coordinates) # points where a change of direction happens


    def __fetch_route(self, start: Point, start_bear: float, destination: Point):
        self.__logger.info("OrsRouter.__fetch_route() called, start=" + str(start) + "start_bear=" + str(start_bear) + "destination=" + str(destination)) # TODO: log values
        in_coords = ((start.x,start.y), (destination.x,destination.y))

        routes = directions(self.__client, in_coords, profile="cycling-safe", instructions="true", bearings=[[40,45]], continue_straight="true", optimized="false") # TODO: add further parameters, see https://openrouteservice-py.readthedocs.io/en/latest/#module-openrouteservice.directions
        # TODO: fix bearings=...

        #print("routes=" + str(routes))
        #print("route=" + str(routes['routes'][0]))

        # TODO: overwrite destination coordinates with the ones received from ORS, since there may be no way leading exactly to the desired destination coordinates
        # TODO: maybe it's better to implement "arrival at the destination" using the same technique as the other pois

        return routes['routes'][0]

        #print("geometry=" + str(convert.decode_polyline(routes['routes'][0]['geometry'])))
        #print("type(geometry)=" + str(type(convert.decode_polyline(routes['routes'][0]['geometry'])))) # type = dict
        #print("coordinates=" + str(convert.decode_polyline(routes['routes'][0]['geometry'])['coordinates']))
        #print("geometry[0]=" + str(convert.decode_polyline(routes['routes'][0]['geometry'][0])))

        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(routes)

    def __coords2ls84(self, coords): # lon, lat
        points = []
        for coord in coords:
            print("coord=" + str(coord))
            points.append(Point(coord[0], coord[1])) # lon, lat
        return LineString(points)
        


class Pois():
    """
    Store location and type of POIs (point of interest) in an ordered fashion
    """

    def __init__(self, route, coordinates):
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel("DEBUG")
        self.__logger.info("Pois.__init__() called")

        self.__pois = []

        #print("steps=" + str(routes['routes'][0]['segments'][0]['steps']))
        #print("coordinates=" + str(coordinates))

        for step in route['segments'][0]['steps']:
            way_point = step['way_points'][0]
            #print("way_point=" + str(way_point))
            self.__pois.append({'position': Point(coordinates[way_point][0], coordinates[way_point][1]), 'thetype': step['type']})

        #print("pois=" + str(pois))
        #return pois


    def check_position(self, cur):
        """
        Test if there is a POI near the given position.
        
        If yes, return its type and disable all previous POIs.

        If no, return None and keep all POIs.
        """



