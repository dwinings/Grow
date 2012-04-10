#Author: Jonathan Haslow-Hall
import gui, glevel, gcolors, pygame

class MenuScreen(gui.Screen):
    def __init__(self, width, height):
        self.playButton = gui.Button((width/2)-50,(height*.6) + 50, 'Play')
        self.guideButton = gui.Button((width/2)-50,(height*.6) + 100,'Guide')
        self.guideBackButton = gui.Button(380,450,'Back');

        self.showGuide = False;
        self.tutImage = pygame.image.load('res/tut.png').convert()

        self.menub = pygame.image.load('res/titleb.png').convert()
        
    def update(self, g, seconds):
	#g.openGameScreen()
        if self.showGuide == False:
            self.playButton.update(g, seconds)
            self.guideButton.update(g,seconds)
            if self.playButton.clicked:
                g.openGameScreen()
            if self.guideButton.isClicked():
                self.showGuide = True;
        else:
            self.guideBackButton.update(g,seconds)
            if self.guideBackButton.isClicked():
                self.showGuide = False;
    def draw(self, screen):
        screen.blit(self.menub, (0,0))
        if self.showGuide:
            screen.blit(self.tutImage, (0,0))
            self.guideBackButton.draw(screen)
        else:
            self.playButton.draw(screen)
            self.guideButton.draw(screen)
class CreditsScreen(gui.Screen):
    def __init__(self, width, height):
        self.quit = gui.Button(380,450,'Quit');
        self.aboutImage = pygame.image.load('res/credit.png').convert()
    def update(self, g, seconds):
        self.quit.update(g, seconds)
        if self.quit.isClicked():
            g.quit = True
    def draw(self, screen):
        screen.blit(self.aboutImage, (0,0))
        self.quit.draw(screen)
class GameScreen(gui.Screen):
    def __init__(self, width, height, levelFile):
        self.paused = False
        self.pauseBackground = pygame.image.load('res/pausedimage.png')
        self.pauseBRect = self.pauseBackground.get_rect()
        
        self.levelFile = levelFile

        #Pause menu buttons
        self.resumeButton = gui.Button((width/2)-50,(height*.28) + 50, 'Resume')
        self.restartButton = gui.Button((width/2)-50,(height*.28) + 100,'Restart')
        self.quitButton = gui.Button((width/2)-50,(height*.28) + 150,'Quit')

        #Gameover Variables
        self.gameoverI = pygame.image.load('res/gameover.png')
        self.gameoverRec = self.gameoverI.get_rect()
        self.respawnButton = gui.Button((width/2)-50,height*.4,'Respawn')

        #Background
        self.bg = pygame.image.load('res/bg.png').convert()
        self.bgrect = self.bg.get_rect()

        #Completion Variables
        self.completionT = 1.4
        self.currentCT = 0.0

        self.level = glevel.Level(width, height, levelFile)
    def update(self, g, seconds):
        if self.paused:
            #Update Pause menu
            self.resumeButton.update(g,seconds)
            if self.resumeButton.isClicked():
                self.paused = False
            self.restartButton.update(g,seconds)
            if self.restartButton.isClicked():
                g.openGameScreen()
            self.quitButton.update(g,seconds)
            if self.quitButton.isClicked():
                g.quit = True
        else:
            self.level.update(g, seconds)
            
            #If player is no longer alive, prompt them to respawn
            if self.level.b2.alive == False:
                self.respawnButton.update(g, seconds)
                if self.respawnButton.isClicked():
                    self.level.respawn()
                    
            if self.level.completed:
                self.currentCT += seconds
                if self.currentCT >= self.completionT:
                    g.incrementLevel()
                    g.openGameScreen()
        if g.control.p[0] and not g.control.p[1]:
            self.paused = not self.paused
    def draw(self, screen):
        screen.fill(gcolors.CORNFLOWER_BLUE)
        screen.blit(self.bg, self.bgrect)
	self.level.draw(screen)
	if self.paused:
            screen.blit(self.pauseBackground, self.pauseBRect)
            self.resumeButton.draw(screen)
            self.restartButton.draw(screen)
            self.quitButton.draw(screen)
        if self.level.b2.alive == False:
            screen.blit(self.gameoverI, self.gameoverRec)
            self.respawnButton.draw(screen)
    def restartLevel(self, width, height):
        self.level = glevel.Level(width, height, self.levelFile)
            
