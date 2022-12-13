#!/usr/bin/env python3

"""
BROKEN BROKEN BROKEN BROKEN BROKEN BROKEN
"""
# Import and initialize the pygame library
import pygame
import random
import math
from rich import print

""" Example 04 - Still moving

    1) Fix the bounce so its better looking (less off screen)
    2) Starts the ball in a random location
    3) Still randomly colors the ball


"""

pygame.init()

width = 500         # width of overall screen
height = 500        # same but height
running = True      # Run until the user asks to quit
count = 0           # loop counter
x = 0
y = 0
dx = 1
dy = 1
modded = 1         # print ball when this val divides even
pace = 15            # pixels to move ball each game loop
ob_size = 10


# Set up the drawing window
screen = pygame.display.set_mode([width, height])

# some simple vector helper functions, stolen from http://stackoverflow.com/a/4114962/142637
def magnitude(v):
    print(v)
    return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))

def add(u, v):
    return [ u[i]+v[i] for i in range(len(u)) ]

def sub(u, v):
    return [ u[i]-v[i] for i in range(len(u)) ]

def dot(u, v):
    return sum(u[i]*v[i] for i in range(len(u)))

def normalize(v):
    vmag = magnitude(v)
    return [ v[i]/vmag  for i in range(len(v)) ]

class Ball(object):

    def __init__(self):
        self.x, self.y = (0, 0)
        self.speed = 2.5
        self.color = (200, 200, 200)
        self._direction = [1, 0]

    # the "real" position of the object
    @property
    def pos(self):
        return self.x, self.y

    # for drawing, we need the position as tuple of ints
    # so lets create a helper property
    @property
    def int_pos(self):
        return map(int, self.pos)

    def set_dir(self, direction):
        self._direction = normalize(direction)

    def set_dir_d(self, degrees):
        self.set_dir_r(math.radians(degrees))

    def set_dir_r(self, radians):
        self._direction = (math.cos(radians), math.sin(radians))

    def update(self):
        # apply the balls's speed to the vector
        move_vector = [c * self.speed for c in self._direction]
        # update position
        self.x, self.y = add(self.pos, move_vector)

    def draw(self):
        pygame.draw.circle(screen, self.color, self.int_pos, 4)


def moveBall(x, y, dx, dy, ob_size, pace=3):
    """
    Description: moveBall - returns coords and the direction (-dx is left and -dy is up) of the ball.
    Params:
        x  [int]        : x coordinate
        y  [int]        : y coordinate
        dx [int]        : x direction (-1 is left, 1 is right)
        dy [int]        : y direction (-1 is up, 1 is down)
        ob_size [int]   : size of object
        pace [int]      : how many spaces to move each game loop
    """

    half = int((ob_size * 1.6) / 2) # not perfect, a little guessing
                                    # with the 1.6 ...

    x = x + (pace * dx)         # add pace * direction to current x
    y = y + (pace * dy)         # add pace * direction to current y

    if y <= 0 + half:           # if y off screen top reverse direction
        dy *= -1
    elif y >= height - half:    # if y off screen bottom reverse direction
        dy *= -1

    if x <= 0 + half:           # if x off screen left reverse direction
        dx *= -1
    elif x >= height - half:    # if x off screen right reverse direction
        dx *= -1

    return (x, y, dx, dy)       # return 4 values! (Try that c++!)



red = random.randint(0, 255)
green = random.randint(0, 255)
blue = random.randint(0, 255)

x = int(width * random.random())    # faster than random.randint(low,high)
y = int(width * random.random())    # faster than random.randint(low,high)

b = Ball()

while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    b.update()
    b.set_dir(random.randint(0,360))
    b.draw()


    # Fill the background with white
    screen.fill((255, 255, 255))

    #if count % modded == 0:
    x, y, dx, dy = moveBall(x, y, dx, dy, ob_size, pace)

    #count = 0

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (red, green, blue), (x, y), ob_size)

    # Flip the display
    pygame.display.flip()

    # increment our counter
    count += 1
    pygame.time.wait(20)

# Done! Time to quit.
pygame.quit()
