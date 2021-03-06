#Author: Jonathan Haslow-Hall
import pygame, glevel, math, gmath, gobjects, random
from random import randint

DIRT_GRASS = 0
SPIKES_B = 1
SPIKES_L = 2
SPIKES_T = 3
SPIKES_R = 4

#Player Gravity switches
SWITCH_U = 5
SWITCH_R = 6
SWITCH_D = 7
SWITCH_L = 8

ROCK = 9
CHASER = 10
VAPOR_CLOUD = 11
ICE_CUBE = 12

#Player Automatic Gravity switches
SWITCH_A_U = 13
SWITCH_A_R = 14
SWITCH_A_D = 15
SWITCH_A_L = 16

VINE = 17
CBJ = 18
CBD = 19
CBE = 20

#Corner spikes
SPIKES_BR = 21
SPIKES_BL = 22
SPIKES_TR = 23
SPIKES_TL = 24
DARK_ROCK = 25
CRATE = 26

#Block Gravity switches
SWITCH_B_U = 27
SWITCH_B_R = 28
SWITCH_B_D = 29
SWITCH_B_L = 30

class BlockImages():
    def __init__(self):
        self.GrassSheet = pygame.image.load('res/grass-dirt.png').convert()
        self.colorkey = self.GrassSheet.get_at((0,0))
        self.GrassSheet.set_colorkey(self.colorkey, pygame.RLEACCEL)

        self.spike1 = pygame.image.load('res/spikesB.png')
        self.spike2 = pygame.image.load('res/spikesL.png')
        self.spike3 = pygame.image.load('res/spikesT.png')
        self.spike4 = pygame.image.load('res/spikesR.png')

        self.spike5 = pygame.image.load('res/spikesBR.png')
        self.spike6 = pygame.image.load('res/spikesBL.png')
        self.spike7 = pygame.image.load('res/spikesTR.png')
        self.spike8 = pygame.image.load('res/spikesTL.png')

        self.switch1 = pygame.image.load('res/switchUp.png')
        self.switch2 = pygame.image.load('res/switchRight.png')
        self.switch3 = pygame.image.load('res/switchDown.png')
        self.switch4 = pygame.image.load('res/switchLeft.png')

        self.rock = pygame.image.load('res/rock.png').convert()

        self.dark_rock = pygame.image.load('res/dark_rock.png').convert()

        self.chaser = pygame.image.load('res/rock.png').convert()

        self.icecube = pygame.image.load('res/icecube.png').convert()

        self.aswitch1 = pygame.image.load('res/switchaUp.png')
        self.aswitch2 = pygame.image.load('res/switchaRight.png')
        self.aswitch3 = pygame.image.load('res/switchaDown.png')
        self.aswitch4 = pygame.image.load('res/switchaLeft.png')

        #Vine images
        self.vine1 = pygame.image.load('res/vine1.png').convert()
        self.colorkey = self.vine1.get_at((0,0))
        self.vine1.set_colorkey(self.colorkey, pygame.RLEACCEL)
        
        self.vine2 = pygame.image.load('res/vine2.png').convert()
        self.colorkey = self.vine1.get_at((0,0))
        self.vine2.set_colorkey(self.colorkey, pygame.RLEACCEL)
        
        self.vine3 = pygame.image.load('res/vine3.png').convert()
        self.colorkey = self.vine3.get_at((0,0))
        self.vine3.set_colorkey(self.colorkey, pygame.RLEACCEL)

        self.qbox = pygame.image.load('res/qbox.png').convert()
        self.cbj = pygame.image.load('res/cbj.png')
        self.cbd = pygame.image.load('res/cbd.png')
        self.cbe = pygame.image.load('res/cbe.png')

        self.vc = pygame.image.load('res/vc.png').convert()
        self.colorkey = self.vc.get_at((0,0))
        self.vc.set_colorkey(self.colorkey, pygame.RLEACCEL)

        self.crate = pygame.image.load('res/crate.png').convert()
        self.colorkey = self.crate.get_at((0,0))
        self.crate.set_colorkey(self.colorkey, pygame.RLEACCEL)

        #Block switches
        self.bswitch1 = pygame.image.load('res/switchbUp.png')
        self.bswitch2 = pygame.image.load('res/switchbRight.png')
        self.bswitch3 = pygame.image.load('res/switchbDown.png')
        self.bswitch4 = pygame.image.load('res/switchbLeft.png')
class Block(object):
    def __init__(self):
        object.__init__(self)
        self.collides = True
        self.stopsPMovement = True
        self.drawOnTop = False
        self.canChange_gstate = False
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)
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
        self.canChange_gstate = True
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
    def onCollide(self, ball, g):
        pass
