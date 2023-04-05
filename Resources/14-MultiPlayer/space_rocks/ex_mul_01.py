"""
THIS IS A COPY FROM LECTURES/04-MultiPlayer
"""


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
        xy = data.get("location", None)
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
                    self.players[sender].location.x = xy[0]
                    self.players[sender].location.y = xy[1]
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
    """A class mainly for one reason, placing game window in new xy location"""

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
        x,y  (int,int)  : starting location for player (dot)
        color (tuple)   : rgb color value
    """
    globals = Globals(x, y)
    manager = GameManager(globals.screen)

    localPlayer = Player(
        screen=globals.screen, creds=creds, callback=manager.callBack, color=color
    )

    manager.addPlayer(player=localPlayer, localPlayer=True)

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
