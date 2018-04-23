#!/usr/bin/env python3

import argparse
from helper import Helper

class Main:
    def __init__(self, args, name):
        self.blub(name)
        helper = Helper()

    def blub(self, asdf):
        print(asdf)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    x = Main(args, "hans")
