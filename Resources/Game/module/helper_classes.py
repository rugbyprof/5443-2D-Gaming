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

try :
    from .helper_functions import *
except ImportError as e:
    from helper_functions import *
    import helper_functions


####################################################################################
####################################################################################
#    ____      _                
#   / ___|___ | | ___  _ __ ___ 
#  | |   / _ \| |/ _ \| '__/ __|
#  | |__| (_) | | (_) | |  \__ \
#   \____\___/|_|\___/|_|  |___/
                              
                                                                                                                     

class Colors:
    """ Dictionary of events all kept in one place for use in other classes.
        Not sure on "best practices" or performance, but this lets me pass
        all the events to any class or function that needs em.
    """
    def __init__(self):
        pass
        
    @staticmethod
    def RGB(name):
        if 'module' in os.getcwd():
            path = 'colors.json'
        else:
            path = "./resources/data/colors.json"
        f = open(path,"r")
        data = json.loads(f.read())
        if name in data:
            return data[name]['rgb']
        
        return None
    @staticmethod
    def HEX(name):
        if 'module' in os.getcwd():
            path = 'colors.json'
        else:
            path = "./resources/data/colors.json"
        f = open(path,"r")
        data = json.loads(f.read())
        if name in data:
            return data[name]['hex']
        
        return None



#######################################################################################################################
#######################################################################################################################
#   ____                                    ____             
#  |  _ \ _ __ ___   __ _ _ __ ___  ___ ___| __ )  __ _ _ __ 
#  | |_) | '__/ _ \ / _` | '__/ _ \/ __/ __|  _ \ / _` | '__|
#  |  __/| | | (_) | (_| | | |  __/\__ \__ \ |_) | (_| | |   
#  |_|   |_|  \___/ \__, |_|  \___||___/___/____/ \__,_|_|   
#                   |___/                                    

class ProgressBar(object):
    """
        barPos      = (120, 360)
        barSize     = (200, 20)
        borderColor = (0, 0, 0)
        barColor    = (0, 128, 0)
    """
    def __init__(self,**kwargs):
        pos             = kwargs.get("pos",(0,0))
        size            = kwargs.get("size",(0,0))
        border_color    = kwargs.get("border_color",Colors.RGB("black"))
        bar_color       = kwargs.get("bar_color",Colors.RGB("green"))
        progress        = kwargs.get("progress",0.0)
        max_items       = kwargs.get("max_items",100)

    def drawBar(self):
        pygame.draw.rect(screen, borderC, (*pos, *size), 1)
        innerPos  = (pos[0]+3, pos[1]+3)
        innerSize = ((size[0]-6) * progress, size[1]-6)
        pygame.draw.rect(screen, barC, (*innerPos, *innerSize))


#######################################################################################################################
#######################################################################################################################
#   _____                 _    ____            _        _                 
#  | ____|_   _____ _ __ | |_ / ___|___  _ __ | |_ __ _(_)_ __   ___ _ __ 
#  |  _| \ \ / / _ \ '_ \| __| |   / _ \| '_ \| __/ _` | | '_ \ / _ \ '__|
#  | |___ \ V /  __/ | | | |_| |__| (_) | | | | || (_| | | | | |  __/ |   
#  |_____| \_/ \___|_| |_|\__|\____\___/|_| |_|\__\__,_|_|_| |_|\___|_|   
                                                                       
                                                                                                                     

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
        game_window = kwargs.get('game_window',None)

        if not game_window:
            print("Error: need game window size for a hitbox")
            sys.exit()


        self.game_width,self.game_height = game_window 


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

################################################################################################################
################################################################################################################
#   _                      
#  | |    ___   __ _  __ _ 
#  | |   / _ \ / _` |/ _` |
#  | |__| (_) | (_| | (_| |
#  |_____\___/ \__, |\__, |
#              |___/ |___/ 

class Logg:
    """
    Simple little logger clas to help with debugging.
    Python has built in logging, so check it out if your interested.
    """
    def __init__(self):
        self.logfile = open("logger.txt","w")

    def log(self,stuff):
        self.logfile.write(stuff+"\n")


class MouseClickRect(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,y,1,1)




###########################################################################################################################
###########################################################################################################################
#   ____  _                        _          _                 _   _             
#  |  _ \| | __ _ _   _  ___ _ __ / \   _ __ (_)_ __ ___   __ _| |_(_) ___  _ __  
#  | |_) | |/ _` | | | |/ _ \ '__/ _ \ | '_ \| | '_ ` _ \ / _` | __| |/ _ \| '_ \ 
#  |  __/| | (_| | |_| |  __/ | / ___ \| | | | | | | | | | (_| | |_| | (_) | | | |
#  |_|   |_|\__,_|\__, |\___|_|/_/   \_\_| |_|_|_| |_| |_|\__,_|\__|_|\___/|_| |_|
#                 |___/                                                           
                                                                                                                     

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
#   ____  _                 _         _          _                 _   _             
#  / ___|(_)_ __ ___  _ __ | | ___   / \   _ __ (_)_ __ ___   __ _| |_(_) ___  _ __  
#  \___ \| | '_ ` _ \| '_ \| |/ _ \ / _ \ | '_ \| | '_ ` _ \ / _` | __| |/ _ \| '_ \ 
#   ___) | | | | | | | |_) | |  __// ___ \| | | | | | | | | | (_| | |_| | (_) | | | |
#  |____/|_|_| |_| |_| .__/|_|\___/_/   \_\_| |_|_|_| |_| |_|\__,_|\__|_|\___/|_| |_|
#                    |_|                                                             
                                                                                                                     
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
        self.images = loadSpriteImages(path)

        # container for all the pygame images
        self.frames = []

        print(self.images)

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

