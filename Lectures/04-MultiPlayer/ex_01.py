"""
Moves a dot around the screen using the keyboard
No classes or organization, just barebones code.
"""
import pygame

# initialize Pygame
pygame.init()

# set the window size
size = (400, 400)

# create the window
screen = pygame.display.set_mode(size)

# set the window title
pygame.display.set_caption("Move the Dot")

# set the initial position of the dot
dot_position = pygame.math.Vector2(200, 200)

# set the speed of the dot
dot_speed = 1

# run the game loop
running = True
while running:

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # move the dot based on key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        dot_position.y -= dot_speed
    if keys[pygame.K_DOWN]:
        dot_position.y += dot_speed
    if keys[pygame.K_LEFT]:
        dot_position.x -= dot_speed
    if keys[pygame.K_RIGHT]:
        dot_position.x += dot_speed

    # clear the screen
    screen.fill((255, 255, 255))

    # draw the dot
    pygame.draw.circle(screen, (0, 0, 255), dot_position, 10)

    # update the screen
    pygame.display.flip()

# quit Pygame
pygame.quit()