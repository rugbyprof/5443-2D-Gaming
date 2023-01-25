import pygame
import math

'''
Pygame example of firing a projectile that follows a ballistic path.

This code creates a window with the size 700x500, and loads an image called "projectile.png" 
into the variable projectile_image. It sets the initial position of the projectile and the 
angle and speed of the projectile, in this case 45 degrees and 5 units/frame. The script 
converts the angle to radians using the math.radians(angle) method. Then it calculates the 
initial velocity of the projectile in the x and y direction using the math.cos(angle_rad) 
and math.sin(angle_rad) methods. The script applies gravity to the projectile's vertical 
velocity every frame by adding the value of g to it. Then it updates the projectile's 
position based on its velocity and draws the projectile on the screen. Finally, it updates 
the screen with the flip method.
'''

# Initialize Pygame
pygame.init()

# Set the size of the window
size = (700, 500)
screen = pygame.display.set_mode(size)

# Set the title of the window
pygame.display.set_caption("Pygame Ballistic Projectile Example")

# Load the projectile image
projectile_image = pygame.image.load("projectile.png")

# Set the starting position of the projectile
projectile_x = 50
projectile_y = 50

# Set the angle and speed of the projectile
angle = 45 # in degrees
speed = 5

# Convert the angle to radians
angle_rad = math.radians(angle)

# Calculate the initial velocity of the projectile in the x and y direction
projectile_vx = speed * math.cos(angle_rad)
projectile_vy = -speed * math.sin(angle_rad)

# Set the gravitational acceleration
g = 0.1

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #added by Griffin
    screen.fill((0,0,0))

    # Apply gravity to the projectile's vertical velocity
    projectile_vy += g

    # Update the projectile's position based on its velocity
    projectile_x += projectile_vx
    projectile_y += projectile_vy

    # Draw the projectile on the screen
    screen.blit(projectile_image, (projectile_x, projectile_y))

    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
