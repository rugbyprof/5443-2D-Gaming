import pygame
import os
import sys
from module import *

config = loadJson('./resources/config.json')


class TypedText(object):
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

class Splash(State):
    def __init__(self):
        super(State, self).__init__()

        self.griff_x = 50
        self.griff_y = 150

        self.sprite_w = 150
        self.sprite_h = 108

        self.dx = 0
        self.dy = 0

        self.text_loc_x = 75
        self.text_loc_y = 100
        self.rect_x = 0

        self.textTyperTop = TypedText(font_color=Colors.RGB('gold'),font_size=200,font_path='./resources/fonts/ARCADE.TTF',base_x=self.text_loc_x,chunk=0)
        self.textTyperTop.setText("GRIFFIN")
        self.obj_top,self.rect_top,self.rect_right_top = self.textTyperTop.printNext((self.text_loc_x, self.text_loc_y),True)

        self.textTyperBot = TypedText(font_color=Colors.RGB('gold'),font_size=200,font_path='./resources/fonts/ARCADE.TTF',base_x=self.text_loc_x)
        self.textTyperBot.setText("GAMES")
        self.obj_bot,self.rect_bot,self.rect_right_bot = self.textTyperTop.printNext((self.text_loc_x, self.text_loc_y+150))

        self.last_rect_right = self.rect_right_bot
        self.padding = 0
        self.pad = 1.8


        griffin_sprite = loadSpriteImages(path='./resources/graphics/griffin_frames')
        self.animations = {}
        for move,images in griffin_sprite.items():
            self.animations[move] = []
            for img in images:
                im = pygame.image.load(img)
                frame = pygame.sprite.Sprite()
                frame.image = pygame.transform.scale(im, (self.sprite_w, self.sprite_h))
                self.animations[move].append(frame.image)

        self.frame_number = 0
        self.current_animation = 'walking'
        self.loop_animation = True
        self.current_image = self.getNextAnimationFrame(self.current_animation,(self.griff_x,self.text_loc_y+150))

        self.dx = 5

        # in case we need to time some things
        self.last_update = pygame.time.get_ticks()
    

    def getNextAnimationFrame(self,name,loc):

        if self.loop_animation:
            next = self.frame_number % len(self.animations[name])
        else:
            if self.frame_number > len(self.animations[name]) - 1:
                next = len(self.animations[name]) - 1

        self.image = self.animations[name][next]
        self.rect = self.image.get_rect()
        self.rect.center = loc   
        self.frame_number += 1
        return self.image

    def changeAnimation(self,name):
        self.current_animation = name
        self.frame_number = 0

    def render(self,screen):
        
        self.padding += self.pad
        screen.blit(self.current_image, (100+self.padding, self.text_loc_y+150))
        
        screen.blit(self.obj_top, (self.text_loc_x, self.text_loc_y))
        screen.blit(self.obj_bot, (self.text_loc_x, self.text_loc_y+150))
            

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 30:
            self.last_update = now
            self.griff_x += self.dx
            self.current_image = self.getNextAnimationFrame(self.current_animation,(100+self.padding,self.text_loc_y+150))
            
        if 100+self.padding >= 600:
            self.loop_animation = False
            self.current_animation = 'sit'
            self.dx = 0
            self.pad = 0
            self.done = True
        else:
            self.done = False

        if self.done:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, done=True))
            


        #self.obj_top,self.rect_top,self.rect_right_top = self.textTyperTop.printNext((self.text_loc_x, self.text_loc_y))
        self.obj_bot,self.rect_bot,self.rect_right_bot = self.textTyperBot.printNext((self.text_loc_x, self.text_loc_y+150))

        # if self.rect_right_bot != self.last_rect_right:
        #     self.last_rect_right = self.rect_right_bot
        #     self.padding = 0


    def handle_events(self,events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                pass
            if event.type == pygame.MOUSEMOTION:
                mouse_position = pygame.mouse.get_pos()
                

if __name__=='__main__':
    game_width = config["game_window"][0]
    game_height = config["game_window"][1]
    game_title = config["title"]

    gameState = StateManager()

    pygame.init()

    # sets the window title
    pygame.display.set_caption(game_title)

    # Set up the drawing window
    screen = pygame.display.set_mode((game_width,game_height))

    #################################################################################
    #################################################################################

    splash = Splash()

    menu = GameMenu(game_width=game_width,game_height=game_height)
    kwargs = {
        "font_size":32,
        "font_color":Colors.RGB('white'),
        "txt_box_fill":False,
        "txt_box_color":Colors.RGB("white"),
        "txt_box_shadow":Colors.RGB("gray"),
        "txt_box_fill_roll":Colors.RGB('purple'),
        "roll_fg_color":Colors.RGB("purple"),
        "roll_bg_color":Colors.RGB("orchid"),
        "drop_txt_shadow":1
    }
    menu.addChoice(card_text="Edit Profile",**kwargs)
    menu.addChoice(card_text="View High Scores",**kwargs)
    menu.addChoice(card_text="Start Game",**kwargs)

    

    #################################################################################
    #################################################################################

    gameState.addState(splash)
    gameState.addState(menu)

    gameState.next()

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

            if event.type == 24:
                gameState.next()
        
        

        gameState.state.render(screen)
        gameState.state.handle_events(events)
        gameState.state.update()

        pygame.display.flip()

    pygame.quit()
