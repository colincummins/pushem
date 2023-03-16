import pygame
from itertools import product
from .constants import BLACK, WHITE, GRAY, P1_COLOR, P2_COLOR, HOLE_COLOR, SQUARE_SIZE, SQUARE_PAD, ROWS, COLS
from .piece import PlayerPiece, HolePiece

class Board:
    def __init__(self):
        self.selected_piece = None
        self.square = pygame.Rect(0, 0, SQUARE_SIZE - SQUARE_PAD, SQUARE_SIZE - SQUARE_PAD)
        self.board = [[None] * COLS for j in range(ROWS)]
        for col in range(1, COLS - 1):
            self.board[1][col] = PlayerPiece(P1_COLOR, 1, col)
            self.board[ROWS - 2][col] = PlayerPiece(P2_COLOR, ROWS - 2, col)
            self.board[3][3] = HolePiece(HOLE_COLOR, 3, 3)

    def draw_grid(self, win):
        win.fill(GRAY)
        for row, col in product(range(1, ROWS - 1), range(1, COLS - 1)):
            self.square.center = ((SQUARE_SIZE // 2) + row * SQUARE_SIZE, (SQUARE_SIZE // 2) + col * SQUARE_SIZE)
            pygame.draw.rect(win, WHITE, self.square)

    def draw_pieces(self, win):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] is not None:
                    self.board[row][col].draw(win)



