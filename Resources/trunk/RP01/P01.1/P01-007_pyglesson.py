"""
Pygame P01-007

Description:
   DOES NOT WORK !!!!!!!!!!
   Background Images and Scrolling Tile Background

New Code:

    bgimg = pygame.image.load("./media/tile.png")
    bgimg_size = bgimg.get_rect().size

"""
# Import and initialize the pygame library
import pygame
import random
import json
import pprint
import sys
import os
import math

print("Doesn't work right now .... ")
sys.exit()

# Tells OS where to open the window
# Delete later or change to your own values
os.environ['SDL_VIDEO_WINDOW_POS'] = str(1000) + "," + str(100)

from helper_module import rgb_colors
from helper_module import mykwargs
from helper_module import straightDistance
from helper_module import getCardinalDirection

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

config = {
    'title' :'007 Pygame Lesson',
    'window_size' : {
        'width' : 500,
        'height' : 500
    }
}

colors = rgb_colors('colors.json')


class EventContainer:
    """ Dictionary of events all kept in one place for use in other classes
    """
    def __init__(self):
        self.events = {
            'keydown':None,
            'keyup':None,
            'mouse_motion':None,
            'mouse_button_up':None,
            'all_pressed':None
        }

    def reset(self):
        """ Set all to None
        """
        for k,v in self.events.items():
            self.events[k] = None

    def __str__(self):
        """Dump instance to screen or wherever
        """
        s = ''
        for k,v in self.events.items():
            if k == 'all_pressed':
                continue
            s += f"{k} : {v}\n"

        return s

# class ImageClipper:
#     def __init__(self,image=None):
#         """
#         My Blitting Terms:
#             background:  image to show
#             clipped_rect: The section of the backround to show
#             floor_x: x coordinate of where to place upper left corner of clipped_rect
#             floor_y: y coordinate
#             buffer: the
#         """
#         (100+self.scroll_x)%100,(100+self.scroll_y)%100,400,400)

class TileScroller:
    def __init__(self,screen,tile):
        # assumes squares for now


        self.screen = screen                            # pygame screen handle
        self.bgimg = pygame.image.load(tile)            # background img handle
        self.bgimg_size = self.bgimg.get_rect().size    # size of bg image: tuple (x,y)

        self.gw = config['window_size']['width']        # game width
        self.gh = config['window_size']['height']       # game height

        #self.bgimg = pygame.transform.scale(self.bgimg, (1280, 720))

        self.tilew = self.bgimg_size[0]
        self.tileh = self.bgimg_size[1]

        self.cx = self.gw // 2                          # center x (of game window)
        self.cy = self.gh // 2                          # center y
        self.step = 4                                   # move size in any direction
        self.target_location = None                     # tuple (x,y) of where to move to
        self.cardinal_direction = None                  # direction to move to go toward goal
        self.distance_to_target = 0

        self.move = 1


    def setScrollTarget(self,loc=None):
        """If keys are pressed or mouse is clicked, set a goal location to scroll toward.
        """
        self.target_location = loc
        self.cardinal_direction = getCardinalDirection((self.cx,self.cy), self.target_location)
        self.distance_to_target = straightDistance((self.cx,self.cy),self.target_location)
        self.scroll_x = 0
        self.scroll_y = 0

        print(self.target_location)
        print(self.cardinal_direction)
        print(self.distance_to_target)


    def drawBackground(self):
        self.screen.fill(colors['white'])

        self.drawTiles()


    def drawTiles(self):
        yoffset = 0
        xoffset = 0

        if self.target_location != None:
            if 'N' in self.cardinal_direction :
                yoffset -= self.step
            if 'S' in self.cardinal_direction :
                yoffset += self.step
            if 'E' in self.cardinal_direction :
                xoffset += self.step
            if 'W' in self.cardinal_direction :
                xoffset -= self.step

        if xoffset % self.tilew == 0:
            xoffset = 0
        if yoffset % self.tileh == 0:
            yoffset = 0


        self.move += 7

        rect = (0,0,self.tilew,self.tileh)
        for i in range(0,self.gw,self.tilew):
            col = i + self.move
            for j in range(0,self.gh,self.tileh):
                row = j + self.move
                self.screen.blit(self.bgimg, (col,row),rect)

    def reset(self):
        self.move = 0

    def calculateScroll(self):

        if self.target_location == None:
            return (0,0,self.gw,self.gh)










def main():
    pygame.init()

    eventHelper = EventContainer()

    # sets the window title
    pygame.display.set_caption(config['title'])

    # set circle location
    width = config['window_size']['width']
    height = config['window_size']['height']

    # Set up the drawing window
    screen = pygame.display.set_mode((width,height))

    floor = TileScroller(screen,"./media/tile_light_20px.png")

    # Run until the user asks to quit
    # game loop
    running = True

    while running:

        # Did the user click the window close button?
        eventHelper.reset()

        floor.drawBackground()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                eventHelper.events['keydown'] = event.key

            if event.type == pygame.KEYUP:
                eventHelper.events['keyup'] = event.key

            if event.type == pygame.MOUSEMOTION:
                eventHelper.events['mouse_motion'] = pygame.mouse.get_pos()


            if event.type == pygame.MOUSEBUTTONUP:
                eventHelper.events['mouse_button_up'] = pygame.mouse.get_pos()
                floor.setScrollTarget(pygame.mouse.get_pos())
                floor.reset()

        eventHelper.events['all_pressed'] = pygame.key.get_pressed()

        pygame.display.flip()


    # Done! Time to quit.
    pygame.quit()

if __name__=='__main__':

    main()


