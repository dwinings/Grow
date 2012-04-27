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
        self.loc = (x,y)

        self.text_s =  Button.basicFont.render(self.text, True, gcolors.WHITE)
        self.srec = self.text_s.get_rect()
        self.sx = self.srec.left + self.rec.left + (self.rec.width/2) - (self.srec.width / 2)
        self.sy = self.srec.top + self.rec.top + (self.rec.height/2) - (self.srec.height / 2)
        self.sloc = (self.sx, self.sy)
        self.srec.left = self.sx
        self.srec.top = self.sy

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
    def draw2(self, screen, offset):
        if self.hovered:
            screen.blit(Button.button_hover, ((self.loc[0] + offset[0]),(self.loc[1] + offset[1])))
        else:
            screen.blit(Button.button_normal, ((self.loc[0] + offset[0]),(self.loc[1] + offset[1])))
        
        screen.blit(self.text_s, ((self.sloc[0] + offset[0]),(self.sloc[1] + offset[1])))
    def pressed(self, g):
        if self.clickMethod != None:
            self.clickMethod(self,g)
        else:
            self.clicked = True
    def isClicked(self):
        if self.clicked:
            self.clicked = False
            return True;
    def setClickedMethod(self, method):
        self.clickMethod = method
class ButtonGroup:
    def __init__(self, locx, locy, spacingy):
        self.loc = [locx, locy]
        self.spacing_y = spacingy
        self.buttons = []
        self.selected_index = 0
        self.selector = pygame.image.load('res/selector.png')
        
    def update(self, g, seconds):
        if g.control.space:
            self.buttons[self.selected_index].pressed(g)

        if g.control.down and not g.control.old_down:
            self.selected_index += 1
            if self.selected_index >= len(self.buttons):
                self.selected_index = 0
        if g.control.up and not g.control.old_up:
            self.selected_index -= 1
            if self.selected_index < 0:
                self.selected_index = len(self.buttons) - 1
                
        for i in range(len(self.buttons)):
            self.buttons[i].update(g, seconds)
    def draw(self, screen):
        for i in range(len(self.buttons)):
            self.buttons[i].draw2(screen, (self.loc[0], self.loc[1] + (self.spacing_y * i)))
        screen.blit(self.selector, (self.loc[0] - 50, self.loc[1] + (self.spacing_y * self.selected_index)))
    def add(self, button):
        self.buttons.append(button)
        self.buttons[len(self.buttons)-1].rec = self.buttons[len(self.buttons)-1].rec.move(self.loc[0], self.loc[1] + (self.spacing_y * (len(self.buttons)-1)))
    def locChanged(self):
        for i, button in enumerate(self.buttons):
            button.rec.left = self.loc[0]
            button.rec.top  = self.loc[1] + (self.spacing_y * i)
class Screen:
    def __init__(self):
        pass
    def update(self, g, event, seconds):
        pass
    def draw(self, screen):
        pass
