#!/usr/bin/env python3

# Import and initialize the pygame library
import pygame
import random
import sys
import math
import os
import glob

print(os.getcwd())

print(glob.glob("*.*"))

shipsPath = "./images/ships/"

def bendTrajectory(line,coefficient=0.009,direction=1):
    """
    Params: 
        coefficient (float) : value to bend line with. Bigger means more bend.
        line (list) : list of xy coords (list of [x,y])
        direction (int) : 1 for pos -1 for 
    """
    factor = 0
    j = 1
    for i in range(0, len(line) // 2):
        line[i][1] -= factor
        line[-j][1] -= factor
        factor = factor + coefficient * (len(line) // 2 - i)
        j += 1
    
    return line


def makeLine(r=400):
    x = 450
    y = 450
    line = []
    for i in range(r):
        line.append([x,y])
        x -= 1
        y -= 1
    return line

def drawLine(line,screen,line_color,percent=1):
    stop = int(len(line) * percent)
    for i in range(stop-1):
        pygame.draw.line(screen, line_color, (line[i][0],line[i][1]), (line[i+1][0],line[i+1][1]))

if __name__=='__main__':

    pygame.init()

    line1 = makeLine()
    line2 = bendTrajectory(line1)

    clock = pygame.time.Clock()
    

 

    width = 500         # width of overall screen
    height = 500        # same but height
    running = True      # Run until the user asks to quit

    screen_color = (49, 150, 100)
    line_color = (255, 0, 0)

    # Set up the drawing window
    screen = pygame.display.set_mode([width, height])


    ship1 = pygame.image.load(os.path.join(shipsPath,"Bismarck.png")).convert_alpha()
    ship2 = pygame.image.load(os.path.join(shipsPath,"Iowa.png")).convert_alpha()

    ship1Scaled = pygame.transform.scale(ship1, (15,75))
    ship2Scaled = pygame.transform.scale(ship2, (15,75))

    ship1Scaled = pygame.transform.rotate(ship1Scaled, 125)
    ship2Scaled = pygame.transform.rotate(ship2Scaled, 125)

    # font = pygame.font.Font('./fonts/Roboto-Black.ttf', 20) 

    percent = .01


    screen.blit(ship1Scaled, ( 450,450)) # paint to screen
    screen.blit(ship2Scaled, ( 50,50)) # paint to screen
    pygame.display.flip() # paint screen one time

    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        # This also helps "clear" the screen everytime
        screen.fill((255, 255, 255))

        #drawLine(line1,screen,line_color)
        drawLine(line2,screen,line_color,percent)
        screen.blit(ship1Scaled, ( 420,420)) # paint to screen
        screen.blit(ship2Scaled, ( 25,25)) # paint to screen

        percent += 0.01

        if percent > 1:
            percent = 1

        # Flip the display
        pygame.display.flip()
        clock.tick(60)
        pygame.time.wait(30)

    # Done! Time to quit.
    pygame.quit()
