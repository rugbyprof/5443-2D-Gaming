import pygame

'''
Here is an example of how to use Pygame to check for collisions between two groups of sprites:

This code creates two groups of sprites, group1 and group2, and adds some sprites 
to each group. The groupcollide function is used to check for collisions between 
the sprites in group1 and group2. If a collision is detected, the function returns 
a dictionary with the collided sprites. The number of collisions is printed to the 
screen. You can modify the code to take action based on the collisions, such as 
removing sprites or updating their position.
'''

# Initialize Pygame
pygame.init()

# Set the window size
size = (700, 500)
screen = pygame.display.set_mode(size)

# Create a group for the first set of sprites
group1 = pygame.sprite.Group()

# Add some sprites to the first group
for i in range(5):
    sprite1 = pygame.sprite.Sprite()
    sprite1.image = pygame.Surface((50, 50))
    sprite1.rect = sprite1.image.get_rect()
    sprite1.rect.x = 50 * i
    sprite1.rect.y = 50
    group1.add(sprite1)

# Create a group for the second set of sprites
group2 = pygame.sprite.Group()

# Add some sprites to the second group
for i in range(5):
    sprite2 = pygame.sprite.Sprite()
    sprite2.image = pygame.Surface((50, 50))
    sprite2.rect = sprite2.image.get_rect()
    sprite2.rect.x = 50 * i
    sprite2.rect.y = 100
    group2.add(sprite2)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check for collisions between the sprites in the two groups
    collisions = pygame.sprite.groupcollide(group1, group2, False, False)

    # Print the number of collisions
    print("Number of collisions:", len(collisions))

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the sprites on the screen
    group1.draw(screen)
    group2.draw(screen)

    # Update the display
    pygame.display.flip()

# Exit Pygame
pygame.quit()
