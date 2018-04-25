from abstractrouter import AbstractRouter

class OrsRouter(AbstractRouter):

    def __init__(self, start_pos_bear: tuple, destination_pos: tuple):
        self.__cur_pos_bear = start_pos_bear

    def initialize(self):
        pass

    def update_pos(self, cur_pos_bear: tuple):
        self.__cur_pos_bear = cur_pos_bear
        return False
