from typing import Optional

import pygame
from pushem.constants import WIDTH, HEIGHT, SQUARE_SIZE, P1_COLOR, P2_COLOR, WHITE, BLACK
from pushem.board import Board
from random import randint
from pushem.automa import Automa
from pushem.announcement import show_announcement
from pushem.piece import PLAYER_SIZE, PIECE_BORDER

MENU_PANEL_SIZE = (420, 410)
HOW_TO_PLAY_PANEL_SIZE = (590, 560)
PANEL_SHADOW_INFLATE = 24
PANEL_SHADOW_OFFSET = (-12, 10)
PANEL_BORDER_WIDTH = 5
PANEL_INNER_BORDER_INSET = 18
PANEL_INNER_BORDER_WIDTH = 2
MENU_TITLE_CENTER_Y = 72
MENU_ITEM_START_Y = 136
MENU_ITEM_SPACING_Y = 64
MENU_BUTTON_PADDING = (88, 26)
HOW_TO_PLAY_TITLE_CENTER_Y = 44
HOW_TO_PLAY_START_Y = 82
HOW_TO_PLAY_BODY_WIDTH_MARGIN = 76
HOW_TO_PLAY_HEADING_INDENT = 34
HOW_TO_PLAY_BODY_INDENT = 44
HOW_TO_PLAY_HEADING_SPACING = 24
HOW_TO_PLAY_LINE_HEIGHT = 19
HOW_TO_PLAY_LINE_SPACING = 4
HOW_TO_PLAY_SECTION_SPACING = 5
HOW_TO_PLAY_FOOTER_BOTTOM_OFFSET = 24
PANEL_COLOR = (244, 233, 211)
PANEL_BORDER_COLOR = (92, 60, 38)
PANEL_INNER_BORDER_COLOR = (255, 248, 236)
PANEL_SHADOW_COLOR = (25, 18, 12, 70)
MENU_BUTTON_ACTIVE_TEXT = (255, 248, 236)
MENU_BUTTON_INACTIVE_TEXT = (92, 60, 38)
MENU_BUTTON_ACTIVE_BG = (148, 87, 52)
MENU_BUTTON_INACTIVE_BG = (236, 220, 192)


