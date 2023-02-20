"""
Source: https://python-forum.io/thread-21996.html
User: Windspar
"""

import os
import pygame
from pygame.sprite import Sprite
from math import radians, sin, cos
import random
import sys
import json
from comms import CommsSender
from comms import CommsListener


class Scene:
    def on_draw(self, surface):
        pass

    def on_event(self, event):
        pass

    def on_update(self, delta):
        pass


class Manager:
    def __init__(self, caption, width, height, center=True):
        if center:
            os.environ["SDL_VIDEO_CENTERED"] = "1"

        # Basic pygame setup
        pygame.display.set_caption(caption)
        self.surface = pygame.display.set_mode((width, height))
        self.rect = self.surface.get_rect()
        self.clock = pygame.time.Clock()
        self.running = False
        self.delta = 0
        self.fps = 60

        # Scene Interface
        self.scene = Scene()

    def mainloop(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                self.scene.on_event(event)

            self.scene.on_update(self.delta)
            self.scene.on_draw(self.surface)
            pygame.display.flip()
            self.delta = self.clock.tick(self.fps)


class BaseSprite(Sprite):
    def __init__(self, image, position, anchor="topleft"):
        Sprite.__init__(self)
        self.original_image = image
        self.image = image
        self.rect = image.get_rect()
        setattr(self.rect, anchor, position)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class RotationStyleMovement:
    """ This class is injected to a sprite class to handle smooth control
        for sprites that need a top down driving type effect that includes
        forward, backward, and left / right rotation to change direction. 
    """

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
        self.center = pygame.Vector2(self.sprite.rect.center)
        self.set_direction()

    def set_direction(self):
        rad = radians(self.angle)
        self.direction = pygame.Vector2(sin(rad), cos(rad))

    def do_rotate(self):
        self.sprite.image = pygame.transform.rotate(
            self.sprite.original_image, self.angle
        )
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.center = self.center
        self.set_direction()

    def get_input(self, up, down, left, right, delta):

        if up:
            self.center -= self.direction * delta * self.speed
            self.sprite.rect.center = self.center
        elif down:
            self.center += self.direction * delta * (self.speed / 2)
            self.sprite.rect.center = self.center

        if right:
            self.angle = (self.angle - self.rotation_speed * delta) % 360
            self.do_rotate()
        elif left:
            self.angle = (self.angle + self.rotation_speed * delta) % 360
            self.do_rotate()


class Player:
    """ A simple player class that either:
            1) uses an image to create a car 
            2) creates some rectangles to do the same
        DependsOn:
            RotationStyleMovement: to handle moving
        Params:
            pos (tuple: x,y location
            image (string): if exists will attempt to create sprite with image
    """

    def __init__(self, **kwargs):
        pos = kwargs.get('pos',(0,0))
        image = kwargs.get('image',None)
        creds = kwargs.get('creds',None)

        self.messageQueue = None

        if creds:
            self.messageQueue = Message(creds)
            self.player = creds['user']
        else:
            self.player = None
        
        colors = ["red", "green", "blue", "white"]
        self.turnChoice = [True, False]

        if image:
            self.rectangle = pygame.image.load(image)
            self.rectangle = pygame.transform.rotate(self.rectangle, 90)
            print(self.rectangle)
        else:
            self.rectangle = pygame.Surface((20, 40), pygame.SRCALPHA)
            self.rectangle.fill(pygame.Color(random.choice(colors)))
            self.rectangle.fill(pygame.Color("white"), (2, 2, 16, 8))

        self.sprite = BaseSprite(self.rectangle, pos, "center")
        self.sprite_movement = RotationStyleMovement(
            self.sprite, None, None, None, None
        )
        self.lastTurn = 0
        self.turnThreshold = random.randrange(1000, 2000)
        self.up, self.down, self.left, self.right = (True, False, True, False)

    def move(self, delta):
        random.shuffle(self.turnChoice)
        if pygame.time.get_ticks() - self.lastTurn > self.turnThreshold:
            self.lastTurn = pygame.time.get_ticks()
            self.up, self.down, self.left, self.right = [
                True,
                False,
                self.turnChoice[0],
                self.turnChoice[1],
            ]
        self.sprite_movement.get_input(self.up, self.down, self.left, self.right, delta)
        if self.player:
            self.messageQueue.commsSender.threadedSend(
                    target='broadcast', sender=self.player,body =json.dumps({'message':'message content'})
            )


class Message:
    def __init__(self,creds):
        self.player = creds["user"]
        self.creds = creds

        # create instances of a comms listener and sender
        # to handle message passing.
        self.commsListener = CommsListener(**creds)
        self.commsSender = CommsSender(**creds)

        # Start the comms listener to listen for incoming messages
        self.commsListener.threadedListen(self.callBack)

    def callBack(self):
        print("this is a local callback")


class Game(Scene):
    def __init__(self, manager):
        self.manager = manager
        self.players = []

    def add_player(self, **kwargs):
        pos = kwargs.get('pos',None)
        image = kwargs.get('image',None)
        creds = kwargs.get('creds',None)

        if not pos or not image or not creds:
            print("Error!!! Missing param in Game class")
            sys.exit()

        self.players.append(Player(pos=pos, image=image,creds=creds))

    def on_draw(self, surface):
        surface.fill(pygame.Color("black"))
        for player in self.players:
            player.sprite.draw(surface)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.manager.running = False
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     self.add_player(event.pos)

    def on_update(self, delta):
        # keys = pygame.key.get_pressed()
        for player in self.players:
            player.move(delta)


def main(creds):
    pygame.init()
    manager = Manager("Random Cars", 800, 600)
    manager.scene = Game(manager)

    image_path = "./images/cars/"
    images = [
        "Car64.png",
        "CarBlue64.png",
        "CarGreen64.png",
        "CarRed64.png",
        "CarYellow64.png",
    ]

    image = random.choice(images)
    
    pos = (random.randint(10, 800), random.randint(500, 600))
    manager.scene.add_player(pos=pos,creds=creds,image=image_path+image)
    manager.mainloop()


def mykwargs(argv):
    """
    Processes argv list into plain args and kwargs.
    Just easier than using a library like argparse for small things.
    Example:
        python file.py arg1 arg2 arg3=val1 arg4=val2 -arg5 -arg6 --arg7
        Would create:
            args[arg1, arg2, -arg5, -arg6, --arg7]
            kargs{arg3 : val1, arg4 : val2}

        Params with dashes (flags) can now be processed seperately
    Shortfalls:
        spaces between k=v would result in bad params
    Returns:
        tuple  (args,kargs)
    """
    args = []
    kwargs = {}

    for arg in argv:
        if "=" in arg:
            key, val = arg.split("=")
            kwargs[key] = val
        else:
            args.append(arg)
    return args, kwargs

if __name__ == "__main__":
    args,kwargs = mykwargs(sys.argv)

    creds = {
        "exchange": kwargs.get('exchange','messages'),
        "port": kwargs.get('port','5672'),
        "host": kwargs.get('host','terrywgriffin.com'),
        "user": kwargs.get('user','player-2'),
        "password": kwargs.get('password','player-22023!!!!!')
    }
    
    main(creds)
