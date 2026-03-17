from typing import Optional

import pygame
from pushem.constants import WIDTH, HEIGHT, SQUARE_SIZE, P1_COLOR, P2_COLOR, WHITE, BLACK
from pushem.board import Board
from random import randint
from pushem.automa import Automa
from pushem.announcement import show_announcement
from pushem.how_to_play import HOW_TO_PLAY_SECTIONS
from pushem.menu_ui import MenuUI
from pushem.piece import PLAYER_SIZE, PIECE_BORDER


class Game:

    def __init__(self):
        pygame.init()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.FPS = 60
        pygame.display.set_caption("PushEm")
        self.difficulty = 2
        self.mode: Optional[str] = None
        self.start_new_game = False
        self.capture_animation = None
        self.menu_ui = MenuUI(HOW_TO_PLAY_SECTIONS)

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

    def set_difficulty(self, difficulty_str: str, difficulty_num: int)-> None:
        self.difficulty = difficulty_num
        print(f"Difficulty {self.difficulty}")

    def cycle_difficulty(self, step: int) -> None:
        current_index = next(
            (index for index, (_, value) in enumerate(self.menu_ui.difficulty_options) if value == self.difficulty),
            0,
        )
        next_index = (current_index + step) % len(self.menu_ui.difficulty_options)
        difficulty_str, difficulty_num = self.menu_ui.difficulty_options[next_index]
        self.set_difficulty(difficulty_str, difficulty_num)

    def start_capture_animation(self, capture_event: Optional[dict]) -> None:
        if not capture_event:
            return
        self.capture_animation = {
            **capture_event,
            "start_time": pygame.time.get_ticks(),
            "move_duration_ms": 160,
            "shrink_duration_ms": 180,
        }

    def update_capture_animation(self) -> None:
        if self.capture_animation is None:
            return

        elapsed = pygame.time.get_ticks() - self.capture_animation["start_time"]
        total_duration = (
            self.capture_animation["move_duration_ms"] +
            self.capture_animation["shrink_duration_ms"]
        )
        if elapsed >= total_duration:
            self.capture_animation = None

    @staticmethod
    def interpolate(start: float, end: float, progress: float) -> float:
        return start + (end - start) * progress

    def draw_capture_animation(self) -> None:
        if self.capture_animation is None:
            return

        elapsed = pygame.time.get_ticks() - self.capture_animation["start_time"]
        move_duration = self.capture_animation["move_duration_ms"]
        shrink_duration = self.capture_animation["shrink_duration_ms"]

        if elapsed < move_duration:
            progress = elapsed / move_duration
            x = self.interpolate(self.capture_animation["start_x"], self.capture_animation["end_x"], progress)
            y = self.interpolate(self.capture_animation["start_y"], self.capture_animation["end_y"], progress)
            scale = 1.0
        else:
            shrink_elapsed = min(elapsed - move_duration, shrink_duration)
            x = self.capture_animation["end_x"]
            y = self.capture_animation["end_y"]
            scale = max(0.0, 1.0 - (shrink_elapsed / shrink_duration))

        outer_size = max(1, round(PLAYER_SIZE * scale))
        inner_size = max(1, round((PLAYER_SIZE - 2 * PIECE_BORDER) * scale))
        outer_rect = pygame.Rect(0, 0, outer_size, outer_size)
        outer_rect.center = (round(x), round(y))
        inner_rect = pygame.Rect(0, 0, inner_size, inner_size)
        inner_rect.center = outer_rect.center

        pygame.draw.rect(self.WIN, self.capture_animation["bg_color"], outer_rect)
        pygame.draw.rect(self.WIN, self.capture_animation["color"], inner_rect)

    def handle_main_menu_event(self, event: pygame.event.Event) -> None:
        action = self.menu_ui.handle_main_menu_event(event, self.difficulty)
        self.handle_menu_action(action)

    def handle_how_to_play_event(self, event: pygame.event.Event) -> None:
        action = self.menu_ui.handle_how_to_play_event(event)
        self.handle_menu_action(action)

    def handle_menu_action(self, action: Optional[str]) -> None:
        if action == "quit":
            raise SystemExit
        if action == "difficulty_prev":
            self.cycle_difficulty(-1)
        elif action == "difficulty_next":
            self.cycle_difficulty(1)
        elif action == "announce_first":
            self.set_mode("announce_first")
        elif action == "how_to_play":
            self.set_mode("how_to_play")
        elif action == "main_menu":
            self.set_mode("main_menu")

    def handle_announce_first_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            raise SystemExit
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_mode("main_menu")
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.set_mode("play")

    def handle_winner_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            raise SystemExit
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.start_new_game = True
            self.mode = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.event.wait(pygame.MOUSEBUTTONUP)
            pygame.time.wait(250)
            pygame.event.clear()
            self.start_new_game = True
            self.mode = None

    def run_game(self):
        """
        sets up new game, provides user input to same.
        :return:
        """
        while True:
            # We have to re-run game setup when we start a new game
            self.mode = "main_menu"
            self.start_new_game = False
            self.capture_animation = None

            # randomly determine starting player
            first_player = randint(0, 1)

            run = True
            clock = pygame.time.Clock()
            board = Board(first_player)
            automa = Automa(board)
            self.menu_ui.reset()

            """Main logic/rendering loop"""
            while run and not self.start_new_game:
                clock.tick(self.FPS)
                self.update_capture_animation()


                if board.get_winner() and self.capture_animation is None:
                    self.mode = "winner"

                if board.get_turn_player() == P2_COLOR and self.mode == "play" and self.capture_animation is None:
                    _, move = automa.find_move(self.difficulty)
                    moving_piece = board.get_piece((move[0], move[1]))
                    moving_piece.toggle_selected()
                    moving_piece.draw(self.WIN)
                    pygame.display.update()
                    pygame.time.wait(1000)
                    moving_piece.toggle_selected()
                    moving_piece.draw(self.WIN)
                    pygame.display.update()
                    if board.take_turn(*move, False):
                        self.start_capture_animation(board.last_capture)

                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        raise SystemExit
                    elif self.mode == "main_menu":
                        self.handle_main_menu_event(event)
                    elif self.mode == "how_to_play":
                        self.handle_how_to_play_event(event)
                    elif event.type == pygame.MOUSEBUTTONDOWN and self.mode == "play" and board.get_turn_player() == P1_COLOR and self.capture_animation is None:
                        position = self.get_row_col(pygame.mouse.get_pos())
                        selected = board.get_piece(position)
                        if board.selected_piece is None and selected is not None and board.is_turn(selected):
                            board.set_selected(position)
                        elif board.selected_piece is not None and board.selected_piece == position:
                            board.set_selected(position)
                        elif board.selected_piece is not None:
                            if board.take_turn(board.selected_piece[0], board.selected_piece[1], position[0], position[1]):
                                self.start_capture_animation(board.last_capture)

                if self.mode == "announce_first":
                    board.draw_grid(self.WIN)
                    board.draw_pieces(self.WIN)
                    pygame.display.update()
                    message = "You go first" if board.get_turn_player() == P1_COLOR else "CPU goes first"
                    show_announcement(message, self.WIN)
                    while self.mode == "announce_first":
                        events = pygame.event.get()
                        for event in events:
                            self.handle_announce_first_event(event)

                if self.mode == "winner":
                    winner_message = ("You" if board.get_winner() == P1_COLOR else "CPU") + " Won!"
                    show_announcement(winner_message, self.WIN)
                    while self.mode == "winner":
                        events = pygame.event.get()
                        for event in events:
                            self.handle_winner_event(event)

                board.draw_grid(self.WIN)
                board.draw_pieces(self.WIN)
                board.draw_score(self.WIN)
                self.draw_capture_animation()

                if self.mode == "main_menu":
                    self.menu_ui.draw_main_menu(self.WIN, self.difficulty)
                if self.mode == "how_to_play":
                    self.menu_ui.draw_how_to_play(self.WIN)

                pygame.display.update()
