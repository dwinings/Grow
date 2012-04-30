#Author: Jonathan Haslow-Hall
import gui, glevel, gcolors, pygame, re, os

class MenuScreen(gui.Screen):
    def __init__(self, width, height):
        self.playButton = gui.Button(0,0, 'Play',0)
        self.guideButton = gui.Button(0,0,'Guide',1)
        self.guideBackButton = gui.Button(380,450,'Back',2)
        
        self.playButton.setClickedMethod(self.onClick)
        self.guideButton.setClickedMethod(self.onClick)
        self.guideBackButton.setClickedMethod(self.onClick)
        
        self.bgroup = gui.ButtonGroup((width/2)-50,(height*.6),70)
        self.bgroup.add(self.playButton)
        self.bgroup.add(self.guideButton)

        self.showGuide = False;
        self.tutImage = pygame.image.load('res/tut.png').convert()

        self.menub = pygame.image.load('res/titleb.png').convert()
        
    def update(self, g, seconds):
        if self.showGuide == False:
            self.bgroup.update(g, seconds)
        else:
            self.guideBackButton.update(g,seconds)
    def draw(self, screen):
        screen.blit(self.menub, (0,0))
        if self.showGuide:
            screen.blit(self.tutImage, (0,0))
            self.guideBackButton.draw(screen)
        else:
            self.bgroup.draw(screen)
    def onClick(self, button, g):
        if button.my_id == 0:
            g.openGameScreen()
        elif button.my_id == 1:
            self.showGuide = True
        elif button.my_id == 2:
            self.showGuide = False
class CreditsScreen(gui.Screen):
    def __init__(self, width, height):
        self.quit = gui.Button(380,450,'Quit',0);
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
        #Pause background
        self.paused = False
        self.pausebg = pygame.image.load('res/pausedimage.png').convert()
        self.colorkey = self.pausebg.get_at((0,0))
        self.pausebg.set_colorkey(self.colorkey, pygame.RLEACCEL)
        
        self.pauseBRect = self.pausebg.get_rect()
        self.pause_fade = 50
        self.alpha = 0
        
        self.levelFile = levelFile

        #Pause menu buttons
        self.resumeButton = gui.Button(0,0, 'Resume',0)
        self.restartButton = gui.Button(0,0,'Restart',1)
        self.quitButton = gui.Button(0,0,'Quit',2)

        self.resumeButton.setClickedMethod(self.onClick)
        self.restartButton.setClickedMethod(self.onClick)
        self.quitButton.setClickedMethod(self.onClick)

        self.bgroup = gui.ButtonGroup((width/2),500,50)
        self.bgroup.add(self.resumeButton)
        self.bgroup.add(self.restartButton)
        self.bgroup.add(self.quitButton)

        self.bgroup_open = (height*.28) + 50
        self.bgroup_closed = 500.0
        self.bgroup_speed = 20.0
        
        #Gameover Variables
        self.gameoverI = pygame.image.load('res/gameover.png').convert()
        self.colorkey = self.gameoverI.get_at((0,0))
        self.gameoverI.set_colorkey(self.colorkey, pygame.RLEACCEL)
        self.gameoverRec = self.gameoverI.get_rect()
        self.respawnButton = gui.Button(0,0,'Why Not',3)

        self.bgroup2 = gui.ButtonGroup((width/2)-10,height*.5,70)
        self.bgroup2.add(self.respawnButton)

        #Background
        m = re.match('(.*)\.gmap', levelFile)
        bg_image_file = os.path.join('.', 'levels', m.group(1) + '_bg.png')
        if os.path.exists(bg_image_file):
            self.bg = pygame.image.load(bg_image_file.convert())
        else:
            self.bg = pygame.image.load('res/bg.png').convert()
        self.bgrect = self.bg.get_rect()

        #Completion Variables
        self.completionT = 1.4
        self.currentCT = 0.0

        self.level = glevel.Level(width, height, levelFile)
    def update(self, g, seconds):
        if g.control.one[0] and not g.control.one[1]:
            g.incrementLevel()
            g.openGameScreen()
        if self.paused:
            #Move bgroup
            if self.bgroup.loc[1] > self.bgroup_open:
                self.bgroup.loc[1] = self.bgroup.loc[1] - self.bgroup_speed
                if self.bgroup.loc[1] < self.bgroup_open:
                    self.bgroup.loc[1] = self.bgroup_open
                self.bgroup.locChanged()

            if self.alpha < 200:
                self.alpha += self.pause_fade
                if self.alpha > 200:
                    self.alpha = 200

            #Update Pause menu
            self.bgroup.update(g,seconds)
            if g.control.p[0] and not g.control.p[1]:
                self.paused = not self.paused
        else:
            if self.bgroup.loc[1] < self.bgroup_closed:
                self.bgroup.loc[1] = self.bgroup.loc[1] + self.bgroup_speed
                if self.bgroup.loc[1] > self.bgroup_closed:
                    self.bgroup.loc[1] = self.bgroup_closed
                self.bgroup.locChanged()

            if self.alpha > 0:
                self.alpha -= self.pause_fade
                if self.alpha < 0:
                    self.alpha = 0
                    
            #If player is no longer alive, prompt them to respawn
            if self.level.b2.alive == False:
                self.bgroup2.update(g, seconds)
                if self.respawnButton.isClicked():
                    g.openGameScreen()
            elif self.level.completed:
                self.currentCT += seconds
                self.level.update(g, seconds)
                if self.currentCT >= self.completionT:
                    g.incrementLevel()
                    g.openGameScreen()
            else:
                self.level.update(g, seconds)
                if g.control.p[0] and not g.control.p[1]:
                    self.paused = not self.paused
    def draw(self, screen):
        screen.fill(gcolors.CORNFLOWER_BLUE)
        screen.blit(self.bg, self.bgrect)
    	self.level.draw(screen)
        if self.level.b2.alive == False:
            #Draw the death screen
            self.gameoverI.set_alpha(200)
            screen.blit(self.gameoverI, self.gameoverRec)
            self.bgroup2.draw(screen)
        self.pausebg.set_alpha(self.alpha)
        screen.blit(self.pausebg, self.pauseBRect)
        self.bgroup.draw(screen)
    def restartLevel(self, width, height):
        self.level = glevel.Level(width, height, self.levelFile)
    def onClick(self, button, g):
        if button.my_id == 0:
            self.paused = False
        elif button.my_id == 1:
            g.openGameScreen()
        elif button.my_id == 2:
            g.quit = True
            
