#!/usr/bin/env python3

import argparse
import logging
from helper import Helper

class Main:
    def __init__(self, args, name):
        helper = Helper()
        self.__logger = logging.getLogger(__name__)
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') # https://docs.python.org/3/howto/logging-cookbook.html
        console_handler.setFormatter(formatter)
        self.__logger.addHandler(console_handler)

        self.blub(name)

    def blub(self, asdf):
        print(asdf)
        self.__logger.warn('log-eintrag von Main')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    x = Main(args, "hans")
