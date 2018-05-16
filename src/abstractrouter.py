from abc import ABC, abstractmethod
from shapely.geometry import Point, LineString
from announcermanager import AnnouncerManager

class AbstractRouter(ABC):

    def __init__(self, start: Point, start_bear: float, destination: Point, announcer_manager: AnnouncerManager):
        pass

    @abstractmethod
    def update_pos(self, cur: Point, cur_bear: float):
        """
        Notify the router of a new position so he can evaluate if there is a new announcement to be made.

        :param cur: the current position
        :param cur_bear: the current bearing (direction of movement)
        :returns: has destination been reached
        """
        pass
