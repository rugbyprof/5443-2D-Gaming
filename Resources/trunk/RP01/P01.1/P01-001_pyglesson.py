"""
Pygame P01-001

Description:

   Starting a player class

New Code:

    None

"""
# Import and initialize the pygame library
import pygame
import random
import json
import pprint
import sys

from helper_module import load_colors
from helper_module import mykwargs


config = {
    'title' :'001 Pygame Lesson',
    'window_size' : (500,500)
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
        """This move method moves the "player" in the x and y direction changing direction
           when wall contact is detected (collision)
        """
        w, h = pygame.display.get_surface().get_size()

        self.x += (self.speed * self.dx)
        self.y += (self.speed * self.dy)

        half = self.radius

        if self.x  <= half or self.x + half >= w:
            self.dx *= -1

        if self.y  <= half or self.y + half >= h:
            self.dy *= -1


def main():
    pygame.init()

    # sets the window title
    pygame.display.set_caption(config['title'])

    # Set up the drawing window
    screen = pygame.display.set_mode(config['window_size'])

    # set circle location
    x = 20
    y = 250

    # construct the ball
    b1 = Ball(screen,colors['rebeccapurple']['rgb'],x,y,30)

    # Run until the user asks to quit
    # game loop
    running = True
    while running:

        screen.fill(colors['white']['rgb'])

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        b1.Draw()
        b1.Move()


        pygame.display.flip()


    # Done! Time to quit.
    pygame.quit()

if __name__=='__main__':
    #colors = fix_colors("colors.json")
    #pprint.pprint(colors)
    main()
