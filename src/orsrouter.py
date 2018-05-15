from abstractrouter import AbstractRouter
import logging
import openrouteservice # TODO: wie installieren?
from openrouteservice.directions import directions, convert
import pprint # only for debugging
import pyproj
from shapely.ops import transform
from shapely.geometry import Point, LineString

class OrsRouter(AbstractRouter):

    def __init__(self, start_pos_bear: tuple, destination_pos: tuple):
        self.__logger = logging.getLogger(__name__)
        self.__logger.info("OrsRouter.__init__() called")
        self.__cur_pos_bear = start_pos_bear
        self.__client = openrouteservice.Client(key='***REMOVED***', retry_timeout=3600)
        self.__fetch_ls84_pois(start_pos_bear, destination_pos)


    def update_pos(self, cur_pos_bear: tuple):
        self.__logger.info("OrsRouter.update_pos() called with cur_pos_bear=" + str(cur_pos_bear))
        self.__cur_pos_bear = cur_pos_bear
        print("cur_pos_bear=" + str(cur_pos_bear))
        distance = self.__get_distance(self.__linestring84, self.__cur_pos_bear)
        print("distance=" + str(distance))
        return False

    def __fetch_ls84_pois(self, start_pos_bear: tuple, destination_pos: tuple):
        """
        Fetch
            1. a linestring containing all points of the route and
            2. an array of points where a change of direction happens
        """
        self.__logger.info("OrsRouter.__fetch_ls84_pois() called")

        route = self.__fetch_route(start_pos_bear, destination_pos)

        coordinates = convert.decode_polyline(route['geometry'])['coordinates']
        #print("coordinates=" + str(coordinates))

        self.__linestring84 = self.__coords2ls84(coordinates) # all coordinates

        self.__pois = self.__generate_pois(route, coordinates) # points where a change of direction happen


    def __fetch_route(self, start_pos_bear: tuple, destination_pos: tuple):
        self.__logger.info("OrsRouter.__fetch_route() called")
        start_lat = start_pos_bear[0]
        start_lon = start_pos_bear[1]
        dest_lat  = destination_pos[0]
        dest_lon  = destination_pos[1]
        in_coords = ((start_lon,start_lat), (dest_lon,dest_lat))

        routes = directions(self.__client, in_coords, profile="cycling-safe", instructions="true", bearings=[[40,45]], continue_straight="true", optimized="false") # TODO: add further parameters, see https://openrouteservice-py.readthedocs.io/en/latest/#module-openrouteservice.directions

        #print("routes=" + str(routes))
        #print("route=" + str(routes['routes'][0]))

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
        

    def __generate_pois(self, route, coordinates):
        #print("steps=" + str(routes['routes'][0]['segments'][0]['steps']))
        #print("coordinates=" + str(coordinates))

        pois = []

        for step in route['segments'][0]['steps']:
            way_point = step['way_points'][0]
            #print("way_point=" + str(way_point))
            pois.append({'lat': coordinates[way_point][1], 'lon': coordinates[way_point][0], 'thetype': step['type']}) # TODO: fix lat,lon

        #print("pois=" + str(pois))
        return pois


    def __get_distance(self, linestring84, pos_bear):
        """
        Return distance in meters between linestring and a position/bearing tuplet
        """
        lat = pos_bear[0]
        lon = pos_bear[1]
        linestring95 = self.__wgs84ToLv95(linestring84)
        point95 = self.__wgs84ToLv95(Point(lon, lat))
        return linestring95.distance(point95)

    # according to https://gis.stackexchange.com/a/127432
    def __wgs84ToLv95(self, old):
        project = lambda x, y: pyproj.transform(pyproj.Proj(init='epsg:4326'), pyproj.Proj(init='epsg:2056'), x, y)
        return transform(project,old)
