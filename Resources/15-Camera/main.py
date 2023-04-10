import pygame
from pygame.locals import *
from pygame.math import Vector2

gameWorldX = 10000
gameWorldY = 10000
cameraX = 500
cameraY = 500

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.position = Vector2(x, y)
        self.speed = 2

    def update(self, pressed_keys):
        velocity = Vector2(0, 0)

        if pressed_keys[K_w] or pressed_keys[K_UP]:
            velocity.y -= self.speed
        if pressed_keys[K_s] or pressed_keys[K_DOWN]:
            velocity.y += self.speed
        if pressed_keys[K_a] or pressed_keys[K_LEFT]:
            velocity.x -= self.speed
        if pressed_keys[K_d] or pressed_keys[K_RIGHT]:
            velocity.x += self.speed

        self.position += velocity

        self.position.x = max(0, min(gameWorldX - self.rect.width, self.position.x))
        self.position.y = max(0, min(gameWorldY - self.rect.height, self.position.y))

        self.rect.topleft = self.position

screen = pygame.display.set_mode((cameraX, cameraY))
background_image = pygame.image.load("./media/tile_1000x1000_40_light.png").convert()

player = Player(cameraX//2, cameraY//2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill((0,0,0))
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    camera = pygame.Rect(player.position.x - cameraX//2, player.position.y - cameraY//2, cameraX, cameraY)
    camera.clamp_ip(pygame.Rect(0, 0, gameWorldX, gameWorldY))

    for y in range(-camera.y % background_image.get_height(), cameraY, background_image.get_height()):
        for x in range(-camera.x % background_image.get_width(), cameraX, background_image.get_width()):
            screen.blit(background_image, (x, y))

    screen.blit(player.image, (player.position.x - camera.x, player.position.y - camera.y))
    pygame.display.flip()

pygame.quit()