class Spikes(Block):
    def __init__(self, x, y, stype):
        Block.__init__(self)
        if stype == 0:
            self.rec = pygame.Rect(2,8,6,2)
        elif stype == 1:
            self.rec = pygame.Rect(0,2,2,6)
        elif stype == 2:
            self.rec = pygame.Rect(2,0,6,2)
        elif stype == 3:
            self.rec = pygame.Rect(8,2,2,6)
        else:
            self.rec = pygame.Rect(3,3,5,5)

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
        elif self.type == 3:
            screen.blit(bimages.spike4, self.drec)
        elif self.type == 4:
            screen.blit(bimages.spike5, self.drec)
        elif self.type == 5:
            screen.blit(bimages.spike6, self.drec)
        elif self.type == 6:
            screen.blit(bimages.spike7, self.drec)
        else:
            screen.blit(bimages.spike8, self.drec)
    def onCollide(self, ball, g):
        ball.kill(g)
        return 'You have plummeted to your demise!'
class Switch(Block):
    def __init__(self, x, y, stype):
        Block.__init__(self)
        x -= 3
        y -= 3
        self.type = stype
        self.rec = pygame.Rect(0,0,20,20)
        self.rec = self.rec.move(x, y)
        self.collides = False
        self.stopsPMovement = False
        self.type = stype
        self.drawOnTop = True
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
    def onCollide(self, ball, g):
        pass
class Rock(Block):
    def __init__(self, x, y):
        Block.__init__(self)
        self.rec = pygame.Rect(0,0,10,10)
        self.rec = self.rec.move(x, y)   
        self.canChange_gstate = True
    def update(self, level, g, seconds):
        pass
    def draw(self, screen, bimages):
        screen.blit(bimages.rock, self.rec)
    def onCollide(self, ball, g):
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
    def onCollide(self, ball, g):
        ball.alive = False
        return 'You have been slain by a Chaser!'
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
        screen.blit(bimages.vc, self.rec)
    def onCollide(self, ball, g):
        pass
class IceCube(Block):
    def __init__(self, x, y):
        Block.__init__(self)
        self.rec = pygame.Rect(0,0,10,10)
        self.rec = self.rec.move(x,y)
        self.collides = False
        self.stopsPMovement = False
        self.state = 0
        self.setUp = False
    def update(self, level, g, seconds):
        if not self.setUp:
            topRec = pygame.Rect(self.rec.left, self.rec.top - 10, 10, 10)
            bottomRec = pygame.Rect(self.rec.left, self.rec.top + 10, 10, 10)
            leftRec = pygame.Rect(self.rec.left - 10, self.rec.top, 10, 10)
            rightRec = pygame.Rect(self.rec.left + 10, self.rec.top, 10, 10)
            
            for i in range(50):
                for j in range(50):
                    if level.blocks[i][j] != None and level.blocks[i][j].collides:
                        if level.blocks[i][j].rec.colliderect(topRec):
                            self.state = glevel.GSTATE_UP
                            self.setUp = True
                        elif level.blocks[i][j].rec.colliderect(bottomRec):
                            self.state = glevel.GSTATE_DOWN
                            self.setUp = True
                        elif level.blocks[i][j].rec.colliderect(leftRec):
                            self.state = glevel.GSTATE_LEFT
                            self.setUp = True
                        elif level.blocks[i][j].rec.colliderect(rightRec):
                            self.state = glevel.GSTATE_RIGHT
                            self.setUp = True

        if level.b2.state == gobjects.MODE_VAPOR and self.rec.colliderect(level.b2.rec) and not level.b2.touchingBlock:
            level.b2.hud.drawInteract = True
            if g.control.f:
                level.b2.state = gobjects.MODE_NORMAL
                level.gstate = self.state
    def draw(self, screen, bimages):
        screen.blit(bimages.icecube, self.rec)
    def onCollide(self, ball, g):
        pass
class AutoSwitch(Block):
    def __init__(self, x, y, stype):
        Block.__init__(self)
        x -= 3
        y -= 3
        self.type = stype
        self.rec = pygame.Rect(0,0,20,20)
        self.rec = self.rec.move(x, y)
        self.collides = False
        self.stopsPMovement = False
        self.stype = stype
        self.drawOnTop = True
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
    def onCollide(self, ball, g):
        pass
