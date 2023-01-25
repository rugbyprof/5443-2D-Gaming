import pygame

'''
Show me a pygame gravity example.

This code creates a window with the size 700x500 and a ball with the starting position (50,50), a velocity of (0,0), 
and a radius of 20px. The ball's velocity will increase by a value of g = 0.1 every frame. The ball is drawn on the 
screen every frame using the draw.circle method.
'''
# Initialize Pygame
pygame.init()

# Set the size of the window
size = (700, 500)
screen = pygame.display.set_mode(size)

# Set the title of the window
pygame.display.set_caption("Pygame Gravity Example")

# Create a ball with a starting position and velocity
ball_x = 50
ball_y = 50
ball_vx = 0
ball_vy = 0
ball_radius = 20

# Set the gravitational acceleration
g = 0.01

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))

    # Apply gravity to the ball's vertical velocity
    ball_vy += g

    # Update the ball's position based on its velocity
    ball_x += ball_vx
    ball_y += ball_vy

    # Draw the ball on the screen
    pygame.draw.circle(screen, (255, 255, 255), (int(ball_x), int(ball_y)), ball_radius)

    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
