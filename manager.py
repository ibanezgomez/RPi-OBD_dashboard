import time

from render import *    
from obd.capture import *
from gpio.switch import *
from utils.logger import log

class Manager:

    def __init__(self):
        
        # name: function name
        # font: sensors neeeded
        self.modes = {
            0 : { 'name': self.drawLogo    , 'sensors': []      },
            1 : { 'name': self.drawSpeed   , 'sensors': [13, 12]},
            2 : { 'name': self.drawIntakeManifold , 'sensors': [11]    },
            3 : { 'name': self.drawThrottle, 'sensors': [17, 14]},
            4 : { 'name': self.drawMAF     , 'sensors': [16]    },
            0 : { 'name': self.drawTemp    , 'sensors': [5, 15] },

        }

        # name:  skin name
        # font:  font name
        # fontC: font color
        # backC: background color
        self.skins = {
            0: {'name': 'oemDay',   'font': 'fonts/digital7.ttf', 'fontC': (36,44,43), 'backC': (165,186,145)},
            1: {'name': 'oemNight', 'font': 'fonts/digital7.ttf', 'fontC': (36,44,43), 'backC': (28,70,156)}
        }

        # OBD
        self.obd = OBD_Capture(threads=True)
        
        # PYGAME
        self.render = RenderPygame(self.skins[0])

        self.change = False

    def refreshData(self, opt):
        self.obd.change_sensors(self.modes[opt]['sensors'])
        while self.obd.locked(): 
            print("Waiting for unlock...")
            time.sleep(0.1)
        return True

    def loadMode(self, fMode):
        if self.render.touchDetect(): self.change = True;
        h=int(time.strftime("%H"))
        if h>19 or h<7: self.changeSkin(self.skins[1]) 
        else: self.changeSkin(self.skins[0])
        self.render.clean()
        fMode()
        self.updateScreen()


    def updateScreen(self):
        self.render.pygame.display.update()
       
    def changeSkin(self, skin):
        self.render.skin=skin
        return True

    def drawLogo(self):
        #IMG
        self.render.drawIMG('images/car.jpg', (0, 0))

    def drawSpeed(self):  
        # Speed
        spd=self.obd.lastRead[0]
        self.render.draw(180, (100,0), "{:03d}".format(spd['value']))     
        self.render.draw(50, (370,10), spd['unit'])

        self.render.drawLine(self.render.skin['fontC'], (0,160), (480,160), 5)

        # RPM
        rpm=self.obd.lastRead[1]
        self.render.draw(180, (20,170), "{:04d}".format(rpm['value']))
        self.render.draw(50, (370,180), rpm['unit'])

    def drawIntakeManifold(self):
        # Boost
        intake=self.obd.lastRead[0]
        self.render.draw(250, (100,50), "{:01.2f}".format(float(intake['value'])))
        self.render.draw(60, (550,190), intake['unit'])  
        self.render.draw(70, (75,350), intake['name'].split()[0]+" "+intake['name'].split()[1])
        self.render.draw(70, (190,410), intake['name'].split()[2])
        self.render.drawBar(480, (75, 480), percent(intake['value'],8))
      

    def drawThrottle(self):
        # Throttle
        throttle=self.obd.lastRead[0]
        self.render.draw(100, (365,50), "{:03.1f}".format(throttle['value']))
        
        self.render.drawBar(580, (30,260), throttle['value'])
        self.render.draw(50, (10,60), throttle['name'])

        # Timing Advance
        timming=self.obd.lastRead[1]
        self.render.draw(100, (365,280), "{:02.1f}".format(abs(timming["value"])))
        self.render.draw(60, (555, 310), timming["unit"])
        self.render.draw(50, (10,290), timming["name"])
        self.render.drawBar(580, (30,650), percent(timming['value'], 65))


    def drawMAF(self):
        # MAF
        maf=self.obd.lastRead[0]
        self.render.draw(180, (20,40), "{:07d}".format(maf["value"]))
        self.render.draw(60, (505, 190), maf["unit"]) 
        self.render.draw(70, (15,380), maf["name"])
        self.render.drawBar(480, (75,480), percent(maf['value'],2340515))

    def drawTemp(self):
        # Coolant temperature
        temp_cool=self.obd.lastRead[0]
        self.render.draw(200, (50,20), "{:02d}".format(temp_cool["value"]))
        self.render.draw(60, (320,120), temp_cool["unit"])
        self.render.draw(60, (20,190), temp_cool["name"])

        # Intake air temperature
        temp_intake=self.obd.lastRead[1]
        self.render.draw(200, (320,250), "{:02d}".format(temp_intake["value"]))
        self.render.draw(60, (590,350), temp_intake["unit"])
        self.render.draw(60, (210,420), temp_intake["name"])


def percent(n, max):
    return (n*100)/max