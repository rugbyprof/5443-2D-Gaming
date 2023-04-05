"""
Pygame P01-008

Description:

   Shows simple animation using a pacman sprite sheet.
   A spritesheet has

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


def rgb_colors(infile):
    """
    Loads a json color file into a python dictionary.
        Params:
            infile (string) : path to json input file
        Returns:
            colors (dictionary) : dictionary of colors (rgb only)
    """
    rgb = {}
    with open(infile, "r") as f:
        data = f.read()
        colors = json.loads(data)
    for key, color in colors.items():
        rgb[key] = color["rgb"]
    return rgb


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
    "title": "008 Sprite Sheet Lesson",
    "window_size": {"width": 500, "height": 500},
    "sprite_sheet": "./media/pacman_ghosts_40x.png",
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
        color = kwargs.get("color", "orange")

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

        #
        self.frameCounter = 0

        self.diedframe = 0

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

        # for i in range(len(events['all_pressed'])):
        #     if events['all_pressed'][i] > 0:
        #         print(i)

        self.frameCounter += 1

        # midpoint of a frame
        mid = self.tilesize // 2

        xoffset = self.color_offset

        if is_key_pressed[pygame.K_SPACE]:
            print("space")

            yoffset = 0
            xoffset = 960
            frame = xoffset + self.diedframe % 5 * self.tilesize
            self.screen.blit(
                self.image,
                (self.x - mid, self.y - mid),
                (frame, yoffset, self.tilesize, self.tilesize),
            )
            self.diedframe += 1
            if self.diedframe == 5:
                self.diedframe = 0

        print(xoffset)

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
    """
    NOT USED!!
    Dictionary of events all kept in one place for use in other classes

    """

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

    screen.fill(colors["white"])

    pman = PacmanSprite(screen=screen, color="blue")

    # Run until the user asks to quit
    # game loop
    running = True

    direction = None

    while running:
        screen.fill(colors["white"])

        # Did the user click the window close button?
        eventHelper.reset()

        is_key_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                eventHelper.events["keydown"] = event.key
                direction = event.key

            if event.type == pygame.KEYUP:
                eventHelper.events["keyup"] = event.key
                direction = None

            if event.type == pygame.MOUSEMOTION:
                eventHelper.events["mouse_motion"] = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                eventHelper.events["mouse_button_up"] = pygame.mouse.get_pos()

        pman.Move(is_key_pressed)

        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()


if __name__ == "__main__":
    main()
