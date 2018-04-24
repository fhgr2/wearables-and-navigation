from abc import ABC, abstractmethod

class AbstractRouter():

    def __init__(self, start_pos_bearing: tuple, destination_pos: tuple):
        pass

    @abstractmethod
    def initialize():
        pass

    @abstractmethod
    def update_pos(cur_pos: tuple):
        pass
