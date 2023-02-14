#!/usr/bin/env python3

# Import and initialize the pygame library
import pygame
import random
from comms import CommsSender, CommsListener
import sys
import json

"""
Pygame hello world: Print a circle in middle of screen.
"""


pygame.init()

screen = pygame.display.set_mode([500, 500])

circles = []

def addCircle(**kwargs):
    red = kwargs.get('red',random.randint(0,255))
    green = kwargs.get('green',random.randint(0,255))
    blue = kwargs.get('blue',random.randint(0,255))
    m_x = kwargs.get('m_x',0)
    m_y = kwargs.get('m_y',0)
    circles.append({'red':red,'green':green,'blue':blue,'m_x':m_x,'m_y':m_y})
    return circles[-1]


def drawCircles():
    for c in circles:
        pygame.draw.circle(screen, (c['red'], c['green'], c['blue']), (c['m_x'], c['m_y']), 25)


def callBack(ch, method, properties, body):
    global game_array
    global player
    body = json.loads(body)
    # print(player)
    # print(ch)
    # print(method)
    # print(properties)
    print(body)
    addCircle(**body)

def main(player,otherplayer):


    creds = {
        "exchange": "pygame2d",
        "port": "5672",
        "host": "terrywgriffin.com",
        "user": player,
        "password": "rockpaperscissorsdonkey",
    }


    # create instances of a comms listener and sender
    # to handle message passing.
    commsListener = CommsListener(**creds)
    commsSender = CommsSender(**creds)

    # Start the comms listener to listen for incoming messages
    commsListener.threadedListen(callBack)

    # Set up the drawing window
    

    # Run until the user asks to quit
    running = True

    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                m_x, m_y = pygame.mouse.get_pos()
                circle = addCircle(m_x=m_x, m_y=m_y)
                commsSender.threadedSend(
                    otherplayer, json.dumps(circle)
            )
        # Fill the background with white
        screen.fill((255, 255, 255))

        drawCircles()


        # Flip the display
        pygame.display.flip()


    # Done! Time to quit.
    pygame.quit()



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("need player name")
        sys.exit()
    player = sys.argv[1]
    
    if player == 'player-1':
        otherPlayer = 'player-2'
    else:
        otherPlayer = 'player-1'
    main(player,otherPlayer)

