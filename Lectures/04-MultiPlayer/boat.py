"""
Source: https://python-forum.io/thread-21996.html
User: Windspar
"""

import os
import pygame
from pygame.sprite import Sprite
from math import radians, sin, cos
import sys
  
class Scene:
    """ A scene packages together the major necessary items to display and move things
        in a pygame instance.

        This is pythons version of an abstract base class forcing any subclass to implement
        the proper methods.
    """
    def on_draw(self, surface): pass
    def on_event(self, event): pass
    def on_update(self, delta): pass
  
class Manager:
    """
    """
    def __init__(self, caption, width, height, center=True):
        if center:
            os.environ['SDL_VIDEO_CENTERED'] = '1'
  
        # Basic pygame setup
        pygame.display.set_caption(caption)
        self.surface = pygame.display.set_mode((width, height))
        self.rect = self.surface.get_rect()
        self.clock = pygame.time.Clock()
        self.running = False
        self.delta = 0
        self.fps = 60
  
        # Scene Interface
        self.scene = Scene()
  
    def mainloop(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                self.scene.on_event(event)
  
            self.scene.on_update(self.delta)
            self.scene.on_draw(self.surface)
            pygame.display.flip()
            self.delta = self.clock.tick(self.fps)


class GameImage(Sprite):
    def __init__(self, **kwargs):
        self.screen = kwargs.get("screen", None)
        if not self.screen:
            print("Error! Need surface / screen")
            sys.exit()

        self.imagePath = kwargs.get("image_path", None)

        self.gameWidth = kwargs.get("width", None)
        self.gameHeight = kwargs.get("height", None)

        self.location = kwargs.get("location", None)
        self.x = kwargs.get("x", None)
        self.y = kwargs.get("y", None)

        if self.location:
            self.x = self.location[0]
            self.y = self.location[1]
        else:
            if self.x and self.y:
                self.location = (self.x, self.y)
            else:
                self.location = (0, 0)
                self.x = 0
                self.y = 0

        self.scaleX = kwargs.get("scaleX", 1)
        self.scaleY = kwargs.get("scaleY", 1)
        self.angle = kwargs.get("angle", 0)

        self.image = pygame.image.load(self.imagePath).convert_alpha()
        self.image.convert()

        self.imWidth = self.image.get_width()
        self.imHeight = self.image.get_height()

        self.image = pygame.transform.scale(
            self.image,
            (int(self.imWidth * self.scaleX), int(self.imHeight * self.scaleY)),
        )

        if self.angle:
            self.image = pygame.transform.rotate(self.image, self.angle)

        self.rect = self.image.get_rect()
        self.rect.center = self.location

    def scale(self, scaleX, scaleY):
        pass

    def rotate(self, change):
        """
        https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame

        not implemented
        """
        self.angle += change
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.bbox = self.image.get_rect(center = self.image.get_rect(center = (self.x, self.y)).center)

    def move(self, x=0, y=0):
        self.x += x
        self.y += y
        self.location = (self.x, self.y)
        self.rect.center = self.location

        self.sprite_movement = RotationMovementKeys(self.sprite,
            pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)

class RotationMovementKeys:
    def __init__(self, sprite, up, down, left, right):
        self.sprite = sprite
        self.up = up
        self.down = down
        self.left = left
        self.right = right
  
        self.angle = 0
        self.speed = 0.04
        self.rotation_speed = 0.08
        self.center = pygame.Vector2(self.sprite.rect.center)
        self.set_direction()
  
    def set_direction(self):
        rad = radians(self.angle)
        self.direction = pygame.Vector2(sin(rad), cos(rad))
  
    def do_rotate(self):
        self.sprite.image = pygame.transform.rotate(self.sprite.original_image, self.angle)
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.center = self.center
        self.set_direction()
  
    def on_keydown(self, keys_press, delta):
        if keys_press[self.up]:
            self.center -= self.direction * delta * self.speed
            self.sprite.rect.center = self.center
        elif keys_press[self.down]:
            self.center += self.direction * delta * (self.speed / 2)
            self.sprite.rect.center = self.center
  
        if keys_press[self.right]:
            self.angle = (self.angle - self.rotation_speed * delta) % 360
            self.do_rotate()
        elif keys_press[self.left]:
            self.angle = (self.angle + self.rotation_speed * delta) % 360
            self.do_rotate()


class Player:
    def __init__(self,**kwargs):
        # required
        self.image_path = kwargs.get("image_path", None)
        self.manager = kwargs.get("manager", None)
        
        #optional
        self.scaleX = kwargs.get("scaleX", 1)
        self.scaleY = kwargs.get("scaleY", 1)
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        
        self.sprite = GameImage(self.image_path, self.manager.rect.center, "center")
        self.sprite_movement = RotationMovementKeys(self.sprite,
            pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)

class MultiPlayerExample(Scene):
    def __init__(self, manager):
        self.manager = manager
        self.players = []

    def add_player(self):
        self.players.append(Player(image_path='./images/ships/PT_Boat_One.png',manager=self.manager))
  
    def on_draw(self, surface):
        surface.fill(pygame.Color("black"))
        for player in self.players:
            player.draw(surface)
  
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.manager.running = False
  
    def on_update(self, delta):
        keys = pygame.key.get_pressed()
        self.sprite_movement.on_keydown(keys, delta)
  
def main():
    pygame.init()
    manager = Manager("PT Boat Multiplayer Example", 800, 600)
    manager.scene = MultiPlayerExample(manager)
    manager.scene.add_player()
    manager.mainloop()
  
if __name__ == "__main__":
    main()