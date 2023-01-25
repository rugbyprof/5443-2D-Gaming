import pygame

'''
Here is an example of how to use Pygame to move an image with the keyboard:

This code will load an image called "image.png" and display it on the 
screen in the center of the window. The image can be moved using the 
arrow keys on the keyboard. The speed variable controls how fast the 
image moves, you can adjust the value of speed to make the image move 
faster or slower.
'''

# Initialize Pygame
pygame.init()

# Set the window size
size = (700, 500)
screen = pygame.display.set_mode(size)

# Load the image and get its rectangle
image = pygame.image.load("image.png")
image_rect = image.get_rect()

# Set the initial position of the image
image_rect.x = 350
image_rect.y = 250

# Speed of the image
speed = 5

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current pressed keys
    pressed_keys = pygame.key.get_pressed()

    # Move the image left or right
    if pressed_keys[pygame.K_LEFT]:
        image_rect.x -= speed
    if pressed_keys[pygame.K_RIGHT]:
        image_rect.x += speed

    # Move the image up or down
    if pressed_keys[pygame.K_UP]:
        image_rect.y -= speed
    if pressed_keys[pygame.K_DOWN]:
        image_rect.y += speed

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the image on the screen
    screen.blit(image, image_rect)

    # Update the display
    pygame.display.flip()

# Exit Pygame
pygame.quit()
