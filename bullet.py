import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, center_pos):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=center_pos)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, center_pos):
        super().__init__()
        self.image = pygame.Surface((20, 10))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect(center=center_pos)

    def update(self):
        self.rect.x += 10
        if self.rect.right > 300:
            self.kill()

    def newMethod(self):
        pass


pygame.init()
window = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

player = Player((25, window.get_height() // 2))
all_sprites = pygame.sprite.Group(player)

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                all_sprites.add(Bullet(player.rect.center))

    all_sprites.update()
    print(len(all_sprites))

    window.fill(0)
    pygame.draw.rect(window, (255, 0, 0), (300, 0, 10, window.get_height()))
    all_sprites.draw(window)
    pygame.display.flip()

pygame.quit()
exit()
