#!/usr/bin/env python3
"""
This starts an image class ...
https://gist.github.com/abcsds/8093698
"""
# Import and initialize the pygame library

import pygame
from pygame.locals import *

from pygame.sprite import Sprite
from math import radians, sin, cos

import random
import sys
import math
import os
import glob
from rich import print
import json

from comms import CommsListener
from comms import CommsSender

pygame.init()

screen = pygame.display.set_mode([500, 700])


class RotationMovementKeys:

    def __init__(self, sprite, up, down, left, right):
        self.sprite = sprite
        self.up = up
        self.down = down
        self.left = left
        self.right = right

        self.angle = 0
        # self.speed = 0.04
        # self.rotation_speed = 0.08
        self.speed = 0.12
        self.rotation_speed = 0.08
        print(self.sprite)
        self.center = pygame.Vector2(self.sprite.rect.center)
        self.set_direction()

    def set_direction(self):
        rad = radians(self.angle)
        self.direction = pygame.Vector2(sin(rad), cos(rad))

    def do_rotate(self):
        self.sprite.image = pygame.transform.rotate(self.sprite.original_image,
                                                    self.angle)
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.center = self.center
        self.set_direction()

    def on_keydown(self, keys_press, delta):
        if keys_press[self.up]:
            self.center -= self.direction * delta * self.speed
            self.sprite.rect.center = self.center
        elif keys_press[self.down]:
            self.center += self.direction * delta * (self.speed / 2)
            self.sprite.rect.center = self.center

        if keys_press[self.right]:
            self.angle = (self.angle - self.rotation_speed * delta) % 360
            self.do_rotate()
        elif keys_press[self.left]:
            self.angle = (self.angle + self.rotation_speed * delta) % 360
            self.do_rotate()

class BaseSprite(Sprite):

    def __init__(self, **kwargs):
        Sprite.__init__(self)
        anchor = kwargs.get('anchor','center')
        position = kwargs.get('position',(0,0))
        self.original_image = kwargs.get('image')
        self.image = kwargs.get('image')
        self.rect = self.image.get_rect()

        setattr(self.rect, anchor, position)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class PyImage(Sprite):
    def __init__(self, **kwargs):
        Sprite.__init__(self)
        self.imagePath = kwargs.get("image_path", None)
        self.image = pygame.image.load(self.imagePath)

        self.position = kwargs.get('position',(0,0))
        self.anchor = kwargs.get("anchor", "center")
        self.original_image = self.image
        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)





        self.image = pygame.transform.rotate(self.image, 90)

        self.imWidth = self.image.get_width()
        self.imHeight = self.image.get_height()


        self.rect.center = self.position

        self.sprite_movement = RotationMovementKeys(self.image, pygame.K_UP,
                                                    pygame.K_DOWN,
                                                    pygame.K_LEFT,
                                                    pygame.K_RIGHT)
    def draw(self, surface):
        surface.blit(self.image, self.rect)



def callBack(ch, method, properties, body):
    body = json.loads(body)
    car.draw()


def main(player,otherplayer):


    creds = {
        "exchange": "pygame2d",
        "port": "5672",
        "host": "terrywgriffin.com",
        "user": player,
        "password": "rockpaperscissorsdonkey",
    }

    car = PyImage(
        screen=screen,
        image_path="./images/cars/CarRed64.png",
        scaleX=0.2,
        scaleY=0.2,
        x=250,
        y=300,
        position=(250,300)
    )


    # create instances of a comms listener and sender
    # to handle message passing.
    commsListener = CommsListener(**creds)
    commsSender = CommsSender(**creds)

    # Start the comms listener to listen for incoming messages
    commsListener.threadedListen(callBack)


    print(callBack)


    clock = pygame.time.Clock()

    width = 500  # width of overall screen
    height = 500  # same but height
    running = True  # Run until the user asks to quit

    screen_color = (47, 109, 158)

    # Set up the drawing window


    car.draw()


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
                    

                    commsSender.threadedSend(otherplayer, json.dumps({'from':player,'data':'up'}))
                elif event.key == pygame.K_LEFT:
                    print('left')
                    
                elif event.key == pygame.K_RIGHT:
                    print('right')
                    

        car.draw()

# Flip the display
        pygame.display.flip()
        clock.tick(60)
        pygame.time.wait(5)
        pygame.display.update()

    # Done! Time to quit.
    pygame.quit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("need player name")
        sys.exit()
    player = sys.argv[1]
    
    if player == 'player-1':
        otherPlayer = 'player-2'
    else:
        otherPlayer = 'player-1'
    main(player,otherPlayer)