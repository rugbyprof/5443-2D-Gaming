"""
Pygame P01-002

Description:

   Starting a player class
   Keyboard

New Code:

    None

"""
# Import and initialize the pygame library
import pygame
import random
import json
import pprint
import sys
import os

# Tells OS where to open the window
os.environ['SDL_VIDEO_WINDOW_POS'] = str(1000) + "," + str(100)


from helper_module import load_colors
from helper_module import mykwargs


# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

config = {
    'title' :'002 Pygame Lesson',
    'window_size' : {
        'width' : 600,
        'height' : 480
    }
}

colors = load_colors('colors.json')


class Ball:
    def __init__(self,screen,color,x,y,r):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.radius = r
        self.dx = random.choice([-1,1])
        self.dy = random.choice([-1,1])
        self.speed = 15

    def Draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def Move(self):
        """ Going to change the way we move a player
        """
        pass


def main():
    pygame.init()

    # sets the window title
    pygame.display.set_caption(config['title'])

    # set circle location
    width = config['window_size']['width']
    height = config['window_size']['height']

    # Set up the drawing window
    screen = pygame.display.set_mode((width,height))

    # construct the ball
    b1 = Ball(screen,colors['rebeccapurple']['rgb'],width//2,height//2,30)

    # Run until the user asks to quit
    # game loop
    running = True
    while running:

        screen.fill(colors['white']['rgb'])

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == 2:     # type == 2 is a "keydown"
                print(event.key)    # print the value of the key pressed


        pressed_keys = pygame.key.get_pressed()

        b1.Draw()

        pygame.display.flip()


    # Done! Time to quit.
    pygame.quit()

if __name__=='__main__':
    #colors = fix_colors("colors.json")
    #pprint.pprint(colors)
    main()
