#Author: Jonathan Haslow-Hall
import sys, pygame, glevel, gui, gscreens, ginput, time, gcolors
from pygame import font

class Game:
        def __init__(self):
                #Create Screen
                pygame.init()
                pygame.display.set_caption('Grow!')

                #Create Controls for tracking
                self.control = ginput.Controls()

                self.quit = False

                self.size = self.width, self.height = 500, 500

                self.screen = pygame.display.set_mode(self.size,pygame.DOUBLEBUF, 32)

                self.oldt = 0.0
                self.t = 0.0
                self.seconds = 0.0
                
                self.currentScreen = gscreens.MenuScreen(self.width, self.height)

                self.currentLevel = 0;
                self.levelcount = 4;
                self.levelFiles = ['levels/level1.1.gmap','levels/level1.gmap','levels/level2.gmap','levels/level3.gmap']

        def openMenuScreen(self):
                return gscreens.MenuScreen(self.width, self.height)
        def openGameScreen(self):
                if (self.currentLevel < self.levelcount):
                        self.currentScreen = gscreens.GameScreen(self.width, self.height, self.levelFiles[self.currentLevel])
                else:
                        self.currentScreen = gscreens.CreditsScreen(self.width, self.height)
        def incrementLevel(self):
                self.currentLevel = self.currentLevel +1
        def run(self):
                while 1:
                        pygame.time.Clock().tick(60)

                        #Grab time
                        self.t = time.time()
                        if self.oldt != 0:
                                self.seconds = self.t - self.oldt
                
                        #Update events
                        for event in pygame.event.get():
                                if event.type == pygame.QUIT: sys.exit()

                        #Update Controls state if event was pressed
                        self.control.updateControls()
                        
                        #Update
                        self.currentScreen.update(self, self.seconds)
        
                        #Draw
                        self.currentScreen.draw(self.screen)
                        pygame.display.flip()

                        #Set old time
                        self.oldt = self.t

                        #Update Controls second state to keep track of releases
                        self.control.updateLast()

                        if self.quit:
                                return
