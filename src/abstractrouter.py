from abc import ABC, abstractmethod

class AbstractRouter():

    def __init__(self, start_pos_bear: tuple, destination_pos: tuple):
        pass

    @abstractmethod
    def initialize():
        pass

    @abstractmethod
    def update_pos(cur_pos: tuple):
        """
        Notify the router that we have arrived at a new position so he can evaluate if there is a new announcement to be made.

        :returns: has destination beed arrived
        """
        pass
