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

# necessary libs for rabbitmq
from comms import CommsListener
from comms import CommsSender


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
        """ """
        target = kwargs.get("target", "broadcast")
        self.commsSender.threadedSend(
            target=target, sender=self.user, body=json.dumps(kwargs), debug=False
        )


class BasicPlayer:
    def __init__(self, screen):
        """_summary_

        Args:
            screen (_type_): _description_
            creds (_type_): _description_
        """

        self.screen = screen  # copy of screen to display dot on

        # set the initial position of the dot
        self.dot_position = pygame.math.Vector2(randint(25, 400), randint(25, 400))
        self.speed = 1
        self.color = (randint(0, 256), randint(0, 256), randint(0, 256))
        self.ticks = 0
        self.width, self.height = screen.get_size()
        self.lastUpdated = pygame.time.get_ticks()

    def update(self, keys):
        """Get the keys from main, then adjust position based
        on keys pressed
        """
        if keys[pygame.K_UP]:
            self.dot_position.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.dot_position.y += self.speed
        if keys[pygame.K_LEFT]:
            self.dot_position.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.dot_position.x += self.speed

        if self.dot_position.x > self.width:
            self.dot_position.x = 0
        if self.dot_position.x < 0:
            self.dot_position.x = self.width

        if self.dot_position.y > self.height:
            self.dot_position.y = 0
        if self.dot_position.y < 0:
            self.dot_position.y = self.height

    def draw(self):
        # draw the dot
        pygame.draw.circle(self.screen, self.color, self.dot_position, 10)


class Player(BasicPlayer):
    def __init__(self, screen, creds, callback=None):
        """_summary_

        Args:
            screen (_type_): _description_
            creds (_type_): _description_
        """

        super().__init__(screen)
        self.creds = creds
        self.id = self.creds["user"]
        self.messenger = Messenger(self.creds, callback)
        self.lastBroadcast = pygame.time.get_ticks()
        self.broadCastDelay = 100

    def timeToBroadCast(self):
        return pygame.time.get_ticks() - self.lastBroadcast > self.broadCastDelay

    def broadcastLocation(self):
        # only send a message so many ticks otherwise problems occur!
        pos = (self.dot_position.x, self.dot_position.y)

        self.messenger.send(
            target="broadcast", sender=self.id, player=self.id, dot_position=pos
        )
        self.lastBroadcast = pygame.time.get_ticks()

    def threadedBroadcastLocation(self):
        # only send a message so many ticks otherwise problems occur!
        # print(pygame.time.get_ticks() - self.ticks)
        while True:
            if pygame.time.get_ticks() - self.ticks > 100:
                pos = (self.dot_position.x, self.dot_position.y)

                self.messenger.send(
                    target="broadcast", sender=self.id, player=self.id, dot_position=pos
                )
                self.ticks = pygame.time.get_ticks()

    def threadedBroadcast(self):
        Thread(
            target=self.broadcastLocation,
            args=(),
            daemon=True,
        ).start()

    def draw(self):
        # draw the dot
        pygame.draw.circle(self.screen, self.color, self.dot_position, 10)


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
            if not id == self.localPlayer:
                player.draw()

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
        sender = body["sender"]
        x, y = body["dot_position"]

        # for k,v in body.items():
        #     results[k] = v

        if not sender in self.players:
            self.players[sender] = BasicPlayer(self.screen)
            print(len(self.players))
        else:
            if pygame.time.get_ticks() - self.players[sender].lastUpdated > 100:
                self.players[sender].dot_position.x = x
                self.players[sender].dot_position.y = y
                self.players[sender].lastUpdated = pygame.time.get_ticks()


############################################################
# GLOBALS
############################################################

# initialize Pygame
pygame.init()

# set the window size
size = (400, 400)

# create the window
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

FPS = 60
############################################################


def main(creds):
    manager = GameManager(screen)

    localPlayer = Player(screen, creds, manager.callBack)

    # localPlayer.threadedBroadcast()

    manager.addPlayer(localPlayer, True)

    # set the window title
    pygame.display.set_caption(f"{creds['user']}")

    # create list for lookup for keys 0-9
    # The keys 0-9 are ascii 48-57
    numericKeys = [x for x in range(0, 58)]

    # run the game loop
    running = True
    while running:
        # clear the screen
        screen.fill((255, 255, 255))

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # get the keys 0-9 if pressed
                elif event.key in numericKeys:
                    print(f"Speed set to: {event.key-48}")
                    # choose current dot by which key pressed
                    localPlayer.speed = event.key - 48

        # move the dot based on key input
        keys = pygame.key.get_pressed()
        localPlayer.update(keys)
        localPlayer.draw()

        if localPlayer.timeToBroadCast():
            localPlayer.broadcastLocation()

        manager.draw()

        # update the screen
        pygame.display.flip()

        clock.tick(FPS)

    # quit Pygame
    pygame.quit()


if __name__ == "__main__":
    """
    python ex_05.py game1 player-1 'player-12023!!!!!'
    """
    if len(sys.argv) < 3:
        print("Need: exchange and player ")
        print("Example: python ex05.py game-01 player-02")
        sys.exit()
    game = sys.argv[1]
    player = sys.argv[2]
    creds = {
        "exchange": game,
        "port": "5672",
        "host": "terrywgriffin.com",
        "user": player,
        "password": player + "2023!!!!!",
    }

    main(creds)
