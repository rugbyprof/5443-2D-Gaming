"""
This example has a series of classes to help with the multiplayer issue:

Messenger: 
    Handles messaging for the players
BasicPlayer:
    Handles basic drawing and moving and is extended by `Player`
Player:
    Adds messaging to a basic player.
GameManager:
    Since we want most updating to be done locally, the game manager creates basic
    instances of each player (BasicPlayer) to move them around the screen. This reduces
    messaging to a minimum.
Globals:
    This was kind of an experiment to see about class level variables. I didn't want pygame
    to get instantiated until I grabbed to window location. So this was my solution. 

This multiplayer example moves a bunch of dots around the screen. However, they are pygame
shapes and NOT sprites. I discovered sprites act much differently when moving via vectors.
So, I will create yet another version using sprites instead of shapes and attempt to get the
movement correct. 

USAGE:

    python ex_99.py queue=game-01 player=player-02 windowLocation=400,400 color=Red
    
    - queue             : the exchange or channel you want to join
    - player            : the name or id of a player
    - windowLocation    : allows me to test better by moving pygame windows to different locations
    - color             : player dot color
"""


import pygame
from random import randint
import random
import json
import sys
from rich import print
from threading import Thread
import math
import os
from pygame.math import Vector2

import pygame.display

import colorsys


# necessary libs for rabbitmq
from comms import CommsListener
from comms import CommsSender

globals = None

# bunches of named colors!
with open("colors.json") as f:
    colors = json.load(f)


def randLocation(width=None, height=None):
    global globals
    if not width or not height:
        width, height = globals.screen.get_size()

    x = randint(0, width)
    y = randint(0, height)

    return (x, y)


def randColor():
    # bright_color = { h: Random(0, 255), s: 100, l: 50 }

    h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
    r, g, b = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]

    # minRed = kwargs.get("minRed", 0)
    # maxRed = kwargs.get("maxRed", 255)
    # minGreen = kwargs.get("minRed", 0)
    # maxGreen = kwargs.get("maxRed", 255)
    # minBlue = kwargs.get("minRed", 0)
    # maxBlue = kwargs.get("maxRed", 255)

    return (r, g, b)


class Messenger:
    """
    - Handles messaging (sending and receiving) for each player.
    - Requires a callback to be passed in so received messages can be handled.
    """

    def __init__(self, creds, callback=None):
        self.creds = creds
        self.callBack = callback

        if not self.creds:
            print(
                "Error: Message handler needs `creds` or credentials to log into rabbitmq. "
            )
            sys.exit()

        if not self.callBack:
            print(
                "Error: Message handler needs a `callBack` function to handle responses from rabbitmq. "
            )
            sys.exit()

        # Identify the user
        self.user = self.creds["user"]

        # create instances of a comms listener and sender
        # to handle message passing.
        self.commsListener = CommsListener(**self.creds)
        self.commsSender = CommsSender(**self.creds)

        # Start the comms listener to listen for incoming messages
        self.commsListener.threadedListen(self.callBack)

    def send(self, **kwargs):
        """Sends the message to a target or broadcasts to all."""
        target = kwargs.get("target", "broadcast")
        self.commsSender.threadedSend(
            target=target, sender=self.user, body=json.dumps(kwargs), debug=False
        )


class SpritePlayer(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        super().__init__()
        self.color = kwargs.get("color", (0, 0, 0))
        self.width, self.height = globals.winsize
        self.position = kwargs.get("position", (self.width / 2, self.height / 2))
        self.size = kwargs.get("size", (20, 20))
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=self.position)
        self.speed = kwargs.get("speed", 1)
        self.destination = self.rect.center

    def update(self, keys=None):
        print(self.destination)
        print(self.rect.center)
        if self.rect.center != self.destination:
            direction = Vector2(self.destination) - Vector2(self.rect.center)
            print(f"direction: {direction}")
            distance = direction.length()
            print(f"distance: {distance}")
            normalized_direction = direction.normalize()
            speed = Vector2(self.speed)
            if distance < speed.length():
                print(f"less than: {distance} < {speed.length()}")
                self.rect.center = self.destination
            else:
                print(f"normalized_direction: {normalized_direction}, speed:{speed}")
                moveip = normalized_direction * speed
                mover = (
                    normalized_direction[0] * speed[0],
                    normalized_direction[1] * speed[1],
                )

                print(f"mover: {mover}")
                self.newrect = self.rect.move_ip(mover)
                print(f"rect: {self.rect}")

    def move(self):
        self.rect.center = self.newrect

    def goto(self, x, y):
        self.destination = (x, y)


