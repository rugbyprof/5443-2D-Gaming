import pygame

'''
Pygame example of firing a projectile and killing a sprite.

This code creates a window with the size 700x500, and loads an image called 
"projectile.png" and another image called "sprite.png" into the variables 
projectile_image and sprite_image, respectively. Then it sets the initial 
position of the projectile and the sprite. The projectile is moved to the 
right by a value of projectile_speed every frame. Within the game loop, the 
script checks if the projectile hit the sprite by checking if the x and y 
coordinates of the projectile are within the x and y boundaries of the sprite. 
If the sprite is hit, the script sets the sprite_image to an empty surface 
with the pygame.Surface((0,0)) method and prints "Sprite killed!" on the 
console. Finally, it draws the images on the screen and updates it with 
the flip method.
'''

# Initialize Pygame
pygame.init()

# Set the size of the window
size = (700, 500)
screen = pygame.display.set_mode(size)

# Set the title of the window
pygame.display.set_caption("Pygame Projectile and Sprite Example")

# Load the projectile image
projectile_image = pygame.image.load("projectile.png") # 16x16 image

# Load the sprite image
sprite_image = pygame.image.load("sprite.png") # 153x188

# Set the starting position of the projectile
projectile_x = 0
projectile_y = 250

# Set the starting position of the sprite
sprite_x = 600
sprite_y = 150

# Set the projectile speed
projectile_speed = 3

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # added by Terry
    screen.fill((0,0,0))

    # Move the projectile
    projectile_x += projectile_speed

    # Check if the projectile hit the sprite
    if (projectile_x > sprite_x and projectile_x < sprite_x+153) and (projectile_y > sprite_y and projectile_y < sprite_y+188):
        # Kill the sprite
        sprite_image = pygame.Surface((0,0))
        print("Sprite killed!")

    # Draw the projectile on the screen
    screen.blit(projectile_image, (projectile_x, projectile_y))

    # Draw the sprite on the screen
    screen.blit(sprite_image, (sprite_x, sprite_y))

    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
