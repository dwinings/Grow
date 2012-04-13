#Author: Jonathan Haslow-Hall
import sys, os, re, pygame, glevel, gui, gscreens, ginput, time, gcolors
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

                # Os.walk() returns a generator; I don't want to do a potentially expensive recursive
                # file enumeration, so by using next, I only deal with the first folder. By 
                # iterating over os.walk, we could easily deal with recursive file location.
                # os.walk.next() returns a list in the form [current_dir, sub_dirs, files].
                # We obviously only want the last of these.
                
                self.levelFiles = []
                for current_file in sorted(os.walk(os.path.join('.', 'levels')).next()[2]):
                    m = re.search("""\.gmap\Z""", current_file)
                    if m is not None:
                        self.levelFiles.append(os.path.join('.', 'levels', current_file))
                print self.levelFiles

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

if __name__ == '__main__':
    g = Game()
    g.run()
