import pygame
import os
import sys

from module import Colors

"""
NOT DONE!! 

Was Meant to implement typing text one char at a time. Minimal working example in main.py
"""

class TextRect(object):
    def __init__(self,**kwargs):
        self.font_path      = kwargs.get('font_path',None)
        if self.font_path is None or not os.path.isfile(self.font_path):
            print("Error: font path is not an actual file!")
            sys.exit()

        self.font_color     = kwargs.get('font_color',Colors.RGB('white'))
        self.bg_color       = kwargs.get('bg_color',None)
        self.font_size      = kwargs.get('font_size',32)
        self.top            = kwargs.get('top',0)
        self.left           = kwargs.get('left',0)
        self.top            = kwargs.get('y',0)
        self.left           = kwargs.get('x',0)
        self.font           = pygame.font.Font(self.font_path, self.font_size)
        self.text           = kwargs.get('text',"")
        self.surface        = self.font.render(self.text, True, self.font_color,self.bg_color)
        self.rect           = self.surface.get_rect()

    def rect(self,size):
        pass


    def text(self,txt,loc=None):
        self.surface = self.font.render(txt, True, self.font_color,self.background)
        # self.rect    = self.surface.get_rect()
        # if loc:
        #     self.location(loc)
        # else:
        #     self.rect.left = self.left
        #     self.rect.top = self.top

    def display(self):
        return self.surface



class TypedText(object):
    def __init__(self,**kwargs):

        self.text           = None
        self.index          = None
        self.last_update    = pygame.time.get_ticks()
        self.speed          = kwargs.get('speed',50)
        self.calls          = 0

    def printNext(self,loc,all=False):
        self.calls += 1
        if self.chunk == 0:
            self.surface_obj = self.font.render(self.text, True, self.font_color)
        else:
            if self.calls % self.chunk == 0:
                self.index += 1
            self.surface_obj  = self.font.render(self.text[0:self.index], True, self.font_color)

        return self.surface_obj,self.rect_obj,self.rect_obj.right

    def setText(self,text):
        self.text = text


if __name__=='__main__':

    pygame.init()

    # sets the window title
    pygame.display.set_caption("Test Game Menu")

    # Set up the drawing window
    screen = pygame.display.set_mode((800,800))


    t = TextRect(text="Hello World",x=100,y=100,font_color=Colors.RGB("gold"),font_path='./resources/fonts/ARCADE.TTF')

    # loc = [200,200]
    # t.location(loc)

    # Run until the user asks to quit
    # Basic game loop
    running = True
    while running:

        #screen.fill((0,0,0))

        events = pygame.event.get()
        # Did the user click the window close button?
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            # Not used in this instance of our game
            if event.type == pygame.MOUSEBUTTONUP:
                # debug(pygame.mouse.get_pos(),10)
                pass

        screen.blit(t.display(),(200,200))

        pygame.display.flip()

    pygame.quit()