class Vine(Block):
    def __init__(self, x, y):
        Block.__init__(self)

        self.rec = pygame.Rect(0,0,10,10)
        self.rec = self.rec.move(x,y)
        self.collides = False
        self.stopsPMovement = False

        self.type = randint(0, 2)
    def update(self, level, g, seconds):
        if level.b2.state == gobjects.MODE_NORMAL and self.rec.colliderect(level.b2.rec):
            level.b2.hud.drawInteract = True
            if g.control.f:
                level.b2.state = gobjects.MODE_ON_VINE
    def draw(self, screen, bimages):
        if self.type == 0:
            screen.blit(bimages.vine1, self.rec)
        elif self.type == 1:
            screen.blit(bimages.vine2, self.rec)
        elif self.type == 2:
            screen.blit(bimages.vine2, self.rec)
    def onCollide(self, ball, g):
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
    def onCollide(self, ball, g):
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
    def onCollide(self, ball, g):
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
    def onCollide(self, ball, g):
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
    def onCollide(self, ball, g):
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
    def onCollide(self, ball, g):
        pass
class CB_E(Block):
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
            screen.blit(bimages.cbe, self.loc)
    def onCollide(self, ball, g):
        pass
class DarkRock(Block):
    def __init__(self, x, y):
        Block.__init__(self)
        self.rec = pygame.Rect(0,0,10,10)
        self.rec = self.rec.move(x, y)   
        self.canChange_gstate = True
    def update(self, level, g, seconds):
        pass
    def draw(self, screen, bimages):
        screen.blit(bimages.dark_rock, self.rec)
    def onCollide(self, ball, g):
        pass
class Crate(Block):
    def __init__(self, x, y):
        Block.__init__(self)
        self.rec = pygame.Rect(0,0,10,10)
        self.rec = self.rec.move(x,y)
        self.t = [0.0, 0.0]
    def update(self, level, g, seconds):
        #Make 2 copies of the location rectangle.
        #One copy is made for each axis because there
        #might not allways be a collision on both.
        self.newLocX = self.rec.copy()
        self.newLocY = self.rec.copy()

        #Apply gravity
        if level.block_gstate == glevel.GSTATE_UP:
            self.t[1] = self.t[1] - seconds
            self.newLocY.top = self.newLocY.top + (self.t[1] * glevel.G)
        elif level.block_gstate == glevel.GSTATE_DOWN:
            self.t[1] = self.t[1] + seconds
            self.newLocY.top = self.newLocY.top + (self.t[1] * glevel.G)
        elif level.block_gstate == glevel.GSTATE_LEFT:
            self.t[0] = self.t[0] - seconds
            self.newLocX.left = self.newLocX.left + (self.t[0] * glevel.G)
        elif level.block_gstate == glevel.GSTATE_RIGHT:
            self.t[0] = self.t[0] + seconds
            self.newLocX.left = self.newLocX.left + (self.t[0] * glevel.G)

        #Booleans used for collision detection
        self.collpassx = True
        self.collpassy = True

        for i in range(50):
            for j in range(50):
                if level.blocks[i][j] != None:
                    if self != level.blocks[i][j]:
                        if level.blocks[i][j].collides:
                            if self.newLocX.colliderect(level.blocks[i][j].rec):
                                    self.collpassx = False
                                    self.t[0] = 0.0
                            if self.newLocY.colliderect(level.blocks[i][j].rec):
                                    self.collpassy = False
                                    self.t[1] = 0.0

        #If collision checks pass, set the location equal to the new location
        if self.collpassx:
            self.rec.left = self.newLocX.left
        if self.collpassy:
            self.rec.top = self.newLocY.top
    def draw(self, screen, bimages):
        screen.blit(bimages.crate, self.rec)
    def onCollide(self, ball, g):
        pass
class BlockSwitch(Block):
    def __init__(self, x, y, stype):
        Block.__init__(self)
        x -= 3
        y -= 3
        self.type = stype
        self.rec = pygame.Rect(0,0,20,20)
        self.rec = self.rec.move(x, y)
        self.collides = False
        self.stopsPMovement = False
        self.type = stype
        self.drawOnTop = True
    def update(self, level, g, seconds):
        if self.rec.colliderect(level.b2.rec):
            level.b2.hud.drawInteract = True
            if g.control.f:
                if self.type == 0:
                    level.block_gstate = glevel.GSTATE_UP
                elif self.type == 1:
                    level.block_gstate = glevel.GSTATE_RIGHT
                elif self.type == 2:
                    level.block_gstate = glevel.GSTATE_DOWN
                else:
                    level.block_gstate = glevel.GSTATE_LEFT
    def draw(self, screen, bimages):
        if self.type == 0:
            screen.blit(bimages.bswitch1, self.rec)
        elif self.type == 1:
            screen.blit(bimages.bswitch2, self.rec)
        elif self.type == 2:
            screen.blit(bimages.bswitch3, self.rec)
        else:
            screen.blit(bimages.bswitch4, self.rec)
    def onCollide(self, ball, g):
        pass
