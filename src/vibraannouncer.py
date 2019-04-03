from abstractannouncer import AbstractAnnouncer
import logging
import config
import datetime
import time

# if gpiozero is used on a non-raspberry-pi system, the environment variable GPIOZERO_PIN_FACTORY=mock needs to be set
# to work around needing to set the environment variable, we don't import gpiozero if the vibra announcer is disabled
if config.announcers['vibra']:
    import gpiozero as io

class VibraAnnouncer(AbstractAnnouncer):

    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.__logger.info("VibraAnnouncer.__init__() called")
        super(VibraAnnouncer, self).__init__()

        # Output-GPIO zuordnen
        self.__vm_left_front  = io.LED(5)  # GPIO 5 für VM left front
        self.__vm_left_back   = io.LED(12) # GPIO 5 für VM left back
        self.__vm_middle      = io.LED(6)  # GPIO 6 für VM middle
        self.__vm_right_front = io.LED(13) # GPIO 13 für VM right front
        self.__vm_right_back  = io.LED(16) # GPIO 16 für VM right back

        self.__impulsdauer = config.vibration['impulsdauer']
        self.__nachpause   = config.vibration['nachpause']
        self.__signalpause = config.vibration['signalpause']

    def left(self, exit_number):
        self.__impuls_left()
        self.__impuls_left()
        time.sleep(self.__signalpause)
        self.__impuls_left()
        self.__impuls_left()

    def right(self, exit_number):
        self.__impuls_right()
        self.__impuls_right()
        time.sleep(self.__signalpause)
        self.__impuls_right()
        self.__impuls_right()

    def sharp_left(self, exit_number):
        self.__impuls_left_back()
        self.__impuls_left_back()
        time.sleep(self.__signalpause)
        self.__impuls_left_back()
        self.__impuls_left_back()

    def sharp_right(self, exit_number):
        self.__impuls_right_back()
        self.__impuls_right_back()
        time.sleep(self.__signalpause)
        self.__impuls_right_back()
        self.__impuls_right_back()

    def slight_left(self, exit_number):
        self.__impuls_left_front()
        self.__impuls_left_front()
        time.sleep(self.__signalpause)
        self.__impuls_left_front()
        self.__impuls_left_front()

    def slight_right(self, exit_number):
        self.__impuls_right_front()
        self.__impuls_right_front()
        time.sleep(self.__signalpause)
        self.__impuls_right_front()
        self.__impuls_right_front()

# 2019_02_23: changed
    def continue_way(self, exit_number):
        #pass
        self.__impuls_straight()
        self.__impuls_straight()
        time.sleep(self.__signalpause)
        self.__impuls_straight()
        self.__impuls_straight()

    def enter_roundabout(self, exit_number):
        for i in range(exit_number):
            self.__impuls_middle()
        time.sleep(self.__signalpause)
        for i in range(exit_number):
            self.__impuls_middle()

    def exit_roundabout(self, exit_number):
        self.enter_roundabout(exit_number)

    def uturn(self, exit_number):
        for i in range(3):
            for j in range(3):
                self.__impuls_middle()
            time.sleep(self.__signalpause)

# 2019_04_03: changed, added left and right
    def arrival(self, exit_number):
        for i in range(6):
            self.__impuls_middle()
            self.__impuls_left()
            self.__impuls_right()

# 2019_02_22: changed
    def departure(self, exit_number):
        #self.__impuls_left_right()
        #time.sleep(self.__signalpause)
        #self.__impuls_left_right()
        pass

# 2019_02_22: new
    def keep_left(self, exit_number):
        pass

# 2019_02_22: new
    def keep_right(self, exit_number):
        pass

    def unknown(self, exit_number):
        self.__logger.info("VibraAnnouncer.unknown() called, exit_number=" + str(exit_number))

    def __impuls_left_right(self):
        self.__vm_left_front.on()
        self.__vm_left_back.on()
        self.__vm_right_front.on()
        self.__vm_right_back.on()
        time.sleep(self.__impulsdauer)
        self.__vm_left_front.off()
        self.__vm_left_back.off()
        self.__vm_right_front.off()
        self.__vm_right_back.off()
        time.sleep(self.__nachpause)

# 2019_02_23: new
    def __impuls_straight(self):
        self.__vm_left_front.on()
        self.__vm_right_front.on()
        time.sleep(self.__impulsdauer)
        self.__vm_left_front.off()
        self.__vm_right_front.off()
        time.sleep(self.__nachpause)

    def __impuls_left_front(self):
        self.__vm_left_front.on()
        time.sleep(self.__impulsdauer)
        self.__vm_left_front.off()
        time.sleep(self.__nachpause)

    def __impuls_left(self):
        self.__vm_left_front.on()
        self.__vm_left_back.on()
        time.sleep(self.__impulsdauer)
        self.__vm_left_front.off()
        self.__vm_left_back.off()
        time.sleep(self.__nachpause)

    def __impuls_left_back(self):
        self.__vm_left_back.on()
        time.sleep(self.__impulsdauer)
        self.__vm_left_back.off()
        time.sleep(self.__nachpause)

    def __impuls_right_front(self):
        self.__vm_right_front.on()
        time.sleep(self.__impulsdauer)
        self.__vm_right_front.off()
        time.sleep(self.__nachpause)

    def __impuls_right(self):
        self.__vm_right_front.on()
        self.__vm_right_back.on()
        time.sleep(self.__impulsdauer)
        self.__vm_right_front.off()
        self.__vm_right_back.off()
        time.sleep(self.__nachpause)

    def __impuls_right_back(self):
        self.__vm_right_back.on()
        time.sleep(self.__impulsdauer)
        self.__vm_right_back.off()
        time.sleep(self.__nachpause)

    def __impuls_middle(self):
        self.__vm_middle.on()
        time.sleep(self.__impulsdauer)
        self.__vm_middle.off()
        time.sleep(self.__nachpause)