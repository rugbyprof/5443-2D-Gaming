import pygame
import sys
import csv
from rich import print
from pygame.locals import *
import math

# Initialize Pygame
pygame.init()

DEBUG = True

# Colors
WHITE = (255, 255, 255)
TILESIZE = 32
WIDTH = 800
HEIGHT = 600
CAMERA_WIDTH = 600
CAMERA_HEIGHT = 500

# Level data
config = {
    "Font": "./resources/fonts/joystix.ttf",
    "Levels": {
        "Entrance": {
            "background": "./resources/Entrance/_composite_32x32.png",
            "thumb": "./resources/Entrance/_composite_thumb.png",
            "csv": "./resources/Entrance/Collisions.csv",
            "width": 1152,
            "height": 640,
            "startx": 32,
            "starty": 320,
            "transition_locations": [(35, 13), (3, 20)],
            "target_level": "Elevator",
        },
        "Elevator": {
            "background": "./resources/Elevator/_composite_32x32.png",
            "thumb": "./resources/Entrance/_composite_thumb.png",
            "csv": "./resources/Elevator/Collisions.csv",
            "width": 544,
            "height": 576,
            "startx": 512,
            "starty": 192,
            "transition_locations": [(35, 12)],
            "target_level": "Basement",
        },
        "Basement": {
            "background": "./resources/Basement/_composite.png",
            "thumb": "./resources/Entrance/_composite_thumb.png",
            "csv": "./resources/Basement/Collisions.csv",
        },
    },
}

font = pygame.font.SysFont(config["Font"], 24)


def get_player_tile_coordinates(player,tile_size=TILESIZE):
    x = player.rect.x // tile_size
    y = player.rect.y // tile_size
    return x,y

def display_tile_coordinates(player, screen):
    x,y = get_player_tile_coordinates(player)
    text = font.render(f" ({x}, {y})", True, WHITE)
    screen.blit(text, (screen.get_width() - text.get_width() - 10, 10))
    print(f"({x},{y})")


# Load level data
def load_level_data(level):
    background = pygame.image.load(
        config["Levels"][level]["background"]
    ).convert_alpha()
    # background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    bg_width, bg_height = background.get_size()

    mapThumb = pygame.image.load(
        config["Levels"][level]["thumb"]
    ).convert_alpha()

    with open(config["Levels"][level]["csv"], newline="\n") as csvfile:
        layout_reader = csv.reader(csvfile)
        layout = [list(map(int, row)) for row in layout_reader]

    # for row in layout:
    #     print(row)

    return background, layout, (bg_width, bg_height), mapThumb


def point_inside_rect(point, rect):
    x, y = point
    print(f"{rect.x }<= {x} <= {rect.x + rect.width} and {rect.y} <= {abs(CAMERA_HEIGHT-y)} <= {rect.y + rect.height}")
    print(rect.x <= x <= rect.x + rect.width and rect.y <= abs(CAMERA_HEIGHT-y)<= rect.y + rect.height)
    return rect.x <= x <= rect.x + rect.width and rect.y <= abs(CAMERA_HEIGHT-y) <= rect.y + rect.height


