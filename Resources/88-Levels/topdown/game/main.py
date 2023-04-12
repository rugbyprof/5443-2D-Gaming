import pygame
import sys
import csv
from rich import print

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)

# Player starting position
START_X = 32
START_Y = 320

TILESIZE = 32

# Level transition locations
TRANSITION_LOCATIONS = {
    "Entrance": (1136, 432),
    "Elevator": (200, 100),
    "Basement": (600, 400),
}

# Level data
LEVELS = {
    "Entrance": {
        "background": "./resources/Entrance/_composite_32x32.png",
        "csv": "./resources/Entrance/Collisions.csv",
        "width":1152,
        "height":640,
        "startx":32,
        "starty":320,
        "transition_locations":[(35,12),(3,10)],
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

# Load level data
def load_level_data(level):
    background = pygame.image.load(LEVELS[level]["background"]).convert_alpha()
    #background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    bg_width, bg_height = background.get_size()

    with open(LEVELS[level]["csv"], newline="\n") as csvfile:
        layout_reader = csv.reader(csvfile)
        layout = [list(map(int, row)) for row in layout_reader]

    # for row in layout:
    #     print(row)

    return background, layout,(bg_width, bg_height)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-level Game")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self,level):
        super().__init__()
        self.image = pygame.image.load("./resources/player.png").convert_alpha()
        # self.image = pygame.Surface((32, 32))
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        LEVELS[level]["startx"]

        self.rect.x = LEVELS[level]["startx"]
        self.rect.y = LEVELS[level]["starty"]

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

        print(self.rect.centerx//TILESIZE,self.rect.centery//TILESIZE)

# Set the starting level
current_level = "Entrance"
background, layout,screen_size = load_level_data(current_level)

# Update the display surface based on the level background size
screen = pygame.display.set_mode(screen_size)

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
    print(f"{LEVELS[current_level]['transition_locations']}")
    for transition_location in LEVELS[current_level]["transition_locations"]:
        # print(f"{current_level} {transition_location}")
        # print(f"px: {player.rect.centerx // TILESIZE} == tlx: {transition_location[0]}")
        # print(f"py: {player.rect.centery // TILESIZE} == tly: {transition_location[1]}")
        if player.rect.centerx // TILESIZE == transition_location[0] and player.rect.centery // TILESIZE == transition_location[1]:
            print("changing levels")
            
            current_level = LEVELS[current_level]["target_level"]
            player.rect.x == LEVELS[current_level]['startx']
            player.rect.y == LEVELS[current_level]['starty']
            background, layout, screen_size = load_level_data(current_level)
            screen = pygame.display.set_mode(screen_size)  # Update the display surface
            break


    # Draw everything
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.delay(100)

# Clean up and quit
pygame.quit()
sys.exit()
