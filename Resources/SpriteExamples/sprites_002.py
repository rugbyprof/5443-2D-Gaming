"""
Sprite Helper

Description:
    Loading a sprite animation and displaying it (still)
    Create multiple instances.
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


from helper_module import rgb_colors
from helper_module import mykwargs
from helper_module import straightDistance
from helper_module import getCardinalDirection

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

# Keep up with the config stuff. Adding sprite sheets for
# characters and other graphics now
config = {
    'title' :'P01.3 Pygame Sprite Movement',
    'window_size' : {
        'width' : 640,
        'height' : 480
    },
    'sprite_sheets':{
        'explosion_01':{'path':'./media/fx/explosion_01'},
        'green_monster':{'path':'./media/characters/green_monster'}
    },
    'background':'./media/backgrounds/tile_1000x1000_40_light.png',
    'fps':60
}

colors = rgb_colors('colors.json')

def  LoadSpriteImages(path):
    """ Load sprite images into either a dictionary of moves or a list of images depending
        on whether the "sprite" is a multi move character or a single effect with just frames
        to play.

        This method reads a json file looking for the following formats (right now):

    """
    if not os.path.isdir(path):
        print(f"Error: {path} not a valid sprite folder!")
        sys.exit()

    if not os.path.isfile(os.path.join(path,"moves.json")):
        print(f"Error: 'moves.json' is required to be in folder!")
        sys.exit()

    # open the json file thats expected to be in the folder
    # and read it in as a string
    f = open(os.path.join(path,"moves.json"),"r")

    # make raw string into a python dictionary 
    sprite_info = json.loads(f.read())

    # base name is used to build filename
    base_name = sprite_info['base_name']
    # ext as well
    ext = sprite_info['ext']

    # If moves is a key in the dictionary then we create a dictionary of
    # of moves where each move points to a list of images for that move
    if 'moves' in sprite_info:
        moves = {}

        for move,nums in sprite_info['moves'].items():
            images = []
            for num in nums:
                images.append(os.path.join(path,base_name+num+ext))
            moves[move] = images

        return moves
    # If frames in the dictionary, then its an effect with a list of images
    # for that effect. We need to order them before return since glob
    # doesn't get directory items in order. 
    elif 'frames' in sprite_info:
        images = sprite_info['frames']
        
        if type(images) == list:
            pass
        elif type(images) == str and images == '*':
            images = glob.glob(os.path.join(path,'*'+ext))
            images.sort()
            return images

    else:
        print(f"Error: 'moves' or 'frames' key not in json!!")
        sys.exit()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, **kwargs):

        # Initiate this sprite
        pygame.sprite.Sprite.__init__(self)

        # get location of sprites for this animation
        fx_sprites = kwargs.get('fx_sprites',None)

        # if not throw error
        if not fx_sprites:
            print("Error: Need location of fx_sprites!")
            sys.exit(0)

        self.center = kwargs.get('loc',(0,0))

        # This function finds the json file and loads all the 
        # image names into a list
        self.images = LoadSpriteImages(fx_sprites)

        # container for all the pygame images
        self.frames = []

        # load images and "convert" them. (see link at top for explanation)
        for image in self.images:
            self.frames.append(pygame.image.load(image))

        # animation variables
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 0                        # smaller = faster

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
        if now - self.last_update > self.frame_rate:    # 
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.frames):
                self.kill()
                self.frame = 0
            else:
                center = self.rect.center
                self.image = self.frames[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def main():
    pygame.init()

    # sets the window title
    pygame.display.set_caption(config['title'])

    # Game size of game window from config
    width = config['window_size']['width']
    height = config['window_size']['height']

    # Set up the drawing window
    screen = pygame.display.set_mode((width,height))

    # load our background
    background = pygame.image.load(config['background'])

    # sprite group to handle all the visuals
    all_sprites = pygame.sprite.Group()

    # help control event timing
    clock = pygame.time.Clock()

    

    # Run until the user asks to quit
    # game loop
    running = True

    while running:

        clock.tick(config['fps'])

        # fill screen with white
        screen.fill(colors['white'])

        # show background grid (no moving it)
        screen.blit(background, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                event.key

            if event.type == pygame.KEYUP:
                event.key

            if event.type == pygame.MOUSEMOTION:
                pass
                

            if event.type == pygame.MOUSEBUTTONUP:
                print(pygame.mouse.get_pos())
                e = Explosion(fx_sprites=config['sprite_sheets']['explosion_01']['path'],loc=pygame.mouse.get_pos())
                all_sprites.add(e)

        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()


    # Done! Time to quit.
    pygame.quit()

if __name__=='__main__':

    main()