class BasicPlayer(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        super().__init__()

        # sprite_image = pygame.image.load("sprite.png").convert_alpha()
        # sprite = GameSprite(sprite_image, (320, 240), (5, 5))

        self.screen = kwargs.get("screen", None)
        self.pos = kwargs.get("pos", randLocation())
        self.target = kwargs.get("target", randLocation())
        self.color = kwargs.get("color", (0, 0, 0))
        self.size = kwargs.get("size", (40, 40))
        self.speed = kwargs.get("speed", (0, 0))

        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=self.pos)

        self.speed = Vector2(self.speed)
        self.velocity = Vector2(self.speed)
        self.target = Vector2(self.pos)
        self.pos = Vector2(self.pos)

    def update(self, keys):
        self.rect.move_ip(self.speed)
        self.move()

    def change_speed(self, speed):
        self.speed = speed
        self.speed = Vector2(self.speed)

    def goto(self, target_x, target_y):
        self.target = Vector2(target_x, target_y)
        self.pos = Vector2(self.rect.centerx, self.rect.centery)

        distance = math.sqrt(
            (target_x - self.rect.centerx) ** 2 + (target_y - self.rect.centery) ** 2
        )

        # set players direction based on clicked location and current dot location
        self.direction = Vector2(self.target) - Vector2(self.pos)

        # Normalize the direction vector to get a unit vector
        direction_normalized = Vector2(self.direction).normalize()

        # Calculate the velocity vector by multiplying the direction vector by the speed
        self.velocity = direction_normalized * self.speed

    def move(self, keys=None):
        """
        - Change player position based on velocity.
        - Stop player if space bar is pressed.
        """
        # print(f"updating {self.color}")
        if keys:
            if keys[pygame.K_SPACE]:
                self.speed.x = 0
                self.speed.y = 0

        print(self.pos)
        print(self.velocity)
        # Move the sprite towards the target each frame
        self.pos.x += self.velocity.x
        self.pos.y += self.velocity.y

        # Wrap player around the screen so
        # they never get lost.
        if self.pos.x > globals.winsize[0]:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = globals.winsize[0]
        if self.pos.y > globals.winsize[1]:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = globals.winsize[1]


class Player(BasicPlayer):
    def __init__(self, **kwargs):
        """Extends BasicPlayer to add messaging capabilities to a player.

        Args:
            callback (function)     : callback function to handle messages.
            color (tuple)           : tuple of (r,g,b)
            creds (json)            : credentials for messaging back end
            name (string)           : unique identifier
            screen (pygame surface) : pygame surface to display player
        """

        super().__init__(**kwargs)

        self.creds = kwargs.get("creds", None)
        self.callback = kwargs.get("callback", None)
        self.id = self.creds["user"]
        self.messenger = Messenger(self.creds, self.callback)
        self.lastBroadcast = pygame.time.get_ticks()
        self.broadCastDelay = 50

    def timeToBroadCast(self):
        """check to see if there was enough delay to broadcast again"""
        return pygame.time.get_ticks() - self.lastBroadcast > self.broadCastDelay

    def broadcastData(self, data):
        """Sends data to all other players in the game.

        Args:
            data (dict) : key value dict of data to send
        """
        if self.timeToBroadCast():
            self.messenger.send(
                target="broadcast", sender=self.id, player=self.id, data=data
            )
            self.lastBroadcast = pygame.time.get_ticks()
            return True

        return False

    def goto(self, target_x, target_y):
        """Overloaded method which simply calls parent "goto" method, but
            necessary since this method needs to broadcast a target xy to
            other players and base class doesn't have messaging capabilities.
        Args:
            x (int) : x coord
            y (int) : y coord
        """
        print("child goto")
        self.target = (target_x, target_y)
        super(Player, self).goto(target_x, target_y)
        print("broadcasting target")

        # print(
        #     {
        #         "target": (self.target[0], self.target[1]),
        #         "location": (self.rect.centerx, self.rect.centery),
        #         "speed": (self.speed[0], self.speed[1]),
        #         "color": self.color,
        #     }
        # )

        self.broadcastData(
            {
                "target": (self.target[0], self.target[1]),
                "pos": (self.rect.centerx, self.rect.centery),
                "speed": (self.speed[0], self.speed[1]),
                "color": self.color,
            }
        )

    def setSpeed(self, speed):
        """Yup. This sets the players speed.
            It also broadcasts the speed to everyone else.
        Args:
            speed (int) : players speed
        """
        super(Player, self).setSpeed(speed)
        print("broadcasting speed")
        self.broadcastData(
            {
                "target": (self.target[0], self.target[1]),
                "pos": (self.rect.centerx, self.rect.centery),
                "speed": (self.speed[0], self.speed[1]),
                "color": self.color,
            }
        )


