#Author: Jonathan Haslow-Hall
import pygame, glevel, math, gmath, gobjects

DIRT_GRASS = 0
SPIKES_B = 1
SPIKES_L = 2
SPIKES_T = 3
SPIKES_R = 4
SWITCH_U = 5
SWITCH_R = 6
SWITCH_D = 7
SWITCH_L = 8
ROCK = 9
CHASER = 10
VAPOR_CLOUD = 11
ICE_CUBE = 12
SWITCH_A_U = 13
SWITCH_A_R = 14
SWITCH_A_D = 15
SWITCH_A_L = 16

class Block(object):
    def __init__(self):
        object.__init__(self)
        self.collides = True
        self.stopsPMovement = True
class DirtGrass(Block):
    def __init__(self, x, y):
        Block.__init__(self)
        #super(Block, self).__init__()
        self.spritesheet = pygame.image.load('res/grass-dirt.png').convert()
        self.colorkey = self.spritesheet.get_at((0,0))
        self.spritesheet.set_colorkey(self.colorkey, pygame.RLEACCEL)
        
        #for drawing
        self.drec = pygame.Rect(0,0,20,20)
        self.drec = self.drec.move(x-5, y-5)

        #for collisions
        self.rec = pygame.Rect(0,0,10,10)
        self.rec = self.rec.move(x, y)

        #Frame variables
        self.srec = pygame.Rect(0,0,20,20)
        self.currentTime = 0.0
        self.animateTime = .12
        self.currentFrame = 0
        self.frames = 5
        
        #self.collides = True
        #self.stopsPMovement = True
        self.grown = False
        self.justGrown = False
        
    def update(self, level, g, seconds):
        if self.grown == False and level.b2.state == gobjects.MODE_NORMAL and self.rec.colliderect(level.b2.growRec):
            level.b2.score += 5
            self.grown = True
            self.justGrown = True
        if self.grown:
            if self.currentFrame < self.frames:
                self.currentTime += seconds
                if self.currentTime > self.animateTime:
                    self.currentTime -= self.animateTime
                    self.currentFrame += 1
                    if self.currentFrame < self.frames:
                        self.srec.left += 20
            if self.justGrown:
                level.grownCount += 1
                self.justGrown = False
    def draw(self, screen):
        screen.blit(self.spritesheet, self.drec, self.srec)
    def onCollide(self, ball):
        pass
class Spikes(Block):
    def __init__(self, x, y, stype):
        Block.__init__(self)
        if stype == 0:
            self.image = pygame.image.load('res/spikesB.png')
            self.rec = pygame.Rect(0,8,10,2)
        elif stype == 1:
            self.image = pygame.image.load('res/spikesL.png')
            self.rec = pygame.Rect(0,0,2,10)
        elif stype == 2:
            self.image = pygame.image.load('res/spikesT.png')
            self.rec = pygame.Rect(0,0,10,2)
        else:
            self.image = pygame.image.load('res/spikesR.png')
            self.rec = pygame.Rect(8,0,2,10)
            
        self.drec = self.image.get_rect()
        self.drec = self.drec.move(x,y)
        
        self.rec = self.rec.move(x, y)
        
        #self.collides = True
        #self.stopsPMovement = True
    def update(self, level, g, seconds):
        x = 0
    def draw(self, screen):
        screen.blit(self.image, self.drec)
    def onCollide(self, ball):
        ball.alive = False
class Switch(Block):
    def __init__(self, x, y, stype):
        Block.__init__(self)
        if stype == 0:
            self.image = pygame.image.load('res/switchUp.png')
        elif stype == 1:
            self.image = pygame.image.load('res/switchRight.png')
        elif stype == 2:
            self.image = pygame.image.load('res/switchDown.png')
        else:
            self.image = pygame.image.load('res/switchLeft.png')
        self.rec = self.image.get_rect()
        self.rec = self.rec.move(x, y)
        self.collides = False
        self.stopsPMovement = False
        self.stype = stype
    def update(self, level, g, seconds):
        if self.rec.colliderect(level.b2.rec):
            level.b2.hud.drawInteract = True
            if g.control.f:
                if self.stype == 0:
                    level.gstate = glevel.GSTATE_UP
                elif self.stype == 1:
                    level.gstate = glevel.GSTATE_RIGHT
                elif self.stype == 2:
                    level.gstate = glevel.GSTATE_DOWN
                else:
                    level.gstate = glevel.GSTATE_LEFT
    def draw(self, screen):
        screen.blit(self.image, self.rec)
    def onCollide(self, ball):
        pass
