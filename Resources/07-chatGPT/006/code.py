import pygame

'''
Pygame example of a sound being played when a projectile hits a sprite.

This code is similar to the previous example, but it also loads a sound file called "hit.wav" 
into the variable hit_sound using the pygame.mixer.Sound() method. Within the game loop, it 
checks if the projectile hit the sprite, and if it did, it plays the sound effect by calling 
the play() method on the hit_sound object. When the sound is played, the script also kills 
the sprite in the same way as the previous example. This way, the sound is played when the 
sprite is hit by the projectile and the sprite disappears from the screen.
'''

# Initialize Pygame
pygame.init()

# Set the size of the window
size = (700, 500)
screen = pygame.display.set_mode(size)

# Set the title of the window
pygame.display.set_caption("Pygame Sound Effect Example")

# Load the projectile image
projectile_image = pygame.image.load("projectile.png")

# Load the sprite image
sprite_image = pygame.image.load("sprite.png")

# Set the starting position of the projectile
projectile_x = 50
projectile_y = 50

# Set the starting position of the sprite
sprite_x = 200
sprite_y = 200

# Set the projectile speed
projectile_speed = 5

# Load the sound effect
hit_sound = pygame.mixer.Sound("hit.wav")

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the projectile
    projectile_x += projectile_speed

    # Check if the projectile hit the sprite
    if (projectile_x > sprite_x and projectile_x < sprite_x + 64) and (projectile_y > sprite_y and projectile_y < sprite_y + 64):
        # Play the sound effect
        hit_sound.play()
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
