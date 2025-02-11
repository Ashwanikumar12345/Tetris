import pygame
import random

# Initialize pygame module for the game 
pygame.init()

# Screen dimensions for the game 
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors for this game 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
    (128, 0, 128),  # Purple
]

# Tetromino shapes shapes that  are used i this game in different colors
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
]

class Tetrimino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = SCREEN_WIDTH // BLOCK_SIZE // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.board = [[BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
        self.current_piece = Tetrimino()
        self.running = True

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (SCREEN_WIDTH, y))

    def draw_board(self):
        for y, row in enumerate(self.board):
            for x, color in enumerate(row):
                if color != BLACK:
                    pygame.draw.rect(
                        self.screen,
                        color,
                        (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    )

    def draw_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, block in enumerate(row):
                if block:
                    pygame.draw.rect(
                        self.screen,
                        self.current_piece.color,
                        (
                            (self.current_piece.x + x) * BLOCK_SIZE,
                            (self.current_piece.y + y) * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE,
                        ),
                    )

    def check_collision(self, dx=0, dy=0):
        for y, row in enumerate(self.current_piece.shape):
            for x, block in enumerate(row):
                if block:
                    new_x = self.current_piece.x + x + dx
                    new_y = self.current_piece.y + y + dy
                    if (
                        new_x < 0
                        or new_x >= SCREEN_WIDTH // BLOCK_SIZE
                        or new_y >= SCREEN_HEIGHT // BLOCK_SIZE
                        or self.board[new_y][new_x] != BLACK
                    ):
                        return True
        return False

    def lock_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, block in enumerate(row):
                if block:
                    self.board[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color
        self.clear_lines()
        self.current_piece = Tetrimino()
        if self.check_collision():
            self.running = False

    def clear_lines(self):
        self.board = [row for row in self.board if any(color == BLACK for color in row)]
        while len(self.board) < SCREEN_HEIGHT // BLOCK_SIZE:
            self.board.insert(0, [BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)])

    def run(self):
        drop_time = 500
        last_drop = pygame.time.get_ticks()

        while self.running:
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_board()
            self.draw_piece()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and not self.check_collision(dx=-1):
                        self.current_piece.x -= 1
                    if event.key == pygame.K_RIGHT and not self.check_collision(dx=1):
                        self.current_piece.x += 1
                    if event.key == pygame.K_DOWN and not self.check_collision(dy=1):
                        self.current_piece.y += 1
                    if event.key == pygame.K_UP:
                        self.current_piece.rotate()
                        if self.check_collision():
                            for _ in range(3):  # Rotate back if collision occurs
                                self.current_piece.rotate()

            if pygame.time.get_ticks() - last_drop > drop_time:
                if not self.check_collision(dy=1):
                    self.current_piece.y += 1
                else:
                    self.lock_piece()
                last_drop = pygame.time.get_ticks()

            self.clock.tick(30)

# Run the game condition for the game to be run and wehile ther eis an issue this condition works as the backend 
if __name__ == "__main__":
    game = Tetris()
    game.run()
    pygame.quit()
