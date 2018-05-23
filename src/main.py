#!/usr/bin/env python3

import argparse
import logging
import time
from abstractrouter import AbstractRouter
from orsrouter import OrsRouter
from gps import Gps
from shapely.geometry import Point, LineString
from announcermanager import AnnouncerManager

class Main:
    def __init__(self, args):
        self.__init_logging()

        self.__logger.info("Going to initialize Gps()")
        self.__gps = Gps()

        self.__logger.debug("Going to read position and direction")
        start, start_bear = self.__gps.fetch_get_pos_bearing()
        self.__logger.debug("start=" + str(start))
        self.__logger.debug("start_bear=" + str(start_bear))

        destination = Point(args.lon, args.lat)

        announcer_manager = AnnouncerManager()

        self.__logger.debug("Going to initialize router")
        router = OrsRouter(start, start_bear, destination, announcer_manager)

        while self.__update_pos_wrapped(self.__gps.fetch_get_pos_bearing(), router) == False: time.sleep(1)

        self.__logger.info("Arrival at destination")
        # TODO: need to announce arrival at destination?

    def __update_pos_wrapped(self, pos_bear, router):
        return router.update_pos(pos_bear[0], pos_bear[1])

    def __init_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel("DEBUG") # level for this class only
        # TODO: configure logging into file

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", required=True, type=float, help="destination latitude")
    parser.add_argument("--lon", required=True, type=float, help="destination longitude")
    args = parser.parse_args()

    x = Main(args)
