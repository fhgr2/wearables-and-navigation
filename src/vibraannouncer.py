from abstractannouncer import AbstractAnnouncer
import logging
import config
import datetime
import time
import gpiozero as io

class VibraAnnouncer(AbstractAnnouncer):

    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.__logger.info("VibraAnnouncer.__init__() called")
        super(VibraAnnouncer, self).__init__()

        # Output-GPIO zuordnen
        self.__vm_lf = io.LED(5)  # GPIO 5 für VM left front
        self.__vm_lb = io.LED(12) # GPIO 5 für VM left back
        self.__vm_m  = io.LED(6)  # GPIO 6 für VM middle
        self.__vm_rf = io.LED(13) # GPIO 13 für VM right front
        self.__vm_rb = io.LED(16) # GPIO 16 für VM right back

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

    def continue_way(self, exit_number):
        pass

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

    def arrival(self, exit_number):
        for i in range(6):
            self.__impuls_middle()

    def departure(self, exit_number):
        self.__impuls_left_right()
        time.sleep(self.__signalpause)
        self.__impuls_left_right()

    def unknown(self, exit_number):
        self.__logger.info("VibraAnnouncer.unknown() called, exit_number=" + str(exit_number))

    def __impuls_left_right(self):
        self.__vm_lf.on()
        self.__vm_lb.on()
        self.__vm_rf.on()
        self.__vm_rb.on()
        time.sleep(self.__impulsdauer)
        self.__vm_lf.off()
        self.__vm_lb.off()
        self.__vm_rf.off()
        self.__vm_rb.off()
        time.sleep(self.__nachpause)
        
    def __impuls_left_front(self):
        self.__vm_lf.on()
        time.sleep(self.__impulsdauer)
        self.__vm_lf.off()
        time.sleep(self.__nachpause)
        
    def __impuls_left(self):
        self.__vm_lf.on()
        self.__vm_lb.on()
        time.sleep(self.__impulsdauer)
        self.__vm_lf.off()
        self.__vm_lb.off()
        time.sleep(self.__nachpause)
        
    def __impuls_left_back(self):
        self.__vm_lb.on()
        time.sleep(self.__impulsdauer)
        self.__vm_lb.off()
        time.sleep(self.__nachpause)

    def __impuls_right_front(self):
        self.__vm_rf.on()
        time.sleep(self.__impulsdauer)
        self.__vm_rf.off()
        time.sleep(self.__nachpause)

    def __impuls_right(self):
        self.__vm_rf.on()
        self.__vm_rb.on()
        time.sleep(self.__impulsdauer)
        self.__vm_rf.off()
        self.__vm_rb.off()
        time.sleep(self.__nachpause)

    def __impuls_right_back(self):
        self.__vm_rb.on()
        time.sleep(self.__impulsdauer)
        self.__vm_rf.off()
        time.sleep(self.__nachpause)

    def __impuls_middle(self):
        self.__vm_m.on()
        time.sleep(self.__impulsdauer)
        self.__vm_m.off()
        time.sleep(self.__nachpause)


