import os
import time
import subprocess
import sys
import math
#import serial
import random
import logging
import pygame
from pygame.locals import *

from obd.capture import *

class render_pygame:

    def __init__(self, skin):

        self.options = {
            0 : self.drawLogo,
            1 : self.drawSpeed,
            2 : self.drawBoost,
            3 : self.drawThrottle,
            4 : self.drawMAF
        }

        self.skin=skin

        #OBD
        self.obd = OBD_Capture()
        self.obd.connect()
        if self.obd.is_connected():
            print "OBD serial interface connected"
        else:
            print "OBD serial interface not found"

        disp_no = os.getenv("DISPLAY")

        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break

        if not found:
            raise Exception('No suitable video driver found!')
         
        #size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        size = [640, 480]
        print "Framebuffer size: %d x %d" % (size[0], size[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        print "Ready for update"
        
        self.screen.fill((0, 0, 0))        
        pygame.mouse.set_visible(0)
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()

    def changeSkin(self, skin):
        #ToDo: check if skin is instance of "skin type" 
        self.skin=skin
        return True

    def drawLogo(self):
        logo = pygame.image.load('images/vw.png')
        self.screen.blit(logo, (0, 0))
        pygame.display.update()

    def drawBoost(self):
        i=self.obd.capture_once(11)['value']
        self.screen.fill(self.skin['backC'])
        myfont = pygame.font.Font(self.skin['font'],250)
        spdText = myfont.render("{:01.2f}".format(float(abs(i))), 1, self.skin['fontC'])
        self.screen.blit(spdText, (100,50))
        labelFont = pygame.font.Font(self.skin['font'],60)
        lblText = labelFont.render("Bar", 1, self.skin['fontC'])
        self.screen.blit(lblText, (555,190))
        self.drawBar((i*100)/8)
        labelFont = pygame.font.Font(self.skin['font'],90)
        lblText = labelFont.render("Boost charge", 1, self.skin['fontC'])
        self.screen.blit(lblText, (85,350))
        pygame.display.update()

    def drawThrottle(self):
        throttle=self.obd.capture_once(17)
        self.screen.fill(self.skin['backC'])
        myfont = pygame.font.Font(self.skin['font'],250)
        spdText = myfont.render("{:03.1f}".format(throttle['value']), 1, self.skin['fontC'])
        self.screen.blit(spdText, (100,50))
        labelFont = pygame.font.Font(self.skin['font'],60)
        lblText = labelFont.render(throttle['unit'], 1, self.skin['fontC'])
        self.screen.blit(lblText, (555,190))
        self.drawBar(throttle['value'])
        labelFont = pygame.font.Font(self.skin['font'],90)
        lblText = labelFont.render(throttle['name'], 1, self.skin['fontC'])
        self.screen.blit(lblText, (85,350))
        pygame.display.update()

    def drawMAF(self):
        maf=self.obd.capture_once(16)
        self.screen.fill(self.skin['backC'])
        myfont = pygame.font.Font(self.skin['font'],180)
        spdText = myfont.render("{:07d}".format(int(maf['value'])), 1, self.skin['fontC'])
        self.screen.blit(spdText, (40,50))
        labelFont = pygame.font.Font(self.skin['font'],60)
        lblText = labelFont.render(maf['unit'], 1, self.skin['fontC'])
        self.screen.blit(lblText, (555,190))
        self.drawBar((maf['value']*100)/2340515) 
        labelFont = pygame.font.Font(self.skin['font'],90)
        lblText = labelFont.render(maf['name'], 1, self.skin['fontC'])
        self.screen.blit(lblText, (85,350))
        pygame.display.update()

    
    def drawSpeed(self):
        self.screen.fill(self.skin['backC'])
        if self.obd.is_connected():
            # Getting serial data
            last_coord=(random.randrange(10),random.randrange(10))
            spd=self.obd.capture_once(13)
            rpm=self.obd.capture_once(12)
            temp_intake=self.obd.capture_once(15)
            temp_cool=self.obd.capture_once(5)
            timming=self.obd.capture_once(14)         
           
            # Draw speed
            myfont = pygame.font.Font(self.skin['font'], 250)
            spdText = myfont.render("{:03d}".format(spd['value']), 1, self.skin['fontC'])
            self.screen.blit(spdText, (20,20))
            labelFont = pygame.font.Font(self.skin['font'], 100)
            lblText = labelFont.render(spd['unit'], 1, self.skin['fontC'])
            self.screen.blit(lblText, (380,130))

            # Draw revolutions
            subFont = pygame.font.Font(self.skin['font'], 140)
            altText = subFont.render("{:04d}".format(rpm['value']), 1, self.skin['fontC'])
            self.screen.blit(altText, (10,220))
            labelFont = pygame.font.Font(self.skin['font'], 50)
            lblText = labelFont.render(rpm['unit'], 1, self.skin['fontC'])
            self.screen.blit(lblText, (265,285))

            # Draw coolant temperature
            subFont = pygame.font.Font(self.skin['font'], 90)
            altText = subFont.render("{:02d}".format(temp_cool["value"]), 1, self.skin['fontC'])
            self.screen.blit(altText, (420,220))
            labelFont = pygame.font.Font(self.skin['font'], 60)
            lblText = labelFont.render(temp_cool["unit"], 1, self.skin['fontC'])
            self.screen.blit(lblText, (545,240))
            labelFont = pygame.font.Font(self.skin['font'], 40)
            lblText = labelFont.render(temp_cool["name"], 1, self.skin['fontC'])
            self.screen.blit(lblText, (380,290))

            # Draw intake air temperature
            subFont = pygame.font.Font(self.skin['font'], 90)
            altText = subFont.render("{:02d}".format(temp_intake["value"]), 1, self.skin['fontC'])
            self.screen.blit(altText, (420,330))
            labelFont = pygame.font.Font(self.skin['font'], 60)
            lblText = labelFont.render(temp_intake["unit"], 1, self.skin['fontC'])
            self.screen.blit(lblText, (545,350))
            labelFont = pygame.font.Font(self.skin['font'], 40)
            lblText = labelFont.render(temp_intake["name"], 1, self.skin['fontC'])  
            self.screen.blit(lblText, (360,400))

            # Draw Timing Advance
            subFont = pygame.font.Font(self.skin['font'], 90)
            altText = subFont.render("{:02.1f}".format(timming["value"]), 1, self.skin['fontC'])
            self.screen.blit(altText, (40,330))
            labelFont = pygame.font.Font(self.skin['font'], 60)
            lblText = labelFont.render(timming["unit"], 1, self.skin['fontC'])
            self.screen.blit(lblText, (250, 350))
            labelFont = pygame.font.Font(self.skin['font'], 40)
            lblText = labelFont.render(timming["name"], 1, self.skin['fontC'])  
            self.screen.blit(lblText, (60,400))
        else:
            labelFont = pygame.font.Font(self.skin['font'], 60)
            lblText = labelFont.render("OBD Disconnect...", 1, self.skin['fontC'])
            self.screen.blit(lblText, (100,50))
            self.obd.connect()
        pygame.display.update()


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



#       if self.obd.is_connected():
#            draw...
#        else:
#            labelFont = pygame.font.Font(self.skin['font'], 60)
#            lblText = labelFont.render("OBD Disconnect...", 1, self.skin['fontC'])
#           self.screen.blit(lblText, (100,50))
#           self.obd.connect()
#       pygame.display.update()