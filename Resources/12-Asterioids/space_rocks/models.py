from pygame.math import Vector2
from pygame import transform

import random
from utils import get_random_velocity, load_sound, load_sprite, wrap_position, distance
import math

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


# class NPCShip(pygame.sprite.Sprite):
#     def __init__(self, x, y, target_list, projectile_group):
#         super().__init__()
#         self.image = pygame.image.load(
#             "../assets/sprites/space_ship5_40x40.png.png"
#         ).convert_alpha()
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         self.speed = 2
#         self.rotation_speed = 2
#         self.target_list = target_list
#         self.projectile_group = projectile_group
#         self.target = None
#         self.target_time = 0
#         self.target_time_quantum = 120  # 2 seconds at 60 FPS
#         self.shooting_delay = 60
#         self.shooting_timer = 0

#     def choose_target(self):
#         if self.target_time >= self.target_time_quantum:
#             if self.target_list:
#                 self.target = random.choice(self.target_list)
#             else:
#                 self.target = None
#             self.target_time = 0
#         else:
#             self.target_time += 1

#     def follow_target(self):
#         if self.target:
#             direction = Vector2(
#                 self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y
#             )
#             distance = direction.length()
#             direction.normalize_ip()

#             angle = math.degrees(math.atan2(direction.y, direction.x)) - 90
#             current_angle = (
#                 pygame.transform.rotate(self.image, self.rotation_speed)
#                 .get_rect()
#                 .angle
#             )
#             new_angle = angle - current_angle
#             self.image = pygame.transform.rotate(self.image, new_angle)
#             self.rect = self.image.get_rect(center=self.rect.center)

#             if distance > 100:
#                 self.rect.x += direction.x * self.speed
#                 self.rect.y += direction.y * self.speed

#     def shoot(self):
#         if self.shooting_timer >= self.shooting_delay:
#             if self.target:
#                 projectile = Projectile(
#                     self.rect.x, self.rect.y, self.target.rect.x, self.target.rect.y
#                 )
#                 self.projectile_group.add(projectile)
#             self.shooting_timer = 0
#         else:
#             self.shooting_timer += 1

#     def update(self):
#         self.choose_target()
#         self.follow_target()
#         self.shoot()


class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.25
    BULLET_SPEED = 100

    def __init__(self, position, create_bullet_callback, ship="space_ship_40x40"):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        # Make a copy of the original UP vector
        self.direction = Vector2(UP)

        super().__init__(position, load_sprite(ship), Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
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
        self.create_bullet_callback(bullet)
        self.laser_sound.play()


class NPC(Spaceship):
    def __init__(
        self, position, create_bullet_callback, ship="space_ship5_40x40", targets=[]
    ):
        self.targets = targets

        super().__init__(position, create_bullet_callback, ship)

    def choose_target(self):
        closestDistance = pow(2, 20)
        closestTarget = None
        for target in self.targets:
            d = distance(target.position, self.position)
            if distance(target.position, self.position) < closestDistance:
                closestTarget = target
                closestDistance = d

        self.target = closestTarget
        # print(self.target)
        # if self.target_time >= self.target_time_quantum:
        #     if self.target_list:
        #         self.target = random.choice(self.target_list)
        #     else:
        #         self.target = None
        #     self.target_time = 0
        # else:
        #     self.target_time += 1

    def follow_target(self):
        if self.target:
            self.direction = Vector2(
                self.target.position[0] - self.position[0],
                self.target.position[1] - self.position[1],
            )

            print(self.direction)

            # distance = self.direction.length()
            # direction.normalize_ip()

            # angle = math.degrees(math.atan2(direction.y, direction.x)) - 90
            # current_angle = (
            #     transform.rotate(self.image, self.rotation_speed).get_rect().angle
            # )
            # new_angle = angle - current_angle
            # self.image = transform.rotate(self.image, new_angle)
            # self.rect = self.image.get_rect(center=self.rect.center)

            # if distance > 100:
            #     self.rect.x += direction.x * self.speed
            #     self.rect.y += direction.y * self.speed


class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        size_to_scale = {3: 1.0, 2: 0.5, 1: 0.25}
        scale = size_to_scale[size]
        sprite = transform.rotozoom(load_sprite("asteroid"), 0, scale)

        super().__init__(position, sprite, get_random_velocity(1, 3))

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
