#Author: Jonathan Haslow-Hall
import pygame, ginput, gobjects, gblocks, gui, gcolors
from pygame import font
font.init()

basicFont = pygame.font.SysFont(None, 24, bold=False, italic=False)

#Gravity state values
GSTATE_UP = 0
GSTATE_DOWN = 1
GSTATE_LEFT = 2
GSTATE_RIGHT = 3

G = 7.0

class Level:
    def __init__(self, width, height, levelfile):
        #Play area
        self.levelRect = pygame.Rect(0, 0, width, height)

        #Player Object
        self.b2 = gobjects.Ball(0, 0, width, height)
        self.gstate = GSTATE_DOWN
        self.sgstate = 0
        self.block_gstate = GSTATE_DOWN
        self.sblock_gstate = 0
        
        #Player spawn point
        self.spawnx = 0
        self.spawny = 0

        self.completed = False

        #Growth variables
        self.dirtCount = 0
        self.grownCount = 0
        self.leavesI = pygame.image.load('res/leaves.png')
        self.leavesLoc = [width - 80,height - 30]
        self.leavesTextOffset = [27,0]

        #Block images
        self.bimages = gblocks.BlockImages()
        
        #Block array for level
        self.blocks = [[None for col in range(50)] for row in range(50)]
        #Load level data 
        self.parseLevelFile(levelfile)
        
    def update(self, g, seconds):
        #Update player
        self.b2.update(self, g, self.levelRect.width, self.levelRect.height, seconds)

        #Update all blocks 
        for i in range(50):
            for j in range(50):
                if self.blocks[i][j] != None:
                    self.blocks[i][j].update(self, g, seconds)

        if self.dirtCount == self.grownCount:
            self.completed = True
                
    def draw(self, screen):
        #Level draw layer
        for i in range(50):
            for j in range(50):
                if self.blocks[i][j] != None and not self.blocks[i][j].drawOnTop:
                    self.blocks[i][j].draw(screen, self.bimages)
	self.b2.draw(screen)
	for i in range(50):
            for j in range(50):
                if self.blocks[i][j] != None and self.blocks[i][j].drawOnTop:
                    self.blocks[i][j].draw(screen, self.bimages)

        #Hud draw layer
        self.b2.drawHud(screen)
        screen.blit(self.leavesI, self.leavesLoc)

        self.count = int((float(self.grownCount)/float(self.dirtCount)) * 100)
        self.textI = basicFont.render(str(self.count)+'%',True, gcolors.WHITE)
        screen.blit(self.textI, (self.leavesLoc[0] + self.leavesTextOffset[0],self.leavesLoc[1] + self.leavesTextOffset[1]))
    def respawn(self):
        self.b2.respawn(self.spawnx, self.spawny)
        self.b2.addScore(-15)
        self.gstate = self.sgstate
        self.block_gstate = self.sblock_gstate
    def getLevelRec(self):
        return self.levelRect
    def parseLevelFile(self, levelFile):
        f = open(levelFile, 'r')
        for line in f:
            #print line,
            s = str(line)
            sp = s.split()
            if len(sp) >= 2:
                if sp[0] == 'spawn':
                    self.spawnx = int(sp[1])
                    self.spawny = int(sp[2])
                    self.b2.respawn(self.spawnx, self.spawny)
                elif sp[0] == 'block':
                    x = int(sp[1])
                    y = int(sp[2])
                    btype = int(sp[3])
                    if btype == gblocks.DIRT_GRASS:
                        self.blocks[x][y] = gblocks.DirtGrass((10*x),(10* y))
                        self.dirtCount += 1
                    elif btype == gblocks.SPIKES_B:
                        self.blocks[x][y] = gblocks.Spikes((10*x),(10* y),0)
                    elif btype == gblocks.SPIKES_L:
                        self.blocks[x][y] = gblocks.Spikes((10*x),(10* y),1)
                    elif btype == gblocks.SPIKES_T:
                        self.blocks[x][y] = gblocks.Spikes((10*x),(10* y),2)
                    elif btype == gblocks.SPIKES_R:
                        self.blocks[x][y] = gblocks.Spikes((10*x),(10* y),3)
                    elif btype == gblocks.SPIKES_BR:
                        self.blocks[x][y] = gblocks.Spikes((10*x),(10* y),4)
                    elif btype == gblocks.SPIKES_BL:
                        self.blocks[x][y] = gblocks.Spikes((10*x),(10* y),5)
                    elif btype == gblocks.SPIKES_TR:
                        self.blocks[x][y] = gblocks.Spikes((10*x),(10* y),6)
                    elif btype == gblocks.SPIKES_TL:
                        self.blocks[x][y] = gblocks.Spikes((10*x),(10* y),7)
                    elif btype == gblocks.SWITCH_U:
                        self.blocks[x][y] = gblocks.Switch((10*x),(10* y),0)
                    elif btype == gblocks.SWITCH_R:
                        self.blocks[x][y] = gblocks.Switch((10*x),(10* y),1)
                    elif btype == gblocks.SWITCH_D:
                        self.blocks[x][y] = gblocks.Switch((10*x),(10* y),2)
                    elif btype == gblocks.SWITCH_L:
                        self.blocks[x][y] = gblocks.Switch((10*x),(10* y),3)
                    elif btype == gblocks.ROCK:
                        self.blocks[x][y] = gblocks.Rock((10*x),(10* y))
                    elif btype == gblocks.CHASER:
                        self.blocks[x][y] = gblocks.Chaser((10*x),(10* y))
                    elif btype == gblocks.VAPOR_CLOUD:
                        self.blocks[x][y] = gblocks.VaporCloud((10*x),(10* y))
                    elif btype == gblocks.ICE_CUBE:
                        self.blocks[x][y] = gblocks.IceCube((10*x),(10*y))
                    elif btype == gblocks.SWITCH_A_U:
                        self.blocks[x][y] = gblocks.AutoSwitch((10*x),(10* y),0)
                    elif btype == gblocks.SWITCH_A_R:
                        self.blocks[x][y] = gblocks.AutoSwitch((10*x),(10* y),1)
                    elif btype == gblocks.SWITCH_A_D:
                        self.blocks[x][y] = gblocks.AutoSwitch((10*x),(10* y),2)
                    elif btype == gblocks.SWITCH_A_L:
                        self.blocks[x][y] = gblocks.AutoSwitch((10*x),(10* y),3)
                    elif btype == gblocks.VINE:
                        self.blocks[x][y] = gblocks.Vine((10*x),(10* y))
                    elif btype == gblocks.CBJ:
                        self.blocks[x][y] = gblocks.CB_J((10*x),(10* y))
                    elif btype == gblocks.CBD:
                        self.blocks[x][y] = gblocks.CB_D((10*x),(10* y))
                    elif btype == gblocks.CBE:
                        self.blocks[x][y] = gblocks.CB_E((10*x),(10* y))
                    elif btype == gblocks.DARK_ROCK:
                        self.blocks[x][y] = gblocks.DarkRock((10*x),(10* y))
                    elif btype == gblocks.CRATE:
                        self.blocks[x][y] = gblocks.Crate((10*x),(10* y))
                    elif btype == gblocks.SWITCH_B_U:
                        self.blocks[x][y] = gblocks.BlockSwitch((10*x),(10* y),0)
                    elif btype == gblocks.SWITCH_B_R:
                        self.blocks[x][y] = gblocks.BlockSwitch((10*x),(10* y),1)
                    elif btype == gblocks.SWITCH_B_D:
                        self.blocks[x][y] = gblocks.BlockSwitch((10*x),(10* y),2)
                    elif btype == gblocks.SWITCH_B_L:
                        self.blocks[x][y] = gblocks.BlockSwitch((10*x),(10* y),3)
                elif sp[0] == 'gdir':
                    self.gstate = int(sp[1])
                    self.sgstate = int(sp[1])
                elif sp[0] == 'bgdir':
                    self.block_gstate = int(sp[1])
                    self.sblock_gstate = int(sp[1])
