import pygame
import sys
import csv

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)

# Player starting position
START_X = 100
START_Y = 100

# Level transition locations
TRANSITION_LOCATIONS = {
    "Entrance": (400, 300),
    "Elevator": (200, 100),
    "Basement": (600, 400),
}

# Level data
LEVELS = {
    "Entrance": {
        "background": "./resources/Entrance/_composite.png",
        "csv": "./resources/Entrance/Collosions.csv",
    },
    "Elevator": {
        "background": "./resources/Elevator/_composite.png",
        "csv": "./resources/Elevator/Collosions.csv",
    },
    "Basement": {
        "background": "./resources/Basement/_composite.png",
        "csv": "./resources/Basement/Collosions.csv",
    },
}

# Load level data
def load_level_data(level):
    background = pygame.image.load(LEVELS[level]["background"]).convert_alpha()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    with open(LEVELS[level]["csv"], newline="") as csvfile:
        layout_reader = csv.reader(csvfile)
        layout = [list(map(int, row)) for row in layout_reader]

    return background, layout

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-level Game")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./resources/player.png").convert_alpha()
        # self.image = pygame.Surface((32, 32))
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, layout):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if layout[self.rect.y // 32][(self.rect.x - 32) // 32] != 1:
                self.rect.x -= 32
        if keys[pygame.K_RIGHT]:
            if layout[self.rect.y // 32][(self.rect.x + 32) // 32] != 1:
                self.rect.x += 32
        if keys[pygame.K_UP]:
            if layout[(self.rect.y - 32) // 32][self.rect.x // 32] != 1:
                self.rect.y -= 32
        if keys[pygame.K_DOWN]:
            if layout[(self.rect.y + 32) // 32][self.rect.x // 32] != 1:
                self.rect.y += 32

# Set the starting level
current_level = "Entrance"
background, layout = load_level_data(current_level)

# Create player
player = Player(START_X, START_Y)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update player and check for level transitions
    player.update(layout)
    for level, transition_location in TRANSITION_LOCATIONS.items():
        if player.rect.topleft == transition_location and level != current_level:
            current_level = level
            background, layout = load_level_data(current_level)
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
