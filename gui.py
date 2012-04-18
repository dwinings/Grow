#Author: Jonathan Haslow-Hall
import pygame, gcolors
from pygame import font

class Button:
    button_width = 77
    button_height = 25
    button_normal = pygame.image.load('res/button_normal.png')
    button_hover = pygame.image.load('res/button_hover.png')
    font.init()
    basicFont = pygame.font.SysFont(None, 24, bold=False, italic=False)
	
    def __init__(self, x, y, da_text, button_id):
        self.hovered = False
        self.clicked = False
        self.text = da_text
        self.rec = pygame.Rect(x, y, Button.button_width, Button.button_height)

        self.text_s =  Button.basicFont.render(self.text, True, gcolors.WHITE)
        self.srec = self.text_s.get_rect()
        self.srec.left = self.srec.left + self.rec.left + (self.rec.width/2) - (self.srec.width / 2)
        self.srec.top = self.srec.top + self.rec.top + (self.rec.height/2) - (self.srec.height / 2)

        self.clickMethod = None
        self.my_id = button_id
    def update(self, g, seconds):
        if self.rec.collidepoint(g.control.mloc):
            self.hovered = True
            if g.control.mClicked:
                if self.clickMethod != None:
                    self.clickMethod(self,g)
                else:
                    self.clicked = True
        else:
            self.hovered = False
    def draw(self, screen):
        if self.hovered:
            screen.blit(Button.button_hover, self.rec)
        else:
            screen.blit(Button.button_normal, self.rec)
        
        screen.blit(self.text_s, self.srec)
    def isClicked(self):
        if self.clicked:
            self.clicked = False
            return True;
    def setClickedMethod(self, method):
        self.clickMethod = method
class ButtonGroup:
    def __init__(self, locx, locy, spacingy):
        self.loc = (locx, locy)
        self.spacing_y = spacingy
    def update(self, g):
        pass
    def draw(screen):
        pass
class Screen:
    def __init__(self):
        pass
    def update(self, g, event, seconds):
        pass
    def draw(self, screen):
        pass
