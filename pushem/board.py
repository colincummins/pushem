import pygame
from itertools import product
from .constants import BLACK, WHITE, GRAY, P1_COLOR, SQUARE_SIZE, SQUARE_PAD, ROWS, COLS


class Board:
    def __init__(self):
        self.selected_piece = None
        self.square = pygame.Rect(0, 0, SQUARE_SIZE - SQUARE_PAD, SQUARE_SIZE - SQUARE_PAD)
        self.board = [[0] * COLS for j in range(ROWS)]

    def draw_grid(self, win):
        win.fill(GRAY)
        for row, col in product(range(ROWS), range(COLS)):
            self.square.center = ((SQUARE_SIZE // 2) + row * SQUARE_SIZE, (SQUARE_SIZE // 2) + col * SQUARE_SIZE)
            pygame.draw.rect(win, WHITE, self.square)


