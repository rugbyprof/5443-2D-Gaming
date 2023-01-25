import pygame

'''
Here is an example of how to use Pygame to rotate a group of blocks as a single entity using Pygame:

This code creates a group of blocks, and adds some blocks to the group. The blocks are 
arranged in a line and can be rotated using the left and right arrow keys on the keyboard. 
The angle variable controls the angle of rotation, and it's increased or decreased by the 
value of the speed variable depending on the arrow key pressed. The pygame.transform.rotate() 
function is used to rotate the group of blocks. The original position of the group is stored, 
so that the rotated group is centered in the same position. Each time the angle variable changes, 
the group of blocks is rotated to the new angle and then it's drawn on the screen.
'''

# Initialize Pygame
pygame.init()

# Set the window size
size = (700, 500)
screen = pygame.display.set_mode(size)

# Create a group for the blocks
block_group = pygame.sprite.Group()

# Add some blocks to the group
for i in range(5):
    block = pygame.sprite.Sprite()
    block.image = pygame.Surface((50, 50))
    block.rect = block.image.get_rect()
    block.rect.x = 50 * i
    block.rect.y = 50
    block_group.add(block)

# Set the angle to rotate the group by
angle = 0

# Speed of the rotation
speed = 5

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current pressed keys
    pressed_keys = pygame.key.get_pressed()

    # Rotate the group clockwise or counterclockwise
    if pressed_keys[pygame.K_LEFT]:
        angle -= speed
    if pressed_keys[pygame.K_RIGHT]:
        angle += speed

    # Get the original position of the group
    original_rect = block_group.sprites()[0].rect.copy()

    # Rotate the group
    rotated_group = pygame.transform.rotate(block_group, angle) ## error!!

    # Get the rectangle for the rotated group
    rotated_rect = rotated_group.get_rect(center=original_rect.center)

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the rotated group on the screen
    screen.blit(rotated_group, rotated_rect)

    # Update the display
    pygame.display.flip()

# Exit Pygame
pygame.quit()
