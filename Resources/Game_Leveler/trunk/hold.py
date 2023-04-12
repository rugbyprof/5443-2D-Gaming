"""
P02.004

Description:


"""
# Import and initialize the pygame library
import pygame
import pygame.freetype
import random
import os
import sys
import json
import pprint
import glob
import more_itertools 

# from helper_functions import loadSpriteImages
# from helper_functions import loadJson
# from helper_classes import Colors

from module import *

# Our typical config, but a lot smaller right now.
config = {
    'title' :'P02.001 ',
    'window_size' : (1000,500),
    'sprite_sheets':{
        'mario':{'path':'./resources/graphics/mario_frames'}
    },
    'pink_block':"./resources/graphics/pink_block.png",
    'tile_size':20,
    'debug': True,
    'debug_level':20
    }


def debug(statement,level=0):
    """ An easy way to globally turn on and off debug statements. Just change config['debug'] to False
    """
    if config['debug']:
        if level <= config['debug_level']:
            print(statement)

###############################################################################
#   _   _ _ _   ____            
#  | | | (_) |_| __ )  _____  __
#  | |_| | | __|  _ \ / _ \ \/ /
#  |  _  | | |_| |_) | (_) >  < 
#  |_| |_|_|\__|____/ \___/_/\_\
###############################################################################
class HitBox(pygame.sprite.Sprite):
    """ Helps implement a proper hitbox. Where "proper" is a negotiable term. 

    """
    def __init__(self,**kwargs):
        """
            Params:
                rect <tuple> : rectangle tuple

                or

                x <int> : x coord
                y <int> : y coord
                w <int> : width of sprite
                h <int> : height of sprite

                buffer <int> : padding around sprite

                or 

                buffer <tuple> : (left_buffer,top_buffer,right_buffer,bottom_buffer)
        """
        pygame.sprite.Sprite.__init__(self)

        # Get game window size to help with calculations
        self.game_width,self.game_height = config['window_size']
    

        # Get a rect if exists
        self.rect = kwargs.get('rect',None)

        # Otherwise we need all 4 of these 
        self.x = kwargs.get('x',0)
        self.y = kwargs.get('y',0)
        self.w = kwargs.get('w',0)
        self.h = kwargs.get('h',0)

        # buffer defaults to 10px
        self.buffer = kwargs.get('buffer',10)

        # choose which params to build hitbox with
        if not self.rect == None:
            self.box = self.adjustHitBox()
        elif x and y and w and h:
            self.box = self.adjustHitBox()
        else:
            print("Error: Hitbox needs either a rect(x,y,w,h) or all 4 params seperate.")

    def adjustHitBox(self):
        """ This takes the sprite params and widens the hitbox accordingly. You can 
            set each side of the hitbox seperately depending on circumstances. Just pass
            in a buffer tuple like (l,t,r,b) or left, top, right, bottom (clockwise).
            The buffer is passed into the constructor or to the `resetHitBox` method.
                        +--------------+
                        |       t      |
                        |     +---+    |
                        |  l  |   | r  |
                        |     +---+    |
                        |       b      |
                        +--------------+

            The bottom buffer is a little odd in a platformer since we are mostly on the ground. So I
            would recommend setting it to zero.

            Params:
                None
            Returns:
                None
        """

        # if we have a rect passed in the constructor
        if not self.rect == None:
            x,y,w,h = self.rect
        else:
            # get individual values from constructor
            x = self.x
            y = self.y
            w = self.w
            h = self.h

        # if self.buffer is a single integer value add that 
        # to every side of the rectangle
        if type(self.buffer) == int:
            x = x - self.buffer
            y = y - self.buffer
            w = w + 2*self.buffer
            h = h + self.buffer
        else:
            # use the exlicit values in the tuple
            x = x - self.buffer[0]                      # left buffer
            y = y - self.buffer[1]                      # top
            w = w + self.buffer[0] + self.buffer[2]     # width adds left + right buffers
            h = h + self.buffer[1] + self.buffer[3]     # height adds bottom and top

        # adjust if off left screen
        if x < 0:
            x = 0

        # same for top
        if y < 0:
            y = 0

        # same for right
        if x + w > self.game_width:
            w = self.game_width - x

        # same for bottom
        if y + h > self.game_height:
            h = self.game_height - y

        # create a new sprite (so we can use built in collision detection)
        self.image = pygame.Surface([w, h])
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def resetHitBox(self,buffer):
        """ resets the bit box to a different buffer size
            Params:
                buffer <tuple> : (left,top,right,bottom)
            Returns:
                None
        """
        self.buffer = buffer
        self.box = self.adjustHitBox()

