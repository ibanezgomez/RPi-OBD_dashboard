import serial
import platform
from datetime import datetime
import time

import sensors
import io
from utils import *

from threading import Thread

class OBD_Capture():

    def __init__(self, threads=False):
        self.port = None
        self.connect()
        #time.sleep(10)
        if threads:
            self.currentSensors = [12, 13, 4, 5]
            self.lastRead = []
            self.reading  = True
            self.block  = False
            self.running = True
            self.t = Thread(target=self.capture_thread)
            self.t.start() 

    def connect(self):
        portnames = scanSerialTest()
        print portnames
        if len(portnames) == 0: return
        self.port = io.OBDPort(portnames[0], None, 2, 2)
        if(self.port.State == 0):
            self.port.close()
            self.port = None

        if(self.port):
            print("Connected to "+self.port.port.name)

    def disconnect(self):
        return True
            
    def is_connected(self):
        return self.port
    
    def capture_once(self, sensor):
        (n, v, u) = self.port.sensor(sensor)
        return {"name": n.strip(), "value": v, "unit": u}

    def capture_thread(self):
        while self.running:
            while self.reading:
                read = []
                for i in self.currentSensors:
                    read.append(self.capture_once(i))
                self.block=False
                self.lastRead = read
            print("End OBD read thread")
            self.reading=True

    def change_sensors(self, sensors):
        self.block=True
        self.currentSensors=sensors
        self.reading=False

    def getDTCstatus(self):
        return self.capture_once(1)

    def getDTCFF(self):
        return self.capture_once(2)

    def getFuelStatus(self):
        return self.capture_once(3)

    def getLoad(self):
        return self.capture_once(4)

    def getTemp(self):
        return self.capture_once(5)

    def getShortTermFuel1(self):
        return self.capture_once(6)

    def getLongTermFuel1(self):
        return self.capture_once(7)

    def getShortTermFuel2(self):
        return self.capture_once(8)
    
    def getLongTermFuel2(self):
        return self.capture_once(9)

    def getFuelPress(self):
        return self.capture_once(10)

    def getManifoldPress(self):
        return self.capture_once(11)

    def getRPM(self):
        return self.capture_once(12)

    def getSpeed(self):
        return self.capture_once(13)

    def getTimmingAdv(self):
        return self.capture_once(14)

    def getIntakeAirTemp(self):
        return self.capture_once(15)

    def getMAF(self):
        return self.capture_once(16)

    def getThrottlePos(self):
        return self.capture_once(17)
    
    def getSecondaryAirStatus(self):
        return self.capture_once(18)

    def getO2SensorPosition(self):
        return self.capture_once(19)

    def getO211(self):
        return self.capture_once(20)

    def getO212(self):
        return self.capture_once(21)

    def getO213(self):
        return self.capture_once(22)

    def getO214(self):
        return self.capture_once(23)

    def getO221(self):
        return self.capture_once(24)

    def getO222(self):
        return self.capture_once(25)

    def getO223(self):
        return self.capture_once(26)
    
    def getO224(self):
        return self.capture_once(27)

    def getOBDStandard(self):
        return self.capture_once(28)

    def getO2SensorPositionB(self):
        return self.capture_once(29)

    def getAuxInput(self):
        return self.capture_once(30)

    def getEngineTime(self):
        return self.capture_once(31)

    def getEngineMilTime(self):
        return self.capture_once(32)

