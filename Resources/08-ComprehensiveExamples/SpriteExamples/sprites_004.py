"""
Sprite Helper

Description:
    Loading a sprite player and moving without animation

https://stackoverflow.com/questions/43549448/finding-the-position-of-center-using-pygame

x,y
top, left, bottom, right
topleft, bottomleft, topright, bottomright
midtop, midleft, midbottom, midright
center, centerx, centery
size, width, height
w,h
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
        'explosion_02':{'path':'./media/fx/green_blob_explosion_01'},
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
            moves[move] = []
            for num in nums:
                moves[move].append(os.path.join(path,base_name+num+ext))
        
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

class Player(pygame.sprite.Sprite):
    def __init__(self, **kwargs):

        # Initiate this sprite
        pygame.sprite.Sprite.__init__(self)

        # get location of sprites for this animation
        player_sprites = kwargs.get('player_sprites',None)

        # if not throw error
        if not player_sprites:
            print("Error: Need location of player_sprites!")
            sys.exit(0)

        self.center = kwargs.get('loc',(0,0))

        # This function finds the json file and loads all the 
        # image names into a list
        self.animation_images = LoadSpriteImages(player_sprites)

        # container for all the pygame images
        self.sprites = {}

        # load images and "convert" them. (see link at top for explanation)
        for anim,imglist in self.animation_images.items():
            self.sprites[anim] = []
           
            for img in imglist:
                self.sprites[anim].append(pygame.image.load(img))


        # animation variables
        self.moves = list(self.sprites.keys())

        print(self.moves)

        self.frame = 0
        self.move = 'down'
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50               
   

        # prime the animation
        self.image = self.sprites[self.move][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.center 

        self.dx = 1
        self.dy = 1
        self.speed = 3
    
    """
    Discuss the different methods of moving and updating x,y
    - simply adding to x and y based on key press
    - not setting dx and dy to 0
    """

    def update2(self):

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_UP]:
            self.rect.centery -= self.speed

        if keystate[pygame.K_DOWN]:
            self.rect.centery += self.speed

        if keystate[pygame.K_LEFT]:
            self.rect.centerx -= self.speed

        if keystate[pygame.K_RIGHT]:
            self.rect.centerx += self.speed

        if keystate[pygame.K_SPACE]:
            #self.shoot()
            pass

    def update(self):
        """ Not resetting dx dy to zero lets you keep moving.
            But you cannot go in cardinal directions. How do we fix.
        """
        keystate = pygame.key.get_pressed()
        # self.dx = 0
        # self.dy = 0
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
            pass

        x = self.rect.centerx + (self.speed * self.dx)
        y = self.rect.centery + (self.speed * self.dy)

        self.rect.center = (x,y)

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

    player = Player(player_sprites=config['sprite_sheets']['green_monster']['path'],loc=(random.randint(0,width),random.randint(0,height)))

    all_sprites.add(player)

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
                # if pygame.time.get_ticks() % 2 == 0:
                #     e = Explosion(fx_sprites=config['sprite_sheets']['explosion_01']['path'],loc=pygame.mouse.get_pos())
                # else:
                #     e = Explosion(fx_sprites=config['sprite_sheets']['explosion_02']['path'],loc=pygame.mouse.get_pos())
                # all_sprites.add(e)

        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()


    # Done! Time to quit.
    pygame.quit()

if __name__=='__main__':

    main()


