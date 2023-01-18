#!/usr/bin/env python3
"""
This starts an image class ...
https://gist.github.com/abcsds/8093698
"""
# Import and initialize the pygame library

import pygame
from pygame.locals import *

import random
import sys
import math
import os
import glob
from rich import print


class PyImage(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        self.screen = kwargs.get("screen", None)
        if not self.screen:
            print("Error! Need surface / screen")
            sys.exit()

        self.imagePath = kwargs.get("image_path", None)

        self.gameWidth = kwargs.get("width", None)
        self.gameHeight = kwargs.get("height", None)

        self.location = kwargs.get("location", None)
        self.x = kwargs.get("x", None)
        self.y = kwargs.get("y", None)

        if self.location:
            self.x = self.location[0]
            self.y = self.location[1]
        else:
            if self.x and self.y:
                self.location = (self.x, self.y)
            else:
                self.location = (0, 0)
                self.x = 0
                self.y = 0

        self.scaleX = kwargs.get("scaleX", 1)
        self.scaleY = kwargs.get("scaleY", 1)
        self.angle = kwargs.get("angle", None)

        self.image = pygame.image.load(self.imagePath).convert_alpha()
        self.image.convert()

        self.imWidth = self.image.get_width()
        self.imHeight = self.image.get_height()

        self.image = pygame.transform.scale(
            self.image,
            (int(self.imWidth * self.scaleX), int(self.imHeight * self.scaleY)),
        )

        if self.angle:
            self.image = pygame.transform.rotate(self.sprite, self.angle)

        self.rect = self.image.get_rect()
        self.rect.center = self.location

    def scale(self, scaleX, scaleY):
        pass

    def rotate(self, angle):
        pass

    def move(self, x, y):
        self.x = x
        self.y = y
        self.location = (x, y)
        self.rect.center = self.location


class PySprite(PyImage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frames = kwargs.get("frames", 0)
        self.currFrame = 0

    def update(self):
        screen.blit(self.image, self.location)


class Game:
    def __init__(self, **kwargs):
        self.running = False
        self.initialized = False
        self.clock = pygame.time.Clock()
        self.width = kwargs.get("width", 800)
        self.height = kwargs.get("height", 600)
        self.size = (self.width, self.height)
        self.caption = kwargs.get("caption", "My Game!")
        self.surfaceColor = kwargs.get("surface_color", (47, 109, 158))
        self.surface = kwargs.get("surface", None)
        if not self.screen:
            print("Error: need pygame screen / window instance to run!")
            sys.exit()

        self.initGame()

    def initGame(self):
        pygame.init()
        if not self.surface:
            self.surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)
        pygame.display.flip()
        self.running = True
        self.initialized = True

    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.running = False
                self.cleanup()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                print(event.pos)

    def loop(self):
        pass

    def render(self):
        pass

    def cleanup(self):
        pygame.quit()

    def on_execute(self):
        if not self.initialized:
            self.running = False
        while self.running:
            for event in pygame.event.get():
                self.handleEvent(event)
            self.loop()
            self.render()
        self.cleanup()


if __name__ == "__main__":

    pygame.init()

    clock = pygame.time.Clock()

    width = 500  # width of overall screen
    height = 500  # same but height
    running = True  # Run until the user asks to quit

    screen_color = (47, 109, 158)

    # Set up the drawing window
    screen = pygame.display.set_mode([width, height])

    ptBoat = PySprite(
        screen=screen,
        image_path="./images/ships/PT_Boat_One.png",
        scaleX=0.2,
        scaleY=0.2,
    )

    screen.blit(ptBoat.image, (250, 250))  # paint to screen

    pygame.display.flip()  # paint screen one time

    while running:

        screen.fill(screen_color)

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Flip the display
        pygame.display.flip()
        clock.tick(60)
        pygame.time.wait(5)
        pygame.display.update()

    # Done! Time to quit.
    pygame.quit()
