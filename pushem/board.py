import pygame
from itertools import product

import pushem
from pushem.constants import BLACK, WHITE, GRAY, P1_COLOR, P2_COLOR, HOLE_COLOR, SQUARE_SIZE, SQUARE_PAD, ROWS, COLS
from pushem.piece import Piece, PlayerPiece, HolePiece


class Board:
    def __init__(self):
        # For selecting a piece to move
        self.selected_piece:Piece = None
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

    def set_selected(self, pos) -> None:
        """
        Set position of selected piece for movement
        :param pos: row, col of selected piece
        :return: None
        """
        if pos is None:
            print("Deselected piece:",pos)
            self.selected_piece.toggle_selected()
            self.selected_piece = None
            return

        self.selected_piece = self.board[pos[0]][pos[1]]
        self.selected_piece.toggle_selected()

        print("Selected piece:",pos)

    def set_target_square(self, pos) -> None:
        """
        Set position of targeted square for movement
        :param pos: row, col of selected square
        :return: None
        """
        if pos is None:
            self.target_square = None
            print("Deselected target square:",pos)

        self.target_square = pos
        print("Selected square:",pos)

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

    def toggle_selected(self, pos):
        """
        Toggle piece from selected to unselected
        :param pos: (row, col) of piece to toggle
        :return:
        """
        self.board[pos[0]][pos[1]].toggle_selected()

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

    def try_move(self, current_row:int, current_col:int, target_row:int, target_col:int, pieces_moved = None) :
        """
        Try to move piece from current to target.
        :param pieces_moved: List of pieces affected by this move so far
        :param current_row: Row of moving piece on self.board
        :param current_col: Col of moving piece on self.board
        :param target_row: Row of target piece on self.board
        :param target_col: Col of target piece on self.board
        :return: List of pieces moved, starting with initiating piece and ending with final destination square [(int,int)]
        """

        if pieces_moved is None:
            pieces_moved = []

        # Check for invalid move - cannot push Hole off of board or onto another piece
        if self.board[current_row][current_col].get_color() == HOLE_COLOR and (self.is_out_of_bounds(target_row, target_col) or self.board[target_row, target_col] is not None):
            return None

        # Move may be good. Add to list of pieces moved this time and test further
        pieces_moved.append((current_row, current_col))

        # Pushing a piece off the board or into the hole eliminates it, so there's no way this move is duplicating the
        # last board state. Move successful.
        if self.is_out_of_bounds(target_row, target_col) or self.board[target_row][target_col] is not None:
            # We add the target row and col as a kind of 'capstone', which tells other functions 1) which direction
            # we're shifting in the case of a single piece and 2) if we're pushing off board or into a hole
            self.pieces_moved.append((target_row, target_col))
            return pieces_moved

        # Pushing a piece into another piece requires recursion
        if self.board[target_row][target_col] is not None:
            ph_row, ph_col = target_row, target_col
            target_row, target_col = 2 * target_row - current_row, 2 * target_col - current_col
            current_row, current_col = ph_row, ph_col
            return self.make_move(current_row, current_col, target_row, target_col, pieces_moved)

        # Pushing onto an empty square is valid, but we have to check if we are simply reversing the last move made,
        # and returning to the preceding board position which is invalid.
        # This case is indicated by the same set of pieces being moved, but in the opposite order
        # So 'A pushes B pushes C' and 'C pushes B pushes A' is invalid
        if pieces_moved == reversed(self.last_move):
            return None

        # Move valid - ends with a piece being pushed onto an empty square
        # Add the target row/col to make later movement easier
        self.pieces_moved.append((target_row, target_col))
        return pieces_moved
