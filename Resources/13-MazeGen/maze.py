import random

WALL = 0
PATH = 1


class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [[WALL for _ in range(width)] for _ in range(height)]

    def is_valid(self, x, y):
        return 0 < x < self.width - 1 and 0 < y < self.height - 1

    def count_adjacent_walls(self, x, y):
        count = 0
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if not self.is_valid(x + dx, y + dy) or self.maze[y + dy][x + dx] == WALL:
                count += 1
        return count

    def visit(self, x, y):
        if not self.is_valid(x, y):
            return

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # print(f"nx:{nx} ny:{ny}")

            if (
                self.is_valid(nx, ny)
                and self.maze[ny][nx] == WALL
                and self.count_adjacent_walls(nx, ny) == 3
            ):
                self.maze[ny][nx] = PATH
                self.maze[y + dy][x + dx] = PATH
                self.visit(nx, ny)

    def generate(self):
        if self.width % 2 == 0:
            self.width -= 1
        if self.height % 2 == 0:
            self.height -= 1

        start_x, start_y = 1, 1
        self.maze[start_y][start_x] = PATH

        self.visit(start_x, start_y)

        self.maze[0][1] = PATH
        self.maze[self.height - 1][self.width - 2] = PATH

        return self.maze


def main():
    width = 25
    height = 25

    generator = MazeGenerator(width, height)
    maze = generator.generate()

    for row in maze:
        for cell in row:
            if cell == WALL:
                print("█", end="")
            else:
                print(" ", end="")
        print()


if __name__ == "__main__":
    main()
