from abstractrouter import AbstractRouter

class OrsRouter(AbstractRouter):

    def __init__(self, start_pos_bearing: tuple, destination_pos: tuple):
        pass

    def initialize(self):
        pass

    def update_pos(self, cur_pos: tuple):
        self.__cur_pos = cur_pos
        pass