class Rock(Block):
    def __init__(self, x, y):
        Block.__init__(self)
        self.rock = pygame.image.load('res/rock.png').convert()
        self.rec = self.rock.get_rect()
        self.rec = self.rec.move(x, y)
        #self.collides = True
        #self.stopsPMovement = True
    def update(self, level, g, seconds):
        pass
    def draw(self, screen):
        screen.blit(self.rock, self.rec)
    def onCollide(self, ball):
        pass
class Chaser(Block):
    def __init__(self, x, y):
        Block.__init__(self)
        self.image = pygame.image.load('res/rock.png').convert()
        self.rec = self.image.get_rect()
        self.rec = self.rec.move(x,y)
        self.direc = [0.0,0.0]
        self.speed = 150
        self.minDistanceForAttack = 225
        #self.collides = True
        #self.stopsPMovement = True
    def update(self, level, g, seconds):
        if gmath.distance(self.rec, level.b2.rec) < self.minDistanceForAttack:
            self.setDirection(level.b2)
            self.rec.left = self.rec.left + (self.direc[0] * self.speed * seconds)
            self.rec.top = self.rec.top + (self.direc[1] * self.speed * seconds)
    def draw(self, screen):
        screen.blit(self.image, self.rec)
    def onCollide(self, ball):
        ball.alive = False
    def setDirection(self, ball):
        sx = ball.rec.left - self.rec.left
        sy = ball.rec.top - self.rec.top
        dx = 0.0
        dy = 0.0

        angle = math.atan2(sy, sx)

        dx = float(math.fabs(math.cos(angle)))
        dy = float(math.fabs(math.sin(angle)))

        if ball.rec.left < self.rec.left:
            dx = -dx
        if ball.rec.top < self.rec.top:
            dy = -dy

        self.direc[0] = dx
        self.direc[1] = dy
class VaporCloud(Block):
    def __init__(self, x, y):
        Block.__init__(self)
        self.image = pygame.image.load('res/rock.png').convert()
        self.rec = self.image.get_rect()
        self.rec = self.rec.move(x,y)
        self.collides = False
        self.stopsPMovement = False
    def update(self, level, g, seconds):
        if level.b2.state == gobjects.MODE_NORMAL and self.rec.colliderect(level.b2.rec):
            level.b2.hud.drawInteract = True
            if g.control.f:
                level.b2.state = gobjects.MODE_VAPOR
    def draw(self, screen):
        screen.blit(self.image, self.rec)
    def onCollide(self, ball):
        pass
class IceCube(Block):
    def __init__(self, x, y):
        Block.__init__(self)
        self.image = pygame.image.load('res/icecube.png').convert()
        self.rec = self.image.get_rect()
        self.rec = self.rec.move(x,y)
        self.collides = False
        self.stopsPMovement = False
    def update(self, level, g, seconds):
        if level.b2.state == gobjects.MODE_VAPOR and self.rec.colliderect(level.b2.rec) and not level.b2.touchingBlock:
            level.b2.hud.drawInteract = True
            if g.control.f:
                level.b2.state = gobjects.MODE_NORMAL
    def draw(self, screen):
        screen.blit(self.image, self.rec)
    def onCollide(self, ball):
        pass
class AutoSwitch(Block):
    def __init__(self, x, y, stype):
        Block.__init__(self)
        if stype == 0:
            self.image = pygame.image.load('res/switchaUp.png')
        elif stype == 1:
            self.image = pygame.image.load('res/switchaRight.png')
        elif stype == 2:
            self.image = pygame.image.load('res/switchaDown.png')
        else:
            self.image = pygame.image.load('res/switchaLeft.png')
        self.rec = self.image.get_rect()
        self.rec = self.rec.move(x, y)
        self.collides = False
        self.stopsPMovement = False
        self.stype = stype
    def update(self, level, g, seconds):
        if self.rec.colliderect(level.b2.rec):
            if self.stype == 0:
                level.gstate = glevel.GSTATE_UP
            elif self.stype == 1:
                level.gstate = glevel.GSTATE_RIGHT
            elif self.stype == 2:
                level.gstate = glevel.GSTATE_DOWN
            else:
                level.gstate = glevel.GSTATE_LEFT
    def draw(self, screen):
        screen.blit(self.image, self.rec)
    def onCollide(self, ball):
        pass
