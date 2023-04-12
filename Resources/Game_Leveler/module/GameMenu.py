import pygame

try :
    from .helper_functions import *
    from .helper_classes import *
except ImportError as e:
    from helper_functions import *
    from helper_classes import *




# The level manager / loader is based on code from stack overflow.
# Link and user referenced below.
# https://gist.github.com/programmingpixels/27b7f8f59ec53b401183c68f4be1634b#file-step4-py
# https://stackoverflow.com/users/142637/sloth


# class State(object):
#     def __init__(self):
#         pass

#     def render(self, screen):
#         raise NotImplementedError

#     def update(self):
#         raise NotImplementedError

#     def handle_events(self, events):
#         raise NotImplementedError


# class MouseClickRect(pygame.sprite.Sprite):
#     def __init__(self,x,y):
#         pygame.sprite.Sprite.__init__(self)
#         self.rect = pygame.Rect(x,y,1,1)


# def pointInRect(p,rect):
#     return rect[0] < p[0] < rect[0] + rect[2] and rect[1] < p[1] < rect[1] + rect[3]

# # def pointInRect(p,x1,y1,x2,y2):
# #     b = (x1 < x < x2) and (y1 < y < y2)


font_path = "/Users/griffin/Dropbox/_Courses/4443-2D-PyGame/Game/resources/fonts/joystix.ttf"

