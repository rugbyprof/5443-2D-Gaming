"""
Sprite Sounds and Collision

Description:
    
    
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
    'images':{
        'bad_guy':{'path':'./media/collections/shoot_example/silhouette.png'},
        'green_bullet':{'path':'./media/collections/shoot_example/green_bullet.png'},
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
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
    

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

    def shoot(self,target):
        print("shooting")
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet1(self.rect.centerx, self.rect.top,target[0],target[1])
            return bullet
        return None


class Mob(pygame.sprite.Sprite):
    def __init__(self, **kwargs):

        # Initiate this sprite
        pygame.sprite.Sprite.__init__(self)

        self.game_width = config['window_size']['width']
        self.game_height = config['window_size']['height']
        self.new_size = kwargs.get('new_size',(10,15))
   

        # get location of sprites for this animation
        path = kwargs.get('path',None)
        self.center = kwargs.get('loc',(random.randint(10,self.game_width-10),random.randint(10,self.game_height-10)))

        # if not throw error
        if not path:
            print("Error: Need path of sprites!")
            sys.exit(0)


        # prime the animation
        self.image = pygame.image.load(os.path.join(path))
        self.image = pygame.transform.scale(self.image, self.new_size)
        self.rect = self.image.get_rect()
        self.rect.center = self.center 

        self.dx = 0
        self.dy = 0
        # make sure items aren't motionless
        while self.dx + self.dy == 0:
            self.dx = random.choice([-1,0,1])
            self.dy = random.choice([-1,0,1])
        self.speed = 3
        self.speed = 3

    def update(self):

        if self.rect.centerx <= 0 or self.rect.centerx >= self.game_width:
            self.dx *= -1

        if self.rect.centery <= 0 or self.rect.centery >= self.game_height:
            self.dy *= -1

        x = self.rect.centerx + (self.speed * self.dx)
        y = self.rect.centery + (self.speed * self.dy)

        self.rect.center = (x,y)


class Bullet2(pygame.sprite.Sprite):
    def __init__(self, **kwargs):

        # Initiate this sprite
        pygame.sprite.Sprite.__init__(self)

        # Project Assignment Part 4 !!


class Bullet1(pygame.sprite.Sprite):
    def __init__(self, x, y,target_x,target_y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.game_width = config['window_size']['width']
        self.game_height = config['window_size']['height']
        self.image = pygame.image.load(config['images']['green_bullet']['path'])
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = 3
        self.angle = self.CalcDirection()

    def CalcDirection(self):
        """ returns the angle in which to send the bullet
        """
        # Get the angle to move (in radians)
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        return math.atan2(dy, dx)

    def offWorld(self):
        return self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > self.game_width or self.rect.top > self.game_height

    def update(self):

        self.rect.x += int(self.speed * math.cos(self.angle))
        self.rect.y += int(self.speed * math.sin(self.angle))

        # kill if it moves off the top of the screen
        if self.offWorld():
            self.kill()


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
    mob_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()

    # help control event timing
    clock = pygame.time.Clock()

    player = Player(player_sprites=config['sprite_sheets']['pac_man_orange']['path'],loc=(random.randint(0,width),random.randint(0,height)))

    player_group.add(player)
    

    for i in range(10):
        m = Mob(path=config['images']['bad_guy']['path'],new_size=(20,30))
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
                bullet = player.shoot(pygame.mouse.get_pos())
                if bullet:
                    all_sprites.add(bullet)
                    bullets_group.add(bullet)
                    #shoot_sound.play()


        all_sprites.update()


        for item in mob_group:
            gets_hit = pygame.sprite.collide_rect(item, player)
            if gets_hit:
                item.kill()

        all_sprites.draw(screen)

        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()

if __name__=='__main__':

    main()


