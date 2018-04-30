from abstractrouter import AbstractRouter
import logging

class OrsRouter(AbstractRouter):

    def __init__(self, start_pos_bear: tuple, destination_pos: tuple):
        self.__logger = logging.getLogger(__name__)
        #self.__logger.info("") #TODO: kommentar erstellen, dass die aktuelle funktion aufgerufen wurde
        self.__cur_pos_bear = start_pos_bear

    def update_pos(self, cur_pos_bear: tuple):
        # TODO: log-eintrag mit aktuellen koordinaten erstellen
        self.__logger.info("OrsRouter.update_pos() called with cur_pos_bear=" + str(cur_pos_bear))
        self.__cur_pos_bear = cur_pos_bear
        return False
