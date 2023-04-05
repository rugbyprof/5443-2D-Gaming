"""
Pygame P01-005

Description:

   Moving a player with Mouse AND Keyboard also writes
   text the the game screen using a helper text class.


"""
# Import and initialize the pygame library
import pygame
import random
import json
import pprint
import sys
import os
import math

# Tells OS where to open the window
os.environ['SDL_VIDEO_WINDOW_POS'] = str(1000) + "," + str(100)

from helper_module import rgb_colors
from helper_module import mykwargs
from helper_module import straightDistance

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
    'title' :'005 Pygame Lesson',
    'window_size' : {
        'width' : 600,
        'height' : 480
    }
}

colors = rgb_colors('colors.json')

class Logg:
    def __init__(self):
        self.logfile = open("logger.txt","w")

    def log(self,stuff):
        self.logfile.write(stuff+"\n")

logg = Logg()

class TextWriter:
    def __init__(self,screen,size=32):
        self.screen = screen
        self.font = pygame.font.Font('./media/FreeSansBold.ttf', size)
        self.color = colors['black']
        self.bgcolor = colors['lightgray']
        self.blurbs = []
        self.game_width = config['window_size']['width']
        self.game_height = config['window_size']['height']
        self.locations = {
            'ul':(25,0,190,40),
            'uc':(20,0,190,40),
            'ur':(400,0,190,40)
        }

    def AddText(self,text,loc,color=None,bgcolor=None):
        if color == None:
            color = self.color
        if bgcolor == None:
            bgcolor = self.bgcolor

        loc = self.locations[loc]

        self.blurbs.append({'text':text,'loc':loc,'color':color,'bgcolor':bgcolor})

    def Write(self):

        pygame.draw.rect(self.screen, self.bgcolor, (0,0,self.game_width,40))

        for blurb in self.blurbs:

            text = self.font.render(blurb['text'], True, blurb['color'], blurb['bgcolor'])

            textRect = text.get_rect()

            textRect.left = blurb['loc'][0]

            # draw a rectangle to erase previous text. If you don't, and write
            # shorter string, some text may be left over.
            pygame.draw.rect(self.screen, self.bgcolor, blurb['loc'])
            self.screen.blit(text, textRect)


    def Remove(self,loc=None):
        if loc == None:
            self.blurbs = []


class Player:
    def __init__(self,screen,color,x,y,r):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.radius = r
        self.dx = random.choice([-1,1])
        self.dy = random.choice([-1,1])
        self.speed = 15
        self.last_direction = None
        self.target_location = None
        self.key_down = None
        self.print = TextWriter(screen,20)

    def Draw(self):
        """Draw: places a single circle on the surface.
        """
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        self.print.Write()


    def OnWorld(self):
        """ OnWorld: Returns a boolean indicating if your location is within
                     the bounds of the pygame surface
            Returns: boolean
        """
        w, h = pygame.display.get_surface().get_size()

        return self.x > 0 and self.x < w and self.y > 0 and self.y < h

    def Move(self,input):
        """ Move: Determines the type of input from the user and moves accordingly.

        """
        # If key was pressed, adjust state accordingly
        if input.events['keydown'] != None:
            self.print.AddText(f"KeyDown:{input.events['keydown']}",'ul')   # print to game window
            self.key_down = input.events['keydown']                         # save key down state
            self.target_location = None                                     # erase mouses target location

        # Mouse was clicked, adjust state accordingly
        if input.events['mouse_button_up'] != None:
            self.print.AddText(f"MouseUp:{input.events['mouse_button_up']}",'ur') # print to game window
            self.target_location = input.events['mouse_button_up']                # save target location
            self.key_down = None                                                  # erase key down

        # Now choose action to take

        # if there is a keydown, we call move with keys
        if self.key_down:
            self.print.AddText(f"MouseUp: false   ",'ur')
            self.MoveWithKeys()

        # if there is a target location,
        if self.target_location:
            self.print.AddText(f"KeyDown: false   ",'ul')
            self.MoveWithMouse()

    def MoveWithMouse(self):
        """ Moves a player toward the location of a mouse click.
        """
        x = self.target_location[0]   # get location from saved
        y = self.target_location[1]   # target

        # Get the angle to move (in radians)
        dx = x - self.x
        dy = y - self.y
        angle = math.atan2(dy, dx)

        # if we acheive the target location don't keep moving
        if straightDistance(self.x,self.y,x,y) > 10:
            self.x += int(self.speed * math.cos(angle))
            self.y += int(self.speed * math.sin(angle))


    def TelePort(self,input):
        """ Jumps "player" to a clicked location
        """
        x = input[0]
        y = input[1]

        self.x = x
        self.y = y

    def MoveWithKeys(self):
        """ Moves a player in the direction of the last pressed arrow key/

            Issues:
               Will not handle multiple keys down at once.
        """
        if self.OnWorld() or self.key_down != self.last_direction:
            if self.key_down == K_UP:
                self.y -= self.speed
                self.last_direction = K_UP
            elif self.key_down == K_DOWN:
                self.y += self.speed
                self.last_direction = K_DOWN
            elif self.key_down == K_LEFT:
                self.x -= self.speed
                self.last_direction = K_LEFT
            elif self.key_down == K_RIGHT:
                self.x += self.speed
                self.last_direction = K_RIGHT

class EventContainer:
    """ Probably not necessary, but I was trying to keep event handling organized and
        I was having issues with events cancelling or not firing (as I expected them to).

        This is basically a dictionary where an event can be stored and passed somewhere
        with every other event. Since multiple events can happen on the same game loop,
        I wanted to pass this around to wherever I needed it.
    """
    def __init__(self):
        self.events = {
            'keydown':None,
            'keyup':None,
            'mouse_motion':None,
            'mouse_button_up':None,
            'all_pressed':None
        }

    def reset(self):
        """ Set all to None
        """
        for k,v in self.events.items():
            self.events[k] = None

    def __str__(self):
        """Dump instance to screen or wherever
        """
        s = ''
        for k,v in self.events.items():
            if k == 'all_pressed':
                continue
            s += f"{k} : {v}\n"

        return s



def main():
    pygame.init()

    eventHelper = EventContainer()

    # sets the window title
    pygame.display.set_caption(config['title'])

    # set circle location
    width = config['window_size']['width']
    height = config['window_size']['height']

    # Set up the drawing window
    screen = pygame.display.set_mode((width,height))

    # construct the ball
    p1 = Player(screen,colors['rebeccapurple'],width//2,height//2,30)

    # Run until the user asks to quit
    # game loop
    running = True

    while running:
        screen.fill(colors['white'])

        # Did the user click the window close button?
        eventHelper.reset()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                eventHelper.events['keydown'] = event.key

            if event.type == pygame.KEYUP:
                eventHelper.events['keyup'] = event.key

            if event.type == pygame.MOUSEMOTION:
                eventHelper.events['mouse_motion'] = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                eventHelper.events['mouse_button_up'] = pygame.mouse.get_pos()

        eventHelper.events['all_pressed'] = pygame.key.get_pressed()

        p1.Move(eventHelper)
        p1.Draw()

        pygame.display.flip()


    # Done! Time to quit.
    pygame.quit()

if __name__=='__main__':
    #colors = fix_colors("colors.json")
    #pprint.pprint(colors)
    main()


