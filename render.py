import os
#import time
#import subprocess
#import sys
#import math
#import random
#import logging
import pygame
from pygame.locals import *

from utils.logger import log

class RenderPygame:

    def __init__(self, skin):

        disp_no = os.getenv("DISPLAY")
        self.skin=skin
        self.pygame=pygame

        if disp_no:
            log.debug("I'm running under X display = {0}".format(disp_no))
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                self.pygame.display.init()
            except self.pygame.error:
                log.error('Driver: {0} failed.'.format(driver))
                continue
            found = True
            break

        if not found:
            raise Exception('No suitable video driver found!')
         
        #size = (self.pygame.display.Info().current_w, self.pygame.display.Info().current_h)
        size = [640, 480]
        log.debug("Framebuffer size: %d x %d" % (size[0], size[1]))
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT: sys.exit()
        
        self.screen = self.pygame.display.set_mode(size, self.pygame.FULLSCREEN)

        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT: sys.exit()
        log.debug("Ready for update")
        
        self.screen.fill((0, 0, 0))        
        self.pygame.mouse.set_visible(0)
        # Initialise font support
        self.pygame.font.init()
        # Render the screen
        self.pygame.display.update()


    def draw(self, size, pos, value):
        myfont = self.pygame.font.Font(self.skin['font'], size)
        spdText = myfont.render(value, 1, self.skin['fontC'])
        self.screen.blit(spdText, pos)

    def drawIMG(self, img, pos):
        logo = self.pygame.image.load(img)
        self.screen.blit(logo, pos)

    def drawTest(self):
        self.screen.fill(self.skin['backC'])
        color=(148, 255, 53)
        #size = [640, 480]
        #self.pygame.draw.circle(self.screen, color, (20,20), 10, 0) # Esquina sup. izq
        #self.pygame.draw.circle(self.screen, color, (620,20), 10, 0) # Esquina sup. der
        #self.pygame.draw.circle(self.screen, color, (20,460), 10, 0) # Esquina inf. izq
        #self.pygame.draw.circle(self.screen, color, (620,460), 10, 0) # Esquina inf. der
        #self.pygame.display.update()
        #time.sleep(2)
          
        self.screen.fill(self.skin['backC'])
        x=20
        while x<=620:
            self.pygame.draw.circle(self.screen, color, (x,20), 10, 0) # Esquina sup. izq
            self.pygame.display.update()
            time.sleep(0.1)
            x=x+20

        y=20
        while y<=460:
            self.pygame.draw.circle(self.screen, color, (620,y), 10, 0) # Esquina sup. izq
            self.pygame.display.update()
            time.sleep(0.1)
            y=y+20


        x=620
        while x>=20:
            self.pygame.draw.circle(self.screen, color, (x,460), 10, 0) # Esquina sup. izq
            self.pygame.display.update()
            time.sleep(0.1)
            x=x-20

        y=460
        while y>=20:
            self.pygame.draw.circle(self.screen, color, (20,y), 10, 0) # Esquina sup. izq
            self.pygame.display.update()
            time.sleep(0.1)
            y=y-20

    def drawBar(self, percent=20):
        color=(148, 255, 53)
        y1 = self.screen.get_height()*0.6
        y2 = y1 +20
        max_width=500-40
        if percent>0:
            if percent>80: color=(246, 2, 27)
            marco=self.pygame.draw.rect(self.screen, color, (100,y1,max_width,              50), 2 )
            progr=self.pygame.draw.rect(self.screen, color, (100,y1,(percent*max_width)/100,50), 0)
        else:
            color=(246, 2, 27)
            font = self.pygame.font.Font(self.skin['font'], 90)
            vacum =font.render("VACUM", True, color)
            self.screen.blit(vacum, (240,260))
