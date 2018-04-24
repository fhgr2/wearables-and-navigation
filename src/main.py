#!/usr/bin/env python3

import argparse
import logging
import time
from abstractrouter import AbstractRouter
from orsrouter import OrsRouter
from gps import Gps

class Main:
    def __init__(self, args):
        self.init_logging()

        self.__logger.info("Going to initialize Gps()")
        self.__gps = Gps()

        # TODO: use @retry decorator
        start_pos = None
        while start_pos == None:
            self.__logger.debug("Going to read position and direction")
            try:
                start_pos = self.__gps.get_pos_bearing()
            except:
                start_pos = None
            self.__logger.debug("start_pos=" + str(start_pos))
            time.sleep(0.5)

        destination_pos = (args.lat, args.lon)

        self.__logger.debug("Going to initialize router")
        router = OrsRouter(start_pos, destination_pos)

        cur_pos = start_pos # TODO: read cur_pos freshly from Gps
        router.update_pos(cur_pos)

    def init_logging(self):
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
