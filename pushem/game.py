import pygame
import pygame_menu
from pushem.constants import WIDTH, HEIGHT, SQUARE_SIZE, P1_COLOR, P2_COLOR
from pushem.board import Board
from random import randint
from automa import Automa


class Game:

    def __init__(self):
        pygame.init()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.FPS = 60
        pygame.display.set_caption("PushEm")
        self.mode = "main_menu"
        self.start_new_game = False

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        self.mode = mode

    def get_start_new_game(self):
        return self.start_new_game

    def set_start_new_game(self, newgame):
        self.start_new_game = newgame

    def get_row_col(self, pos: (int, int)) -> (int, int):
        """
        Get grid row and column from mouse position
        :param pos: mouse pos from pygame
        :return: row and column (int, int)
        """
        return pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE

    def run_game(self):
        """
        sets up new game, provides user input to same.
        :return:
        """
        while True:
            # We have to re-run game setup when we start a new game
            self.__init__()

            # randomly determine starting player
            first_player = randint(0, 1)
            print("First Player: ", first_player)

            run = True
            clock = pygame.time.Clock()
            board = Board(first_player)
            automa = Automa(board)

            announce_first = pygame_menu.Menu('First Player', WIDTH / 2, HEIGHT / 2, theme=pygame_menu.themes.THEME_BLUE)
            announce_first.add.label("Computer is first" if first_player else "You are first")
            announce_first.add.button('OK', self.set_mode, "play")

            main_menu = pygame_menu.Menu('PushEm', WIDTH / 2, HEIGHT / 2, theme=pygame_menu.themes.THEME_BLUE)
            main_menu.add.button('Play', self.set_mode, announce_first)
            main_menu.add.button('Quit', pygame_menu.events.EXIT)

            announce_winner = pygame_menu.Menu('Game Over', WIDTH / 2, HEIGHT / 2,
                                               theme=pygame_menu.themes.THEME_BLUE)

            self.set_mode(main_menu)

            """Main logic/rendering loop"""
            while run and not self.start_new_game:
                clock.tick(self.FPS)

                winner = board.get_winner()
                if winner and self.mode != announce_winner:
                    announce_winner.add.label("You Won!" if winner == P1_COLOR else "Computer Won")
                    announce_winner.add.button('Quit', pygame_menu.events.EXIT)
                    announce_winner.add.button('Play Again', self.set_start_new_game, True)
                    self.mode = announce_winner

                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and self.mode == "play":
                        position = self.get_row_col(pygame.mouse.get_pos())
                        selected = board.get_piece(position)
                        if board.selected_piece is None and selected is not None and board.is_turn(selected):
                            board.set_selected(position)
                        elif board.selected_piece is not None and board.selected_piece == position:
                            board.set_selected(position)
                        elif board.selected_piece is not None:
                            board.take_turn(board.selected_piece[0], board.selected_piece[1], position[0], position[1])
                            print(automa.calculate_score())

                board.draw_grid(self.WIN)
                board.draw_pieces(self.WIN)
                board.draw_score(self.WIN)

                if self.mode != "play":
                    self.mode.draw(self.WIN)
                    self.mode.update(events)

                pygame.display.update()


if __name__ == "__main__":
    mygame = Game()
    mygame.run_game()
