import pygame

'''
Create a pygame example that loads a spritesheet.

This code creates a window with the size 700x500, and loads an image called 
"spritesheet.png" into the variable spritesheet. The dimensions of each 
animation frame are defined as frame_width = 64 and frame_height = 64. The 
frame_x, frame_y variables are used to specify the starting position of the 
animation frame within the spritesheet. In this example is always (0,0). The 
current animation frame is obtained by calling the subsurface method on the 
spritesheet, which takes four arguments: the x and y coordinates of the top-left 
corner of the frame, and the width and height of the frame. The current frame is 
then drawn on the screen using the blit method, and the screen is updated using 
the flip method.
'''

# Initialize Pygame
pygame.init()

# Set the size of the window
size = (700, 500)
screen = pygame.display.set_mode(size)

# Set the title of the window
pygame.display.set_caption("Pygame Spritesheet Example")

# Load the spritesheet
spritesheet = pygame.image.load("spritesheet.png")

# Define the dimensions of each animation frame
frame_width = 60
frame_height = 60

# Define the starting position of the animation frame
frame_x = 0
frame_y = 0

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current animation frame from the spritesheet
    current_frame = spritesheet.subsurface((frame_x, frame_y, frame_width, frame_height))

    # Draw the current frame on the screen
    screen.blit(current_frame, (50, 50))

    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
