from abc import ABC, abstractmethod

class AbstractRouter():

    def __init__(self, start_pos_bear: tuple, destination_pos: tuple):
        pass

    @abstractmethod
    def update_pos(cur_pos_bear: tuple):
        """
        Notify the router of a new position so he can evaluate if there is a new announcement to be made.

        :param cur_pos_bear: a tuple (latitude, longitude, bearing)
        :returns: has destination beed arrived
        """
        pass
