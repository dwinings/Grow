#Author: Jonathan Haslow-Hall
import pygame, glevel, gcolors
from pygame import font
font.init()
basicFont = pygame.font.SysFont(None, 24, bold=False, italic=False)

MODE_NORMAL = 0
MODE_VAPOR = 1

class Ball:
    def __init__(self, x, y, width, height):
        self.image = pygame.image.load('res/box.png').convert()
        self.colorkey = self.image.get_at((0,0))
        self.image.set_colorkey(self.colorkey, pygame.RLEACCEL)

        self.vimage = pygame.image.load('res/boxv.png').convert()
        self.colorkey = self.vimage.get_at((0,0))
        self.vimage.set_colorkey(self.colorkey, pygame.RLEACCEL)

        self.rec = self.image.get_rect()
        self.rec = self.rec.move(x, y)

        self.growRec = pygame.Rect(0,0,30,30)
        
        self.speed = 200
        self.speedAir = 100
        self.direcmax = 1.0
        self.direc = [0.0, 0.0]
        self.vel = [0.0, 0.0]
        self.t = [0.0, 0.0]
        self.score = 0
        self.alive = True
        self.hud = Hud(width, height)

        self.inAirx = False
        self.inAiry = False
        self.airT = 0

        self.state = MODE_NORMAL

        self.touchingBlock = False
        
    def update(self, level, g, width, height, seconds):
        if self.alive:
            self.kMoveBounds = level.getLevelRec().copy()
            self.kMoveBounds = self.kMoveBounds.inflate(-(self.rec.width*2), -(self.rec.height*2))
            
            self.updateControls(level, g)
            self.updateVelocity(seconds)
            
            #Make 2 copies of the location rectangle.
            #One copy is made for each axis because there
            #might not allways be a collision on both.
            self.newLocX = self.rec.copy()
            self.newLocY = self.rec.copy()
            
            #Move new location recs by velocity respectivly 
            self.newLocX = self.newLocX.move(self.vel[0], 0)
            self.newLocY = self.newLocY.move(0, self.vel[1])

            #If in normal mode, apply gravity
            if self.state == MODE_NORMAL:
                #Apply gravity
                self.updateGravity(level,seconds)
            
            #Booleans used for collision detection
            self.collpassx = True
            self.collpassy = True

            ################
            #check collision
            ################
            if self.newLocX.colliderect(self.kMoveBounds) == False:
                self.collpassx = False
                self.vel[0] = 0
                self.t[0] = 0.0
                
            if self.newLocY.colliderect(self.kMoveBounds) == False:
                self.collpassy = False
                self.vel[1] = 0
                self.t[1] = 0.0

            self.touchingBlock = False
            self.gSwitched = False
            
            for i in range(50):
                for j in range(50):
                    if level.blocks[i][j] != None:
                        if level.blocks[i][j].collides:
                            if self.newLocX.colliderect(level.blocks[i][j].rec):
                                if self.state == MODE_NORMAL and level.blocks[i][j].stopsPMovement:
                                    self.collpassx = False
                                    self.vel[0] = 0
                                    self.t[0] = 0.0
                                    if level.gstate == glevel.GSTATE_UP or level.gstate == glevel.GSTATE_DOWN:
                                        if level.blocks[i][j].rec.centerx < self.rec.centerx:
                                            level.gstate = glevel.GSTATE_LEFT
                                            self.gSwitched = True
                                        else:
                                            level.gstate = glevel.GSTATE_RIGHT
                                            self.gSwitched = True
                                self.touchingBlock = True
                                level.blocks[i][j].onCollide(self)
                            if self.newLocY.colliderect(level.blocks[i][j].rec):
                                if self.state == MODE_NORMAL and level.blocks[i][j].stopsPMovement:
                                    self.collpassy = False
                                    self.vel[1] = 0
                                    self.t[1] = 0.0
                                    if level.gstate == glevel.GSTATE_LEFT or level.gstate == glevel.GSTATE_RIGHT:
                                        if not self.gSwitched:
                                            if level.blocks[i][j].rec.centery < self.rec.centery:
                                                level.gstate = glevel.GSTATE_UP
                                            else:
                                                level.gstate = glevel.GSTATE_DOWN
                                self.touchingBlock = True
                                level.blocks[i][j].onCollide(self)
                
            #if collision checks pass, set location to new locations respectively
            self.inAirx = False
            self.inAiry = False
            
            if self.collpassx:
                self.rec.left = self.newLocX.left
                if level.gstate == glevel.GSTATE_LEFT or level.gstate == glevel.GSTATE_RIGHT:
                    self.airT += seconds
                    if self.airT > .27:
                        self.inAirx = True
            elif not self.collpassx and (level.gstate == glevel.GSTATE_LEFT or level.gstate == glevel.GSTATE_RIGHT):
                self.airT = 0.0
            if self.collpassy:
                self.rec.top = self.newLocY.top
                if level.gstate == glevel.GSTATE_UP or level.gstate == glevel.GSTATE_DOWN:
                    self.airT += seconds
                    if self.airT > .27:
                        self.inAiry = True
            elif not self.collpassy and (level.gstate == glevel.GSTATE_UP or level.gstate == glevel.GSTATE_DOWN):
                self.airT = 0.0

            self.hud.update(self, level)

            self.growRec.x = self.rec.x - 5
            self.growRec.y = self.rec.y - 5
    def draw(self, screen):
        if self.state == MODE_NORMAL:
            screen.blit(self.image, self.rec)
        elif self.state == MODE_VAPOR:
            screen.blit(self.vimage, self.rec)
    def drawHud(self, screen):
        self.hud.draw(screen)
    def updateControls(self, level, game):
        if self.state == MODE_NORMAL:
            if level.gstate == glevel.GSTATE_LEFT or level.gstate == glevel.GSTATE_RIGHT:
                if game.control.up or game.control.down:
                    if game.control.up:
                        #if self.inAirx:
                        #    self.direc[1] = -(self.direcmax/2)
                        #else:
                        self.direc[1] = -self.direcmax
                    elif game.control.down:
                        #if self.inAirx:
                        #   self.direc[1] = (self.direcmax/2)
                        #else:
                        self.direc[1] = self.direcmax
                else:
                    self.direc[1] = 0
            else:
                self.direc[1] = 0
            if level.gstate == glevel.GSTATE_UP or level.gstate == glevel.GSTATE_DOWN:
                if game.control.left or game.control.right:
                    if game.control.left:
                        #if self.inAiry:
                        #    self.direc[0] = -(self.direcmax/2)
                        #else:
                        self.direc[0] = -self.direcmax
                    elif game.control.right:
                        #if self.inAiry:
                        #    self.direc[0] = (self.direcmax/2)
                        #else:
                        self.direc[0] = self.direcmax
                else:
                    self.direc[0] = 0
            else:
                self.direc[0] = 0
        elif self.state == MODE_VAPOR:
            if game.control.up:
                self.direc[1] = -self.direcmax
            elif game.control.down:
                self.direc[1] = self.direcmax
            else:
                self.direc[1] = 0
            if game.control.left:
                self.direc[0] = -self.direcmax
            elif game.control.right:
                self.direc[0] = self.direcmax
            else:
                self.direc[0] = 0
            
    def updateVelocity(self,seconds):
        #if self.state == MODE_NORMAL:
        #Update speed based on directions from input
        if not self.inAiry:
            self.vel[0] = self.speed * self.direc[0] * seconds
        else:
            self.vel[0] = self.speedAir * self.direc[0] * seconds
        if not self.inAirx:
            self.vel[1] = self.speed * self.direc[1] * seconds
        else:
            self.vel[1] = self.speedAir * self.direc[1] * seconds
    def updateGravity(self,level, seconds):
        if level.gstate == glevel.GSTATE_DOWN or level.gstate == glevel.GSTATE_UP:
            if level.gstate == glevel.GSTATE_DOWN:
                self.t[1] = self.t[1] + seconds
                self.newLocY.top = self.newLocY.top + (self.t[1] * glevel.G)
            if level.gstate == glevel.GSTATE_UP:
                self.t[1] = self.t[1] - seconds
                self.newLocY.top = self.newLocY.top + (self.t[1] * glevel.G)
            self.t[0] = 0.0

        elif level.gstate == glevel.GSTATE_LEFT or level.gstate == glevel.GSTATE_RIGHT:
            if level.gstate == glevel.GSTATE_LEFT:
                self.t[0] = self.t[0] - seconds
                self.newLocX.left = self.newLocX.left + (self.t[0] * glevel.G)
            if level.gstate == glevel.GSTATE_RIGHT:
                self.t[0] = self.t[0] + seconds
                self.newLocX.left = self.newLocX.left + (self.t[0] * glevel.G)
            self.t[1] = 0.0
    def respawn(self, x, y):
        self.rec.left = x
        self.rec.top = y
        self.alive = True
    def addScore(self, value):
        self.score += value
        if self.score < 0:
            self.score = 0
