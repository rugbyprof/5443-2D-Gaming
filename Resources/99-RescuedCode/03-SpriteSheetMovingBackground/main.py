"""
Pygame P01-009

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
    "title": "009 Pygame Sprite Movement",
    "window_size": {"width": 500, "height": 500},
    "sprite_sheet": "./media/pacman_ghosts_40x.png",
    "background": "./media/tile_1000x1000_40_light.png",
}

colors = rgb_colors("colors.json")


class PacmanSprite(pygame.sprite.Sprite):
    # This code gets executed as soon as we create a new instance
    def __init__(self, **kwargs):
        # Initiate this sprite
        pygame.sprite.Sprite.__init__(self)

        self.screen = kwargs.get("screen", None)

        if not self.screen:
            print("Error: PacmanSprite needs a copy of the screen!!")
            sys.exit()

        # Mandatory Params
        self.gameWidth = config["window_size"]["width"]
        self.gameHeight = config["window_size"]["height"]

        if not self.gameWidth or not self.gameHeight:
            print("Error: No gameWidth or gameHeight!")
            sys.exit(0)

        self.frame_nums = [0, 1, 2]

        # possible pacman colors
        colors = ["red", "purple", "orange", "blue"]
        # color choice
        color = kwargs.get("color", "purple")

        colors.index(color)

        self.sprite = kwargs.get("sprite_sheet", config["sprite_sheet"])

        self.resizex = kwargs.get("sizefactor", 2)
        self.tilesize = kwargs.get("tilesize", 40) * self.resizex

        # offsets x coord to beginning column of a color
        self.color_offset = colors.index(color) * len(self.frame_nums) * self.tilesize

        # pacmans position
        self.x = self.gameWidth // 2
        self.y = self.gameHeight // 2

        #
        self.image = pygame.image.load(self.sprite)

        # get original image size
        self.image_size = self.image.get_rect().size

        # resize the sprite sheet
        self.image = pygame.transform.scale(
            self.image,
            (self.image_size[0] * self.resizex, self.image_size[1] * self.resizex),
        )

        # preserve alpha channel (I think)
        self.image = self.image.convert_alpha()

        # A bounding rectangle not necessary
        # self.rect = self.image.get_rect()
        # self.rect.center = (self.x, self.y)

        # slow down the rate of frame change
        self.delay = 2

        #

        self.callCounter = 0

        self.frameCounter = 0

    def GetRect(self):
        pass

    def Move(self, is_key_pressed):
        yoffset = 0

        keys_pressed = 0
        if is_key_pressed[pygame.K_RIGHT]:
            keys_pressed += 1
        if is_key_pressed[pygame.K_LEFT]:
            keys_pressed += 1
        if is_key_pressed[pygame.K_UP]:
            keys_pressed += 1
        if is_key_pressed[pygame.K_DOWN]:
            keys_pressed += 1

        if keys_pressed > 1:
            if is_key_pressed[pygame.K_UP]:
                if is_key_pressed[pygame.K_LEFT]:
                    yoffset = self.tilesize * 6
                if is_key_pressed[pygame.K_RIGHT]:
                    yoffset = self.tilesize * 5
            if is_key_pressed[pygame.K_DOWN]:
                if is_key_pressed[pygame.K_LEFT]:
                    yoffset = self.tilesize * 7
                if is_key_pressed[pygame.K_RIGHT]:
                    yoffset = self.tilesize * 8
        else:
            if is_key_pressed[pygame.K_UP]:
                yoffset = self.tilesize * 3
            if is_key_pressed[pygame.K_DOWN]:
                yoffset = self.tilesize * 4
            if is_key_pressed[pygame.K_LEFT]:
                yoffset = self.tilesize * 2
            if is_key_pressed[pygame.K_RIGHT]:
                yoffset = self.tilesize * 1

        # call counter is how many times move is called.
        # we will use it to determine how often to switch between frames in the sprite.
        self.callCounter += 1

        # increment frame counter based on the delay we set
        if self.callCounter % self.delay == 0:
            self.frameCounter += 1

        # midpoint of a frame so it prints centered
        mid = self.tilesize // 2

        # xoffset picks the color of the ghost
        xoffset = self.color_offset

        frame = (
            xoffset
            + self.frame_nums[self.frameCounter % len(self.frame_nums)] * self.tilesize
        )
        self.screen.blit(
            self.image,
            (self.x - mid, self.y - mid),
            (frame, yoffset, self.tilesize, self.tilesize),
        )


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


class BackgroundScroller:
    def __init__(self, screen, floor, tile_size):
        # assumes squares for now

        self.screen = screen  # pygame screen handle
        self.bgimg = pygame.image.load(floor)  # background img handle
        self.bgimg_size = self.bgimg.get_rect().size  # size of bg image: tuple (w,h)

        self.tile_size = tile_size

        self.gw = config["window_size"]["width"]  # game width
        self.gh = config["window_size"]["height"]  # game height

        # self.bgimg = pygame.transform.scale(self.bgimg, (1280, 720))

        self.floorw = self.bgimg_size[0]
        self.floorh = self.bgimg_size[1]

        self.cx = self.gw // 2  # center x (of game window)
        self.cy = self.gh // 2  # center y
        self.step = 2  # move size in any direction
        self.target_location = None  # tuple (x,y) of where to move to
        self.cardinal_direction = None  # direction to move to go toward goal
        self.distance_to_target = 0
        self.scroll_x = 0
        self.scroll_y = 0

        self.w_buffer = (self.floorw - self.gw) // 2
        self.h_buffer = (self.floorh - self.gh) // 2

    def setScrollDirection(self, loc=None):
        """If keys are pressed or mouse is clicked, set a goal location to scroll toward."""
        self.target_location = loc
        self.cardinal_direction = getCardinalDirection(
            (self.cx, self.cy), self.target_location
        )
        self.distance_to_target = straightDistance(
            (self.cx, self.cy), self.target_location
        )

        print(self.target_location)
        print(self.cardinal_direction)
        print(self.distance_to_target)

    def drawBackground(self):
        self.screen.fill(colors["white"])
        self.scrollBackground()

    def scrollBackground(self):
        if self.target_location != None:
            if "N" in self.cardinal_direction:
                self.scroll_y -= self.step
            if "S" in self.cardinal_direction:
                self.scroll_y += self.step
            if "E" in self.cardinal_direction:
                self.scroll_x += self.step
            if "W" in self.cardinal_direction:
                self.scroll_x -= self.step

        self.scroll_x = self.scroll_x % self.tile_size
        self.scroll_y = self.scroll_y % self.tile_size

        basex = self.w_buffer + (self.scroll_x)
        basey = self.h_buffer + (self.scroll_y)

        self.screen.blit(self.bgimg, (0, 0), (basex, basey, self.gw, self.gh))


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

    pman = PacmanSprite(screen=screen, color="blue")

    background = BackgroundScroller(screen, config["background"], 40)

    # Run until the user asks to quit
    # game loop
    running = True

    while running:
        # Did the user click the window close button?
        eventHelper.reset()

        background.drawBackground()

        is_key_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                eventHelper.events["keydown"] = event.key

            if event.type == pygame.KEYUP:
                eventHelper.events["keyup"] = event.key

            if event.type == pygame.MOUSEMOTION:
                eventHelper.events["mouse_motion"] = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                eventHelper.events["mouse_button_up"] = pygame.mouse.get_pos()
                background.setScrollDirection(pygame.mouse.get_pos())

        eventHelper.events["all_pressed"] = pygame.key.get_pressed()

        pman.Move(is_key_pressed)

        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()


if __name__ == "__main__":
    main()
