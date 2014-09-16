from obd.capture import *
import time

obd = OBD_Capture(True)
time.sleep(1)
for i in range(0,10):
	print i, " LastRead: ", obd.lastRead
	time.sleep(0.1)
obd.change_sensors([5, 15, 5, 12])
for i in range(0,10):
	print i, "LastRead: ", obd.lastRead
	time.sleep(0.1)
obd.reading=False