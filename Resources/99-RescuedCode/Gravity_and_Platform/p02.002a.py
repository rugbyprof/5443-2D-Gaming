"""
P01.001

Description:

    Gravity...

"""
# Import and initialize the pygame library
import pygame
import random
import os
import sys
import json

from helper_functions import loadSpriteImages
from helper_functions import loadJson

config = {
    'title' :'P02.001 ',
    'window_size' : (800,800),
    'sprite_sheets':{
        'dude':{'path':'dude_frames'}
    }
}

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
        self.velocity_current   = 15
        self.velocity_original  = 15
        self.mass               = 1
        self.jumping            = False
        self.hitbox             = (0,0,0,0)
        self.padding            = 20

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
        self.adjustHitbox()

    def advanceFrame(self):
        self.currentFrame += 1
        self.image = self.current_animation[self.currentFrame % len(self.current_animation)]
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        self.adjustHitbox()

    def adjustHitbox(self):
        self.hitbox = (self.rect.left - self.padding, self.rect.top - self.padding, self.rect.width + self.padding*2 , self.rect.height + self.padding*2)


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


    def toggleGravity(self):
        # top, left, bottom, right
        # topleft, bottomleft, topright, bottomright
        # midtop, midleft, midbottom, midright
        # center, centerx, centery
        # size, width, height
        # w,h

        if abs(self.rect.bottom - self.height) < 5:
            self.applyGravity = False
        else:
            if not self.jumping:
                self.rect.bottom = self.height


    def jump(self):
        """ jump jump ... jump around
        """
        if self.jumping: 
            # calculate force (F). F = 1 / 2 * mass * velocity ^ 2. 
            F = ((1/2) * self.mass * (self.velocity_current**2)) * .75
        
            # change in the y co-ordinate 
            self.rect.centery -= F 
            
            # decreasing velocity while going up and become negative while coming down 
            self.velocity_current = self.velocity_current-1
            print(self.velocity_current)
            
            # object reached its maximum height 
            if self.velocity_current < 0: 
                
                # negative sign is added to counter negative velocity 
                self.mass =- 1

            # objected reaches its original state 
            if self.velocity_current == -self.velocity_original-1: 

                # making isjump equal to false  
                self.jumping = False

        
                # setting original values to v and m 
                self.velocity_current = self.velocity_original
                self.mass = 1

    def handleCollision(self,platform):
        
        # if abs(self.rect.top - (platform[1] + platform[3])) < 100:
        #     print("hitting")
        #     self.jumping = False
        #     self.rect.bottom = self.height

        if abs(self.rect.bottom - platform[1]) < 100 and self.velocity_current < 0:
            print("this is stupid")
            self.jumping = False
            self.applyGravity = False
            self.rect.bottom = platform[1]
        #self.rect.bottom = ??


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

        self.toggleGravity()
        self.jump()
    

platform1 = (200,700,300,10)
img = pygame.image.load('pink_block.png')
block = pygame.sprite.Sprite()
block.image = pygame.transform.scale(img, (platform1[2], platform1[3]))
block.rect = block.image.get_rect()
block.rect.x = platform1[0]
block.rect.y = platform1[1]


def checkCollidePlatform(player):
    x1 = player.hitbox[0]
    y1 = player.hitbox[1]
    x2 = x1 + player.hitbox[2]
    y2 = y1 + player.hitbox[3]

    if abs(y2 - 700) < 50 and x2 > 200 and x1 < 500:
        return platform1





def main():
    pygame.init()


    # sets the window title
    pygame.display.set_caption(config['title'])

    # Set up the drawing window
    screen = pygame.display.set_mode(config['window_size'])

    player = Player(path=config['sprite_sheets']['dude'],loc=(config['window_size'][0]//2,config['window_size'][0]//2))

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)


    floor_group = pygame.sprite.Group()
    floor_group.add(block)


    # block = pygame.sprite.Sprite()
    # block.image = pygame.transform.scale(img, (800, 10))
    # block.rect = block.image.get_rect()
    # block.rect.x = 0
    # block.rect.y = 790
    # floor_group.add(block)

    # Run until the user asks to quit
    # Basic game loop


    running = True
    while running:

        screen.fill((0,0,0))

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()
        all_sprites.draw(screen)

        floor_group.update()
        floor_group.draw(screen)


        #collision = pygame.sprite.spritecollideany(player.hitbox, floor_group)
        collision = checkCollidePlatform(player)

        if collision:
            print("colliding")
            player.handleCollision(collision)
           


        pygame.display.flip()


    # Done! Time to quit.
    pygame.quit()

if __name__=='__main__':
    #colors = fix_colors("colors.json")
    #pprint.pprint(colors)
    main()