class GameMenu(State):

    def __init__(self,**kwargs):
        super(State, self).__init__()

        self.menu_id = 0

        # list to hold our menu items
        self.menuItemsList = []

        # config items to set up colors and defaults
        self.game_width      = kwargs.get('game_width',0)
        self.game_height      = kwargs.get('game_height',0)

        # get middle of screen
        self.mid_x = self.game_width//2
        self.mid_y = self.game_height//2

        if self.game_width + self.game_height == 0:
            print("Error: Need games width and height.")

        self.def_bg_color           = kwargs.get('bg_color',Colors.RGB('mediumorchid'))
        self.def_fg_color           = kwargs.get('fg_color',Colors.RGB('white'))
        self.def_roll_fg_color      = kwargs.get('roll_fg_color',Colors.RGB('violet'))
        self.def_roll_bg_color      = kwargs.get('roll_bg_color',Colors.RGB('yellow'))
        self.def_font_size          = kwargs.get('font_size',32)
        self.def_font_color         = kwargs.get('font_color',Colors.RGB("white"))
        self.def_shadow_txt_color   = kwargs.get('shadow_txt_color',Colors.RGB("black"))
        self.def_txt_box_color      = kwargs.get('txt_box_color',self.def_font_color)
        self.def_txt_box_fill       = kwargs.get('txt_box_fill',False)
        self.def_txt_box_shadow     = kwargs.get('txt_box_shadow',None)
        self.def_base_location      = kwargs.get('base_location',(self.mid_x,50))
        self.def_buffer             = kwargs.get('buffer',0)
        self.def_shift_size         = kwargs.get('shift_size',4)                            # how much to shift on a rollover event

        # dictionary of font sizes. Not sure how necessary for now
        self.fonts = {}
        self.fonts[56] = pygame.font.Font(font_path, 56)
        self.fonts[32] = pygame.font.Font(font_path, 32)

        self.max_rect_size = (0,0)

    def addFont(self,font_size,font_path=None):
        # add font size if doesn't exist
        if not font_size in self.fonts:
            self.fonts[font_size] = pygame.font.Font(font_path, font_size)

    def generateTextRect(self,font_size,card_text,font_color,loc,shadow=False):
        """ This method creates a rectangle surface object with text. 
        """
        if shadow:
            offset = 2
        else:
            offset = 0

        text_surface_obj        = self.fonts[font_size].render(card_text, True, font_color)
        text_rect_obj           = text_surface_obj.get_rect()
        text_rect_obj.center    = (loc[0]+offset,loc[1]+offset)


        return (text_surface_obj,text_rect_obj)


    def addChoice(self,**kwargs):
        
        # get card info from params
        card_text           = kwargs.get('card_text',None)                                  # what you wanna say?
        font_size           = kwargs.get('font_size',self.def_font_size)                    # ummmm
        font_color          = kwargs.get('font_color',self.def_font_color)                  # ummmm
        shadow_txt_color    = kwargs.get('shadow_txt_color',self.def_shadow_txt_color)      # color of txt that will be the shadow
        drop_txt_shadow     = kwargs.get('drop_txt_shadow',False)                           # add shadow to text true false
        txt_box             = kwargs.get('txt_box',None)                                    # hitbox reference
        txt_box_color       = kwargs.get('txt_box_color',Colors.RGB("gray"))                # color of txt box
        txt_box_fill        = kwargs.get('txt_box_fill',self.def_txt_box_fill)              # 0 = fill txt box with color other wise 1-N is border thickness
        txt_box_shadow      = kwargs.get('txt_box_shadow',self.def_txt_box_shadow)          # add shadow to txt box or None
        roll_fg_color       = kwargs.get('roll_fg_color',self.def_roll_fg_color)            # roll over fore ground color
        roll_bg_color       = kwargs.get('roll_bg_color',self.def_roll_bg_color)            # roll over background color
        txt_box_fill_roll   = kwargs.get('txt_box_fill_roll',None)                          # color to fill txt box on rollover or None
        loc                 = kwargs.get('loc',None)                                        # x,y tuple
        shift_size          = kwargs.get('shift_size',self.def_shift_size )                 # for shadows and rollover events

        # don't want to fill? give it a thickness
        # as a border.
        if txt_box_fill == False:
            txt_box_fill = 1
        else:
            # zero = fill it up ... thanks pygame
            txt_box_fill = 0

        # increment menu item id
        mid = self.menu_id
        self.menu_id += 1

        self.addFont(font_size)

        # calculate width and height based on font size and font
        text_width, text_height = self.fonts[font_size].size(card_text)

        if not loc:
            loc = (self.def_base_location[0],(self.def_base_location[1]+self.def_buffer)*self.menu_id)

        text_surface_obj,text_rect_obj = self.generateTextRect(font_size,card_text,font_color,loc)
        roll_surface_obj,roll_rect_obj = self.generateTextRect(font_size,card_text,roll_fg_color,loc)
        shad_surface_obj,shad_rect_obj = self.generateTextRect(font_size,card_text,shadow_txt_color,loc,True)


        txt_box = HitBox(rect = text_rect_obj,game_window=(self.game_width,self.game_height))
        txt_box_shadow = HitBox(rect = (text_rect_obj[0], text_rect_obj[1], text_rect_obj[2]+2, text_rect_obj[3]+2),game_window=(self.game_width,self.game_height))
    


        choice = {
            'menu_id' : self.menu_id,
            'card_text':card_text,
            'loc':loc,
            'font_size':font_size,
            'font_color':font_color,
            'shadow_txt_color':shadow_txt_color,
            'drop_txt_shadow':drop_txt_shadow,
            'txt_object':text_surface_obj,
            'txt_rect':text_rect_obj,
            'roll_object':roll_surface_obj,
            'roll_rect':roll_rect_obj,
            'shadow_object':shad_surface_obj,
            'shadow_rect':shad_rect_obj,
            'rolled':False,
            'txt_box':txt_box,
            'txt_box_shadow':txt_box_shadow,
            'txt_box_color': txt_box_color,
            'txt_box_shadow_color':Colors.RGB('black'),
            'txt_box_fill': txt_box_fill,
            'txt_box_fill_roll': txt_box_fill_roll,
            'roll_fg_color':roll_fg_color,
            'roll_bg_color':roll_bg_color
        }

        self.menuItemsList.append(choice)

        self.menu_id += 1

    def rollover_menu_item(self,pos):
        x,y = pos
        mouse = MouseClickRect(x,y)
        for item in self.menuItemsList:
            if pointInRect(pos,item['txt_rect']) and not item['rolled']:

                # shift the rectangles for the main text and the shadow text and the rollover text
                item['txt_rect'].y += 4
                item['shadow_rect'].y += 4
                item['roll_rect'].y += 4

                # set our menu item to "rolled" so we display like were focused
                item['rolled'] = True
                
                # shift the text box down and over to look like it moves
                if item['txt_box']:
                    item['txt_box'].rect.y += 4
                if item['txt_box_shadow']:
                    item['txt_box_shadow'].rect.y += 4

                # re-render text "cards" (rectangles) since we shifted them.
                # this can't be efficient
                item['txt_object'] = self.fonts[item['font_size']].render(item['card_text'], True, item['font_color']) 
                item['roll_object'] = self.fonts[item['font_size']].render(item['card_text'], True, item['roll_fg_color']) 
                item['shadow_object'] = self.fonts[item['font_size']].render(item['card_text'], True, item['shadow_txt_color']) 

            if not pointInRect(pos,item['txt_rect']) and item['rolled']:
                item['txt_rect'].y -= 4
                item['shadow_rect'].y -= 4
                item['roll_rect'].y -= 4
                item['rolled'] = False
                if item['txt_box']:
                    item['txt_box'].rect.y -= 4
                if item['txt_box_shadow']:
                    item['txt_box_shadow'].rect.y -= 4

    def clicked_menu_item(self,pos):
        x,y = pos
        mouse = MouseClickRect(x,y)
        for item in self.menuItemsList:
            if pointInRect(pos,item['txt_rect']):
                print(f"{item}")


    def render(self,screen):
        screen.fill(self.def_bg_color)
        for item in self.menuItemsList:
            # If item has a txt_box defined 
            if item['txt_box']:
                # 
                if item['txt_box_fill_roll'] and item['rolled']:
                    fill_text_box = 0 # yes fill it up
                else:
                    fill_text_box = item['txt_box_fill']
                # if there is a shadow for the txt box
                if item['txt_box_shadow']:
                    # display shadow
                    pygame.draw.rect(screen,item['txt_box_shadow_color'],item['txt_box_shadow'].rect,item['txt_box_fill'])
                # display the txt box
                pygame.draw.rect(screen,item['txt_box_color'],item['txt_box'].rect,item['txt_box_fill'])
                
            #print shadow first so it is behind
            if item['drop_txt_shadow']:
                screen.blit(item['shadow_object'], item['shadow_rect'])

            if not item['rolled']:
                screen.blit(item['txt_object'], item['txt_rect'])
            else:
                screen.blit(item['roll_object'], item['roll_rect'])



        
    def update(self):
        # for card in self.card_group:
        #     card.rect.centerx += 1
        pass


    def handle_events(self,events):
        for event in events:
            mouse_position = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                self.clicked_menu_item(mouse_position)
            if event.type == pygame.MOUSEMOTION:
                self.rollover_menu_item(mouse_position)


