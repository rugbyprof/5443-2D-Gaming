"""
Sprite Helper

Description:
    Loading a sprite animation and displaying it. 
    Problems using a single instance of image.
"""
# Import and initialize the pygame library
import pygame
import json
import sys
import os
import glob


# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)



class Explosion(pygame.sprite.Sprite):

    def __init__(self, **kwargs):

        # Initiate this sprite
        pygame.sprite.Sprite.__init__(self)

        # get location of sprites for this animation
        fx_sprites = kwargs.get('fx_sprites', None)

        # if not throw error
        if not fx_sprites:
            print("Error: Need location of fx_sprites!")
            sys.exit(0)

        self.center = kwargs.get('loc', (0, 0))

        # This function finds the json file and loads all the
        # image names into a list
        self.images = glob.glob(os.path.join('../media/fx/explosion_01', '*.png'))
        self.images.sort()

        # container for all the pygame images
        self.frames = []

        # load images and "convert" them. (see link at top for explanation)
        for image in self.images:
            self.frames.append(pygame.image.load(image))

        # animation variables
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 0  # smaller = faster

        # prime the animation
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def setLocation(self, loc):
        """ Set the center of the explosion
        """
        self.center = loc
        self.rect.center = loc

    def update(self):
        """ Overloaded method from sprite which gets called by the game loop when 
            a sprite group gets updated
        """
        now = pygame.time.get_ticks()  # get current game clock
        if now - self.last_update > self.frame_rate:  #
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.frames):
                self.kill()
                self.frame = 0
            else:
                center = self.rect.center
                self.image = self.frames[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def main():

    print(os.getcwd())
    pygame.init()

    # sets the window title
    pygame.display.set_caption("BareBones 001")

    # Game size of game window from config
    width = 800
    height = 600

    # Set up the drawing window
    screen = pygame.display.set_mode((width, height))

    # load our background
    background = pygame.image.load('../media/backgrounds/tile_1000x1000_40_light.png')


    # sprite group to handle all the visuals
    all_sprites = pygame.sprite.Group()

    # help control event timing
    clock = pygame.time.Clock()

    e = Explosion(fx_sprites='./media/fx/explosion_01')

    # Run until the user asks to quit
    # game loop
    running = True

    while running:

        clock.tick(60)

        # fill screen with white
        screen.fill((154,205,50))

        # show background grid (no moving it)
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                event.key

            if event.type == pygame.KEYUP:
                event.key

            if event.type == pygame.MOUSEMOTION:
                pass

            if event.type == pygame.MOUSEBUTTONUP:
                print(pygame.mouse.get_pos())
                e.setLocation(pygame.mouse.get_pos())
                all_sprites.add(e)

        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()


if __name__ == '__main__':

    main()