class Game:

    def __init__(self):
        pygame.init()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.FPS = 60
        pygame.display.set_caption("PushEm")
        self.difficulty = 2
        self.mode: Optional[str] = None
        self.start_new_game = False
        self.menu_options = ["Play", "Difficulty", "How to Play", "Quit"]
        self.menu_index = 0
        self.difficulty_options = [("Easy", 2), ("Medium", 3), ("Hard", 4)]
        self.capture_animation = None
        self.how_to_play_sections = [
            ("Goal", "The first player to push two of their opponent's pieces off the board or into the Hole is the winner."),
            ("Movement", "There are two types of pieces: Player pieces and the Hole."),
            ("Movement", "On your turn, you may move one of your player pieces, or the Hole piece, one square up, down, left, or right."),
            ("Movement", "Moving a player piece pushes all player pieces in line with it."),
            ("Eliminating Pieces", "If a player piece is pushed off the board or into the hole, it is eliminated."),
            ("Eliminating Pieces", "You can eliminate your own pieces, so be careful."),
            ("Forbidden Moves", "You may not push the Hole piece on top of a Player Piece or off of the board."),
            ("Forbidden Moves", "You may not make a move that restores the board to the same position as your last turn."),
        ]

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
            (index for index, (_, value) in enumerate(self.difficulty_options) if value == self.difficulty),
            0,
        )
        next_index = (current_index + step) % len(self.difficulty_options)
        difficulty_str, difficulty_num = self.difficulty_options[next_index]
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

    def draw_panel(self, panel_width: int, panel_height: int) -> pygame.Rect:
        panel_rect = pygame.Rect(0, 0, panel_width, panel_height)
        panel_rect.center = (WIDTH // 2, HEIGHT // 2)

        shadow_surface = pygame.Surface(
            (panel_rect.width + PANEL_SHADOW_INFLATE, panel_rect.height + PANEL_SHADOW_INFLATE),
            pygame.SRCALPHA,
        )
        pygame.draw.rect(shadow_surface, PANEL_SHADOW_COLOR, shadow_surface.get_rect())
        self.WIN.blit(
            shadow_surface,
            (panel_rect.x + PANEL_SHADOW_OFFSET[0], panel_rect.y + PANEL_SHADOW_OFFSET[1]),
        )

        panel_surface = pygame.Surface((panel_rect.width, panel_rect.height))
        panel_surface.fill(PANEL_COLOR)
        self.WIN.blit(panel_surface, panel_rect.topleft)
        pygame.draw.rect(self.WIN, PANEL_BORDER_COLOR, panel_rect, width=PANEL_BORDER_WIDTH)
        pygame.draw.rect(
            self.WIN,
            PANEL_INNER_BORDER_COLOR,
            panel_rect.inflate(-PANEL_INNER_BORDER_INSET, -PANEL_INNER_BORDER_INSET),
            width=PANEL_INNER_BORDER_WIDTH,
        )
        return panel_rect

    def draw_main_menu(self) -> None:
        title_font = pygame.font.Font(None, 92)
        item_font = pygame.font.Font(None, 50)

        panel_width, panel_height = MENU_PANEL_SIZE
        panel_rect = self.draw_panel(panel_width, panel_height)

        title = title_font.render("PushEm", True, PANEL_BORDER_COLOR)
        title_rect = title.get_rect(center=(WIDTH // 2, panel_rect.y + MENU_TITLE_CENTER_Y))
        self.WIN.blit(title, title_rect)

        hovered_index = self.get_hovered_menu_index(pygame.mouse.get_pos())
        for index, option in enumerate(self.menu_options):
            is_selected = index == self.menu_index or index == hovered_index
            text_color = MENU_BUTTON_ACTIVE_TEXT if is_selected else MENU_BUTTON_INACTIVE_TEXT
            background_color = MENU_BUTTON_ACTIVE_BG if is_selected else MENU_BUTTON_INACTIVE_BG
            border_color = PANEL_BORDER_COLOR

            label = option
            if option == "Difficulty":
                label = f"{option}: {self.get_difficulty_name()}"

            text = item_font.render(label, True, text_color)
            text_rect = text.get_rect(
                center=(WIDTH // 2, panel_rect.y + MENU_ITEM_START_Y + index * MENU_ITEM_SPACING_Y)
            )
            button_rect = text_rect.inflate(*MENU_BUTTON_PADDING)

            pygame.draw.rect(self.WIN, background_color, button_rect)
            pygame.draw.rect(self.WIN, border_color, button_rect, width=4)
            self.WIN.blit(text, text_rect)

    def wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list[str]:
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            test_line = " ".join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))
        return lines

    def draw_how_to_play(self) -> None:
        title_font = pygame.font.Font(None, 66)
        heading_font = pygame.font.Font(None, 30)
        body_font = pygame.font.Font(None, 24)
        footer_font = pygame.font.Font(None, 24)

        panel_rect = self.draw_panel(*HOW_TO_PLAY_PANEL_SIZE)

        title = title_font.render("How to Play", True, PANEL_BORDER_COLOR)
        title_rect = title.get_rect(center=(WIDTH // 2, panel_rect.y + HOW_TO_PLAY_TITLE_CENTER_Y))
        self.WIN.blit(title, title_rect)

        current_y = panel_rect.y + HOW_TO_PLAY_START_Y
        body_width = panel_rect.width - HOW_TO_PLAY_BODY_WIDTH_MARGIN
        previous_heading = None

        for heading, body in self.how_to_play_sections:
            if heading != previous_heading:
                heading_surface = heading_font.render(heading, True, PANEL_BORDER_COLOR)
                heading_rect = heading_surface.get_rect(topleft=(panel_rect.x + HOW_TO_PLAY_HEADING_INDENT, current_y))
                self.WIN.blit(heading_surface, heading_rect)
                current_y += HOW_TO_PLAY_HEADING_SPACING
                previous_heading = heading

            wrapped_lines = self.wrap_text(f"- {body}", body_font, body_width)
            for line in wrapped_lines:
                body_surface = body_font.render(line, True, BLACK)
                body_rect = body_surface.get_rect(topleft=(panel_rect.x + HOW_TO_PLAY_BODY_INDENT, current_y))
                self.WIN.blit(body_surface, body_rect)
                current_y += HOW_TO_PLAY_LINE_HEIGHT + HOW_TO_PLAY_LINE_SPACING
            current_y += HOW_TO_PLAY_SECTION_SPACING

        footer = footer_font.render("Press Esc, Enter, or click to return.", True, PANEL_BORDER_COLOR)
        footer_rect = footer.get_rect(center=(WIDTH // 2, panel_rect.bottom - HOW_TO_PLAY_FOOTER_BOTTOM_OFFSET))
        self.WIN.blit(footer, footer_rect)

    def get_difficulty_name(self) -> str:
        return next(
            name for name, value in self.difficulty_options if value == self.difficulty
        )

    def get_hovered_menu_index(self, mouse_pos: tuple[int, int]) -> Optional[int]:
        for index in range(len(self.menu_options)):
            if self.get_menu_button_rect(index).collidepoint(mouse_pos):
                return index
        return None

    def get_menu_button_rect(self, index: int) -> pygame.Rect:
        item_font = pygame.font.Font(None, 54)
        label = self.menu_options[index]
        if label == "Difficulty":
            label = f"{label}: {self.get_difficulty_name()}"
        text = item_font.render(label, True, WHITE)
        panel_rect = pygame.Rect(0, 0, *MENU_PANEL_SIZE)
        panel_rect.center = (WIDTH // 2, HEIGHT // 2)
        text_rect = text.get_rect(center=(WIDTH // 2, panel_rect.y + MENU_ITEM_START_Y + index * MENU_ITEM_SPACING_Y))
        return text_rect.inflate(*MENU_BUTTON_PADDING)

    def handle_main_menu_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                raise SystemExit
            elif event.key == pygame.K_UP:
                self.menu_index = (self.menu_index - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.menu_index = (self.menu_index + 1) % len(self.menu_options)
            elif event.key == pygame.K_LEFT and self.menu_options[self.menu_index] == "Difficulty":
                self.cycle_difficulty(-1)
            elif event.key == pygame.K_RIGHT and self.menu_options[self.menu_index] == "Difficulty":
                self.cycle_difficulty(1)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.activate_menu_option(self.menu_options[self.menu_index])

        if event.type == pygame.MOUSEMOTION:
            hovered_index = self.get_hovered_menu_index(event.pos)
            if hovered_index is not None:
                self.menu_index = hovered_index

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            hovered_index = self.get_hovered_menu_index(mouse_pos)
            if hovered_index is not None:
                self.menu_index = hovered_index
                self.activate_menu_option(self.menu_options[hovered_index])

    def handle_how_to_play_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
            self.set_mode("main_menu")
        if event.type == pygame.MOUSEBUTTONDOWN:
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

    def activate_menu_option(self, option: str) -> None:
        if option == "Play":
            self.set_mode("announce_first")
        elif option == "Difficulty":
            self.cycle_difficulty(1)
        elif option == "How to Play":
            self.set_mode("how_to_play")
        elif option == "Quit":
            raise SystemExit

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
            self.menu_index = 0

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
                    self.draw_main_menu()
                if self.mode == "how_to_play":
                    self.draw_how_to_play()

                pygame.display.update()
