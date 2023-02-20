"""
After we saw how to control each player using event logic,
could we use similar logic to do the same for a multiplayer game?
Instead of directly controlling each player, we could let commands 
comming from a specific player be passed to a "dot" instance to move
it. 

First however, lets get a comms example that will let players wanting
to be added to the same game get added and basically "appear" when they
send a message to the same game queue you are on. 
"""
import pygame
from random import randint
import sys


class Dot:
    def __init__(self,screen,player):
        self.screen = screen    # copy of screen to display dot on

        self.player = player    # we need a player name for messaging

        self.creds = {
            "exchange": 'game1',
            "port": '5672',
            "host": 'terrywgriffin.com',
            "user": self.player,
            "password": self.player+'2023!!!!!'
        }


        # set the initial position of the dot
        self.dot_position = pygame.math.Vector2(randint(25,400), randint(25,400))
        self.speed = 1
        self.color = (randint(0,256),randint(0,256),randint(0,256))

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
        pygame.draw.circle(self.screen, self.color , self.dot_position, 10)


# initialize Pygame
pygame.init()

# set the window size
size = (400, 400)

# create the window
screen = pygame.display.set_mode(size)

# set the window title
pygame.display.set_caption("Move the Dot")

# add 10 dots to our game screen
dots = []
for d in range(10):
    dots.append(Dot(screen))

# who am i currently moving
currentDot = 0

# create list for lookup for keys 0-9
# The keys 0-9 are ascii 48-57 
numericKeys = [x for x in range(0,58)]


if __name__=='__main__':
    if len(sys.argv) < 2:
        print("Error: Need playername: (e.g. player-1, player-2, player-n)")
        sys.exit()


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

                # get the keys 0-9 if pressed
                elif event.key in numericKeys:
                    print(f"You pressed: {48-event.key}")
                    # choose current dot by which key pressed
                    currentDot = 48 - event.key



        # move the dot based on key input
        keys = pygame.key.get_pressed()
        dots[currentDot].eventHandler(keys)

        # clear the screen
        screen.fill((255, 255, 255))
        for i in range(10):
            dots[i].draw()


        # update the screen
        pygame.display.flip()

    # quit Pygame
    pygame.quit()