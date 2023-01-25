import pygame

'''
Here is an example of how to use Pygame to rotate an image using the keyboard:

This code will load an image called "image.png" and display it on the screen in 
the center of the window. The image can be rotated using the left and right arrow 
keys on the keyboard. The angle variable controls the angle of rotation, and it's 
increased or decreased by the value of the speed variable depending on the arrow 
key pressed. Each time the angle variable changes, the image is rotated to the 
new angle. The rotated image is then drawn on the screen.
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

    # Rotate the image clockwise or counterclockwise
    if pressed_keys[pygame.K_LEFT]:
        angle -= speed
    if pressed_keys[pygame.K_RIGHT]:
        angle += speed

    # Create a rotated image using the original image and the angle
    rotated_image = pygame.transform.rotate(image, angle)

    # Get the rectangle for the rotated image
    rotated_rect = rotated_image.get_rect()

    # Position the rotated image in the center of the screen
    rotated_rect.center = screen.get_rect().center

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the rotated image on the screen
    screen.blit(rotated_image, rotated_rect)

    # Update the display
    pygame.display.flip()

# Exit Pygame
pygame.quit()
