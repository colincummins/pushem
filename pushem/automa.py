from pushem.constants import P1_COLOR, P2_COLOR, HOLE_COLOR, ROWS, COLS

class Automa:
    def __init__(self, board):
        self.board = board

    @staticmethod
    def calculate_piece_score(piece) -> int:
        # Central squares are worth 2, 1 less for each side on edge of board (making corner squares 0)
        if piece.row == -1:
            return 0
        curr_score = 2
        if piece.row == 1 or piece.row == 5:
            curr_score -= 1
        if piece.col == 1 or piece.col == 5:
            curr_score -= 1
        return curr_score

    def calculate_score(self) -> float | int:
        """
        Calculates the score based on board position and remaining pieces
        :return: Total score. Positive if p1 has advantage, negative if p2 does
        """
        # Victory means infinite score
        if self.board.p2_score == 2:
            return float("inf")

        if self.board.p1_score == 2:
            return float("-inf")

        score = 0

        if self.board.p1_score == 1:
            score -= 10

        if self.board.p2_score == 1:
            score += 10

        for piece in self.board.p1_pieces:
            score -= self.calculate_piece_score(piece)

        for piece in self.board.p2_pieces:
            score += self.calculate_piece_score(piece)

        # Being next to the Hole is an added vulnerability
        for neighbor in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            row, col = self.board.hole_piece.row + neighbor[0], self.board.hole_piece.col + neighbor[1]
            if self.board.board[row][col] and self.board.board[row][col].color == P1_COLOR:
                score += 1
            if self.board.board[row][col] and self.board.board[row][col].color == P2_COLOR:
                score -= 1

        return score

    def eliminates_own_piece(self, move):
        """
        Determines if a move will eliminate one of the player's own pieces.
        Args:
            move: The squares affected by the move List[Tuple[int]]

        Returns: True if move eliminates the player's own piece, false if not
        """
        player_color = self.board.get_turn_player()
        if self.board.get_piece(move[0]).color == player_color and (self.board.is_out_of_bounds(*move[-1]) or (self.board.get_piece(move[-1]) and self.board.get_piece(move[-1]).color == HOLE_COLOR)):
            return True

        return False

    def minmax(self, depth: int, maxplayer: bool, alpha: float = float("-inf"), beta: float = float("inf")):
        if depth == 0 or self.board.p1_score == 2 or self.board.p2_score == 2:
            return self.calculate_score(), None

        best_move = None
        current_max = float("-inf")
        current_min = float("inf")
        move_candidates = []

        if maxplayer:
            pieces = self.board.p2_pieces
        else:
            pieces = self.board.p1_pieces
        pieces = pieces + [self.board.hole_piece]

        for piece in pieces:
            if piece.row == -1:
                continue
            for neighbor in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                row, col = piece.row + neighbor[0], piece.col + neighbor[1]
                move = self.board.try_move(piece.row, piece.col, row, col)
                if move and not self.eliminates_own_piece(move):
                    move_candidates.append(move)

            if maxplayer:
                for move in move_candidates:
                    state = self.board.save_state(move)
                    start_row, start_col = move[0]
                    target_row, target_col = move[1]
                    if self.board.take_turn(start_row, start_col, target_row, target_col, True):
                        score, _ = self.minmax(depth - 1, not maxplayer, alpha, beta)
                        self.board.restore_state(state)
                        if score > current_max:
                            current_max = score
                            best_move = (start_row, start_col, target_row, target_col)
                            alpha = max(score, alpha)
                            if score >= beta:
                                break
                return current_max, best_move

            else:
                for move in move_candidates:
                    state = self.board.save_state(move)
                    start_row, start_col = move[0]
                    target_row, target_col = move[1]
                    if self.board.take_turn(start_row, start_col, target_row, target_col, True):
                        score, _ = self.minmax(depth - 1, not maxplayer, alpha, beta)
                        self.board.restore_state(state)
                        if score < current_min:
                            current_min = score
                            beta = min(score, beta)
                            if score <= alpha:
                                break
                return current_min, None

    def find_move(self, difficulty):
        return self.minmax(difficulty, True)
