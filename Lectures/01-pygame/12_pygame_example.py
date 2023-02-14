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
        self.angle = kwargs.get("angle", 0)

        self.image = pygame.image.load(self.imagePath).convert_alpha()
        self.image.convert()

        self.imWidth = self.image.get_width()
        self.imHeight = self.image.get_height()

        self.image = pygame.transform.scale(
            self.image,
            (int(self.imWidth * self.scaleX), int(self.imHeight * self.scaleY)),
        )

        if self.angle:
            self.image = pygame.transform.rotate(self.image, self.angle)

        self.rect = self.image.get_rect()
        self.rect.center = self.location

    def scale(self, scaleX, scaleY):
        pass

    def rotate(self, change):
        """
        https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame

        not implemented
        """
        self.angle += change
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.bbox = self.image.get_rect(center = self.image.get_rect(center = (self.x, self.y)).center)

    def move(self, x=0, y=0):
        self.x += x
        self.y += y
        self.location = (self.x, self.y)
        self.rect.center = self.location


class PySprite(PyImage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frames = kwargs.get("frames", 0)
        self.currFrame = 0

    def update(self):
        screen.blit(self.image, self.location)



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
        x=250,
        y=300
    )

    screen.blit(ptBoat.image, (250, 250))  # paint to screen

    ptBoat.update()

    pygame.display.flip()  # paint screen one time

    while running:

        screen.fill(screen_color)


        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:                   
                if event.key == pygame.K_DOWN:
                    print('down')
                elif event.key == pygame.K_UP:
                    print('up')
                    ptBoat.move(0,-5)
                elif event.key == pygame.K_LEFT:
                    print('left')
                    ptBoat.rotate(3)
                elif event.key == pygame.K_RIGHT:
                    print('right')
                    ptBoat.rotate(-3)

        ptBoat.update()

# Flip the display
        pygame.display.flip()
        clock.tick(60)
        pygame.time.wait(5)
        pygame.display.update()

    # Done! Time to quit.
    pygame.quit()
