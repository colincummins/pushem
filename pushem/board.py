import pygame
from itertools import product

import pushem.piece
from .constants import BLACK, WHITE, GRAY, P1_COLOR, P2_COLOR, HOLE_COLOR, SQUARE_SIZE, SQUARE_PAD, ROWS, COLS
from .piece import PlayerPiece, HolePiece


class Board:
    def __init__(self):
        # For selecting a piece to move
        self.selected_piece = None
        self.target_square = None

        # For checking if current move recreates the last board state, which is not allowed
        self.last_move = None

        # Used in turn taking
        self.turn = P1_COLOR

        # Create the grid and the square used to render it
        # Populate grid with starting pieces
        self.square = pygame.Rect(0, 0, SQUARE_SIZE - SQUARE_PAD, SQUARE_SIZE - SQUARE_PAD)
        self.board = [[None] * COLS for j in range(ROWS)]
        for col in range(1, COLS - 1):
            self.board[1][col] = PlayerPiece(P1_COLOR, 1, col)
            self.board[ROWS - 2][col] = PlayerPiece(P2_COLOR, ROWS - 2, col)
            self.board[3][3] = HolePiece(HOLE_COLOR, 3, 3)

    def draw_grid(self, win):
        """
        Draws grid onto surface 'win'
        :param win: Write grid onto this surface
        :return:
        """
        win.fill(GRAY)
        for row, col in product(range(1, ROWS - 1), range(1, COLS - 1)):
            self.square.center = ((SQUARE_SIZE // 2) + row * SQUARE_SIZE, (SQUARE_SIZE // 2) + col * SQUARE_SIZE)
            pygame.draw.rect(win, WHITE, self.square)

    def draw_pieces(self, win):
        """
        Draw all pieces onto surface 'win'
        :param win: Target surface
        :return:
        """
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] is not None:
                    self.board[row][col].draw(win)

    @staticmethod
    def is_out_of_bounds(row, col) -> bool:
        """
        Helper function to test if a coordinate pair is out of bounds on self.board
        Can be used for error checking, or to see if a piece has been pushed off the board and is eliminated
        :return: True if coord pair is off the board
        """
        return row < 1 or row > ROWS - 2 or col < 1 or col > COLS - 2

    def make_move(self, current_row:int, current_col:int, target_row:int, target_col:int, pieces_moved = None) -> [pushem.piece.Piece]:
        """
        Try to move piece from current to target.
        :param pieces_moved: List of pieces affected by this move so far
        :param current_row: Row of moving piece on self.board
        :param current_col: Col of moving piece on self.board
        :param target_row: Row of target piece on self.board
        :param target_col: Col of target piece on self.board
        :return: List of pieces moved, starting with current piece
        """

        if pieces_moved is None:
            pieces_moved = []

        # Test for invalid move - Cannot push Hole off of board
        if self.board[current_row][current_col].get_color() == HOLE_COLOR and self.is_out_of_bounds(target_row, target_col):
            return None

        pieces_moved.append((target_row, target_col))

        # Pushing a piece off the board or into the hole completes the move
        # (but we have to be sure it's not just a reverse of the last move, duplicating the prior board state)
        if self.board[target_row][target_col] is None or self.board[target_row][target_col].color == HOLE_COLOR:
            if pieces_moved == reversed(self.last_move):
                return None
            return pieces_moved

        # Recursive case
        return self.make_move(target_row, target_col, 2 * target_row - current_row, 2* target_col - current_col, pieces_moved)







