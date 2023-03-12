import pygame
from itertools import product
from .constants import BLACK, WHITE, SQUARE_SIZE, SQUARE_PROP


class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None

    def draw_grid(self, win):
        win.fill(BLACK)
        for row, col in product(range(5), range(5)):
            pygame.draw.rect(win, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE * SQUARE_PROP, SQUARE_SIZE * SQUARE_PROP))



