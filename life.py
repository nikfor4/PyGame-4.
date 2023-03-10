import pygame
import sys


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)

                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, pygame.Color(255, 0, 0), (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                        self.cell_size))

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if x < self.left or y < self.top:
            return None
        x = (x - self.left) // self.cell_size
        y = (y - self.top) // self.cell_size
        if x >= self.width or y >= self.height:
            return None
        return y, x

    def on_click(self, cell_coords):
        if cell_coords:
            row, col = cell_coords
            self.board[row][col] = 1 - self.board[row][col]

    def get_neighbours(self, row, col):
        neighbours = []
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i == row and j == col:
                    continue
                if i < 0 or j < 0 or i >= self.height or j >= self.width:
                    continue
                neighbours.append((i, j))
        return neighbours

    def count_neighbours(self, row, col):
        neighbours = self.get_neighbours(row, col)
        return sum([self.board[r][c] for r, c in neighbours])

    def next_move(self):
        new_board = [[0] * self.width for _ in range(self.height)]
        for row in range(self.height):
            for col in range(self.width):
                count = self.count_neighbours(row, col)
                if count == 3 or (count == 2 and self.board[row][col] == 1):
                    new_board[row][col] = 1
        self.board = new_board


class Life(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.paused = True

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode(
            (self.width * self.cell_size + self.left * 2, self.height * self.cell_size + self.top * 2))
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    cell_coords = self.get_cell(event.pos)
                    self.on_click(cell_coords)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused

            screen.fill(pygame.Color(0, 0, 0))
            self.render(screen)
            pygame.display.flip()

            if not self.paused:
                self.next_move()
                pygame.time.delay(100)


if __name__ == '__main__':
    game = Life(20, 20)
    game.run()
