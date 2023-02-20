"""
For multiplayer we probably need to organize a little bit
at least in regards to a player (the dot). This file takes 
necessary code for the dots location and other factors abd
places them in a single class making it easier to create more
than one dot if necessary.
"""
import pygame

class Dot:
    def __init__(self,screen):
        self.screen = screen    # copy of screen to display dot on
        # set the initial position of the dot
        self.dot_position = pygame.math.Vector2(200, 200)
        self.speed = 1

    def eventHandler(self,keys):
        """ Get the keys from main, then adjust position based
            on keys pressed
        """
        if keys[pygame.K_UP]:
            self.dot_position.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.dot_position.y += self.speed
        if keys[pygame.K_LEFT]:
            self.dot_position.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.dot_position.x += self.speed

    def draw(self):
        # draw the dot
        pygame.draw.circle(self.screen, (0, 0, 255), self.dot_position, 10)

# initialize Pygame
pygame.init()

# set the window size
size = (400, 400)

# create the window
screen = pygame.display.set_mode(size)

# set the window title
pygame.display.set_caption("Move the Dot")


dot = Dot(screen)

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
    dot.eventHandler(keys)

    # clear the screen
    screen.fill((255, 255, 255))
    dot.draw()


    # update the screen
    pygame.display.flip()

# quit Pygame
pygame.quit()