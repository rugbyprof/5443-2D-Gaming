""" Helper classes. 
    Banners generated with: http://patorjk.com/software/taag/
"""
# Import and initialize the pygame library
import pygame
import random
import json
import pprint
import sys
import os
import math
import glob

from helper_functions import *

####################################################################################
####################################################################################
#  ██████╗ ██████╗ ██╗      ██████╗ ██████╗  ██████╗██╗      █████╗ ███████╗███████╗
# ██╔════╝██╔═══██╗██║     ██╔═══██╗██╔══██╗██╔════╝██║     ██╔══██╗██╔════╝██╔════╝
# ██║     ██║   ██║██║     ██║   ██║██████╔╝██║     ██║     ███████║███████╗███████╗
# ██║     ██║   ██║██║     ██║   ██║██╔══██╗██║     ██║     ██╔══██║╚════██║╚════██║
# ╚██████╗╚██████╔╝███████╗╚██████╔╝██║  ██║╚██████╗███████╗██║  ██║███████║███████║
#  ╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝
                                                                                                                     

class Colors:
    """ Dictionary of events all kept in one place for use in other classes.
        Not sure on "best practices" or performance, but this lets me pass
        all the events to any class or function that needs em.
    """
    def __init__(self):
        pass
        
    @staticmethod
    def RGB(name):
        f = open("./resources/data/colors.json","r")
        data = json.loads(f.read())
        if name in data:
            return data[name]['rgb']
        
        return None
    @staticmethod
    def HEX(name):
        f = open("./resources/data/colors.json","r")
        data = json.loads(f.read())
        if name in data:
            return data[name]['hex']
        
        return None



#######################################################################################################################
#######################################################################################################################
# ███████╗██╗   ██╗███████╗███╗   ██╗████████╗ ██████╗ ██████╗ ███╗   ██╗████████╗ █████╗ ██╗███╗   ██╗███████╗██████╗ 
# ██╔════╝██║   ██║██╔════╝████╗  ██║╚══██╔══╝██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔══██╗██║████╗  ██║██╔════╝██╔══██╗
# █████╗  ██║   ██║█████╗  ██╔██╗ ██║   ██║   ██║     ██║   ██║██╔██╗ ██║   ██║   ███████║██║██╔██╗ ██║█████╗  ██████╔╝
# ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ██║     ██║   ██║██║╚██╗██║   ██║   ██╔══██║██║██║╚██╗██║██╔══╝  ██╔══██╗
# ███████╗ ╚████╔╝ ███████╗██║ ╚████║   ██║   ╚██████╗╚██████╔╝██║ ╚████║   ██║   ██║  ██║██║██║ ╚████║███████╗██║  ██║
# ╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
                                                                                                                     

