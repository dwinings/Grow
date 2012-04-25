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
VINE = 17
CBJ = 18
CBD = 19

class BlockImages():
    def __init__(self):
        self.GrassSheet = pygame.image.load('res/grass-dirt.png').convert()
        self.colorkey = self.GrassSheet.get_at((0,0))
        self.GrassSheet.set_colorkey(self.colorkey, pygame.RLEACCEL)

        self.spike1 = pygame.image.load('res/spikesB.png')
        self.spike2 = pygame.image.load('res/spikesL.png')
        self.spike3 = pygame.image.load('res/spikesT.png')
        self.spike4 = pygame.image.load('res/spikesR.png')

        self.switch1 = pygame.image.load('res/switchUp.png')
        self.switch2 = pygame.image.load('res/switchRight.png')
        self.switch3 = pygame.image.load('res/switchDown.png')
        self.switch4 = pygame.image.load('res/switchLeft.png')

        self.rock = pygame.image.load('res/rock.png').convert()

        self.chaser = pygame.image.load('res/rock.png').convert()

        self.vapor_cloud = pygame.image.load('res/rock.png').convert()

        self.icecube = pygame.image.load('res/icecube.png').convert()

        self.aswitch1 = pygame.image.load('res/switchaUp.png')
        self.aswitch2 = pygame.image.load('res/switchaRight.png')
        self.aswitch3 = pygame.image.load('res/switchaDown.png')
        self.aswitch4 = pygame.image.load('res/switchaLeft.png')

        self.vine = pygame.image.load('res/vine.png').convert()
        self.colorkey = self.vine.get_at((0,0))
        self.vine.set_colorkey(self.colorkey, pygame.RLEACCEL)

        self.qbox = pygame.image.load('res/qbox.png').convert()
        self.cbj = pygame.image.load('res/cbj.png')
        self.cbd = pygame.image.load('res/cbd.png')
class Block(object):
    def __init__(self):
        object.__init__(self)
        self.collides = True
        self.stopsPMovement = True
class DirtGrass(Block):
    def __init__(self, x, y):
        Block.__init__(self)
        
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
    def draw(self, screen, bimages):
        screen.blit(bimages.GrassSheet, self.drec, self.srec)
    def onCollide(self, ball):
        pass
class Spikes(Block):
    def __init__(self, x, y, stype):
        Block.__init__(self)
        if stype == 0:
            self.rec = pygame.Rect(0,8,10,2)
        elif stype == 1:
            self.rec = pygame.Rect(0,0,2,10)
        elif stype == 2:
            self.rec = pygame.Rect(0,0,10,2)
        else:
            self.rec = pygame.Rect(8,0,2,10)

        self.type = stype
        self.drec = pygame.Rect(0,0,10,10)
        self.drec = self.drec.move(x,y)
        
        self.rec = self.rec.move(x, y)

    def update(self, level, g, seconds):
        pass
    def draw(self, screen, bimages):
        if self.type == 0:
            screen.blit(bimages.spike1, self.drec)
        elif self.type == 1:
            screen.blit(bimages.spike2, self.drec)
        elif self.type == 2:
            screen.blit(bimages.spike3, self.drec)
        else:
            screen.blit(bimages.spike4, self.drec)
    def onCollide(self, ball):
        ball.alive = False
class Switch(Block):
    def __init__(self, x, y, stype):
        Block.__init__(self)
        self.type = stype
        self.rec = pygame.Rect(0,0,10,10)
        self.rec = self.rec.move(x, y)
        self.collides = False
        self.stopsPMovement = False
        self.type = stype
    def update(self, level, g, seconds):
        if self.rec.colliderect(level.b2.rec):
            level.b2.hud.drawInteract = True
            if g.control.f:
                if self.type == 0:
                    level.gstate = glevel.GSTATE_UP
                elif self.type == 1:
                    level.gstate = glevel.GSTATE_RIGHT
                elif self.type == 2:
                    level.gstate = glevel.GSTATE_DOWN
                else:
                    level.gstate = glevel.GSTATE_LEFT
    def draw(self, screen, bimages):
        if self.type == 0:
            screen.blit(bimages.switch1, self.rec)
        elif self.type == 1:
            screen.blit(bimages.switch2, self.rec)
        elif self.type == 2:
            screen.blit(bimages.switch3, self.rec)
        else:
            screen.blit(bimages.switch4, self.rec)
    def onCollide(self, ball):
        pass
class Rock(Block):
    def __init__(self, x, y):
        Block.__init__(self)
        self.rec = pygame.Rect(0,0,10,10)
        self.rec = self.rec.move(x, y)
    def update(self, level, g, seconds):
        pass
    def draw(self, screen, bimages):
        screen.blit(bimages.rock, self.rec)
    def onCollide(self, ball):
        pass
