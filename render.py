import os
import time
import subprocess
import sys
import math
import random
import logging
import pygame
from pygame.locals import *

from obd.capture import *
from utils.logger import log

class render_pygame:

    def __init__(self, skin):

        self.modes = {
            0 : { 'name': self.drawLogo    , 'sensors': []      },
            1 : { 'name': self.drawSpeed   , 'sensors': [13, 12]},
            2 : { 'name': self.drawBoost   , 'sensors': [11]    },
            3 : { 'name': self.drawThrottle, 'sensors': [17, 14]},
            4 : { 'name': self.drawMAF     , 'sensors': [16]    },
            0 : { 'name': self.drawTemp    , 'sensors': [5, 15] },

        }

        self.skin=skin

        #OBD
        self.obd = OBD_Capture(threads=True)
        if self.obd.connected():
            log.debug("OBD serial interface connected")
        else:
            log.debug("OBD serial interface not found")

        disp_no = os.getenv("DISPLAY")

        if disp_no:
            log.debug("I'm running under X display = {0}".format(disp_no))
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                log.error('Driver: {0} failed.'.format(driver))
                continue
            found = True
            break

        if not found:
            raise Exception('No suitable video driver found!')
         
        #size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        size = [640, 480]
        log.debug("Framebuffer size: %d x %d" % (size[0], size[1]))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        log.debug("Ready for update")
        
        self.screen.fill((0, 0, 0))        
        pygame.mouse.set_visible(0)
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()

    def refreshData(self, opt):
        self.obd.change_sensors(self.modes[opt]['sensors'])
        while self.obd.locked(): 
            print("Waiting for unlock...")
            time.sleep(0.1)
        return True

    def changeSkin(self, skin):
        self.skin=skin
        return True

    def drawLogo(self):
        logo = pygame.image.load('images/car.jpg')
        self.screen.blit(logo, (0, 0))
        pygame.display.update()

    def draw(self, size, pos, value):
        myfont = pygame.font.Font(self.skin['font'], size)
        spdText = myfont.render(value, 1, self.skin['fontC'])
        self.screen.blit(spdText, pos)

    def drawSpeed(self):  
        self.screen.fill(self.skin['backC'])  

        # Speed
        spd=self.obd.lastRead[0]
        self.draw(300, (110,40), "{:03d}".format(spd['value']))
        self.draw(50, (520,220), spd['unit'])

        # RPM
        rpm=self.obd.lastRead[1]
        self.draw(140, (190,290), "{:04d}".format(rpm['value']))
        self.draw(50, (450,355), rpm['unit'])

        pygame.display.update()

    def drawBoost(self):
        self.screen.fill(self.skin['backC'])

        # Boost
        boost=self.obd.lastRead[0]
        self.draw(250, (100,50), "{:01.2f}".format(float(abs(boost['value']))))
        self.draw(60, (555,190), boost['unit'])
        self.drawBar((boost['value']*100)/8)
        self.draw(90, (85,350), boost['name'])

        pygame.display.update()

    def drawThrottle(self):
        self.screen.fill(self.skin['backC'])

        # Throttle
        throttle=self.obd.lastRead[0]
        self.draw(250, (100,50), "{:03.1f}".format(throttle['value']))
        self.draw(60, (555,190), throttle['unit'])
        self.drawBar(throttle['value'])
        self.draw(90, (85,350), throttle['name'])

        # Timing Advance
        timming=self.obd.lastRead[1]
        self.draw(90, (40,330), "{:02.1f}".format(timming["value"]))
        self.draw(60, (250, 350), timming["unit"])
        self.draw(40, (60,400), timming["name"])

        pygame.display.update()

    def drawMAF(self):
        self.screen.fill(self.skin['backC'])

        # MAF
        maf=self.obd.lastRead[0]
        self.draw(180, (40,50), "{:02.1f}".format(maf["value"]))
        self.draw(60, (555, 190), maf["unit"])
        self.drawBar((maf['value']*100)/2340515) 
        self.draw(90, (85,350), maf["name"])
        
        pygame.display.update()

    def drawTemp(self):
        self.screen.fill(self.skin['backC'])

        # Draw coolant temperature
        temp_cool=self.obd.lastRead[0]
        self.draw(90, (420,220), "{:02d}".format(temp_cool["value"]))
        self.draw(60, (545,240), temp_cool["unit"])
        self.draw(40, (380,290), temp_cool["name"])

        # Draw intake air temperature
        temp_intake=self.obd.lastRead[1]
        self.draw(90, (420,330), "{:02d}".format(temp_intake["value"]))
        self.draw(60, (545,350), temp_intake["unit"])
        self.draw(40, (360,400), temp_intake["name"])

        pygame.display.update()

    
    def drawTest(self):
        self.screen.fill(self.skin['backC'])

        color=(148, 255, 53)
        #size = [640, 480]
        #pygame.draw.circle(self.screen, color, (20,20), 10, 0) # Esquina sup. izq
        #pygame.draw.circle(self.screen, color, (620,20), 10, 0) # Esquina sup. der
        #pygame.draw.circle(self.screen, color, (20,460), 10, 0) # Esquina inf. izq
        #pygame.draw.circle(self.screen, color, (620,460), 10, 0) # Esquina inf. der
        #pygame.display.update()
        #time.sleep(2)
          
        self.screen.fill(self.skin['backC'])
        x=20
        while x<=620:
            pygame.draw.circle(self.screen, color, (x,20), 10, 0) # Esquina sup. izq
            pygame.display.update()
            time.sleep(0.1)
            x=x+20

        y=20
        while y<=460:
            pygame.draw.circle(self.screen, color, (620,y), 10, 0) # Esquina sup. izq
            pygame.display.update()
            time.sleep(0.1)
            y=y+20


        x=620
        while x>=20:
            pygame.draw.circle(self.screen, color, (x,460), 10, 0) # Esquina sup. izq
            pygame.display.update()
            time.sleep(0.1)
            x=x-20

        y=460
        while y>=20:
            pygame.draw.circle(self.screen, color, (20,y), 10, 0) # Esquina sup. izq
            pygame.display.update()
            time.sleep(0.1)
            y=y-20

    def drawBar(self, percent=20):
        color=(148, 255, 53)
        y1 = self.screen.get_height()*0.6
        y2 = y1 +20
        max_width=500-40
        if percent>0:
            if percent>80: color=(246, 2, 27)
            marco=pygame.draw.rect(self.screen, color, (100,y1,max_width,              50), 2 )
            progr=pygame.draw.rect(self.screen, color, (100,y1,(percent*max_width)/100,50), 0)
        else:
            color=(246, 2, 27)
            font = pygame.font.Font(self.skin['font'], 90)
            vacum =font.render("VACUM", True, color)
            self.screen.blit(vacum, (240,260))
