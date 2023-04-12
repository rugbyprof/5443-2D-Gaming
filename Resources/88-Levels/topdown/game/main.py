import pygame
import sys
import csv
from rich import print

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
    "Font":"./resources/fonts/joystix.ttf",
    "Levels":{
    "Entrance": {
        "background": "./resources/Entrance/_composite_32x32.png",
        "csv": "./resources/Entrance/Collisions.csv",
        "width":1152,
        "height":640,
        "startx":32,
        "starty":320,
        "transition_locations":[(35,13),(3,20)],
        "target_level":"Elevator"
    },
    "Elevator": {
        "background": "./resources/Elevator/_composite_32x32.png",
        "csv": "./resources/Elevator/Collisions.csv",
        "width":544,
        "height":576,
        "startx":512,
        "starty":192,
        "transition_locations":[(35,12)],
        "target_level":"Basement"
    },
    "Basement": {
        "background": "./resources/Basement/_composite.png",
        "csv": "./resources/Basement/Collisions.csv",
    },
    }
}

font = pygame.font.SysFont(config['Font'], 24)



def display_tile_coordinates(player, screen, tile_size=TILESIZE):
    
    x = player.rect.x // tile_size
    y = player.rect.y // tile_size
    text = font.render(f" ({x}, {y})", True, WHITE)
    screen.blit(text, (screen.get_width() - text.get_width() - 10, 10))
    print(f"({x},{y})")

# Load level data
def load_level_data(level):
    background = pygame.image.load(config["Levels"][level]["background"]).convert_alpha()
    #background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    bg_width, bg_height = background.get_size()

    with open(config["Levels"][level]["csv"], newline="\n") as csvfile:
        layout_reader = csv.reader(csvfile)
        layout = [list(map(int, row)) for row in layout_reader]

    # for row in layout:
    #     print(row)

    return background, layout,(bg_width, bg_height)

# Set up the display


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self,level):
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
            if layout[self.rect.y // TILESIZE][(self.rect.x - TILESIZE) // TILESIZE] != 1:
                self.rect.x -= TILESIZE
        if keys[pygame.K_RIGHT]:
            if layout[self.rect.y // TILESIZE][(self.rect.x + TILESIZE) // TILESIZE] != 1:
                self.rect.x += TILESIZE
        if keys[pygame.K_UP]:
            if layout[(self.rect.y - TILESIZE) // TILESIZE][self.rect.x // TILESIZE] != 1:
                self.rect.y -= TILESIZE
        if keys[pygame.K_DOWN]:
            if layout[(self.rect.y + TILESIZE) // TILESIZE][self.rect.x // TILESIZE] != 1:
                self.rect.y += TILESIZE

        #print(self.rect.centerx//TILESIZE,self.rect.centery//TILESIZE)

# Update the camera position based on the player's position
def update_camera_position(player, camera_view, background):
    camera_view.fill((0, 0, 0))
    camera_x = -player.rect.x + CAMERA_WIDTH // 2
    camera_y = -player.rect.y + CAMERA_HEIGHT // 2
    camera_x = player.rect.x 
    camera_y = player.rect.y 
    camera_view.blit(background, (camera_x, camera_y))

# Set the starting level
current_level = "Entrance"

camera_view = pygame.Surface((CAMERA_WIDTH, CAMERA_HEIGHT))
sidebar = pygame.Surface((WIDTH - CAMERA_WIDTH, HEIGHT))
bottom_area = pygame.Surface((WIDTH, HEIGHT - CAMERA_HEIGHT))


screen = pygame.display.set_mode((WIDTH,HEIGHT))
background, layout,screen_size = load_level_data(current_level)

# Update the display surface based on the level background size
pygame.display.set_caption("Multi-level Game")



# Create player
player = Player(current_level)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(layout)
    
    #print(f"{config["Levels"][current_level]['transition_locations']}")
    for transition_location in config["Levels"][current_level]["transition_locations"]:
        # print(f"{current_level} {transition_location}")
        # print(f"px: {player.rect.centerx // TILESIZE} == tlx: {transition_location[0]}")
        # print(f"py: {player.rect.centery // TILESIZE} == tly: {transition_location[1]}")
        if player.rect.centerx // TILESIZE == transition_location[0] and player.rect.centery // TILESIZE == transition_location[1]:
            #print("changing levels")
            
            current_level = config["Levels"][current_level]["target_level"]
            player.rect.x == config["Levels"][current_level]['startx']
            player.rect.y == config["Levels"][current_level]['starty']
            background, layout, screen_size = load_level_data(current_level)
            ##screen = pygame.display.set_mode(screen_size)  # Update the display surface
            break


    # Draw everything
    update_camera_position(player, camera_view, background)
    all_sprites.draw(camera_view)
    display_tile_coordinates(player, camera_view)
    screen.blit(camera_view, (0, 0))
    screen.blit(sidebar, (CAMERA_WIDTH, 0))
    screen.blit(bottom_area, (0, CAMERA_HEIGHT))
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.delay(100)

# Clean up and quit
pygame.quit()
sys.exit()
