from abc import ABC, abstractmethod

class AbstractAnnouncer(ABC):

    @abstractmethod
    def left():
        pass

    @abstractmethod
    def right():
        pass

    @abstractmethod
    def sharp_left():
        pass

    @abstractmethod
    def sharp_right():
        pass

    @abstractmethod
    def slight_left():
        pass

    @abstractmethod
    def slight_right():
        pass

    @abstractmethod
    def continue_way():
        pass

    @abstractmethod
    def enter_roundabout():
        pass

    @abstractmethod
    def exit_roundabout():
        pass

    @abstractmethod
    def uturn():
        pass

    @abstractmethod
    def arrival():
        pass

    @abstractmethod
    def departure():
        pass

    @abstractmethod
    def unknown():
        pass

    def __init__(self):
        # https://stackoverflow.com/a/11479840
        # for instruction types see https://github.com/GIScience/openrouteservice/blob/master/openrouteservice/src/main/java/heigit/ors/routing/instructions/InstructionType.java
        self.__options = {
            0: self.left,
            1: self.right,
            2: self.sharp_left,
            3: self.sharp_right,
            4: self.slight_left,
            5: self.slight_right,
            6: self.continue_way,
            7: self.enter_roundabout,
            8: self.exit_roundabout,
            9: self.uturn,
            10: self.arrival,
            11: self.departure,
            12: self.unknown
            # default value for non-existing keys is defined outside
        }

    def announce(self, announcement_information: dict):
        if announcement_information != None:
            self.__options.get(announcement_information.get("type"), self.unknown)(announcement_information.get("exit_number")) # call self.unknown() if non-existing key was provided

