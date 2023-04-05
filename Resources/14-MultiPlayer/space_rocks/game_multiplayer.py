import pygame

from models import Asteroid, Spaceship, NPC
from utils import get_random_position, load_sprite, print_text


import pygame
import math
import random
from pygame.math import Vector2
import sys


class GameManager:
    """ """

    def __init__(self, screen):
        self.players = {}
        self.localPlayer = None

    def addPlayer(self, **kwargs):
        """Adds a player to the local game as dictated by incoming messages."""
        name = kwargs.get("name", None)
        player = kwargs.get("player", None)
        attributes = kwargs.get("attributes", None)
        localPlayer = kwargs.get("localPlayer", False)

        # we don't want to try and manage the local player instance
        if localPlayer:
            self.localPlayer = player.id
        else:
            # this is a new player that needs just a basic player class
            # with no messaging capabilites. This is a mirror of another
            # player somewhere else.
            player = Spaceship(screen=self.screen, name=name, color=color)
            self.players[name] = player

    def update(self):
        """Update all players registered with the game manager."""
        for id, player in self.players.items():
            player.update()

    def callBack(self, ch, method, properties, body):
        """_summary_: callback for multiple players"""

        game = method.exchange  # not used here but passed in by pika
        exchange = method.exchange  # not used here but passed in by pika
        body = json.loads(body.decode("utf-8"))  # where all the game commands are
        data = body.get("data", None)
        sender = body["sender"]
        xy = data.get("location", None)
        target = data.get("target", None)
        color = data.get("color", None)
        speed = data.get("speed", None)


class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        # current_w = 1680, current_h = 1050
        # self.screen = pygame.display.set_mode((1024, 768))
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship(
            (self.width // 2, self.height // 2), self.bullets.append
        )

        print(self.spaceship)

        self.npcs = []

        self.started = False

        self.npcs.append(
            NPC(
                (self.width * 0.05, self.height * 0.05),
                self.bullets.append,
                "space_ship5_40x40",
                [self.spaceship],
                other_npcs=self.npcs,
            )
        )

        self.npcs.append(
            NPC(
                (self.width * 0.95, self.height * 0.95),
                self.bullets.append,
                "space_ship6_40x40",
                [self.spaceship],
                other_npcs=self.npcs,
            )
        )

        # Griffin changed this to 1 so it would only generate 1 asteroid :)
        for _ in range(0):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def other_npcs(self):
        return self.npcs

    def main_loop(self):
        while True:
            self._handle_input()
            if self.started:
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

        if not self.started:
            if is_key_pressed[pygame.K_g]:
                self.started = True

        if self.spaceship:
            # print(f"velocity: {self.spaceship.velocity}")
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
                if len(self.npcs) > 0:
                    for npc in self.npcs:
                        npc.accelerate()
            if is_key_pressed[pygame.K_DOWN]:
                self.spaceship.accelerate(0)

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    self.message = "You lost!"
                    break

        if len(self.npcs) > 0:
            for npc in self.npcs:
                npc.choose_target()
                npc.rotate()
                npc.follow_target()
                # npc.check_shoot()

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break

        for bullet in self.bullets[:]:
            print(bullet)
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        # if not self.asteroids and self.spaceship:
        #     self.message = "You won!"

    def _draw(self):
        # self.screen.blit(self.background, (0, 0))

        self.screen.fill((0, 0, 0))

        for game_object in self._get_game_objects():
            # print(game_object)
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        pygame.display.flip()
        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        if len(self.npcs) > 0:
            for npc in self.npcs:
                game_objects.append(npc)

        return game_objects
