import pygame
import random
import sys
from rich import print

# Define constants
WIDTH = 800
HEIGHT = 600
TILE_SIZE = 32
FPS = 60


"""
Question:
    Please don't generate any code, just try to answer a question. In the previous code sample, you create a "tileset" list 
    that has (e.g ["0", "0", "1", "1"]) zeros and ones for each of the 16 tiles in the tileset. What are the zeros and ones implying?

Answer:
    In the context of the 2-edge Wang tileset used in the previous code sample, the zeros and ones in each sublist of the tileset 
    list represent whether an edge of the tile is open (a "0") or closed (a "1"). The edges are listed in clockwise order, starting 
    with the top edge.

    So in the example sublist ["0", "0", "1", "1"], the top and left edges are open (represented by "0"), while the right and bottom 
    edges are closed (represented by "1"). This particular tile could be interpreted as a corner piece with an open top and left side 
    and a closed bottom and right side.
"""

# Define the 2-edge Wang tileset
tileset = [
    ["0", "0", "1", "1"],
    ["0", "0", "1", "1"],
    ["1", "1", "0", "0"],
    ["1", "1", "0", "0"],
]

"""
Question:
    Similarly there is a "tile_indices" dictionary defined in the code as well. Are the true and false values used in tuples as keys in the 
    dictionary supposed to return a tile index that corresponds with a certain set of walls that are either up or down?

Answer:
    Yes, in the tile_indices dictionary, the keys are tuples of boolean values that represent the presence or absence of walls on the 
    left, top, right, and bottom edges of an adjacent tile, in that order.

    Each key corresponds to a particular combination of walls, and its associated value is the index of the tile in the tileset list 
    that should be used for tiles with those walls. So when generating the maze, the code determines the adjacent walls of each tile 
    and uses the tile_indices dictionary to choose the appropriate tile from the tileset list.

    This allows for the generation of mazes with varied layouts based on the edges of the adjacent tiles, while using a relatively 
    small set of 2-edge Wang tiles.
"""
# Define the indices of each tile in the tileset
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
}

# Define the maze size and create a 2D array to represent the maze
maze_width = 20
maze_height = 20
maze = [[0 for y in range(maze_height)] for x in range(maze_width)]


# Define a function to get the indices of the adjacent tiles at a given position in the maze
def get_adjacent_tiles(x, y):
    if x == 0:
        left_tile = False
    else:
        left_tile = maze[x - 1][y] in [2, 3, 6, 7, 10, 11, 14, 15]

    if x == maze_width - 1:
        right_tile = False
    else:
        right_tile = maze[x + 1][y] in [1, 3, 5, 7, 9, 11, 13, 15]

    if y == 0:
        top_tile = False
    else:
        top_tile = maze[x][y - 1] in [4, 5, 6, 7, 12, 13, 14, 15]

    if y == maze_height - 1:
        bottom_tile = False
    else:
        bottom_tile = maze[x][y + 1] in [1, 2, 3, 7, 9, 10, 11, 15]

    return (left_tile, top_tile, right_tile, bottom_tile)


def mazeGen():
    # Generate the maze using a random depth-first search algorithm
    visited = set()
    stack = [(random.randint(0, maze_width - 1), random.randint(0, maze_height - 1))]
    while stack:
        current_x, current_y = stack.pop()
        visited.add((current_x, current_y))

        neighbors = []
        if current_x > 0 and (current_x - 1, current_y) not in visited:
            neighbors.append((current_x - 1, current_y))
        if current_x < maze_width:
            current_x, current_y = stack.pop()
            visited.add((current_x, current_y))

            neighbors = []
            if current_x > 0 and (current_x - 1, current_y) not in visited:
                neighbors.append((current_x - 1, current_y))
            if current_x < maze_width - 1 and (current_x + 1, current_y) not in visited:
                neighbors.append((current_x + 1, current_y))
            if current_y > 0 and (current_x, current_y - 1) not in visited:
                neighbors.append((current_x, current_y - 1))
            if (
                current_y < maze_height - 1
                and (current_x, current_y + 1) not in visited
            ):
                neighbors.append((current_x, current_y + 1))

            if neighbors:
                next_x, next_y = random.choice(neighbors)
                stack.append((current_x, current_y))
                stack.append((next_x, next_y))

                x, y = current_x + next_x, current_y + next_y
                adjacent_tiles = get_adjacent_tiles(x, y)
                tile_index = tile_indices[adjacent_tiles]
                maze[x][y] = tile_index


# Define the Pygame classes for the tileset and the maze
class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))


class Maze(pygame.sprite.Sprite):
    def __init__(self, maze, tileset):
        super().__init__()
        self.image = pygame.Surface((maze_width * TILE_SIZE, maze_height * TILE_SIZE))
        self.rect = self.image.get_rect()
        for y in range(maze_height):
            for x in range(maze_width):
                tile_index = maze[x][y]
                tile_key = tuple(tileset[tile_index])
                tile_image = tile_images[tile_key]
                tile_sprite = Tile(tile_image, x, y)
                self.image.blit(tile_image, (x * TILE_SIZE, y * TILE_SIZE))


if __name__ == "__main__":
    # Load the tileset images and create the maze
    tile_images = {}
    for x in range(len(tileset)):
        for y in range(len(tileset[0])):
            tile_key = tuple(tileset[x][y])
            tile_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            tile_images[tile_key] = tile_image
    tile_map = Maze(maze, tileset)

    sys.exit()
    # Create the Pygame window and sprites
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
