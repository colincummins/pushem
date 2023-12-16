import pygame
import pygame_menu
from pushem.constants import WIDTH, HEIGHT, SQUARE_SIZE
from pushem.board import Board
from random import randint


class Game:

    def __init__(self):
        pygame.init()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.FPS = 60
        pygame.display.set_caption("PushEm")
        self.mode = "menu"

    def get_row_col(self, pos: (int, int)) -> (int, int):
        """
        Get grid row and column from mouse position
        :param pos: mouse pos from pygame
        :return: row and column (int, int)
        """
        return pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE

    def start_game(self):
        self.mode = "play"

    def quit_game(self):
        pass

    def run_game(self):
        """
        Sets up new game, provides user input to same.
        :return:
        """
        # Randomly determine starting player
        first_player = randint(0, 1)
        print("First Player: ", first_player)

        run = True
        clock = pygame.time.Clock()
        board = Board(first_player)

        menu = pygame_menu.Menu('PushEm', WIDTH / 2, HEIGHT / 2, theme=pygame_menu.themes.THEME_BLUE)
        menu.add.button('Play', self.start_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)


        """Main logic/rendering loop"""
        while run:
            clock.tick(self.FPS)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and self.mode=="play":
                    position = self.get_row_col(pygame.mouse.get_pos())
                    selected = board.get_piece(position)
                    if board.selected_piece is None and selected is not None and board.is_turn(selected):
                        board.set_selected(position)
                    elif board.selected_piece is not None and board.selected_piece == position:
                        board.set_selected(position)
                    elif board.selected_piece is not None:
                        board.take_turn(board.selected_piece[0], board.selected_piece[1], position[0], position[1])

            board.draw_grid(self.WIN)
            board.draw_pieces(self.WIN)
            if menu.is_enabled():
                menu.update(events)
                menu.draw(self.WIN)
                if self.mode != "menu":
                    menu.toggle()
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    mygame = Game()
    mygame.run_game()
