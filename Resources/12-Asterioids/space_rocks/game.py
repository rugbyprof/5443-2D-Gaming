import pygame

from models import Asteroid, Spaceship
from utils import get_random_position, load_sprite, print_text


import pygame
import math
import random
from pygame.math import Vector2

class NPCShip(pygame.sprite.Sprite):
    def __init__(self, x, y, target_list, projectile_group):
        super().__init__()
        self.image = pygame.image.load('npc_ship_image.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.rotation_speed = 2
        self.target_list = target_list
        self.projectile_group = projectile_group
        self.target = None
        self.target_time = 0
        self.target_time_quantum = 120  # 2 seconds at 60 FPS
        self.shooting_delay = 60
        self.shooting_timer = 0

    def choose_target(self):
        if self.target_time >= self.target_time_quantum:
            if self.target_list:
                self.target = random.choice(self.target_list)
            else:
                self.target = None
            self.target_time = 0
        else:
            self.target_time += 1

    def follow_target(self):
        if self.target:
            direction = Vector2(self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y)
            distance = direction.length()
            direction.normalize_ip()

            angle = math.degrees(math.atan2(direction.y, direction.x)) - 90
            current_angle = pygame.transform.rotate(self.image, self.rotation_speed).get_rect().angle
            new_angle = angle - current_angle
            self.image = pygame.transform.rotate(self.image, new_angle)
            self.rect = self.image.get_rect(center=self.rect.center)

            if distance > 100:
                self.rect.x += direction.x * self.speed
                self.rect.y += direction.y * self.speed

    def shoot(self):
        if self.shooting_timer >= self.shooting_delay:
            if self.target:
                projectile = Projectile(self.rect.x, self.rect.y, self.target.rect.x, self.target.rect.y)
                self.projectile_group.add(projectile)
            self.shooting_timer = 0
        else:
            self.shooting_timer += 1

    def update(self):
        self.choose_target()
        self.follow_target()
        self.shoot()



class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)

        # Griffin changed this to 1 so it would only generate 1 asteroid :)
        for _ in range(1):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (
                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    self.message = "You lost!"
                    break

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        if not self.asteroids and self.spaceship:
            self.message = "You won!"

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        pygame.display.flip()
        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects
