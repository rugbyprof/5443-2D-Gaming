"""
P01.001

Description:

    Floors.

"""
# Import and initialize the pygame library
import pygame
import random
import os
import sys
import json
import pprint

from helper_functions import loadSpriteImages
from helper_functions import loadJson

config = {
    'title' :'P02.001 ',
    'window_size' : (800,800),
    'sprite_sheets':{
        'dude':{'path':'dude_frames'}
    },
    'tile_size':10
}

platforms = {
    200:[200,600],
    300:[100,400],
    400:[400,800],
    600:[50,600],
    799:[0,800]
}


class FloorManager(object):
    """ 
    """
    def __init__(self, **kwargs):

        self.tile_size = kwargs.get('tile_size',10)

        self.platforms = kwargs.get('platforms',None)

        if self.platforms == None:
            print("Error: no platforms to generate!!")
            sys.exit()

        self.platforms = []


    def generateFloor(self):
        for row,cols in platforms.items():
            width = cols[1] - cols[0]
            startx = cols[0]
            height = self.tile_size
            img = pygame.image.load('blank_tile.png')
            block = pygame.sprite.Sprite()
            block.image = pygame.transform.scale(img, (width, height))
            block.rect = block.image.get_rect()
            block.fill((255,0,0))
            block.rect.x = startx
            block.rect.y = row
            self.platforms.append(block)

    def getPlatforms(self):
        return self.platforms
    

class SpriteLoader(object):
    """ Sprite Animation helper to really just load up a json file and turn it into pygame images.
        It has one method: get_animations which returns: 

            {
            'static': [<Surface(80x105x32 SW)>], 
            'down': [<Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>], 
            'right': [<Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>], 
            'left': [<Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>], 
            'up': [<Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>]
            }

            A dictionary of pre-loaded pygame images. I'm not sure how this would tax the system if we had a ton of assets.
    """
    def __init__(self,**kwargs):
        # get location of sprites for this animation
        self.path = kwargs.get('path',None)

        # if not throw error
        if not self.path:
            print("Error: Need path to location of player_sprites!")
            sys.exit(0)

        self.animation_images = loadSpriteImages(self.path['path'])

          # container for all the pygame images
        self.sprites = {}

        # load images and "convert" them. (see link at top for explanation)
        for anim,imglist in self.animation_images.items():
            self.sprites[anim] = []
            for img in imglist:
                self.sprites[anim].append(pygame.image.load(img))

    def get_animations(self):
        return self.sprites  


class Player(pygame.sprite.Sprite):
    """ Player class the uses an instance of SpriteLoader to load up images.
        Up to now everything is straight forward.
    """
    def __init__(self, **kwargs):

        # Initialize parent
        pygame.sprite.Sprite.__init__(self)

        # get location of sprites for this animation
        self.path = kwargs.get('path',None)

        # if not throw error
        if not self.path:
            print("Error: Need path to location of player_sprites!")
            sys.exit(0)

        self.width,self.height  = config['window_size']
        self.center             = kwargs.get('loc',(self.width//2,self.height//2))
        self.speed              = kwargs.get('speed',5)
        self.frame_rate         = kwargs.get('frame_rate',50)
        self.dx                 = kwargs.get('dx',0)
        self.dy                 = kwargs.get('dy',0)
        self.gravity            = 5
        self.applyGravity       = True
        self.jumping            = False
        self.mass_orig          = 2
        self.mass_current       = 2
        self.velocity_orig      = 10
        self.velocity_current   = 10
        self.tired              =.99

        # see comment in the SpriteLoader class to see 
        # what got loaded
        self.sprite_sheet = SpriteLoader(path=self.path)

        # animations = 'key':[list of pygame surface objects]
        self.animations = self.sprite_sheet.get_animations()

        # Holds current animation name (up down left right static)
        self.current_animation = None
        self.current_animation_name = None
        self.currentFrame = 0

        # hmmm whats this do?
        self.setAnimation('static')

        # in case we need to time some things
        self.last_update = pygame.time.get_ticks()


    def setAnimation(self,key):
        """ I turned this into a function since everytime the animation is changed I end up
            running all four of these commands. 
        """
        self.current_animation = self.animations[key]           # put animation image list into current
        self.current_animation_name = key

        self.image = self.current_animation[self.currentFrame % len(self.current_animation)]  # get a single frame to play                                                              
        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def advanceFrame(self):
        self.currentFrame += 1
        self.image = self.current_animation[self.currentFrame % len(self.current_animation)]
        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def chooseAnimation(self):     
        keystate = pygame.key.get_pressed()

        notMoving = True

        if keystate[pygame.K_UP]:
            self.setAnimation('up')
            #self.dy = -1
            notMoving = False

        if keystate[pygame.K_DOWN]:
            self.setAnimation('down')
            #self.dy = 1
            notMoving = False

        if keystate[pygame.K_LEFT]:
            self.setAnimation('left')
            self.dx = -1
            notMoving = False

        if keystate[pygame.K_RIGHT]:
            self.setAnimation('right')
            self.dx = 1
            notMoving = False

        if keystate[pygame.K_SPACE]:
            self.jumping = True

        if notMoving:
            self.setAnimation('static')
            self.dy = 0
            self.dx = 0

    def jump(self):
        """ jump jump ... jump around
        """
        if self.jumping: 
            # calculate force (F). F = 1 / 2 * mass * velocity ^ 2. 
            F = ((1/2) * self.mass_current * (self.velocity_current**2)) * self.tired
        
            # change in the y co-ordinate 
            self.rect.centery -= F 
            
            # decreasing velocity while going up and become negative while coming down 
            self.velocity_current = self.velocity_current-1
            
            # object reached its maximum height 
            if self.velocity_current<0: 
                
                # negative sign is added to counter negative velocity 
                self.mass_current =-1

            # objected reaches its original state 
            if self.velocity_current == -6: 

                # making isjump equal to false  
                self.jumping = False

                # setting original values to v and m 
                self.velocity_current = self.velocity_orig
                self.mass_current = self.mass_orig

    def checkAssertGravity(self):
        if abs(self.rect.bottom - self.height) < 5:
            self.applyGravity = False
        else:
            self.applyGravity = True

        ## Not sure if good fix 
        if self.rect.bottom > self.height:
            print("true dat")
            self.rect.bottom = self.height -2

            
    def update(self):
        """ Updating players state
        """
        now = pygame.time.get_ticks()

        if now - self.last_update > 50:
            self.advanceFrame()
            self.chooseAnimation()
            self.last_update = now

        if self.applyGravity:
            self.rect.centery += self.gravity

        self.rect.centerx += self.speed * self.dx
        self.center = (self.rect.centerx, self.rect.centery)

        self.checkAssertGravity()
        if self.jumping:
            self.jump()
    


def main():
    pygame.init()

    floor_group = None

    # sets the window title
    pygame.display.set_caption(config['title'])

    # Set up the drawing window
    screen = pygame.display.set_mode(config['window_size'])

    player = Player(path=config['sprite_sheets']['dude'],loc=(config['window_size'][0]//2,config['window_size'][0]//2))

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    floor_group = pygame.sprite.Group()


    for row,cols in platforms.items():
        width = cols[1] - cols[0]
        startx = cols[0]
        height = config['tile_size']
        img = pygame.image.load('pink_block.png')
        block = pygame.sprite.Sprite()
        block.image = pygame.transform.scale(img, (width, height))
        block.rect = block.image.get_rect()
        block.rect.x = startx
        block.rect.y = row
        floor_group.add(block)

    # floor = FloorManager(tile_size=10,platforms=platforms,group=floor_group)
    # platforms = floor.getPlatforms()

    # Run until the user asks to quit
    # Basic game loop
    running = True
    while running:

        screen.fill((0,0,0))

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if event.type == pygame.MOUSEBUTTONUP:
            print(pygame.mouse.get_pos())
            print(floor_group)


        if pygame.sprite.spritecollideany(player, floor_group):
            print("collision")

        all_sprites.update()
        all_sprites.draw(screen)

        floor_group.update()
        floor_group.draw(screen)

        pygame.display.flip()


    # Done! Time to quit.
    pygame.quit()

if __name__=='__main__':
    #colors = fix_colors("colors.json")
    #pprint.pprint(colors)
    main()


