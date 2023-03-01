"""
After we saw how to control each player using event logic,
could we use similar logic to do the same for a multiplayer game?
Instead of directly controlling each player, we could let commands 
comming from a specific player be passed to a "dot" instance to move
it. 

First however, lets get a comms example that will let players wanting
to be added to the same game get added and basically "appear" when they
send a message to the same game queue you are on. 
"""
import pygame
from random import randint
import json
import sys
from rich import print
from threading import Thread
import math
import os

import pygame.display


# necessary libs for rabbitmq
from comms import CommsListener
from comms import CommsSender


colors = {
    "red":(255,0,0),
    "green":(0,255,0),
    "blue":(0,0,255),
    "pink":(255,192,203),
    "purple":(191, 64, 191),
    "yellow":(255, 191, 0)
}


class Messenger:
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

        self.user = self.creds["user"]

        # create instances of a comms listener and sender
        # to handle message passing.
        self.commsListener = CommsListener(**self.creds)
        self.commsSender = CommsSender(**self.creds)

        # Start the comms listener to listen for incoming messages
        self.commsListener.threadedListen(self.callBack)

    def send(self, **kwargs):
        """ Sends the message to a target or broadcasts to all.
        """
        target = kwargs.get("target", "broadcast")
        self.commsSender.threadedSend(
            target=target, sender=self.user, body=json.dumps(kwargs), debug=False
        )


class BasicPlayer:
    def __init__(self, screen, id=None,color=None):
        """_summary_

        Args:
            screen (pygame surface): pygame surface to display player
            id (string): unique identifier
        """

        self.screen = screen  # copy of screen to display dot on
        self.name = id
        self.dot_position = pygame.math.Vector2(randint(25, 400), randint(25, 400))
        self.speed = 1
        if color:
            self.color = color
        else:
            self.color = (randint(0, 256), randint(0, 256), randint(0, 256))
        self.ticks = 0
        self.width, self.height = screen.get_size()
        self.lastUpdated = pygame.time.get_ticks()
        self.velocity = pygame.math.Vector2()
        self.direction = (1,1)
        self.target = (0,0)

    def update(self, keys=None):
        """Change player position based on velocity or stop if
           space bar is pressed.
        """
        # print(f"updating {self.color}")
        if keys:
            if keys[pygame.K_SPACE]:
                self.velocity.x = 0
                self.velocity.y = 0

        # Move the sprite towards the target each frame
        self.dot_position.x += self.velocity.x
        self.dot_position.y += self.velocity.y

        if self.dot_position.x > self.width:
            self.dot_position.x = 0
        if self.dot_position.x < 0:
            self.dot_position.x = self.width

        if self.dot_position.y > self.height:
            self.dot_position.y = 0
        if self.dot_position.y < 0:
            self.dot_position.y = self.height

    def goto(self, target_x, target_y):
        """Starts player moving towards the x,y coords passed
           in from a mouse click event.
        """
        distance = math.sqrt(
            (target_x - self.dot_position.x) ** 2
            + (target_y - self.dot_position.y) ** 2
        )
        self.direction = (target_x - self.dot_position.x, target_y - self.dot_position.y)

        # Normalize the direction vector to get a unit vector
        direction_normalized = pygame.math.Vector2(self.direction).normalize()

        # Calculate the velocity vector by multiplying the direction vector by the speed
        self.velocity = direction_normalized * self.speed

        print(f"velocity: {self.velocity}")

    def setSpeed(self,speed):
        self.speed = speed
        direction_normalized = pygame.math.Vector2(self.direction).normalize()

        # change velocity based on input speed 
        self.velocity = direction_normalized * self.speed


    def draw(self):
        # draw the dot
        pygame.draw.circle(self.screen, self.color, self.dot_position, 10)