class Chaser(Block):
    def __init__(self, x, y):
        Block.__init__(self)
        self.rec = pygame.Rect(0,0,10,10)
        self.rec = self.rec.move(x,y)
        self.direc = [0.0,0.0]
        self.speed = 150
        self.minDistanceForAttack = 225
    def update(self, level, g, seconds):
        if gmath.distance(self.rec, level.b2.rec) < self.minDistanceForAttack:
            self.setDirection(level.b2)
            self.rec.left = self.rec.left + (self.direc[0] * self.speed * seconds)
            self.rec.top = self.rec.top + (self.direc[1] * self.speed * seconds)
    def draw(self, screen, bimages):
        screen.blit(bimages.chaser, self.rec)
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
        
        self.rec = pygame.Rect(0,0,10,10)
        self.rec = self.rec.move(x,y)
        self.collides = False
        self.stopsPMovement = False
    def update(self, level, g, seconds):
        if level.b2.state == gobjects.MODE_NORMAL and self.rec.colliderect(level.b2.rec):
            level.b2.hud.drawInteract = True
            if g.control.f:
                level.b2.state = gobjects.MODE_VAPOR
    def draw(self, screen, bimages):
        screen.blit(bimages.vapor_cloud, self.rec)
    def onCollide(self, ball):
        pass
class IceCube(Block):
    def __init__(self, x, y):
        Block.__init__(self)
        self.rec = pygame.Rect(0,0,10,10)
        self.rec = self.rec.move(x,y)
        self.collides = False
        self.stopsPMovement = False
    def update(self, level, g, seconds):
        if level.b2.state == gobjects.MODE_VAPOR and self.rec.colliderect(level.b2.rec) and not level.b2.touchingBlock:
            level.b2.hud.drawInteract = True
            if g.control.f:
                level.b2.state = gobjects.MODE_NORMAL
    def draw(self, screen, bimages):
        screen.blit(bimages.icecube, self.rec)
    def onCollide(self, ball):
        pass
class AutoSwitch(Block):
    def __init__(self, x, y, stype):
        Block.__init__(self)
        self.type = stype
        self.rec = pygame.Rect(0,0,10,10)
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
    def draw(self, screen, bimages):
        if self.stype == 0:
            screen.blit(bimages.aswitch1, self.rec)
        elif self.stype == 1:
            screen.blit(bimages.aswitch2, self.rec)
        elif self.stype == 2:
            screen.blit(bimages.aswitch3, self.rec)
        else:
            screen.blit(bimages.aswitch4, self.rec)
    def onCollide(self, ball):
        pass
class Vine(Block):
    def __init__(self, x, y):
        Block.__init__(self)

        self.rec = pygame.Rect(0,0,10,10)
        self.rec = self.rec.move(x,y)
        self.collides = False
        self.stopsPMovement = False
    def update(self, level, g, seconds):
        if level.b2.state == gobjects.MODE_NORMAL and self.rec.colliderect(level.b2.rec):
            level.b2.hud.drawInteract = True
            if g.control.f:
                level.b2.state = gobjects.MODE_ON_VINE
    def draw(self, screen, bimages):
        screen.blit(bimages.vine, self.rec)
    def onCollide(self, ball):
        pass
class CB_J(Block):
    def __init__(self, x, y):
        Block.__init__(self)
        self.rec = pygame.Rect(0,0,10,10)
        self.rec = self.rec.move(x,y)
        self.hovered = False
        self.loc = (x - 90, y - 50)
    def update(self, level, g, seconds):
        if self.rec.collidepoint(g.control.mloc):
            self.hovered = True
        else:
            self.hovered = False
    def draw(self, screen, bimages):
        screen.blit(bimages.qbox, self.rec)
        if self.hovered:
            screen.blit(bimages.cbj, self.loc)
    def onCollide(self, ball):
        pass
class CB_D(Block):
    def __init__(self, x, y):
        Block.__init__(self)
        self.rec = pygame.Rect(0,0,10,10)
        self.rec = self.rec.move(x,y)
        self.hovered = False
        self.loc = (x - 90, y - 50)
    def update(self, level, g, seconds):
        if self.rec.collidepoint(g.control.mloc):
            self.hovered = True
        else:
            self.hovered = False
    def draw(self, screen, bimages):
        screen.blit(bimages.qbox, self.rec)
        if self.hovered:
            screen.blit(bimages.cbd, self.loc)
    def onCollide(self, ball):
        pass
