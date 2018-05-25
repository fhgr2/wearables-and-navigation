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
from announcermanager import AnnouncerManager

class OrsRouter(AbstractRouter):

    def __init__(self, start: Point, start_bear: float, destination: Point, announcer_manager: AnnouncerManager):
        # logging
        self.__logger = logging.getLogger(__name__)
        self.__logger.info("OrsRouter.__init__() called with start=" + str(start) + " start_bear=" + str(start_bear) + " destination=" + str(destination))

        # value initialization
        self.__start = start
        self.__start_bear = start_bear
        self.__destination = destination
        self.__announcer_manager = announcer_manager
        self.__client = openrouteservice.Client(key='***REMOVED***', retry_timeout=3600)

        self.__calculate_routing_information()

    def __calculate_routing_information(self):
        self.__logger.info("OrsRouter.__calculate_routing_information() called")

        self.__fetch_route()

        coordinates = convert.decode_polyline(self.__route['geometry'])['coordinates']
        #print("coordinates=" + str(coordinates))

        self.__track = self.__coords2linestring(coordinates) # all coordinates

        self.__pois = Pois(self.__route, coordinates) # points where a change of direction happens


    def update_pos(self, cur: Point, cur_bear: float):
        self.__logger.info("OrsRouter.update_pos() called with cur=" + str(cur) + " cur_bear=" + str(cur_bear))
        self.__cur = cur
        self.__cur_bear = cur_bear

        #are we still on track or is a route-recalculation necessary?
        if not self.__is_position_on_track():
            self.__logger.warn("OrsRouter.update_pos(): position is not on track anymore, going to recalculate route")
            self.__start = cur
            self.__start_bear = cur_bear
            self.__calculate_routing_information()

        # make announcement if necessary
        self.__announcer_manager.announce(self.__pois.checkin_position(self.__cur))
        
        return self.__is_destination_reached()

    def __is_destination_reached(self):
        distance = GeometryHelper.get_distance(self.__cur, self.__destination)
        self.__logger.info("OrsRouter.__is_destination_reached() called with distance=" + str(distance) + " and __destination_reached_threshold=" + str(config.routing['destination_reached_threshold']))
        return distance < config.routing['destination_reached_threshold']

    def __is_position_on_track(self):
        return GeometryHelper.get_distance(self.__cur, self.__track) < config.routing['wrong_way_threshold']


    def __fetch_route(self):
        self.__logger.info("OrsRouter.__fetch_route() called, start=" + str(self.__start) + "start_bear=" + str(self.__start_bear) + "destination=" + str(self.__destination))
        in_coords = ((self.__start.x,self.__start.y), (self.__destination.x,self.__destination.y))

        routes = directions(self.__client, in_coords, profile="cycling-safe", instructions="true", bearings=[[40,45]], continue_straight="true", optimized="false") # TODO: add further parameters, see https://openrouteservice-py.readthedocs.io/en/latest/#module-openrouteservice.directions
        # TODO: fix bearings=...

        #print("routes=" + str(routes))
        #print("route=" + str(routes['routes'][0]))

        # TODO: overwrite destination coordinates with the ones received from ORS, since there may be no way leading exactly to the desired destination coordinates
        # TODO: maybe it's better to implement "arrival at the destination" using the same technique as the other pois

        self.__route = routes['routes'][0]

        #print("geometry=" + str(convert.decode_polyline(routes['routes'][0]['geometry'])))
        #print("type(geometry)=" + str(type(convert.decode_polyline(routes['routes'][0]['geometry'])))) # type = dict
        #print("coordinates=" + str(convert.decode_polyline(routes['routes'][0]['geometry'])['coordinates']))
        #print("geometry[0]=" + str(convert.decode_polyline(routes['routes'][0]['geometry'][0])))

        pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(self.__route)

    def __coords2linestring(self, coords): # lon, lat
        points = []
        for coord in coords:
            #print("coord=" + str(coord))
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
            self.__pois.append({'position': Point(coordinates[way_point][0], coordinates[way_point][1]), 'type': step['type'], 'exit_number': step.get('exit_number')}) # get() will return None if key is not available

        #print("pois=" + str(pois))
        #return pois


    def checkin_position(self, cur):
        """
        Test if there is a POI near the given position.
        
        If yes, return a dictionary with keys "type" and "exit_number" (which may be None) and internally delete all previous POIs including the current one

        If no, return None and keep all POIs.
        """
        # TODO: in case of no: return None or (None,None) ?

        is_position_near_poi = False
        matching_index = -1

        # find first poi that is near current position
        for i, poi in enumerate(self.__pois):
            if GeometryHelper.get_distance(poi['position'], cur) < config.routing['poi_reached_threshold']: # TODO: maybe use better logic which includes the current speed
                is_position_near_poi = True
                matching_index = i
                break

        if is_position_near_poi:
            current_poi = self.__pois[i]

            # remove previous pois including(!) current
            self.__pois = self.__pois[i+1:]

            return {"type": current_poi.get("type"), "exit_number": current_poi.get("exit_number")}
        else:
            return None
