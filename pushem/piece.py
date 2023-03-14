import pygame
from .constants import P1_COLOR, P2_COLOR, HOLE_COLOR, ROWS, COLS, SQUARE_SIZE, PLAYER_PADDING, HOLE_PADDING


class Piece:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.calc_pos

    def calc_pos(self):
        # Gets center of piece.
        self.x = SQUARE_SIZE // 2 + COLS * SQUARE_SIZE
        self.y = SQUARE_SIZE // 2 + ROWS * SQUARE_SIZE

    def draw(self, win):
        if self.color in (P1_COLOR, P2_COLOR):
            pygame.draw.rect(win, self.color, (self.x - (SQUARE_SIZE // 2 - PLAYER_PADDING)),
                             self.y - (SQUARE_SIZE // 2 - PLAYER_PADDING))
        else:
            pass
