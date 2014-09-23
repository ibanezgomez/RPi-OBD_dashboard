import RPi.GPIO as GPIO
import time
from threading import Thread

class switch:
    
    PINS = [18]
    
    def __init__(self, threads=False):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for i in self.PINS:
            GPIO.setup(i, GPIO.IN)
        if threads:
            self.change=False
            self.reading=True
            self.t = Thread(target=self.check)
            self.t.start() 

    def read(self, snum):
        if self.getValue(self.PINS[snum]) == 0: return 1
        else: return 0
    
    def getValue(self, pin):
        s=GPIO.input(pin)
        return s

    def check(self): 
        print("Loading button switch thread")      
        while self.reading:
            if self.read(0)==1: self.change=True
            else: self.change=False
            time.sleep(0.3) 