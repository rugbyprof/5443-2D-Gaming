import pygame

'''
Provide a pygame example that shows a splash screen then loads another screen.

This code creates a window with the size 700x500, and loads an image called "splash_screen.png" 
into the variable splash_image. The splash screen is drawn on the screen using the blit method, 
and the screen is updated using the flip method. Then the script waits 3 seconds using the 
pygame.time.wait(3000) method. After the 3 seconds have passed, the script loads a new image 
called "next_screen.png" and displays it on the screen.

You can also use the pygame.time.set_timer(event, milliseconds) method to schedule an event 
that will be fired after the specified number of milliseconds have passed, and you can use 
the pygame.event.get() method to check for the scheduled event in the game loop, instead of 
using the pygame.time.wait(3000) method.
'''

# Initialize Pygame
pygame.init()

# Set the size of the window
size = (700, 500)
screen = pygame.display.set_mode(size)

# Set the title of the window
pygame.display.set_caption("Pygame Splash Screen Example")

# Load the splash screen image
splash_image = pygame.image.load("splash_screen.png")

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the splash screen image on the screen
    screen.blit(splash_image, (0, 0))

    # Update the screen
    pygame.display.flip()

    # Wait for 3 seconds
    pygame.time.wait(3000)

    # Load the next screen
    next_screen = pygame.image.load("next_screen.png")
    screen.blit(next_screen, (0, 0))
    pygame.display.flip()

# Quit Pygame
pygame.quit()
