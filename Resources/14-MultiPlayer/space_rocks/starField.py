import pygame
import random
import sys
from pygame.math import Vector2


class Colors:
    yellow = (255, 255, 0)
    brightPurple = (191, 0, 255)
    darkRed = (213, 42, 42)
    red = (255, 0, 0)
    green = (0, 255, 0)
    black = (0, 0, 0)
    pink = (255, 105, 180)


class Direction:
    up = Vector2(0, -1)
    down = Vector2(0, 1)
    left = Vector2(-1, 0)
    right = Vector2(1, 0)
    none = Vector2(0, 0)


class StarSize:
    small = 1
    medium = 2
    large = 4


class Star:
    """Represents a star in the starfield. The star knows about its own location, direction
    and color. I do pass in world size, which breaks some kine of encapsulation I'm sure,
    meaning it probably doesn't need knowledge of the outside world, but oh well.
    """

    def __init__(self, **kwargs):
        self.layer = kwargs.get("layer", None)
        self.moveDelta = kwargs.get("moveDelta", 1)  # distance to move when it happens
        self.xy = kwargs.get("xy", (0, 0))
        self.pos = Vector2(self.xy)
        self.color = kwargs.get("color", Colors.black)
        self.direction = Direction.up
        self.worldSize = kwargs.get("worldSize", None)
        self.size = kwargs.get("size", StarSize.small)

        if not self.worldSize:
            print("Error: stars need to know how far they can fly!!")

    def _wrap_(self):
        """Private method to ensure star wraps around game world, so our
        star field doesn't go away.
        """
        if not self.worldSize:
            return
        self.pos.x = self.pos.x % self.worldSize[0]
        self.pos.y = self.pos.y % self.worldSize[1]

        self.xy = self.pos.x, self.pos.y

    def setDirection(self, direction):
        """A normalized vector is a vector that is basically less than one
        which represents a direction, with no magnitude. But when multiplied
        with another vector can move it in a smooth fashion.
        """
        if direction.length_squared() > 0:
            self.direction = direction.normalize()

    # def change_scroll_direction(self, direction):
    #     if direction.length_squared() > 0:
    #         self.scrollDirection = direction
    #         normalizedDirection = (
    #             self.scrollDirection.normalize()
    #         )  # example direction as a unit vector
    #         self.move_delta = normalizedDirection * self.move_distance
    #         print(f"move_offset {self.move_delta}")

    def getLocation(self):
        """Returns the current location of the star"""
        return self.vector.x, self.vector.y

    def update(self, keys):
        ud = 0
        lr = 0
        changeScroll = False
        if keys[pygame.K_UP]:
            ud = -1
            changeScroll = True
        if keys[pygame.K_DOWN]:
            ud = 1
            changeScroll = True
        if keys[pygame.K_LEFT]:
            lr = -1
            changeScroll = True
        if keys[pygame.K_RIGHT]:
            lr = 1
            changeScroll = True

        if changeScroll == True:
            self.direction = Vector2(-lr, -ud)

        if event.type == pygame.KEYUP:
            ud = lr = 0

    def move(self, delta=None):
        """Moves the star based on a delta vector."""
        if isinstance(delta, Vector2):
            self.pos += self.direction * delta
        elif isinstance(delta, tuple):
            self.pos += self.direction * Vector2(delta)
        else:
            self.pos += self.direction * self.moveDelta

        self._wrap_()

        self.xy = self.pos.x, self.pos.y


class Starfield:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background = pygame.Surface((width, height)).convert()

        self.numStars = 200
        self.layers = ["close", "medium", "far"]
        self.layerRatio = [0.50, 0.85, 1]  # this is additive
        self.starColors = [Colors.pink, Colors.green, Colors.red]

        # self.stars = {"close": [], "medium": [], "far": []}
        self.stars = []

        self.scrollDirection = Direction.none
        self.move_distance = 1  # distance or speed
        self.move_delta = Direction.none

        self.generate_starfield()

    def _getLayerIndex_(self, ratio):
        for i in range(len(self.layerRatio)):
            if ratio < self.layerRatio[i]:
                return i
        return 0

    def increaseSpeed(self, factor):
        for star in self.stars:
            star.moveDelta += factor

    def decreaseSpeed(self, factor):
        for star in self.stars:
            star.moveDelta -= factor

    def _wrap_position_(self, pos):
        """not used"""
        # create a Pygame Vector2 object from the position
        pos_vec = Vector2(pos)

        # wrap the position around the screen if it moves out of bounds
        pos_vec.x = (pos_vec.x) % self.width
        pos_vec.y = (pos_vec.y) % self.height

        # return the wrapped position as a tuple
        return pos_vec.x, pos_vec.y

    def generate_starfield(self):
        # generate a random starfield
        for i in range(self.numStars):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            ratio = i / self.numStars

            print(f"ratio: {ratio}")

            layerIndex = self._getLayerIndex_(ratio)

            print(f"layer: {layerIndex}")

            if self.layers[layerIndex] == "close":
                moveDelta = 2
                starSize = StarSize.large
            elif self.layers[layerIndex] == "medium":
                moveDelta = 1.2
                starSize = StarSize.medium
            else:
                moveDelta = 1
                starSize = StarSize.small

            star = Star(
                xy=(x, y),
                color=self.starColors[layerIndex],
                moveDelta=moveDelta,
                layer=self.layers[layerIndex],
                worldSize=(self.width, self.height),
                size=starSize,
            )
            self.stars.append(star)
            self.background.set_at((x, y), star.color)
            self.drawStar((x, y), star.size, star.color)

    def drawStar(self, xy, size, color):
        self.background.set_at(xy, color)
        if size > 1:
            xy = (xy[0], xy[1] + 1)
            self.background.set_at(xy, color)
        if size > 2:
            self.background.set_at(xy, color)
            xy = (xy[0] + 1, xy[1])
            self.background.set_at(xy, color)

    def update(self, keys):
        for star in self.stars:
            star.update(keys)

    def draw(self, surface):
        # render the starfield by scrolling the stars in the opposite direction of the scroll offset

        for star in self.stars:
            star.setDirection(self.scrollDirection)
            x, y = star.xy
            # self.background.set_at((int(x), int(y)), Colors.black)
            self.drawStar((int(x), int(y)), star.size, Colors.black)
            star.move()
            x, y = star.xy
            # self.background.set_at((int(x), int(y)), star.color)
            self.drawStar((int(x), int(y)), star.size, star.color)

            surface.blit(self.background, (0, 0))


import pygame

# initialize Pygame
pygame.init()

# set up the game window
screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))


# create a Starfield object
starfield = Starfield(screen_width, screen_height)

# set up the game clock
clock = pygame.time.Clock()


granularity = 1
loops = 0


# run the game loop
while True:
    loops += 1
    # handle Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RSHIFT:
                print("increse")
                starfield.increaseSpeed(0.3)
            elif event.key == pygame.K_MINUS:
                print("decrease")
                starfield.decreaseSpeed(0.3)

    # render the starfield on the screen surface

    if loops % granularity == 0:
        screen.fill((0, 0, 0))
        starfield.update(pygame.key.get_pressed())
        starfield.draw(screen)

    loops %= 100000

    # update the screen
    pygame.display.flip()


# chat GPT test
