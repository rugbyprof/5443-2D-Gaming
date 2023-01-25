import pygame

'''
Here is an example of how to use Pygame to rotate an image:

This code will load an image called "image.png", rotate it by 45 degrees, 
and then display it on the screen in the center of the window. Each time 
through the game loop, the rotated image is drawn on the screen. You can 
change the angle value to rotate the image by a different amount.
'''

# Initialize Pygame
pygame.init()

# Set the window size
size = (700, 500)
screen = pygame.display.set_mode(size)

# Load the image and get its rectangle
image = pygame.image.load("image.png")
image_rect = image.get_rect()

# Set the angle to rotate the image by
angle = 45

# Create a rotated image using the original image and the angle
rotated_image = pygame.transform.rotate(image, angle)

# Get the rectangle for the rotated image
rotated_rect = rotated_image.get_rect()

# Position the rotated image in the center of the screen
rotated_rect.center = screen.get_rect().center

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the rotated image on the screen
    screen.blit(rotated_image, rotated_rect)

    # Update the display
    pygame.display.flip()

# Exit Pygame
pygame.quit()
