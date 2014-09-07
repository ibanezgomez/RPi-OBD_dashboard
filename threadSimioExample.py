import time
from gpio.switch import *
from threading import Thread

estado=False
switch = switch()

def myfunc():
	global estado		
	while True:
		print "Comprobando estado del switch"
		if switch.read(0)==1: estado=True
		else: estado=False
		time.sleep(0.3)


t = Thread(target=myfunc)
t.start()

while True:
	print "Valor de estado "+str(estado)