class Hud:
    def __init__(self, width, height):
        self.score = 0
        self.updownI = pygame.image.load('res/updown.png').convert()
        self.colorkey = self.updownI.get_at((0,0))
        self.updownI.set_colorkey(self.colorkey, pygame.RLEACCEL)
        
        self.leftrightI = pygame.image.load('res/leftright.png').convert()
        self.colorkey = self.leftrightI.get_at((0,0))
        self.leftrightI.set_colorkey(self.colorkey, pygame.RLEACCEL)

        self.arrowLoc = (20, height - 65)
        self.drawLR = True

        self.interactI = pygame.image.load('res/interact.png')
        self.interactLoc = (105, height - 50)

        self.manuals = 0

        self.drawInteract = False
                                         
    def update(self, ball,level):
        self.drawInteract = False
        self.score = ball.score
        if level.gstate == glevel.GSTATE_DOWN or level.gstate == glevel.GSTATE_UP:
            self.drawLR = True
        else:
            self.drawLR = False
        self.manuals = level.manualSwitches
    def draw(self, screen):
        """self.textI = basicFont.render('Score: ' + str(self.score),True, gcolors.WHITE)
        self.textR = self.textI.get_rect()
        screen.blit(self.textI, self.textR)

        self.textI = basicFont.render('Manuals Remaining: '+ str(self.manuals),True, gcolors.WHITE)
        screen.blit(self.textI, (250,0))"""

        if self.drawLR:
            self.updownI.set_alpha(50)
        else:
            self.updownI.set_alpha(200)
        screen.blit(self.updownI, self.arrowLoc)
        if self.drawLR == False:
            self.leftrightI.set_alpha(50)
        else:
            self.leftrightI.set_alpha(200)
        screen.blit(self.leftrightI, self.arrowLoc)

        if self.drawInteract:
            screen.blit(self.interactI, self.interactLoc)

