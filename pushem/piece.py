import pygame
from .constants import SQUARE_SIZE, HOLE_COLOR, BLACK

PLAYER_SIZE = 70
HOLE_SIZE = 90
PLAYER_BORDER = 5


class Piece:
    """
    All game pieces
    """
    def __init__(self, color, row, col):
        """
        Create a new piece
        :param color: Piece color (also doubles as which player owns piece)
        :param row: Grid row to place piece
        :param col: Grid column to place piece
        """
        self.color = color
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        """
        Recalculate piece position based on grid coordinates
        :return:
        """
        self.x = SQUARE_SIZE // 2 + self.col * SQUARE_SIZE
        self.y = SQUARE_SIZE // 2 + self.row * SQUARE_SIZE


class PlayerPiece(Piece):
    """
    Pieces for player 1 and 2
    """
    def draw(self, win):
        pygame.draw.rect(win, BLACK, (self.x - PLAYER_SIZE // 2, self.y - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE))
        pygame.draw.rect(win, self.color, (
        self.x - PLAYER_SIZE // 2 + PLAYER_BORDER, self.y - PLAYER_SIZE // 2 + PLAYER_BORDER,
        PLAYER_SIZE - 2 * PLAYER_BORDER, PLAYER_SIZE - 2 * PLAYER_BORDER))


class HolePiece(Piece):
    """
    Hole Piece, owned by neither player
    """
    def draw(self, win):
        pygame.draw.circle(win, HOLE_COLOR, (self.x, self.y), HOLE_SIZE // 2)