if __name__=='__main__':


    menu_config = {
        "bg_color" : "mediumorchid",
        "fg_color" : 'white',
        "rollover_color" : 'black',
        "font_size"  : 56,
        "font_color" : "white",
        "shadow_color" : "black",
        "txt_box_color"  : 'font_color',
        "txt_box_fill" : 1,
        "txt_box_shadow" : None,
    }

    if os.path.isfile("./resources/data/config.json"):
        config = Config("./resources/data/config.json")
    else:
        config = {
            "title" :"My Game P02",
            "game_window" : [1000,500],
            "sprite_sheets":{
                "mario":{"path":"./resources/mario_frames"}
            },
            "tiles_path":"./resources/maps/forest_clean/Tiles_20",
            "levels_path":"./resources/levels",
            "font_path":"./data/freesansbold.ttf",
            "tile_size":20,
            "debug": 1,
            "debug_level":20
        }

    pygame.init()

    # sets the window title
    pygame.display.set_caption("Test Game Menu")

    # Set up the drawing window
    screen = pygame.display.set_mode((800,800))

    menu = GameMenu(game_width=800,game_height=800)
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

    # Run until the user asks to quit
    # Basic game loop
    running = True
    while running:

        #screen.fill((0,0,0))

        events = pygame.event.get()
        # Did the user click the window close button?
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            # Not used in this instance of our game
            if event.type == pygame.MOUSEBUTTONUP:
                # debug(pygame.mouse.get_pos(),10)
                pass
        menu.render(screen)
        menu.handle_events(events)
        menu.update()

        pygame.display.flip()

    pygame.quit()
