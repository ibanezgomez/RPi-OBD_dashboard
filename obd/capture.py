import serial
import platform
from datetime import datetime
import time

import sensors
import io
from utils import *


class OBD_Capture():

    def __init__(self):
        self.port = None
        localtime = time.localtime(time.time())

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
    
    # 0: pids
    # 1: dtc_status
    # 2: dtc_ff
    # 3: fuel_status
    # 4: load
    # 5: temp
    # 6: short_term_fuel_trim_1
    # 7: long_term_fuel_trim_1
    # 8: short_term_fuel_trim_2
    # 9: long_term_fuel_trim_2
    # 10: fuel_pressure
    # 11: manifold_pressure
    # 12: rpm
    # 13: speed
    # 14: timing_advance
    # 15: intake_air_temp
    # 16: maf
    # 17: throttle_pos
    # 18: secondary_air_status
    # 19: o2_sensor_positions
    # 20: o211
    # 21: o212
    # 22: o213
    # 23: o214
    # 24: o221
    # 25: o222
    # 26: o223
    # 27: o224
    # 28: obd_standard
    # 29: o2_sensor_position_b
    # 30: aux_input
    # 31: engine_time
    # 32: engine_mil_time    
    def capture_once(self, sensor):
        (n, v, u) = self.port.sensor(sensor)
        return {"name": n.strip(), "value": v, "unit": u}