class PlayerAction(object):
    def __init__(self):
        self.actions = {}
        self.actions['walking'] = False
        self.actions['jumping']  = False
        self.actions['standing']  = False
        self.actions['falling']  = False
        self.actions['grounded']  = False

    def clear(self):
        for action in self.actions:
            self.actions[action] = False
    
    def setAction(self,action):
        self.clear()
        self.actions[action] = True

    def getAction(self):
        for action in self.actions:
            if self.actions[action]:
                return action
        return None


###############################################################################
#   ____  _                       
#  |  _ \| | __ _ _   _  ___ _ __ 
#  | |_) | |/ _` | | | |/ _ \ '__|
#  |  __/| | (_| | |_| |  __/ |   
#  |_|   |_|\__,_|\__, |\___|_|   
#                 |___/          
###############################################################################
class Player(pygame.sprite.Sprite):
    """ Player class that represents our platform player. It has the following methods:

        adjustRect(key,value):
            Used to update player location AND it's hitbox. See method for better explanation
        advanceFrame():
            Get the next animation frame for the sprite
        applyGravity():
            A one line function to add to the y coord of the sprite. I made it a function because
            I think future version may have a more complex way of applying gravity.
        chooseAnimation():
            Chooses proper animation based on which keys are pressed and what state the sprite is in.
            Pretty basic right now, but again, I'm looking into the future ... into the year .... 2000! (sorry Conan Obrian joke)
        handlePlatformCollision(platform):
            Game loop sends platorm reference on collision. This method decides what to do. Basically adjusts player position
            based on current state.
        jump():
            You guess.
        movePlayer():
            Based on current state and player location, this method actually updates player position.
        setAnimation(key):
            Choose animation by key (e.g. up, down, left, right)
            This version we only walk up down left right, but future could have: duck, jump, shoot , etc. etc. etc. 
        update()
            The overloaded update method that gets called by the game loop. It does control how fast things happen
            based on the pygame clock. 
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

        self.game_width,self.game_height  = config['window_size']
        self.center             = kwargs.get('loc',(self.game_width//2,self.game_height//2))
        self.speed              = kwargs.get('speed',5)
        self.frame_rate         = kwargs.get('frame_rate',50)
        self.dx                 = kwargs.get('dx',0)
        self.dy                 = kwargs.get('dy',0)
        self.resize             = kwargs.get('resize',None)
        self.gravity_current    = 5
        self.gravity_orig       = 5
        self.jumping            = False
        self.jumpCount          = 0
        self.mass_orig          = 2
        self.mass_current       = 2
        self.velocity_orig      = 8
        self.velocity_current   = 8
        self.tired              =.99
        self.current_platform   = None
        self.hitBox = None
        

        # see comment in the SpriteLoader class to see 
        # what got loaded
        self.sprite_sheet = SpriteLoader(path=self.path,resize=self.resize)

        # animations = 'key':[list of pygame surface objects]
        self.animations = self.sprite_sheet.get_animations()

        # Holds current animation name (up down left right static)
        self.player_direction = 'right'
        self.last_animation = 'standing'
        self.current_animation = 'standing'
        self.current_animation_name = 'standing'
        self.current_frame = 0
        self.animation_loops = 0    # how many times did animation play

        self.action = PlayerAction()

        self.action.setAction('standing')

        # hmmm whats this do?
        self.setAnimation('standing')

        # in case we need to time some things
        self.last_update = pygame.time.get_ticks()

    def adjustRect(self,key,value):
        """ This method adjusts the "hitbox" in conjunction with 
            the players image.rect 
        """ 
        setattr(self.rect, key, value)
        setattr(self.hitBox.rect, key, value)

    def advanceFrame(self,frame_num=-1):
        """ Get the next frame in the list and update the "rectangle"
            Params:
                frame_num <int> : passing in an int sets the frame to that number
        """
        # if frame_num >= 0:
        #     print(f"resetting animaition: {frame_num}")
        #     self.current_frame = frame_num
        #     self.animation_loops = 0
        # else:
        #     self.current_frame += 1
        
        self.current_frame += 1
        
        self.animation_loops = int(self.current_frame/len(self.current_animation))

        index = self.current_frame % len(self.current_animation)
        self.image = self.current_animation[index]
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        self.hitBox = HitBox(rect = self.rect)

    def applyGravity(self):
        """ Add our current gravity to the players y coord.
            Does this need to be a function? Not sure. 
            I was thinking that future versions could have some weird variations...
        """
        self.adjustRect('centery',self.rect.centery + self.gravity_current)

    def chooseAnimation(self):
        """ This a "move" and "animation" method. Based on which keys are pressed
            choose an animation and update player state.
        """

        # get current pygame clock val
        now = pygame.time.get_ticks()

        # get key pressed :)
        keystate = pygame.key.get_pressed()


        if sum(keystate) == 0 and not self.action.getAction() in ['falling','jumping']:
            self.action.setAction('standing')

        if keystate[pygame.K_LEFT]:
            self.player_direction='left'
            self.setAnimation('walk_01')
            self.dx = -1
            self.action.setAction('walking')

        if keystate[pygame.K_RIGHT]:
            self.player_direction='right'
            self.setAnimation('walk_01')
            self.dx = 1
            self.action.setAction('walking')

        # if keystate[pygame.K_x]:
        #     self.setAnimation('bball_hammer')
        #     notMoving = False

        if keystate[pygame.K_SPACE]:
            self.setAnimation('jumping_up')
            self.last_update = now
            self.jumping = True
            self.action.setAction('jumping')
            debug("state: jumping",10)

        if self.action.getAction() == 'jumping':
            self.setAnimation('jumping_up')
            debug("jumping",10)

        if self.action.getAction() == 'falling':
            self.setAnimation('dropping')
            debug("dropping",10)

        if self.action.getAction() == 'walking':
            self.setAnimation('walk_01')
            debug("walking",10)
            
        if self.action.getAction() in ['standing']:
            self.setAnimation('standing')
            debug("standing",10)
            self.dy = 0
            self.dx = 0


    def handlePlatformCollision(self,platform):
        """ Did we contact a platform?
            Parameters:
                platform <pygame.sprite> : a platform sprite with a rectangle info
        """

        # If were on some ground, adjust our feet to be at proper height
        if self.action.getAction() in ['walking','standing']:
            self.adjustRect('bottom',platform.rect.top)

        # If we are jumping, adjust our top to the platforms bottom because
        # we hit the bottom of a platform! Don't go through it!
        if self.action.getAction() in ['jumping']:
            self.adjustRect('top',platform.rect.bottom)


        # If we are falling put our feet on the platform we hit.
        # set our new floor to the current platform and some
        # other stuff ... 
        if self.action.getAction() in ['falling']:
            self.adjustRect('bottom',platform.rect.top) # adjust rect and hitbox
            self.current_platform = platform
            self.action.setAction('walking')
            debug("falling to standing",10)

    def jump(self):
        """ jump jump ... jump around
        """
        # If we triggered the jump variable
        if self.jumping:
            
            # calculate force (F). F = 1 / 2 * mass * velocity ^ 2. 
            F = ((1/2) * self.mass_current * (self.velocity_current**2)) * self.tired
        
            # change in the y co-ordinate 
            #self.rect.centery -= F 
            self.adjustRect('centery',self.rect.centery - F)
            
            # decreasing velocity while going up and become negative while coming down 
            self.velocity_current = self.velocity_current-1
            
            # object reached its maximum height 
            if self.velocity_current<0: 
                self.action.setAction('falling')
                debug("state: falling",10)
                self.jumping = False
                self.velocity_current = self.velocity_orig
                self.mass_current = self.mass_orig
                self.gravity_current = 10

    def movePlayer(self):
        """ First checks to see what "state" its in to apply certain things (like gravity) and 
            then it actually adjusts the players "rectangle" on the game screen by moving its
            center left and right. 
        """

        # if jumping is true run jump function
        if self.jumping:
            self.jump()

        # if player falling, then apply gravity to move player down
        if self.action.getAction() == 'falling' or not self.current_platform:
            self.applyGravity()

        # move player as long as its on the world
        if self.rect.right <= self.game_width and self.rect.left >= 0:
            # Adjust players rect and hiboxes rectangle
            self.adjustRect('centerx',self.rect.centerx + self.speed * self.dx)

            # Comment this out and see what happens
            self.center = (self.rect.centerx, self.rect.centery)
        
        # If your on the edge, you could get stuck. So I made it 
        # so you always get pushed away by one pixel.
        if self.rect.left <= 0:
            self.rect.left = 1
        if self.rect.right >= self.game_width:
            self.rect.right = self.game_width - 1

        # Our current "floor" or "ground"
        if self.current_platform:
            debug("current platform",10)
            # if we go off the left edge ... fall
            if self.rect.right < self.current_platform.rect.left:
                self.action.setAction('falling')

            # same on other side
            if self.rect.left > self.current_platform.rect.right:
                self.action.setAction('falling')


    def setAnimation(self,key):
        """ I turned this into a function since everytime the animation is changed I end up
            running all of these commands. 
        """

        key = key+"_"+self.player_direction

        # it setting animation to what were doing already, just return
        if self.last_animation == key:
            return

        self.last_animation = self.current_animation_name
        self.current_animation = self.animations[key]           # put animation image list into current
        self.current_animation_name = key

        # calling advanceframe with a value sets
        # the frame to that value. So this resets
        # an animation to beginning
        self.advanceFrame(0)



    def update(self):
        """ Updating players state
        """
        now = pygame.time.get_ticks()   

        # This keeps the animation at a little slower speed
        # than the rest of the game. Set 50 to 0 and see the difference.
        if now - self.last_update > 100:
            self.advanceFrame()
            self.chooseAnimation()
            self.last_update = now

        self.movePlayer()

###############################################################################
#   ____             _ _       _                    _           
#  / ___| _ __  _ __(_) |_ ___| |    ___   __ _  __| | ___ _ __ 
#  \___ \| '_ \| '__| | __/ _ \ |   / _ \ / _` |/ _` |/ _ \ '__|
#   ___) | |_) | |  | | ||  __/ |__| (_) | (_| | (_| |  __/ |   
#  |____/| .__/|_|  |_|\__\___|_____\___/ \__,_|\__,_|\___|_|   
#        |_|                                                   
###############################################################################
class SpriteLoader(object):
    """ Sprite Animation helper to really just load up a json file and turn it into pygame images.
        It has one method: get_animations which returns a dictionary of pre-loaded pygame images: 

            {
            'static': [<Surface(80x105x32 SW)>], 
            'down': [<Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>], 
            'right': [<Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>], 
            'left': [<Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>], 
            'up': [<Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>, <Surface(80x105x32 SW)>]
            }

             I'm not sure how this would tax the system if we had a ton of assets, but oh well. 

    """
    def __init__(self,**kwargs):
        """
        Params:
            path <string> : Path to your sprite images
            size <tuple>  : New size for your sprite frames - (new_width,new_height)
        """
        # get location of sprites for this animation
        self.path = kwargs.get('path',None)

        # if not throw error
        if not self.path:
            print("Error: Need path to location of player_sprites!")
            sys.exit(0)

        # Load the images for our sprite
        self.animation_images = self.loadSpriteImages(self.path['path'])

        # get a new size if one is passed in
        self.resize = kwargs.get("resize",None)
        if self.resize != None:
            resize_width,resize_height = kwargs.get("resize",None)

        # container for all the pygame images
        self.sprites = {}

        # load images and "convert" them. (see link at top for explanation)
        for anim,imginfo in self.animation_images.items():

            self.sprites[anim] = []
            for img in imginfo:
                for img in imginfo['frames']:
                    # no size passed in, so just create sprites
                    if self.resize == None:
                        self.sprites[anim].append(pygame.image.load(img))
                    else:
                        img_w = imginfo['frame_width']
                        img_h = imginfo['frame_height']

                        resize_factor = resize_height / img_h 
                       
                        img_h = int(resize_height)
                        img_w = int(imginfo['frame_width'] * resize_factor)

                        # load a resize image by scaling them
                        im = pygame.image.load(img)
                        frame = pygame.sprite.Sprite()
                        frame.image = pygame.transform.scale(im, (img_w, img_h))
                        self.sprites[anim].append(frame.image)


    def loadSpriteImages(self,path):
        # make raw string into a python dictionary 
        sprite_info = loadJson(os.path.join(path,"moves.json"))

        # base name is used to build filename
        base_name = sprite_info['base_name']

        # ext as well
        ext = sprite_info['ext']

        # If moves is a key in the dictionary then we create a dictionary of
        # of moves where each move points to a list of images for that move
        if 'moves' in sprite_info:
            moves = {}

            for move,info in sprite_info['moves'].items():
                moves[move] = info
                temp = []
                for im in moves[move]['frames']:
                    temp.append(os.path.join(path,base_name+im+ext))
                moves[move]['frames'] = temp

            return moves

    def get_animations(self):
        """ returns the dictionary of animations
        """
        return self.sprites  


class LevelLoader(object):
    def __init__(self,**kwargs):
        

        self.tiles_path = kwargs.get('tiles_path',None)
        if self.tiles_path == None:
            print(f"Error: No path to the tile set!!")
            sys.exit()

        if not os.path.isdir(self.tiles_path):
            print(f"Error: {self.tiles_path} is not a directory!")
            sys.exit()

        self.levels_path= kwargs.get('levels_path',None)
        self.level_name = kwargs.get('level_name',None)
        self.tile_size = kwargs.get('tile_size',None)

        if self.tile_size != None:
            if type(self.tile_size) == int:
                self.tile_size = (self.tile_size,self.tile_size)

        self.tiles = []
        self.tile_sprites = []

        if self.tiles_path != None:
            self.loadTiles()

        if self.level_name != None:
            self.loadLevel()

        
    def loadTiles(self):
        self.tiles = glob.glob(os.path.join(self.tiles_path,"*.png"))
        self.tiles.sort()


    def getSurfaceCoords(self,x,y):
        pass

    def loadLevel(self,level_name=None,levels_path=None):
        if levels_path is None and self.levels_path is None:
            print(f"Error: Need a directory to read levels from!")
            sys.exit()

        if levels_path != None:
            self.levels_path = levels_path

        with open(os.path.join(self.levels_path,self.level_name),"r") as f:
            data = f.readlines()

        row = 0
        col = 0
        for line in data:
            line = line.strip()
            for code in more_itertools.chunked(line, 2):
                tilenum = code[0]+code[1]
                if tilenum != "..":
                    tile_loc = os.path.join(self.tiles_path,tilenum+".png")
                    print(tile_loc)
                    if os.path.isfile(tile_loc):
                        img = pygame.image.load(tile_loc)
                        tile = pygame.sprite.Sprite()
                        tile.image = pygame.transform.scale(img, (self.tile_size[0], self.tile_size[0]))
                        tile.rect = tile.image.get_rect()
                        print(row,col)
                        tile.rect.x = col * self.tile_size[0]
                        tile.rect.y = row * self.tile_size[1]
                        self.tile_sprites.append(tile)
                col += 1
            col = 0
            row += 1

    def getTileSprites(self):
        return self.tile_sprites


#https://gist.github.com/programmingpixels/27b7f8f59ec53b401183c68f4be1634b#file-step4-py

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

class UIElement(pygame.sprite.Sprite):
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
            action - the gamestate change associated with this button
        """
        self.mouse_over = False

        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]

        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """ Updates the mouse_over variable and returns the button's
            action value when clicked.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)

class Scene(object):
    def __init__(self):
        pass

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError

def title_screen(screen):
    start_btn = UIElement(
        center_position =(400, 400),
        font_size       =30,
        bg_rgb          =Colors.RGB('mediumorchid'),
        text_rgb        =Colors.RGB('white'),
        text            ="Start",
        action          ="newGame"
    )

    quit_btn = UIElement(
        center_position =   (400, 500),
        font_size       =   30,
        bg_rgb          =   Colors.RGB('mediumorchid'),
        text_rgb        =   Colors.RGB('white'),
        text            =   "Quit",
        action          =   "quitGame"
    )

    buttons = [start_btn, quit_btn]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(Colors.RGB("navy"))

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()

###############################################################################
#   _ __ ___   __ _(_)_ __  
#  | '_ ` _ \ / _` | | '_ \ 
#  | | | | | | (_| | | | | |
#  |_| |_| |_|\__,_|_|_| |_|
###############################################################################          
def main():
    pygame.init()

    # sets the window title
    pygame.display.set_caption(config['title'])

    # Set up the drawing window
    screen = pygame.display.set_mode(config['window_size'])

    player = Player(path=config['sprite_sheets']['mario'],loc=(30,500-25),resize=(50,62))

    # Sprite groups is the easiest way to update and draw many sprites
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()

    # Add player to all sprites
    all_sprites.add(player)

    levels = []
    levels.append(LevelLoader(levels_path="./resources/levels",tiles_path="./resources/maps/forest_clean/Tiles_20",level_name="level_01",tile_size=(20,20)))
    levels.append(LevelLoader(levels_path="./resources/levels",tiles_path="./resources/maps/forest_clean/Tiles_20",level_name="level_02",tile_size=(20,20)))
    levels.append(LevelLoader(levels_path="./resources/levels",tiles_path="./resources/maps/forest_clean/Tiles_20",level_name="level_03",tile_size=(20,20)))

    tile_sprites = levels[1].getTileSprites()

    for tile in tile_sprites:
        tiles_group.add(tile)
        all_sprites.add(tile)

    title = title_screen(screen)

    # Run until the user asks to quit
    # Basic game loop
    running = True
    while running:

        screen.fill((0,0,0))

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Not used in this instance of our game
        if event.type == pygame.MOUSEBUTTONUP:
            debug(pygame.mouse.get_pos(),10)

        # check for collisions using our tiles_group and players hitbox
        platform_collision = pygame.sprite.spritecollide(player.hitBox, tiles_group, False)
        
        # if player collides with platform, tell the player class
        if platform_collision:
            player.handlePlatformCollision(platform_collision[0])
        
        # print out hitbox and bounding rectangle of player
        if config['debug']:
            pygame.draw.rect(screen,(255,0,0),player.rect,1)
            pygame.draw.rect(screen,(0,255,0),player.hitBox.rect,1)

        # These methods will call the "update" method for every sprite that needs it. For example, if 
        # our platforms "moved", then we would need to put an update method in a platform class to 
        # handle it. Right now, they're sprites, but just sit there.
        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()


    # Done! Time to quit.
    player.state.dumpHistory()
    pygame.quit()

if __name__=='__main__':

    main()


