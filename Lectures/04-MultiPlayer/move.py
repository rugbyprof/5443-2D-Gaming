"""
Source: https://python-forum.io/thread-21996.html
User: Windspar
"""

import os
import pygame
from pygame.sprite import Sprite
from math import radians, sin, cos
  
class Scene:
    def on_draw(self, surface): pass
    def on_event(self, event): pass
    def on_update(self, delta): pass
  
class Manager:
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
  
class BaseSprite(Sprite):
    def __init__(self, image, position, anchor="topleft"):
        Sprite.__init__(self)
        self.original_image = image
        self.image = image
        self.rect = image.get_rect()
        setattr(self.rect, anchor, position)
  
    def draw(self, surface):
        surface.blit(self.image, self.rect)
  
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
    def __init__(self, manager):
        self.rectangle = pygame.Surface((10, 20), pygame.SRCALPHA)
        self.rectangle.fill(pygame.Color('dodgerblue'))
        self.rectangle.fill(pygame.Color('white'), (2, 2, 6, 3))
        self.sprite = BaseSprite(self.rectangle, manager.rect.center, "center")
        self.sprite_movement = RotationMovementKeys(self.sprite,
            pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)


class Example(Scene):
    def __init__(self, manager):
        self.manager = manager
        self.player = Player(manager)
  
  
    def on_draw(self, surface):
        surface.fill(pygame.Color("black"))
        self.player.sprite.draw(surface)
  
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.manager.running = False
  
    def on_update(self, delta):
        keys = pygame.key.get_pressed()
        self.player.sprite_movement.on_keydown(keys, delta)
  
def main():
    pygame.init()
    manager = Manager("Rotation Example", 800, 600)
    manager.scene = Example(manager)
    manager.mainloop()
  
if __name__ == "__main__":
    main()