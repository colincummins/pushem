import pygame
import pygame_menu
from pushem.constants import WIDTH, HEIGHT, SQUARE_SIZE, P1_COLOR, P2_COLOR, BLUE, WHITE
from pushem.board import Board
from random import randint
from pushem.automa import Automa


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

    @staticmethod
    def get_row_col(pos: (int, int)) -> (int, int):
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

            run = True
            clock = pygame.time.Clock()
            board = Board(first_player)
            automa = Automa(board)

            announce_first = pygame_menu.Menu('First Player', WIDTH / 2, HEIGHT / 2,
                                              theme=pygame_menu.themes.THEME_BLUE)
            announce_first.add.label("Computer is first" if first_player else "You are first")
            announce_first.add.button('OK', self.set_mode, "play")

            main_menu = pygame_menu.Menu('PushEm', WIDTH / 2, HEIGHT / 2, theme=pygame_menu.themes.THEME_BLUE)
            main_menu.add.button('Play', self.set_mode, announce_first)
            main_menu.add.button('Quit', pygame_menu.events.EXIT)


            self.set_mode(main_menu)

            """Main logic/rendering loop"""
            while run and not self.start_new_game:
                clock.tick(self.FPS)

                if board.get_winner():
                    self.mode = "winner"

                if board.get_turn_player() == P2_COLOR and self.mode == "play":
                    _, move, _ = automa.find_move()
                    moving_piece = board.get_piece((move[0], move[1]))
                    moving_piece.toggle_selected()
                    moving_piece.draw(self.WIN)
                    pygame.display.update()
                    pygame.time.wait(1000)
                    moving_piece.toggle_selected()
                    moving_piece.draw(self.WIN)
                    pygame.display.update()
                    board.take_turn(*move, False)

                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and self.mode == "play" and board.get_turn_player() == P1_COLOR:
                        position = self.get_row_col(pygame.mouse.get_pos())
                        selected = board.get_piece(position)
                        if board.selected_piece is None and selected is not None and board.is_turn(selected):
                            board.set_selected(position)
                        elif board.selected_piece is not None and board.selected_piece == position:
                            board.set_selected(position)
                        elif board.selected_piece is not None:
                            board.take_turn(board.selected_piece[0], board.selected_piece[1], position[0], position[1])

                if self.mode == "winner":
                    winner_name = "You" if board.get_winner() == P1_COLOR else "CPU Player"
                    winner_name += " Won!"
                    font = pygame.font.Font(None, 64)
                    subtitle_font = pygame.font.Font(None, 32)
                    text = font.render(winner_name, True, BLUE)
                    subtext = subtitle_font.render('--Click to Continue--', True, BLUE)
                    textRect = text.get_rect()
                    subtextRect = subtext.get_rect()
                    subtextRect.midtop = textRect.midbottom
                    allTextRect = pygame.Rect.union(textRect,subtextRect)
                    allTextSurf = pygame.Surface((allTextRect.width, allTextRect.height))
                    allTextSurf.fill(WHITE)
                    allTextSurf.blit(text, textRect)
                    allTextSurf.blit(subtext, subtextRect)
                    allTextRect.center = WIDTH // 2, HEIGHT // 2
                    self.WIN.blit(allTextSurf, allTextRect)
                    pygame.display.update()
                    while self.mode == "winner":
                        events = pygame.event.get()
                        for event in events:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                self.start_new_game = True
                                self.mode = None


                board.draw_grid(self.WIN)
                board.draw_pieces(self.WIN)
                board.draw_score(self.WIN)

                if self.mode in [main_menu, announce_first]:
                    self.mode.draw(self.WIN)
                    self.mode.update(events)

                pygame.display.update()