# Set up the display


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.image = pygame.image.load("./resources/player.png").convert_alpha()
        # self.image = pygame.Surface((32, 32))
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        config["Levels"][level]["startx"]

        self.rect.x = config["Levels"][level]["startx"]
        self.rect.y = config["Levels"][level]["starty"]

    def update(self, layout):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if (
                layout[self.rect.y // TILESIZE][(self.rect.x - TILESIZE) // TILESIZE]
                != 1
            ):
                self.rect.x -= TILESIZE
        if keys[pygame.K_RIGHT]:
            if (
                layout[self.rect.y // TILESIZE][(self.rect.x + TILESIZE) // TILESIZE]
                != 1
            ):
                self.rect.x += TILESIZE
        if keys[pygame.K_UP]:
            if (
                layout[(self.rect.y - TILESIZE) // TILESIZE][self.rect.x // TILESIZE]
                != 1
            ):
                self.rect.y -= TILESIZE
        if keys[pygame.K_DOWN]:
            if (
                layout[(self.rect.y + TILESIZE) // TILESIZE][self.rect.x // TILESIZE]
                != 1
            ):
                self.rect.y += TILESIZE

        # print(self.rect.centerx//TILESIZE,self.rect.centery//TILESIZE)


# Update the camera position based on the player's position
def update_camera_position(player, camera_view, background):

    rect = (0, 0, CAMERA_WIDTH, CAMERA_HEIGHT)

    # Get the specific section of the image as a new surface
    section = background.subsurface(rect)

    camera_view.fill((0, 0, 0))
    tiles = get_player_tile_coordinates(player)
    camera_x = -player.rect.x + CAMERA_WIDTH // 2
    camera_y = -player.rect.y + CAMERA_HEIGHT // 2
    # camera_x = player.rect.x
    # camera_y = player.rect.y
    camera_view.blit(section, (0, 0))


class Camera:
    def __init__(self, **kwargs):
        self.player = kwargs.get("player", None)
        self.camera_screen = kwargs.get("camera_screen", None)
        self.background = kwargs.get("background", None)

        if None in [self.player, self.camera_screen, self.background]:
            print(
                "Error: A player sprite, Camera Screen, and Background image are all needed!"
            )
            sys.exit()

    def update(self):
        self.camera_screen.fill((0, 0, 0))
        camera_x = -player.rect.x + CAMERA_WIDTH // 2
        camera_y = -player.rect.y + CAMERA_HEIGHT // 2
        # camera_x = player.rect.x
        # camera_y = player.rect.y
        self.camera_screen.blit(self.background, (camera_x, camera_y))


# Set the starting level
current_level = "Entrance"

camera_view = pygame.Surface((CAMERA_WIDTH, CAMERA_HEIGHT))
sidebar = pygame.Surface((WIDTH - CAMERA_WIDTH, HEIGHT))
bottom_area = pygame.Surface((WIDTH, HEIGHT - CAMERA_HEIGHT))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
background, layout, screen_size, map_thumb = load_level_data(current_level)

# Update the display surface based on the level background size
pygame.display.set_caption("Multi-level Game")


# Create player
player = Player(current_level)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


# Set up the chat box
chat_box_height = 100
chat_box_rect = pygame.Rect(0, screen.get_height() - chat_box_height, screen.get_width(), chat_box_height)
chat_box_surface = pygame.Surface(chat_box_rect.size)
chat_box_surface.fill((20, 20, 20))

# Set up the text input
font = pygame.font.Font(None, 36)
input_box_rect = pygame.Rect(10, chat_box_rect.height - 40, chat_box_rect.width - 120, 30)
input_box_color = pygame.Color('black')
input_box_background = pygame.Color('white')
input_box_active = False
text_input = ""
text_surface = font.render(text_input, True, input_box_color)

# Set up the send button
send_button_rect = pygame.Rect(input_box_rect.right + 10, input_box_rect.y, 100, 30)
send_button_color = pygame.Color('black')
send_button_background = pygame.Color('white')
send_button_font = pygame.font.Font(None, 28)
send_button_text = "Send"
send_button_text_surface = send_button_font.render(send_button_text, True, send_button_color)

# Set up the game map


red_square_size = (4, 4)
red_square_color = (255, 0, 0)



# set up the leader board



def send_message(message):
    # Handle sending and receiving messages here
    print(message)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == MOUSEBUTTONDOWN:
            if point_inside_rect(event.pos,input_box_rect):
                print("active")
                input_box_active = True
            else:
                input_box_active = False

            if point_inside_rect(event.pos,send_button_rect):
                send_message(text_input)
                text_input = ""
                text_surface = font.render(text_input, True, input_box_color)

        if event.type == KEYDOWN:
            if input_box_active:
                if event.key == K_RETURN:
                    # Handle sending and receiving messages here
                    print(text_input)
                    text_input = ""
                elif event.key == K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += event.unicode
                text_surface = font.render(text_input, True, input_box_color)



    player.update(layout)
    # player_position = pygame.Vector2(player.rect.x, player.rect.y)
    # red_square_position = player_position + pygame.Vector2(10, 10)  # Offset from the player


    # print(f"{config["Levels"][current_level]['transition_locations']}")
    for transition_location in config["Levels"][current_level]["transition_locations"]:
        # print(f"{current_level} {transition_location}")
        # print(f"px: {player.rect.centerx // TILESIZE} == tlx: {transition_location[0]}")
        # print(f"py: {player.rect.centery // TILESIZE} == tly: {transition_location[1]}")
        if (
            player.rect.centerx // TILESIZE == transition_location[0]
            and player.rect.centery // TILESIZE == transition_location[1]
        ):
            # print("changing levels")

            current_level = config["Levels"][current_level]["target_level"]
            player.rect.x == config["Levels"][current_level]["startx"]
            player.rect.y == config["Levels"][current_level]["starty"]
            background, layout, screen_size, map_thumb = load_level_data(current_level)
            ##screen = pygame.display.set_mode(screen_size)  # Update the display surface
            break

    # Draw everything
    update_camera_position(player, camera_view, background)
    all_sprites.draw(camera_view)
    display_tile_coordinates(player, camera_view)
    
    ptc = get_player_tile_coordinates(player)

    rx = player.rect.x / WIDTH * map_thumb.get_width()
    ry = player.rect.y / HEIGHT * map_thumb.get_height()
    print(f"rx: {rx} , ry: {ry}")
    

    sidebar.fill((0,0,0))
    sidebar.blit(map_thumb, (0, 0))
    print((rx-3,ry-3,rx,ry))
    pygame.draw.rect(sidebar, red_square_color, (rx,ry,3,3))
    

    screen.blit(camera_view, (0, 0))
    screen.blit(sidebar, (CAMERA_WIDTH, 0))
    screen.blit(bottom_area, (0, CAMERA_HEIGHT))


    # Render the chat box
    screen.blit(chat_box_surface, chat_box_rect.topleft)

    # Render the input box
    input_box_background_color = (255, 255, 255) if input_box_active else (200, 200, 200)
    pygame.draw.rect(chat_box_surface, input_box_background_color, input_box_rect)
    pygame.draw.rect(chat_box_surface, input_box_color, input_box_rect, 2)
    chat_box_surface.blit(text_surface, (input_box_rect.x + 5, input_box_rect.y + 5))

    # Render the send button
    pygame.draw.rect(chat_box_surface, send_button_background, send_button_rect)
    pygame.draw.rect(chat_box_surface, send_button_color, send_button_rect, 2)
    chat_box_surface.blit(send_button_text_surface, (send_button_rect.x + 30, send_button_rect.y + 3))


    pygame.display.flip()

    # Cap the frame rate
    pygame.time.delay(100)

# Clean up and quit
pygame.quit()
sys.exit()
