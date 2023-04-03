#!/usr/bin/env python3

# Import and initialize the pygame library
import pygame
from pygame.math import Vector2
from pygame import transform
import random
from comms import CommsSender, CommsListener
import sys
import json
import math
import os

"""
GameObject: extends pygame.sprite.Sprite and is instantiated with an initial position tuple (x,y) and a pygame image. 
    Contains methods to draw, move, and check for collisions with other game objects. 
    Uses pygame.math.Vector2 for position and velocity calculations.

SpaceShip: extends GameObject and includes the necessary methods to move, rotate left, rotate right, and accelerate. 
    Uses pygame.math.Vector2 for position and velocity calculations.

NPCSpaceShip: extends SpaceShip and includes methods to smoothly target and follow the closest SpaceShip.
    Uses pygame.math.Vector2 for position and velocity calculations. Implements the choose_target, rotate_toward_target, 
       and follow_target methods to select the closest SpaceShip as the target, rotate towards it, and follow it in a controlled manner.


"""

UP = Vector2(0, -1)
ASSETS = "./assets/sprites/"
WIDTH = 500
HEIGHT = 500


def wrap_position(position):
    x, y = position
    w, h = (WIDTH, HEIGHT)
    return Vector2(x % w, y % h)


def load_sprite(name, with_alpha=True):
    path = f"assets/sprites/{name}.png"
    loaded_sprite = pygame.image.load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


# class GameObject2:
#     def __init__(self, position, sprite, velocity):
#         self.position = Vector2(position)
#         self.sprite = sprite
#         self.radius = sprite.get_width() / 2
#         self.velocity = Vector2(velocity)

#     def draw(self, surface):
#         blit_position = self.position - Vector2(self.radius)
#         surface.blit(self.sprite, blit_position)

#     def move(self, surface):
#         self.position = wrap_position(self.position + self.velocity, surface)
#         # print(f"pos: {self.position}")

#     def collides_with(self, other_obj):
#         distance = self.position.distance_to(other_obj.position)
#         return distance < self.radius + other_obj.radius


class MySprite(pygame.sprite.Sprite):
    def __init__(self, pos, image_file):
        super().__init__()
        self.sprite = pygame.image.load(
            os.path.join(ASSETS, image_file + ".png")
        ).convert_alpha()
        self.image = self.sprite
        self.rect = self.sprite.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class GameObject(MySprite):
    def __init__(self, surface, position, imageName):
        super().__init__(position, imageName)
        self.surface = surface
        self.position = Vector2(position)
        self.velocity = UP
        self.radius = self.sprite.get_width() / 2

    # def draw(self, surface):
    #     surface.blit(self.sprite, self.position)

    # def draw(self):
    #     blit_position = self.position - Vector2(self.radius)
    #     self.surface.blit(self.sprite, blit_position)
    #     print("DRAWING")

    def draw(self):
        angle = self.direction.angle_to(UP)
        rotated_surface = transform.rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        self.surface.blit(rotated_surface, blit_position)

    # def move(self):
    #     print("moving")
    #     self.position += self.velocity

    def move(self):
        self.position = wrap_position(self.position + self.velocity)
        # print(f"pos: {self.position}")

    def collides_with_other(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

    def collides_with_group(self, group):
        return pygame.sprite.spritecollide(self, group, False)


class SpaceShip(GameObject):
    def __init__(self, surface, position, imageName):
        super().__init__(surface, position, imageName)
        self.speed = 2
        self.rotation_speed = 3
        self.direction = pygame.math.Vector2(0, -1)

    def update(self):
        self.move()

    def rotate_left(self):
        self.direction.rotate_ip(self.rotation_speed)
        print(self.direction)

    def rotate_right(self):
        self.direction.rotate_ip(-self.rotation_speed)
        print(self.direction)

    def accelerate(self):
        self.velocity += self.direction * self.speed


class NPCSpaceShip(SpaceShip):
    def __init__(self, surface, position, image, all_sprites, player_sprites):
        super().__init__(surface, position, image)
        self.target = None
        self.all_sprites = all_sprites
        self.player_sprites = player_sprites

    def choose_target(self):
        closest_dist = math.inf
        closest_ship = None
        for ship in self.player_sprites:
            dist = self.position.distance_to(ship.position)
            if dist < closest_dist:
                closest_dist = dist
                closest_ship = ship
        self.target = closest_ship

    def rotate_toward_target(self):
        if self.target is not None:
            target_direction = self.target.position - self.position
            target_angle = math.degrees(
                math.atan2(target_direction.y, target_direction.x)
            )
            diff_angle = (
                target_angle - self.direction.angle_to(pygame.math.Vector2(0, -1))
            ) % 360
            if diff_angle < 180:
                self.direction.rotate_ip(min(diff_angle, self.rotation_speed))
            else:
                self.direction.rotate_ip(-min(360 - diff_angle, self.rotation_speed))

    def follow_target(self):
        if self.target is not None:
            distance = self.position.distance_to(self.target.position)
            if distance > 50:
                target_speed = self.target.velocity.magnitude()
                lead_time = distance / (self.speed + target_speed)
                target_pos = self.target.position + self.target.velocity * lead_time
                desired_direction = (target_pos - self.position).normalize()
                steering_force = (desired_direction - self.direction) * 0.1
                self.velocity += steering_force * self.speed

    def update(self):
        self.choose_target()
        self.rotate_toward_target()
        self.follow_target()
        self.move()


pygame.init()

screen = pygame.display.set_mode([WIDTH, HEIGHT])


def main():
    """
    In order to use these classes, you would need to create instances of SpaceShip and NPCSpaceShip,
    and add them to separate sprite groups. For example:
    """
    all_sprites = pygame.sprite.Group()
    player_sprites = pygame.sprite.Group()
    npc_sprites = pygame.sprite.Group()

    player_ship = SpaceShip(screen, (100, 100), "space_ship3_40x40")
    npc_ship = NPCSpaceShip(
        screen, (200, 200), "space_ship5_40x40", all_sprites, player_sprites
    )

    all_sprites.add(player_ship, npc_ship)
    player_sprites.add(player_ship)
    npc_sprites.add(npc_ship)

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        is_key_pressed = pygame.key.get_pressed()

        # Update game objects
        player_ship.rotate_left() if is_key_pressed[pygame.K_LEFT] else None
        player_ship.rotate_right() if is_key_pressed[pygame.K_RIGHT] else None
        player_ship.accelerate() if is_key_pressed[pygame.K_UP] else None

        player_ship.update()
        npc_ship.update()

        # Draw game objects
        screen.fill((0, 0, 0))

        for sprite in all_sprites:
            sprite.draw()
        # all_sprites.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
