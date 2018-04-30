from abstractrouter import AbstractRouter

class OrsRouter(AbstractRouter):

    def __init__(self, start_pos_bear: tuple, destination_pos: tuple):
        self.__logger = logging.getLogger(__name__)
        #self.__logger.info("Arrival at destination") #TODO: kommentar erstellen, dass die aktuelle funktion aufgerufen wurde
        self.__cur_pos_bear = start_pos_bear

    def update_pos(self, cur_pos_bear: tuple):
        # TODO: log-eintrag mit aktuellen koordinaten erstellen
        self.__cur_pos_bear = cur_pos_bear
        return False