#######################################################################################################
#######################################################################################################
#   ____                  
#  | __ )  ___  _ __ __ _ 
#  |  _ \ / _ \| '__/ _` |
#  | |_) | (_) | | | (_| |
#  |____/ \___/|_|  \__, |
#                   |___/ 
class Borg:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state


#######################################################################################################
#######################################################################################################
#   ____  _        _       
#  / ___|| |_ __ _| |_ ___ 
#  \___ \| __/ _` | __/ _ \
#   ___) | || (_| | ||  __/
#  |____/ \__\__,_|\__\___|
                         
class State(object):
    def __init__(self):
        pass

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError


#######################################################################################################
#######################################################################################################
#   ____  _        _       __  __                                         
#  / ___|| |_ __ _| |_ ___|  \/  | __ _ _ __   __ _ _ __   __ _  ___ _ __ 
#  \___ \| __/ _` | __/ _ \ |\/| |/ _` | '_ \ / _` | '_ \ / _` |/ _ \ '__|
#   ___) | || (_| | ||  __/ |  | | (_| | | | | (_| | | | | (_| |  __/ |   
#  |____/ \__\__,_|\__\___|_|  |_|\__,_|_| |_|\__,_|_| |_|\__, |\___|_|   
#                                                         |___/           
class StateManager(Borg):
    """ StateManager lets you add different levels or screens to a pygame
    """
    def __init__(self):
        self.index = -1
        self.states = []

    def addState(self,state):
        self.states.append(state)

    def next(self):
        self.index = (self.index + 1) % len(self.states)
        self.state = self.states[self.index]
        self.state.manager = self

        


#######################################################################################################
#######################################################################################################
#   _                   _ _                    _           
#  | |    _____   _____| | |    ___   __ _  __| | ___ _ __ 
#  | |   / _ \ \ / / _ \ | |   / _ \ / _` |/ _` |/ _ \ '__|
#  | |__|  __/\ V /  __/ | |__| (_) | (_| | (_| |  __/ |   
#  |_____\___| \_/ \___|_|_____\___/ \__,_|\__,_|\___|_|   
                                                         
class LevelLoader(State):

    def __init__(self,**kwargs):
        super(State, self).__init__()

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

        self.tiles_group = pygame.sprite.Group()

        if self.tiles_path != None:
            self.loadTiles()

        if self.level_name != None:
            self.loadLevel()

        
    def loadTiles(self):
        self.tiles = glob.glob(os.path.join(self.tiles_path,"*.png"))
        self.tiles.sort()


    def loadLevel(self,level_name=None,levels_path=None):
        if levels_path is None and self.levels_path is None:
            print(f"Error: Need a directory to read levels from!")
            sys.exit()

        if levels_path != None:
            self.levels_path = levels_path

        with open(os.path.join(self.levels_path,self.level_name),"r") as f:
            data = f.readlines()

        row = 0         # which row on the screen
        col = 0         # which col on the screen
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
                        tile.rect.x = col * self.tile_size[0]   # set pygame screen position
                        tile.rect.y = row * self.tile_size[1]
                        self.tile_sprites.append(tile)
                        self.tiles_group.add(tile)
                col += 1
            col = 0
            row += 1

    def render(self, screen):
        self.tiles_group.update()
        self.tiles_group.draw(screen)

    def update(self):
        pass

    def handle_events(self,events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONUP:
                self.manager.go_to()


class TypedText(object):
    """
    Usage:
        Define Some Text: 
            textTyper = TypedText(font_color=Colors.RGB('gold'),font_size=200,font_path='./resources/fonts/ARCADE.TTF',base_x=self.text_loc_x)
            textTyper.setText("EXAMPLE")
        
        Print The Text:
            self.obj_bot,self.rect_bot,self.rect_right_bot = textTyper.printNext((self.text_loc_x, self.text_loc_y+150))
    """
    def __init__(self,**kwargs):
        self.font_color     = kwargs.get('font_color',Colors.RGB('white'))
        self.font_size      = kwargs.get('font_size',32)
        self.font_path      = kwargs.get('font_path',None)

        if not os.path.isfile(self.font_path):
            print("Error: font path is not an actual file!")
            sys.exit()

        self.font           = pygame.font.Font(self.font_path, self.font_size)
        self.text           = None
        self.index          = 0
        self.base_x         = kwargs.get('base_x',10)
        self.base_y         = kwargs.get('base_y',50)
        self.last_update    = pygame.time.get_ticks()
        self.chunk          = kwargs.get('chunk',50)
        self.calls          = 0

    def printNext(self,loc,all=False):
        self.calls += 1
        if self.chunk == 0:
            self.surface_obj = self.font.render(self.text, True, self.font_color)
        else:
            if self.calls % self.chunk == 0:
                self.index += 1
            self.surface_obj  = self.font.render(self.text[0:self.index], True, self.font_color)

        self.rect_obj           = self.surface_obj.get_rect()
        self.rect_obj.top       = self.base_y
        self.rect_obj.left      = self.base_x

        return self.surface_obj,self.rect_obj,self.rect_obj.right

    def setText(self,text):
        self.text = text


if __name__=='__main__':
    c = ColorClass()

    print(c.RGB("lightgray"))
    print(c.HEX("lightgray"))


    