class Player(BasicPlayer):
    def __init__(self, screen, creds, callback=None,color=None):
        """_summary_

        Args:
            screen (pygame surface): pygame surface to display player
            creds (json): credentials for messaging back end
            callback (function): callback function to handle messages.
        """
        super().__init__(screen, creds["user"],color)
        self.creds = creds
        self.id = self.creds["user"]
        self.messenger = Messenger(self.creds, callback)
        self.lastBroadcast = pygame.time.get_ticks()
        self.broadCastDelay = 50
        self.playerData = {"pos": (self.dot_position.x, self.dot_position.y), "color": self.color, "target": (0, 0),"speed":self.speed}

    def timeToBroadCast(self):
        """ check to see if there was enough delay to broadcast again
        """
        return pygame.time.get_ticks() - self.lastBroadcast > self.broadCastDelay

    def broadcastData(self, data):
        """Sends data to all other players in the game."""
        if self.timeToBroadCast():
            self.messenger.send(
                target="broadcast", sender=self.id, player=self.id, data=data
            )

            self.lastBroadcast = pygame.time.get_ticks()
            return True

        return False

    # def sendPlayerData(self):
    #     self.playerData['pos'] = (self.dot_position.x, self.dot_position.y)
    #     self.playerData['color'] = self.color
    #     self.playerData['target'] = self.target
    #     self.playerData['speed'] = self.speed
    #     self.broadcastData(self.playerData)

    def goto(self, target_x, target_y):
        """ overloaded method which simply calls parent "goto" method, but
            necessary since this method needs to broadcast a target xy to
            other players and base class doesn't have messaging capabilities.
        """
        # print("child goto")
        self.target = (target_x,target_y)
        super(Player, self).goto(target_x, target_y)
        print("broadcasting target")
        self.broadcastData({"target":self.target,"dot_position":(self.dot_position.x,self.dot_position.y),"speed":self.speed,"color":self.color})


    def setSpeed(self,speed):
        super(Player, self).setSpeed(speed)
        print("broadcasting speed")
        self.broadcastData({"speed":self.speed})


class GameManager:
    def __init__(self, screen):
        self.players = {}
        self.screen = screen
        self.localPlayer = None
        self.ticks = pygame.time.get_ticks()

    def addPlayer(self, player, local=False):
        if not player.id in self.players:
            self.players[player.id] = player

        if local:
            self.localPlayer = self.players[player.id]

    def draw(self):
        for id, player in self.players.items():
            # if not id == self.localPlayer:
            player.update()
            player.draw()
            #print(f"drawing player: {player.name} {player.velocity}")



    def callBack(self, ch, method, properties, body):
        """_summary_: callback for multiple players

        Args:
            ch (_type_): _description_
            method (_type_): _description_
            properties (_type_): _description_
            body (_type_): _description_

        Returns:
            dictionary: results of callback
        """

        game = method.exchange
        exchange = method.exchange
        body = json.loads(body.decode("utf-8"))
        data = body.get("data", None)
        sender = body["sender"]
        xy = data.get("dot_position", None)
        target = data.get("target", None)
        color = data.get("color", None)
        speed = data.get("speed", None)

        if self.localPlayer != sender:

            # print(target)
            if not sender in self.players:
                self.players[sender] = BasicPlayer(self.screen, sender,color)
                print(len(self.players))
            else:
                if xy:
                    self.players[sender].dot_position.x = xy[0]
                    self.players[sender].dot_position.y = xy[1]
                if target:
                    print(f"{sender} goto to {target}")
                    self.players[sender].goto(target[0], target[1])
                if speed: 
                    print(f"{sender} speed to {speed}")
                    self.players[sender].setSpeed(speed)
                if color: 
                    print(f"{sender} color to {color}")
                    self.players[sender].color = color  


############################################################
# GLOBALS
############################################################


# # initialize Pygame
# pygame.init()

# # set the window size
# size = (400, 400)

# # create the window
# screen = pygame.display.set_mode(size)

# clock = pygame.time.Clock()

# FPS = 60
############################################################


class Globals:
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


def main(creds, x, y,color=None):
    globals = Globals(x, y)
    manager = GameManager(globals.screen)

    localPlayer = Player(globals.screen, creds, manager.callBack,color)

    manager.localPlayer = creds['user']

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
                localPlayer.goto(mouse_x, mouse_y)

        # move the dot based on key input
        keys = pygame.key.get_pressed()
        localPlayer.update(keys)
        localPlayer.draw()

        manager.draw()

        # update the screen
        pygame.display.flip()

        globals.clock.tick(globals.fps)

    # quit Pygame
    pygame.quit()

def mykwargs(argv):
    '''
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
    '''
    args = []
    kargs = {}

    for arg in argv:
        if '=' in arg:
            key,val = arg.split('=')
            kargs[key] = val
        else:
            args.append(arg)
    return args,kargs

if __name__ == "__main__":
    """
    
    """
    args,kwargs = mykwargs(sys.argv)

    queue = kwargs.get("queue",None)
    player = kwargs.get("player",None)
    windowLocation = kwargs.get("windowLocation",(100,100))
    color = kwargs.get("color","red")

    print(windowLocation)

    if not isinstance(windowLocation,tuple):
        windowLocation = tuple(windowLocation.split(","))

    x,y = windowLocation

    if None in [queue,player]:
        print("Need: queue and player ")
        print("Example: python ex_99.py queue=game-01 player=player-01 windowLocation=100,100 color=blue")
        sys.exit()


    creds = {
        "exchange": queue,
        "port": "5672",
        "host": "terrywgriffin.com",
        "user": player,
        "password": player + "2023!!!!!",
    }

    main(creds, x, y, color)
