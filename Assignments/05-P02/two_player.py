import pygame
import random

# Initialize pygame
pygame.init()

# Set the dimensions of the window
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# Set the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set the font
FONT_SIZE = 24
FONT = pygame.font.Font(None, FONT_SIZE)

# Create the game window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Multiplayer Game")

# Create the players
player1_x = 50
player1_y = 50
player2_x = 590
player2_y = 430

# Define the player movement speed
PLAYER_SPEED = 5

# Create the game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Get the pressed keys
    keys = pygame.key.get_pressed()

    # Move the players
    if keys[pygame.K_LEFT]:
        player1_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player1_x += PLAYER_SPEED
    if keys[pygame.K_UP]:
        player1_y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        player1_y += PLAYER_SPEED

    if keys[pygame.K_a]:
        player2_x -= PLAYER_SPEED
    if keys[pygame.K_d]:
        player2_x += PLAYER_SPEED
    if keys[pygame.K_w]:
        player2_y -= PLAYER_SPEED
    if keys[pygame.K_s]:
        player2_y += PLAYER_SPEED

    # Draw the players
    WINDOW.fill(WHITE)
    pygame.draw.circle(WINDOW, RED, (player1_x, player1_y), 10)
    pygame.draw.circle(WINDOW, BLUE, (player2_x, player2_y), 10)

    # Update the screen
    pygame.display.update()