class GameManager:
    """
    - Manages all external players that are in the same game queue.
    - Any message that gets broadcast is listened to by the game managers
      callback method (call back is not a keyword and is named callBack to
      fit its purpose) and handled based on its content.
    - Commands:
        - xy        : tells manager to put the player at the xy coords
        - target    : tells manager to move player toward the target
        - speed     : tells manager to change a players speed
        - color     : tells a manager what color a dot is
    """

    def __init__(self, screen):
        self.players = {}
        self.screen = screen
        self.localPlayer = None
        self.sprites = pygame.sprite.Group()

    def addPlayer(self, **kwargs):
        """Adds a player to the local game as dictated by incoming messages."""
        name = kwargs.get("name", None)
        player = kwargs.get("player", None)
        color = kwargs.get("color", None)
        localPlayer = kwargs.get("localPlayer", False)

        # we don't want to try and manage the local player instance
        if localPlayer:
            self.localPlayer = player.id
        else:
            # this is a new player that needs just a basic player class
            # with no messaging capabilites. This is a mirror of another
            # player somewhere else.
            player = BasicPlayer(screen=self.screen, name=name, color=color)
            self.players[name] = player

    def update(self):
        """Update all players registered with the game manager."""
        for id, player in self.players.items():
            player.update()

    def callBack(self, ch, method, properties, body):
        """_summary_: callback for multiple players

        Args:
            ch (pika): type of channel connection with rabbitmq
            method (pika): async info
            properties (pika): general info about connection
            body (dict): only thing that really matters. This is your data

        Returns:
            dictionary: results of callback
        """

        game = method.exchange  # not used here but passed in by pika
        exchange = method.exchange  # not used here but passed in by pika
        body = json.loads(body.decode("utf-8"))  # where all the game commands are
        data = body.get("data", None)
        sender = body["sender"]
        xy = data.get("pos", None)
        target = data.get("target", None)
        color = data.get("color", None)
        speed = data.get("speed", None)

        if self.localPlayer != sender:
            print(f"not local: {sender} != {self.localPlayer}")
            if not sender in self.players:
                self.addPlayer(name=sender, color=color)
                print(f"Players: {len(self.players)}")
            else:
                if xy:
                    self.players[sender].pos.x = xy[0]
                    self.players[sender].pos.y = xy[1]
                if target:
                    print(f"{sender} goto to {target}")
                    self.players[sender].goto(target[0], target[1])
                if speed:
                    print(f"{sender} speed to {speed}")
                    self.players[sender].setSpeed(speed)
                if color:
                    print(f"{sender} color to {color}")
                    self.players[sender].color = color
        else:
            print("local player")


############################################################
# GLOBALS
############################################################
class Globals:
    """A class mainly for one reason, placing game window in new xy pos"""

    winx = 0
    winy = 0
    winsize = (400, 400)
    screen = None
    clock = None
    fps = 60

    def __new__(cls, x, y):
        os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (int(x), int(y))
        pygame.init()
        cls.screen = pygame.display.set_mode(cls.winsize)
        cls.clock = pygame.time.Clock()
        instance = super().__new__(cls)
        return instance


def main(creds, x, y, color=None):
    """
    Args:
        creds (dict)    : credentials for messaging
        x,y  (int,int)  : starting pos for player (dot)
        color (tuple)   : rgb color value
    """
    global globals
    globals = Globals(x, y)

    manager = GameManager(globals.screen)

    # localPlayer = Player(
    #     screen=globals.screen, creds=creds, callback=manager.callBack, color=color
    # )

    localPlayer = SpritePlayer()

    # manager.addPlayer(player=localPlayer, localPlayer=True)

    sprites_group = pygame.sprite.Group(localPlayer)

    # set the window title
    pygame.display.set_caption(f"{creds['user']}")

    # create list for lookup for keys 0-9
    # The keys 0-9 are ascii 48-57
    numericKeys = [x for x in range(48, 58)]

    # run the game loop
    running = True
    while running:
        # clear the screen
        globals.screen.fill((255, 255, 255))

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    localPlayer.update(keys)
                # get the keys 0-9 if pressed
                elif event.key in numericKeys:
                    print(f"Speed set to: {event.key-48}")
                    # choose current dot by which key pressed
                    localPlayer.setSpeed(event.key - 48)

            elif event.type == pygame.MOUSEBUTTONUP:
                # Get the position of the mouse click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print(mouse_x, mouse_y)
                localPlayer.goto(mouse_x, mouse_y)

        # move the dot based on key input
        keys = pygame.key.get_pressed()
        localPlayer.update(keys)

        sprites_group.update(keys)
        sprites_group.draw(globals.screen)

        manager.update()

        # update the screen
        pygame.display.flip()

        globals.clock.tick(globals.fps)

    # quit Pygame
    pygame.quit()


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
    kargs = {}

    for arg in argv:
        if "=" in arg:
            key, val = arg.split("=")
            kargs[key] = val
        else:
            args.append(arg)
    return args, kargs


def usage():
    print("Need: queue and player ")
    print(
        "Example: python ex_99.py queue=game-01 player=player-01 windowLocation=100,100 color=blue"
    )
    sys.exit()


if __name__ == "__main__":
    """
    Example: python ex_99.py queue=game-01 player=player-01 windowLocation=100,100 color=blue
    """

    args, kwargs = mykwargs(sys.argv)

    queue = kwargs.get("queue", None)
    player = kwargs.get("player", None)
    windowLocation = kwargs.get("windowLocation", (100, 100))
    color = kwargs.get("color", "Red")

    color = colors[color]["rgb"]

    print(windowLocation)

    if not isinstance(windowLocation, tuple):
        windowLocation = tuple(windowLocation.split(","))

    x, y = windowLocation

    if None in [queue, player]:
        usage()

    # player credentials built based on which temp player chosen (player-01 through player-25)
    creds = {
        "exchange": queue,
        "port": "5672",
        "host": "terrywgriffin.com",
        "user": player,
        "password": player + "2023!!!!!",
    }

    main(creds, x, y, color)
