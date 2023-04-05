"""Create a sprite class that loads an image resource turning it into a pygame
   sprite and manages , radius , velocity using the Vector2 data type.
"""

import pygame
from pygame.math import Vector2
from math import sqrt
import json


def arrowKeys():
    """
    Left arrow: pygame.K_LEFT or 276
    Right arrow: pygame.K_RIGHT or 275
    Up arrow: pygame.K_UP or 273
    Down arrow: pygame.K_DOWN or 274
    """

    print(len())


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_path, initial_pos=(0, 0)):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = min(self.rect.width, self.rect.height) / 2
        self.velocity = Vector2(0, 0)
        self.pos = Vector2(initial_pos)

    def update(self, delta_time):
        self.pos += self.velocity * delta_time
        self.rect.center = self.pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player(GameObject):
    def __init__(self, image_path, initial_pos=(0, 0), speed=100):
        super().__init__(image_path, initial_pos)
        self.speed = speed
        self.direction = Vector2(0, 0)
        self.animations = {
            "idle": [self.image.subsurface(pygame.Rect(0, 0, 32, 32))],
            "walk_right": [
                self.image.subsurface(pygame.Rect(x, 32, 32, 32))
                for x in range(0, 128, 32)
            ],
            "walk_left": [
                self.image.subsurface(pygame.Rect(x, 64, 32, 32))
                for x in range(0, 128, 32)
            ],
            "walk_up": [
                self.image.subsurface(pygame.Rect(x, 96, 32, 32))
                for x in range(0, 128, 32)
            ],
            "walk_down": [
                self.image.subsurface(pygame.Rect(x, 0, 32, 32))
                for x in range(0, 128, 32)
            ],
        }
        self.current_animation = self.animations["idle"][0]
        self.animation_index = 0
        self.animation_speed = 0.1
        self.animation_timer = 0

    def handle_input(self, keys_pressed):
        self.direction = Vector2(0, 0)
        if keys_pressed[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys_pressed[pygame.K_LEFT]:
            self.direction.x = -1
        if keys_pressed[pygame.K_DOWN]:
            self.direction.y = 1
        elif keys_pressed[pygame.K_UP]:
            self.direction.y = -1

    def update(self, delta_time, keys_pressed=None):
        if keys_pressed:
            self.handle_input(keys_pressed)
        else:
            self.handle_input(pygame.key.get_pressed())

        if self.direction.x != 0 or self.direction.y != 0:
            self.velocity = self.direction.normalize() * self.speed
            if self.direction.x > 0:
                self.current_animation = self.animations["walk_right"][
                    self.animation_index
                ]
            elif self.direction.x < 0:
                self.current_animation = self.animations["walk_left"][
                    self.animation_index
                ]
            elif self.direction.y > 0:
                self.current_animation = self.animations["walk_down"][
                    self.animation_index
                ]
            elif self.direction.y < 0:
                self.current_animation = self.animations["walk_up"][
                    self.animation_index
                ]
            self.animation_timer += delta_time
            if self.animation_timer >= self.animation_speed:
                self.animation_index = (self.animation_index + 1) % len(
                    self.animations[self.current_animation]
                )
                self.current_animation = self.animations[self.current_animation][
                    self.animation_index
                ]
                self.animation_timer = 0
        else:
            self.velocity = Vector2(0, 0)
            self.current_animation = self

        super().update(delta_time)


class NPC(Player):
    def __init__(self, image_path, initial_pos=(0, 0), speed=50, players=[]):
        super().__init__(image_path, initial_pos, speed)
        self.speed = speed
        self.players = players
        self.target = None

        # self.npc_key_states = tuple(False for _ in range(len(pygame.key.get_pressed())))
        self.npc_key_states = tuple(False for _ in range(512))

    def reset_pressed_keys(self):
        self.npc_key_states = tuple(False for _ in range(512))

    def get_closest_player(self):
        closest_distance = float("inf")
        self.target = None
        for player in self.players:
            if player == self:
                continue
            distance = sqrt(
                (self.pos.x - player.pos.x) ** 2 + (self.pos.y - player.pos.y) ** 2
            )
            if distance < closest_distance:
                closest_distance = distance
                self.target = player

    def angle_to_target(self):
        # Calculate the angle between the player and the NPC
        player_position = Vector2(self.target.x, self.target.y)
        npc_position = Vector2(self.pos.x, self.pos.y)
        direction = player_position - npc_position
        angle = direction.angle_to(Vector2(1, 0))
        self.press_movement_keys(angle)

    def press_movement_keys(self, angle):
        if abs(angle) < 45:
            self.npc_key_states[pygame.K_RIGHT] = True
        elif abs(angle) > 135:
            self.npc_key_states[pygame.K_LEFT] = True
        if angle < -45:
            self.npc_key_states[pygame.K_DOWN] = True
        elif angle > 45:
            self.npc_key_states[pygame.K_UP] = True

    def update(self, delta_time):
        self.reset_pressed_keys()
        self.target = self.get_closest_player()
        if self.target is not None:
            self.angle_to_target()

        super().update(delta_time, self.npc_key_states)


def main():
    # Define constants
    WINDOW_WIDTH = 640
    WINDOW_HEIGHT = 480

    # Initialize Pygame
    pygame.init()

    # Set up the window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Game")

    # Create the player
    player = Player(image_path="player.png", position=Vector2(100, 100), speed=5)

    # Create the NPCs
    npc1 = NPC(position=Vector2(400, 100), speed=2, image_path="npc1.png")
    npc2 = NPC(position=Vector2(200, 300), speed=3, image_path="npc2.png")

    # Create a list of all the NPCs
    npcs = [npc1, npc2]

    # Start the game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Handle player input
        keys_pressed = pygame.key.get_pressed()
        player.handle_input(keys_pressed)

        # Move the player
        player.update()

        # Move the NPCs towards the player
        for npc in npcs:
            direction = player.position - npc.position
            if direction.length_squared() > 0:
                direction.normalize_ip()
            npc.velocity = direction * npc.speed
            npc.update()

        # Draw the objects to the screen
        screen.fill((255, 255, 255))
        player.draw(screen)
        for npc in npcs:
            npc.draw(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()
