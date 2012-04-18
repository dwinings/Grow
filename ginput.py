#Author: Jonathan Haslow-Hall
import pygame
from pygame import key, mouse

class Controls:
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.w = False
        self.s = False
        self.d = False
        self.a = False
        self.f = False
        self.p = [False, False]
        self.mloc = [0, 0]
        self.mClicked = False
        self.space = False
        self.old_up = False
        self.old_down = False
    def updateControls(self):
        bools = key.get_pressed()
        self.up = bools[pygame.K_UP]
        self.down = bools[pygame.K_DOWN]
        self.left = bools[pygame.K_LEFT]
        self.right = bools[pygame.K_RIGHT]
        self.w = bools[pygame.K_w]
        self.s = bools[pygame.K_s]
        self.a = bools[pygame.K_a]
        self.d = bools[pygame.K_d]
        self.f = bools[pygame.K_f]
        self.p[0] = bools[pygame.K_p]
        m = mouse.get_pressed()
        self.mClicked = m[0]
        self.mloc = mouse.get_pos()
        self.space = bools[pygame.K_SPACE]
    def updateLast(self):
        self.p[1] = self.p[0]
        self.old_up = self.up
        self.old_down = self.down
        
                        
