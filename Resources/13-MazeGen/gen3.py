import random
import pygame
import sys
from rich import print

# Define constants for the maze and tile size
MAZE_WIDTH = 20
MAZE_HEIGHT = 20
TILE_SIZE = 32

# Define the 2-edge Wang tileset as a list of binary values for each tile
TILESET = [
    ["0", "0", "1", "1"],
    ["1", "0", "1", "0"],
    ["1", "1", "0", "0"],
    ["0", "1", "0", "1"],
]

tile_indices = {
    (False, False, False, False): 0,
    (False, False, False, True): 1,
    (False, False, True, False): 2,
    (False, False, True, True): 3,
    (False, True, False, False): 4,
    (False, True, False, True): 5,
    (False, True, True, False): 6,
    (False, True, True, True): 7,
    (True, False, False, False): 8,
    (True, False, False, True): 9,
    (True, False, True, False): 10,
    (True, False, True, True): 11,
    (True, True, False, False): 12,
    (True, True, False, True): 13,
    (True, True, True, False): 14,
    (True, True, True, True): 15,
    0: (False, False, False, False),
    1: (False, False, False, True),
    2: (False, False, True, False),
    3: (False, False, True, True),
    4: (False, True, False, False),
    5: (False, True, False, True),
    6: (False, True, True, False),
    7: (False, True, True, True),
    8: (True, False, False, False),
    9: (True, False, False, True),
    10: (True, False, True, False),
    11: (True, False, True, True),
    12: (True, True, False, False),
    13: (True, True, False, True),
    14: (True, True, True, False),
    15: (True, True, True, True),
}

tile_images = {}
for x in range(len(TILESET)):
    for y in range(len(TILESET[0])):
        tile_key = tuple(TILESET[x][y])
        print(tile_key)
        tile_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        tile_images[tile_key] = tile_image


class WangMazeGenerator:
    def __init__(self, width, height, tileset):
        self.width = width
        self.height = height
        self.tileset = tileset
        self.tile_indices = {
            (False, False, False, False): 0,
            (False, False, False, True): 1,
            (False, False, True, False): 2,
            (False, False, True, True): 3,
            (False, True, False, False): 4,
            (False, True, False, True): 5,
            (False, True, True, False): 6,
            (False, True, True, True): 7,
            (True, False, False, False): 8,
            (True, False, False, True): 9,
            (True, False, True, False): 10,
            (True, False, True, True): 11,
            (True, True, False, False): 12,
            (True, True, False, True): 13,
            (True, True, True, False): 14,
            (True, True, True, True): 15,
            0: (False, False, False, False),
            1: (False, False, False, True),
            2: (False, False, True, False),
            3: (False, False, True, True),
            4: (False, True, False, False),
            5: (False, True, False, True),
            6: (False, True, True, False),
            7: (False, True, True, True),
            8: (True, False, False, False),
            9: (True, False, False, True),
            10: (True, False, True, False),
            11: (True, False, True, True),
            12: (True, True, False, False),
            13: (True, True, False, True),
            14: (True, True, True, False),
            15: (True, True, True, True),
        }

        # Load the tileset images and create the maze
        self.tile_images = {}
        for x in range(len(self.tileset)):
            for y in range(len(self.tileset[0])):
                tile_key = tuple(self.tileset[x][y])
                tile_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
                self.tile_images[tile_key] = tile_image

        self.generate_maze()

    def generate_maze(self):
        self.maze = [[0 for y in range(self.height)] for x in range(self.width)]
        visited = set()
        stack = [
            (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        ]
        while stack:
            current_x, current_y = stack.pop()
            visited.add((current_x, current_y))

            neighbors = []
            if current_x > 0 and (current_x - 1, current_y) not in visited:
                neighbors.append((current_x - 1, current_y))
            if current_x < self.width - 1 and (current_x + 1, current_y) not in visited:
                neighbors.append((current_x + 1, current_y))
            if current_y > 0 and (current_x, current_y - 1) not in visited:
                neighbors.append((current_x, current_y - 1))
            if (
                current_y < self.height - 1
                and (current_x, current_y + 1) not in visited
            ):
                neighbors.append((current_x, current_y + 1))

            if neighbors:
                print(f"neighbors:{neighbors}")
                next_x, next_y = random.choice(neighbors)
                print(f"next_x:{next_x} next_y:{next_y}")
                stack.append((current_x, current_y))
                stack.append((next_x, next_y))

                # x, y = current_x + next_x, current_y + next_y
                adjacent_walls = self.get_adjacent_walls(next_x, next_y)
                tile_index = self.tile_indices[adjacent_walls]
                self.maze[next_x][next_y] = tile_index

        return self.maze

    def get_adjacent_walls(self, x, y):
        print(f"getting adjacent walls - x:{x} y:{y}")
        left_wall = x == 0 or self.maze[x - 1][y] in [2, 3, 6, 7, 10, 11, 14, 15]
        right_wall = x == self.width - 1 or self.maze[x + 1][y] in [
            1,
            3,
            5,
            7,
            9,
            11,
            13,
            15,
        ]
        top_wall = y == 0 or self.maze[x][y - 1] in [4, 5, 6, 7, 12, 13, 14, 15]
        bottom_wall = y == self.height - 1 or self.maze[x][y + 1] in [
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
        ]
        return (left_wall, top_wall, right_wall, bottom_wall)


# Define the Pygame classes for the tileset and the maze
class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))


class Maze(pygame.sprite.Sprite):
    def __init__(self, maze, tileset):
        super().__init__()
        self.image = pygame.Surface((MAZE_WIDTH * TILE_SIZE, MAZE_HEIGHT * TILE_SIZE))
        self.rect = self.image.get_rect()
        self.tileset = tileset
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                tile_index = maze[x][y]
                print(maze)
                print(tile_images)
                print(f"tile_index: {tile_index}")
                print(f"{self.tileset}")
                # sys.exit()
                tile_key = tuple(tile_indices[tile_index])
                tile_image = tile_images[tile_key]
                print(f"tile_key: {tile_key}")
                print(f"tile_image: {tile_image}")
                tile_sprite = Tile(tile_image, x, y)
                self.image.blit(tile_image, (x * TILE_SIZE, y * TILE_SIZE))


if __name__ == "__main__":
    maze_generator = WangMazeGenerator(MAZE_WIDTH, MAZE_HEIGHT, TILESET)
    maze = maze_generator.maze
    tile_map = Maze(maze, TILESET)
    sys.exit()

    # Create the Pygame window and sprites
    pygame.init()
    screen = pygame.display.set_mode((MAZE_WIDTH * TILE_SIZE, MAZE_HEIGHT * TILE_SIZE))
    all_sprites = pygame.sprite.Group(tile_map)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        all_sprites.draw(screen)

        pygame.display.flip()

    pygame.quit()
