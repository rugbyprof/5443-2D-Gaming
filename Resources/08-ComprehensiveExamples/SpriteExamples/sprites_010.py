"""
Sprite Helper

Description:
    Add a mob! Make it move!
    No collisions!
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
        'green_monster':{'path':'./media/characters/green_monster'},
        'pac_man_orange':{'path':'./media/characters/pacman_ghost_orange'},
        'pac_man_red':{'path':'./media/characters/pacman_ghost_red'},
        'pac_man_pink':{'path':'./media/characters/pacman_ghost_pink'},
        'pac_man_blue':{'path':'./media/characters/pacman_ghost_blue'},
        'random':{'path':'./media/collections/pacman_items'},
    },
    'background':'./media/backgrounds/tile_1000x1000_40_light.png',
    'fps':60
}

colors = rgb_colors('colors.json')

def LoadJson(path,filetype):
    """ load a json file for whatever you need!
    """
    if not os.path.isdir(path):
        print(f"Error: {path} not a valid folder!")
        sys.exit()

    if not os.path.isfile(os.path.join(path,filetype)):
        print(f"Error: {filetype} is required to be in folder!")
        sys.exit()

    # open the json file thats expected to be in the folder
    # and read it in as a string
    f = open(os.path.join(path,filetype),"r")

    # make raw string into a python dictionary 
    data = json.loads(f.read())

    return data


def  LoadSpriteImages(path):
    """ Load sprite images into either a dictionary of moves or a list of images depending
        on whether the "sprite" is a multi move character or a single effect with just frames
        to play.

        This method reads a json file looking for the following formats (right now):

    """
    # make raw string into a python dictionary 
    sprite_info = LoadJson(path,"moves.json")

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

        pprint.pprint(self.sprites)

        # animation variables
        self.animations = list(self.sprites.keys())

        print(self.animations)

        self.gameover = False

        self.frame = 0
        self.action = 'down'
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50               
   

        # prime the animation
        self.image = self.sprites[self.action][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.center 

        self.dx = 1
        self.dy = 1
        self.speed = 3
    

    def move(self):

        keystate = pygame.key.get_pressed()
        self.dx = 0
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
            pass

        x = self.rect.centerx + (self.speed * self.dx)
        y = self.rect.centery + (self.speed * self.dy)

        self.rect.center = (x,y)

    def choose_animation(self):
        """ Returns nothing if dx and dy == 0
            But do we want to move when 0,0 ??
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

        return action

    def endlife(self):
        """ Sets class variables to end everything
        """
        self.frame_rate = 60
        self.gameover = True
        self.action = 'die'
        self.frame = 0

    def update(self):
        """ Updating players state
        """
        if not self.gameover:
            self.move() # update dx and dy

            old_action = self.action

            # use dx and dy to pick action (direction)
            self.action  = self.choose_animation()

            if self.action == '':
                self.action = old_action
                center = self.rect.center
                self.image = self.sprites[old_action][0]
                self.rect = self.image.get_rect()
                self.rect.center = center
                return

            self.image = self.sprites[self.action][self.frame]


        now = pygame.time.get_ticks()                   # get current game clock
        if now - self.last_update > self.frame_rate:    # 
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.sprites[self.action]):
                self.frame = 0
                if self.gameover:
                    self.kill()
            else:
                center = self.rect.center
                self.image = self.sprites[self.action][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Mob(pygame.sprite.Sprite):
    def __init__(self, **kwargs):

        # Initiate this sprite
        pygame.sprite.Sprite.__init__(self)

        game_width = config['window_size']['width']
        game_height = config['window_size']['height']
   

        # get location of sprites for this animation
        path = kwargs.get('path',None)
        self.center = kwargs.get('loc',(random.randint(10,game_width-10),random.randint(10,game_width-10)))

        # if not throw error
        if not path:
            print("Error: Need path of sprites!")
            sys.exit(0)

        
        collection = LoadJson(path,'items.json')

        choices = []

        for key,values in collection.items():
            print(key)
            print(values)
            L = [key] * values['weight']         
            choices.extend(L)

        random.shuffle(choices)

        key = random.choice(choices)

        item = collection[key]

        # prime the animation
        self.image = pygame.image.load(os.path.join(path,item['img']))
        self.rect = self.image.get_rect()
        self.rect.center = self.center 

        self.dx = random.choice([-1,0,1])
        self.dy = random.choice([-1,0,1])
        self.speed = 3
        self.speed = 3

    def update(self):
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

    player = Player(player_sprites=config['sprite_sheets']['pac_man_orange']['path'],loc=(random.randint(0,width),random.randint(0,height)))

    mob_group = pygame.sprite.Group()

    for i in range(50):
        m = Mob(path=config['sprite_sheets']['random']['path'])
        mob_group.add(m)
        all_sprites.add(m)

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
                player.endlife()

        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()


    # Done! Time to quit.
    pygame.quit()

if __name__=='__main__':

    main()


