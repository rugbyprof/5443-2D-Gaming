"""
Pygame P01-010

Description:

   Background Images and Scrolling Background

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

# Tells OS where to open the window
# Delete later or change to your own values
os.environ["SDL_VIDEO_WINDOW_POS"] = str(1000) + "," + str(100)

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
    "title": "Pygame Side Scrolling",
    "window_size": {"width": 400, "height": 400},
    "background": "./media/desert_bg_800.png",
    "background2": "./media/desert_bg_800b.png",
}

colors = rgb_colors("colors.json")


class EventContainer:
    """Dictionary of events all kept in one place for use in other classes"""

    def __init__(self):
        self.events = {
            "keydown": None,
            "keyup": None,
            "mouse_motion": None,
            "mouse_button_up": None,
            "all_pressed": None,
        }

    def reset(self):
        """Set all to None"""
        for k, v in self.events.items():
            self.events[k] = None

    def __str__(self):
        """Dump instance to screen or wherever"""
        s = ""
        for k, v in self.events.items():
            if k == "all_pressed":
                continue
            s += f"{k} : {v}\n"

        return s


class BackgroundSideScroller:
    def __init__(self, screen, speed, background,background2=None):
        # assumes squares for now
        
        self.speed = speed

        self.screen = screen  # pygame screen handle
        self.bgimg = pygame.image.load(background)  # background img handle
        if background2:
            self.bgimg2 = pygame.image.load(background2)  # background img handle
        else:
            self.bgimg2 = pygame.image.load(background)  # background img handle
            
        self.bgimg_size = self.bgimg.get_rect().size  # size of bg image: tuple (w,h)

        self.gw = config["window_size"]["width"]  # game width
        self.gh = config["window_size"]["height"]  # game height

        # self.bgimg = pygame.transform.scale(self.bgimg, (1280, 720))

        self.bg_w = self.bgimg_size[0]
        self.bg_h = self.bgimg_size[1]

        self.cx = self.gw // 2  # center x (of game window)
        self.cy = self.gh // 2  # center y
        self.speed = 2  # move size in any direction
        self.scroll_x = 0
        
        self.im_start = 0
        self.im_end = self.bg_w

        # self.w_buffer = (self.bg_w-self.gw) // 2
        # self.h_buffer = (self.bg_h-self.gh) // 2

    def setSpeed(self, speed):
        self.speed = speed

    def scrollBackground(self):
        
        
        self.scroll_x = (self.scroll_x + self.speed) % (self.bg_w - self.gw)
        
        self.screen.blit(self.bgimg, (self.scroll_x, 0), (self.scroll_x, 0, self.gw, self.gh))
        self.screen.blit(self.bgimg2, (self.scroll_x*-1, 0), (self.gw, 0, self.gw, self.gh))
        print(self.scroll_x, 0, self.gw, self.gh)


def main():
    pygame.init()

    eventHelper = EventContainer()

    # sets the window title
    pygame.display.set_caption(config["title"])

    # set circle location
    width = config["window_size"]["width"]
    height = config["window_size"]["height"]

    # Set up the drawing window
    screen = pygame.display.set_mode((width, height))

    # background = BackgroundSideScroller(screen,"./media/grassandtrees_3200x800.png")

    original_speed = 2
    current_speed = original_speed
    
    background = BackgroundSideScroller(screen,original_speed, config["background"],config["background2"],)

    
    # background.setSpeed(current_speed)

    # Run until the user asks to quit
    # game loop
    running = True
    count = 0
    while running:
        # Did the user click the window close button?
        eventHelper.reset()

        is_key_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if is_key_pressed[pygame.K_LEFT]:
                    pass
                if is_key_pressed[pygame.K_RIGHT]:
                    pass

            if event.type == pygame.KEYUP:
                pass

            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                if pos[0] < width//2:
                    background.setSpeed(original_speed * -1)
                else:
                    background.setSpeed(original_speed)

            if event.type == pygame.MOUSEBUTTONUP:
                clickUp = pygame.mouse.get_pos()

        background.scrollBackground()

        count += 1

        # if count % 100 == 0:
        #     speed += 1
        #     background.setSpeed(speed)

        if count % 1000 == 0:
            count = 0

        eventHelper.events["all_pressed"] = pygame.key.get_pressed()
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()


if __name__ == "__main__":
    main()
    
"""
    I am trying to create a pygame example that has a continuously scrolling background, also known as a `side scroller`. To make my game look fluid, I have decided to load the same background image twice, and display portions of each background image in order for my side scroller to look as if it is a never ending world by displaying both images contiguously while they scroll in either direction. For example, if my background image was 800px wide and my game world was 400px wide, I would display the 
"""