class EventContainer:
    """ Dictionary of events all kept in one place for use in other classes.
        Not sure on "best practices" or performance, but this lets me pass
        all the events to any class or function that needs em.
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



################################################################################################################
################################################################################################################
# ██╗      ██████╗  ██████╗  ██████╗ 
# ██║     ██╔═══██╗██╔════╝ ██╔════╝ 
# ██║     ██║   ██║██║  ███╗██║  ███╗
# ██║     ██║   ██║██║   ██║██║   ██║
# ███████╗╚██████╔╝╚██████╔╝╚██████╔╝
# ╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ 

class Logg:
    """
    Simple little logger clas to help with debugging.
    Python has built in logging, so check it out if your interested.
    """
    def __init__(self):
        self.logfile = open("logger.txt","w")

    def log(self,stuff):
        self.logfile.write(stuff+"\n")



###########################################################################################################################
###########################################################################################################################
# ██████╗ ██╗      █████╗ ██╗   ██╗███████╗██████╗  █████╗ ███╗   ██╗██╗███╗   ███╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
# ██╔══██╗██║     ██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗██╔══██╗████╗  ██║██║████╗ ████║██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
# ██████╔╝██║     ███████║ ╚████╔╝ █████╗  ██████╔╝███████║██╔██╗ ██║██║██╔████╔██║███████║   ██║   ██║██║   ██║██╔██╗ ██║
# ██╔═══╝ ██║     ██╔══██║  ╚██╔╝  ██╔══╝  ██╔══██╗██╔══██║██║╚██╗██║██║██║╚██╔╝██║██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
# ██║     ███████╗██║  ██║   ██║   ███████╗██║  ██║██║  ██║██║ ╚████║██║██║ ╚═╝ ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
# ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                                                                                     

class PlayerAnimation(pygame.sprite.Sprite):
    def __init__(self, **kwargs):

        # get location of sprites for this animation
        self.path = kwargs.get('path',None)

        # if not throw error
        if not self.path:
            print("Error: Need path to location of player_sprites!")
            sys.exit(0)

        self.center = kwargs.get('loc',(0,0))
        self.speed = kwargs.get('speed',3)
        self.frame_rate = kwargs.get('frame_rate',50)
        self.dx = kwargs.get('dx',random.choice([-1,0,1]))
        self.dy = kwargs.get('dy',random.choice([-1,0,1]))

        # This function finds the json file and loads all the 
        # image names into a list
        # "./resources/graphics/characters/green_monster"
        self.animation_images = loadSpriteImages(self.path)

        # container for all the pygame images
        self.sprites = {}

        # load images and "convert" them. (see link at top for explanation)
        for anim,imglist in self.animation_images.items():
            self.sprites[anim] = []
            for img in imglist:
                self.sprites[anim].append(pygame.image.load(img))

        # animation variables
        self.animations = list(self.sprites.keys())

        self.frame = 0
        self.action = 'stationary'
        self.last_update = pygame.time.get_ticks()          
   
        # prime the animation
        self.image = self.sprites[self.action][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.center 

        self.blocked = False

        # Initiate this sprite
        pygame.sprite.Sprite.__init__(self)

    def move(self):
 
        keystate = pygame.key.get_pressed()
        self.dx = 0

        if self.gravity_on: 
            self.dy = self.gravity_force
        else:
            self.dy = 0

        if keystate[pygame.K_UP]:
            self.dy = -1

        if keystate[pygame.K_DOWN]:
            self.dy = 1

        if keystate[pygame.K_LEFT]:
            self.dx = -1

        if keystate[pygame.K_RIGHT]:
            self.dx = 1

        if keystate[pygame.K_SPACE]:
            #self.shoot()
            print("jump around")
            self.jumping = True
            self.jump()

        x = self.rect.centerx + (self.speed * self.dx)
        if self.gravity_on:
            y = self.rect.centery + (self.gravity_force * self.dy)
        else:
            y = self.rect.centery

        self.rect.center = (x,y)

    def choose_animation(self):
        """ This function assumes at least "up","down","left","right"
            but can handle two keys being pressed. 
            Possible moves:
                up
                down
                left
                right
                upleft
                upright
                downleft
                downright
            The "moves.json" file in an animation folder should have 
            moves named this way.
        """
        action = ''
        
        if self.dy == -1:
            action += 'up'

        if self.dy == 1:
            action += 'down'

        if self.dx == -1:
            action += 'left'

        if self.dx == 1:
            action += 'right'

        if action == '':
            action = 'stationary'
        return action


    def update(self):
        """ Updating players state
        """
        
        self.move() # update dx and dy

        old_action = self.action

        # use dx and dy to pick action (direction)
        self.action  = self.choose_animation()

        # if for some reason no action is chosen
        # use the "old action" to choose image with
        if self.action == '':
            self.action = old_action
            center = self.rect.center
            self.image = self.sprites[old_action][0]
            self.rect = self.image.get_rect()
            self.rect.center = center
            return

        # if we found an "action" then use it to set image
        self.image = self.sprites[self.action][self.frame]


        now = pygame.time.get_ticks()                           # get current game clock
        if now - self.last_update > self.frame_rate:            # has enough time passed to move?   
            self.last_update = now                              # if so reset the clock
            self.frame += 1                                     # get next animation frame
            if self.frame == len(self.sprites[self.action]):    # if at end goto begin ( assembly :) lol)
                self.frame = 0
            else:   
                center = self.rect.center                       # display next frame in animation
                self.image = self.sprites[self.action][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center



#######################################################################################################################
#######################################################################################################################
# ███████╗██╗███╗   ███╗██████╗ ██╗     ███████╗ █████╗ ███╗   ██╗██╗███╗   ███╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
# ██╔════╝██║████╗ ████║██╔══██╗██║     ██╔════╝██╔══██╗████╗  ██║██║████╗ ████║██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
# ███████╗██║██╔████╔██║██████╔╝██║     █████╗  ███████║██╔██╗ ██║██║██╔████╔██║███████║   ██║   ██║██║   ██║██╔██╗ ██║
# ╚════██║██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝  ██╔══██║██║╚██╗██║██║██║╚██╔╝██║██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
# ███████║██║██║ ╚═╝ ██║██║     ███████╗███████╗██║  ██║██║ ╚████║██║██║ ╚═╝ ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
# ╚══════╝╚═╝╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                                                                                     

class SimpleAnimation(pygame.sprite.Sprite):
    """ Animation:
            This class will run a basic animation for you. 
        Params:
            path <string>   : path to folder of images
            loc <tuple>     : location to place animation
            loop <bool>     : keep running animation?
    """
    def __init__(self, **kwargs):

        # Initiate this sprite
        pygame.sprite.Sprite.__init__(self)

        # get location of sprites for this animation
        path = kwargs.get('path',None)

        # if not throw error
        if not path:
            print("Error: Need location of path!")
            sys.exit(0)

        self.center = kwargs.get('loc',(0,0))

        # Does this animation keep looping?
        self.loop = kwargs.get('loop',False)

        # This function finds the json file and loads all the 
        # image names into a list
        self.images = LoadSpriteImages(path)

        # container for all the pygame images
        self.frames = []

        # load images and "convert" them. (see link at top for explanation)
        for image in self.images:
            self.frames.append(pygame.image.load(image))

        # animation variables
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50                        # smaller = faster

        # prime the animation
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.center 

    def setLocation(self,loc):
        """ Set the center of the explosion
        """
        self.center = loc
        self.rect.center = loc
    
    def update(self):
        """ Overloaded method from sprite which gets called by the game loop when 
            a sprite group gets updated
        """
        now = pygame.time.get_ticks()                   # get current game clock
        if now - self.last_update > self.frame_rate:    
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.frames):
                if not self.loop:
                    self.kill()
                else:
                    self.frame = 0
            else:
                center = self.rect.center
                self.image = self.frames[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center




if __name__=='__main__':
    c = ColorClass()

    print(c.RGB("lightgray"))
    print(c.HEX("lightgray"))


    