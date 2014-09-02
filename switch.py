#import RPi.GPIO as GPIO
import logging

class switch:
    PINS = [18]
    
    def __init__(self):
        log.debug("Initializing GPIO switch")
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for i in self.PINS:
            GPIO.setup(i, GPIO.IN)

    def read(self, snum):
        if self.getValue(self.PINS[snum]) == 0: return 1
        else: return 0
    
    def getValue(self, pin):
        s=GPIO.input(pin)
        return s
