import pygame
import pygame.freetype
import random
import os
import sys
import json
import pprint
import glob
import more_itertools 

# from resources.modules.helper_functions import loadSpriteImages
# from helper_functions import loadJson
# from helper_functions import Config
# from helper_classes import Colors
# from helper_classes import HitBox

from module import *

config = loadJson('./resources/data/config.json')


# Our typical config, but a lot smaller right now.

def debug(statement,level=0):
    """ An easy way to globally turn on and off debug statements. Just change config['debug'] to False
    """
    if config['debug']:
        if level <= config['debug_level']:
            print(statement)


# The level manager / loader is based on code from stack overflow.
# Link and user referenced below.
# https://gist.github.com/programmingpixels/27b7f8f59ec53b401183c68f4be1634b#file-step4-py
# https://stackoverflow.com/users/142637/sloth


class State(object):
    def __init__(self):
        pass

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError


class MouseClickRect(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,y,1,1)


def pointInRect(p,rect):
    return rect[0] < p[0] < rect[0] + rect[2] and rect[1] < p[1] < rect[1] + rect[3]

# def pointInRect(p,x1,y1,x2,y2):
#     b = (x1 < x < x2) and (y1 < y < y2)

class GameMenu(State):

    def __init__(self,**kwargs):
        super(State, self).__init__()

        self.menu_id = 0

        self.game_width,self.game_height = config['game_window']

        # list to hold our menu items
        self.menuItemsList = []

        # get middle of screen
        self.mid_x = self.game_width//2
        self.mid_y = self.game_height//2

        # config items to set up colors and defaults
        self.def_bg_color       = Colors.RGB('mediumorchid')
        self.def_fg_color       = Colors.RGB('white')
        self.def_rollover_color = Colors.RGB('black')
        self.def_font_size      = kwargs.get('font_size',56)
        self.def_font_color     = kwargs.get('font_color',Colors.RGB("white"))
        self.def_shadow_color   = kwargs.get('shadow_color',Colors.RGB("black"))
        self.def_hit_box_color  = kwargs.get('hit_box_color',self.def_font_color)
        self.def_hit_box_fill   = kwargs.get('hit_box_fill',1)
        self.def_hit_box_shadow = kwargs.get('hit_box_shadow',None)
        self.def_base_location  = kwargs.get('base_location',(self.mid_x,50))
        self.def_buffer         = kwargs.get('buffer',0)

        # dictionary of font sizes. Not sure how necessary for now
        self.fonts = {}
        self.fonts[56] = pygame.font.Font(config['font_path'], 56)
        self.fonts[32] = pygame.font.Font(config['font_path'], 32)

        self.max_rect_size = (0,0)

        # hard coded adding for now
        self.addChoice(card_text="Edit Profile",font_size=40,font_color=Colors.RGB('white'),hit_box_fill=1,hit_box_color=Colors.RGB("gray"),hit_box_shadow=Colors.RGB("black"),rollover_color=Colors.RGB("darkviolet"))
        self.addChoice(card_text="View High Scores",font_size=40,font_color=Colors.RGB('white'),hit_box_fill=1,hit_box_color=Colors.RGB("gray"))
        self.addChoice(card_text="Start Game",font_size=40,font_color=Colors.RGB('white'),hit_box_fill=1,hit_box_color=Colors.RGB("gray"))

    
    def getNextLocation(self,id):
        _, height = self.fonts[font_size].size("TESTME")
        loc = None
        if id == 0:
            loc = (self.def_base_location[0],self.def_base_location[1])
            return loc
        else:
            for menu_item in  self.menuItemsList.items():
                if menu_item[id] == id - 1:
                    loc = ( menu_item['text_rect_obj'][0],menu_item['text_rect_obj'][1]+height+self.buffer)
        
        if not loc:
            return (self.def_base_location[0],self.def_base_location[1] + ((height+self.buffer) * id))

    def addChoice(self,**kwargs):
        
        mid = self.menu_id
        self.menu_id += 1

        # get card info from params
        card_text       = kwargs.get('card_text',None)
        font_size       = kwargs.get('font_size',self.def_font_size)
        font_color      = kwargs.get('font_color',self.def_font_color)
        shadow_color    = kwargs.get('shadow_color',self.def_shadow_color)
        hit_box         = kwargs.get('hit_box',None)
        hit_box_color   = kwargs.get('hit_box_color',self.def_font_color)
        hit_box_fill    = kwargs.get('hit_box_fill',self.def_hit_box_fill)
        hit_box_shadow  = kwargs.get('hit_box_shadow',self.def_hit_box_shadow)
        rollover_color  = kwargs.get('rollover_color',None)
        loc             = kwargs.get('loc',None)


        # add font size if doesn't exist
        if not font_size in self.fonts:
            self.fonts[font_size] = pygame.font.Font(config['font_path'], font_size)
            
        # calculate width and height based on font size and font
        text_width, text_height = self.fonts[font_size].size(card_text)

        # find biggest bounding box
        if text_width > self.max_rect_size[0]:
            self.max_rect_size = (text_width,self.max_rect_size[1])
        if text_height > self.max_rect_size[1]:
            self.max_rect_size = (self.max_rect_size[0],text_height)

        if not loc:
            loc = (self.def_base_location[0],self.def_base_location[1]+text_height*self.menu_id)

        if rollover_color != None:
            roll_surface_obj        = self.fonts[font_size].render(card_text, True, rollover_color)
            roll_rect_obj           = roll_surface_obj.get_rect()
            roll_rect_obj.center    = (loc[0],loc[1])
        else:
            roll_surface_obj        = None
            roll_rect_obj           = None

        text_surface_obj        = self.fonts[font_size].render(card_text, True, font_color)
        text_rect_obj           = text_surface_obj.get_rect()
        text_rect_obj.center    = (loc[0],loc[1])

        shadow_surface_obj      = self.fonts[font_size].render(card_text, True, shadow_color)
        shadow_rect_obj         = shadow_surface_obj.get_rect()
        shadow_rect_obj.center  = (loc[0]+2,loc[1]+2)


        if hit_box:
            hit_box = HitBox(rect = text_rect_obj,game_window=config['game_window'])
    
        choice = {
            'menu_id' : self.menu_id,
            'card_text':card_text,
            'loc':loc,
            'font_size':font_size,
            'font_color':font_color,
            'shadow_color':shadow_color,
            'txt_object':text_surface_obj,
            'txt_rect':text_rect_obj,
            'roll_object':roll_surface_obj,
            'roll_rect':roll_rect_obj,
            'shadow_object':shadow_surface_obj,
            'shadow_rect':shadow_rect_obj,
            'shifted':False,
            'hit_box':hit_box,
            'hit_box_color': hit_box_color,
            'hit_box_fill': hit_box_fill,
            'hit_box_shadow':hit_box_shadow,
            'rollover_color':rollover_color
            
        }

        self.menuItemsList.append(choice)

        self.menu_id += 1

    def shift_menu_item(self,pos):
        x,y = pos
        mouse = MouseClickRect(x,y)
        for item in self.menuItemsList:
            if pointInRect(pos,item['txt_rect']) and not item['shifted']:
                print("hit")
                item['txt_rect'].y += 4
                item['shadow_rect'].y += 4
                item['shifted'] = True
                  
                if item['hit_box']:
                    item['hit_box'].rect.y += 4

                item['txt_object'] = self.fonts[item['font_size']].render(item['card_text'], True, Colors.RGB("lavender")) 

            if not pointInRect(pos,item['txt_rect']) and item['shifted']:
                item['txt_rect'].y -= 4
                item['shadow_rect'].y -= 4
                item['shifted'] = False
                if item['hit_box']:
                    item['hit_box'].rect.y -= 4

    def render(self,screen):
        screen.fill(self.def_bg_color)
        for item in self.menuItemsList:
            if item['hit_box']:
                if item['hit_box_shadow']:
                    shadow_rect = (item['hit_box'].rect[0]+1,item['hit_box'].rect[1]+1,item['hit_box'].rect[2]+1,item['hit_box'].rect[3]+1)
                    pygame.draw.rect(screen,Colors.RGB("black"),shadow_rect,item['hit_box_fill'])
                pygame.draw.rect(screen,Colors.RGB("gray"),item['hit_box'].rect,item['hit_box_fill'])

            if item['rollover_color'] != None:
                screen.blit(item['roll_object'], item['roll_rect'])
            screen.blit(item['shadow_object'], item['shadow_rect'])
            screen.blit(item['txt_object'], item['txt_rect'])
            # if item['rollover_color'] != None:
            #     screen.blit(item['roll_object'], item['roll_rect'])

            
    def update(self):
        # for card in self.card_group:
        #     card.rect.centerx += 1
        pass


    def handle_events(self,events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                pass
                #self.manager.go_to()
            if event.type == pygame.MOUSEMOTION:
                mouse_position = pygame.mouse.get_pos()
                self.shift_menu_item(mouse_position)


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


class Borg:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state

class StateMananger(Borg):
    def __init__(self):
        self.index = -1
        self.states = [
            GameMenu(),
            # LevelLoader(levels_path=config['levels_path'],tiles_path=config['tiles_path'],level_name="level_01",tile_size=(20,20)),
            # LevelLoader(levels_path=config['levels_path'],tiles_path=config['tiles_path'],level_name="level_02",tile_size=(20,20)),
            # LevelLoader(levels_path=config['levels_path'],tiles_path=config['tiles_path'],level_name="level_03",tile_size=(20,20))
        ]
        self.go_to()

    def go_to(self):
        self.index = (self.index + 1) % len(self.states)
        print(self.index)
        self.state = self.states[self.index]
        self.state.manager = self
        


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
    screen = pygame.display.set_mode(config['game_window'])

    manager = StateMananger()

    # Run until the user asks to quit
    # Basic game loop
    running = True
    while running:

        screen.fill((0,0,0))


        events = pygame.event.get()
        # Did the user click the window close button?
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            # Not used in this instance of our game
            if event.type == pygame.MOUSEBUTTONUP:
                # debug(pygame.mouse.get_pos(),10)
                pass

        manager.state.handle_events(events)
        manager.state.update()
        manager.state.render(screen)

        pygame.display.flip()

    pygame.quit()

if __name__=='__main__':

    main()

