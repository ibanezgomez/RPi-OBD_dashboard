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
            2 : { 'name': self.drawBoost   , 'sensors': [11]    },
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

        #GPIO switch
        self.switch = switch(threads=True)

    def refreshData(self, opt):
        self.obd.change_sensors(self.modes[opt]['sensors'])
        while self.obd.locked(): 
            print("Waiting for unlock...")
            time.sleep(0.1)
        return True

    def loadMode(self, fMode):
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
        self.render.draw(300, (110,40), "{:03d}".format(spd['value']))
        self.render.draw(50, (520,220), spd['unit'])

        # RPM
        rpm=self.obd.lastRead[1]
        self.render.draw(140, (190,290), "{:04d}".format(rpm['value']))
        self.render.draw(50, (450,355), rpm['unit'])

    def drawBoost(self):
        # Boost
        boost=self.obd.lastRead[0]
        self.render.draw(250, (100,50), "{:01.2f}".format(float(abs(boost['value']))))
        self.render.draw(60, (555,190), boost['unit'])
        self.render.drawBar((boost['value']*100)/8)
        self.render.draw(90, (85,350), boost['name'])

    def drawThrottle(self):
        # Throttle
        throttle=self.obd.lastRead[0]
        self.render.draw(250, (100,50), "{:03.1f}".format(throttle['value']))
        self.render.draw(60, (555,190), throttle['unit'])
        self.render.drawBar(throttle['value'])
        self.render.draw(90, (85,350), throttle['name'])

        # Timing Advance
        timming=self.obd.lastRead[1]
        self.render.draw(90, (40,330), "{:02.1f}".format(timming["value"]))
        self.render.draw(60, (250, 350), timming["unit"])
        self.render.draw(40, (60,400), timming["name"])

    def drawMAF(self):
        # MAF
        maf=self.obd.lastRead[0]
        self.render.draw(180, (40,50), "{:02.1f}".format(maf["value"]))
        self.render.draw(60, (555, 190), maf["unit"])
        self.render.drawBar((maf['value']*100)/2340515) 
        self.render.draw(90, (85,350), maf["name"])

    def drawTemp(self):
        # Draw coolant temperature
        temp_cool=self.obd.lastRead[0]
        self.render.draw(90, (420,220), "{:02d}".format(temp_cool["value"]))
        self.render.draw(60, (545,240), temp_cool["unit"])
        self.render.draw(40, (380,290), temp_cool["name"])

        # Draw intake air temperature
        temp_intake=self.obd.lastRead[1]
        self.render.draw(90, (420,330), "{:02d}".format(temp_intake["value"]))
        self.render.draw(60, (545,350), temp_intake["unit"])
        self.render.draw(40, (360,400), temp_intake["name"])