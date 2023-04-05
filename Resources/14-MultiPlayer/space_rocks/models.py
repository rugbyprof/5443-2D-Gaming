from pygame.math import Vector2
from pygame import transform
from pygame import time

import random
from utils import get_random_velocity, load_sound, load_sprite, wrap_position, distance
import math

import json

UP = Vector2(0, -1)


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)
        # print(f"pos: {self.position}")

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.25
    BULLET_SPEED = 100

    def __init__(self, position, bullet_callback=None, ship="space_ship_40x40"):
        self.bullet_callback = bullet_callback
        self.laser_sound = load_sound("laser")
        self.image = ship
        # Make a copy of the original UP vector
        self.direction = Vector2(UP)

        super().__init__(position, load_sprite(ship), Vector2(0))

    def __str__(self):
        """String version of this objects state"""
        attributes = {}
        attributes["ship_image"] = self.image
        attributes["position"] = (self.position.x, self.position.y)
        return json.dumps(attributes)

    def getAttributes(self):
        """Returns the basic attributes needed to set up a copy of this object
        possibly in a multiplayer setting.
        """
        return self.__str__()

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self, velocity=None):
        if velocity != None:
            self.velocity = Vector2(velocity)
        else:
            self.velocity += self.direction * self.ACCELERATION

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = transform.rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.bullet_callback(bullet)
        self.laser_sound.play()


class NPC(Spaceship):
    def __init__(
        self,
        position,
        bullet_callback,
        ship="space_ship5_40x40",
        targets=[],
        other_npcs=None,
    ):
        self.targets = targets
        self.acceleration = 0.10
        self.speed = random.randint(4, 9)
        self.rotation_speed = random.randint(3, 5)
        self.direction = Vector2(0, 1)
        self.prevVelocity = Vector2(0)
        self.last_randrot_direction = None
        self.tracking_velocity = random.uniform(1.70, 3.0)
        self.other_npcs = other_npcs
        self.bullet_callback = bullet_callback

        self.last_shot_time = 0  # clock tick of last shot
        self.shoot_delay = 250  # millisecond delay between shots
        self.max_shots = self.shoot_delay * 4  # max shots in a group or in a row
        self.shot_time_total = 0  # sum of group shots
        self.shoot_window = (
            1100  # max time a group of shots can be grouped before cooldown
        )
        self.shoot_cooldown = 2000  # delay between shout groupings
        self.cooldown = 0

        super().__init__(position, bullet_callback, ship)

    def accelerate(self):
        self.velocity += self.direction * self.acceleration

    def choose_target(self):
        closestDistance = pow(2, 20)
        closestTarget = None
        for target in self.targets:
            d = distance(target.position, self.position)
            if distance(target.position, self.position) < closestDistance:
                closestTarget = target
                closestDistance = d

        self.target = closestTarget

    def rotate(self):
        if self.target is not None:
            target_direction = self.target.position - self.position
            target_angle = math.degrees(
                math.atan2(target_direction.y, target_direction.x)
            )
            # Added this so it would rotate in proper direction
            target_angle *= -1

            diff_angle = (target_angle - self.direction.angle_to(Vector2(0, 0))) % 360

            if diff_angle < 180:
                self.direction.rotate_ip(-min(360 - diff_angle, self.rotation_speed))
            else:
                self.direction.rotate_ip(min(diff_angle, self.rotation_speed))

    def follow_target(self):
        """Always move toward target"""

        closest_npc = pow(2, 20)
        for other in self.other_npcs:
            if other == self:
                continue
            else:
                dis_other = distance(other.position, self.position)
                if dis_other < closest_npc:
                    closest_npc = dis_other
        # print(f"dis_other: {dis_other}")
        if self.target is not None:
            if dis_other < 100:
                direction = self.direction.rotate_ip(min(30, self.rotation_speed))
            else:
                direction = self.direction
                self.velocity = direction * self.tracking_velocity

    # def check_shoot(self):
    #     self.target_distance = distance(self.target.position, self.position)
    #     current_time = time.get_ticks()

    #     if self.target_distance < 300:
    #         time_from_last_shot = current_time - self.last_shot_time
    #         # check if enough time has elapsed to shoot again

    #         if (
    #             time_from_last_shot > self.shoot_delay
    #             and self.cooldown < self.shoot_cooldown
    #         ):
    #             self.shot_time_total += self.shoot_delay
    #             self.last_shot_time = current_time
    #             if self.shot_time_total < self.shoot_window:
    #                 self.shoot()
    #             else:
    #                 self.shot_time_total = 0
    #                 self.cooldown += time_from_last_shot


class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        size_to_scale = {3: 1.0, 2: 0.5, 1: 0.25}
        scale = size_to_scale[size]
        sprite = transform.rotozoom(load_sprite("asteroid"), 0, scale)

        super().__init__(position, sprite, get_random_velocity(0, 0))

    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size - 1
                )
                self.create_asteroid_callback(asteroid)


class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)

    def move(self, surface):
        self.position = self.position + self.velocity
