from typing import Optional

import pygame

from pushem.constants import WIDTH, HEIGHT, WHITE, BLACK

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


class MenuUI:
    def __init__(self, how_to_play_sections: list[tuple[str, list[str]]]):
        self.menu_options = ["Play", "Difficulty", "How to Play", "Quit"]
        self.menu_index = 0
        self.difficulty_options = [("Easy", 2), ("Medium", 3), ("Hard", 4)]
        self.how_to_play_sections = how_to_play_sections

    def reset(self) -> None:
        self.menu_index = 0

    def get_difficulty_name(self, difficulty: int) -> str:
        return next(
            name for name, value in self.difficulty_options if value == difficulty
        )

    def get_hovered_menu_index(self, mouse_pos: tuple[int, int], difficulty: int) -> Optional[int]:
        for index in range(len(self.menu_options)):
            if self.get_menu_button_rect(index, difficulty).collidepoint(mouse_pos):
                return index
        return None

    def get_menu_button_rect(self, index: int, difficulty: int) -> pygame.Rect:
        item_font = pygame.font.Font(None, 54)
        label = self.menu_options[index]
        if label == "Difficulty":
            label = f"{label}: {self.get_difficulty_name(difficulty)}"
        text = item_font.render(label, True, WHITE)
        panel_rect = pygame.Rect(0, 0, *MENU_PANEL_SIZE)
        panel_rect.center = (WIDTH // 2, HEIGHT // 2)
        text_rect = text.get_rect(center=(WIDTH // 2, panel_rect.y + MENU_ITEM_START_Y + index * MENU_ITEM_SPACING_Y))
        return text_rect.inflate(*MENU_BUTTON_PADDING)

    def draw_panel(self, win: pygame.Surface, panel_width: int, panel_height: int) -> pygame.Rect:
        panel_rect = pygame.Rect(0, 0, panel_width, panel_height)
        panel_rect.center = (WIDTH // 2, HEIGHT // 2)

        shadow_surface = pygame.Surface(
            (panel_rect.width + PANEL_SHADOW_INFLATE, panel_rect.height + PANEL_SHADOW_INFLATE),
            pygame.SRCALPHA,
        )
        pygame.draw.rect(shadow_surface, PANEL_SHADOW_COLOR, shadow_surface.get_rect())
        win.blit(
            shadow_surface,
            (panel_rect.x + PANEL_SHADOW_OFFSET[0], panel_rect.y + PANEL_SHADOW_OFFSET[1]),
        )

        panel_surface = pygame.Surface((panel_rect.width, panel_rect.height))
        panel_surface.fill(PANEL_COLOR)
        win.blit(panel_surface, panel_rect.topleft)
        pygame.draw.rect(win, PANEL_BORDER_COLOR, panel_rect, width=PANEL_BORDER_WIDTH)
        pygame.draw.rect(
            win,
            PANEL_INNER_BORDER_COLOR,
            panel_rect.inflate(-PANEL_INNER_BORDER_INSET, -PANEL_INNER_BORDER_INSET),
            width=PANEL_INNER_BORDER_WIDTH,
        )
        return panel_rect

    def draw_main_menu(self, win: pygame.Surface, difficulty: int) -> None:
        title_font = pygame.font.Font(None, 92)
        item_font = pygame.font.Font(None, 50)

        panel_rect = self.draw_panel(win, *MENU_PANEL_SIZE)

        title = title_font.render("PushEm", True, PANEL_BORDER_COLOR)
        title_rect = title.get_rect(center=(WIDTH // 2, panel_rect.y + MENU_TITLE_CENTER_Y))
        win.blit(title, title_rect)

        hovered_index = self.get_hovered_menu_index(pygame.mouse.get_pos(), difficulty)
        for index, option in enumerate(self.menu_options):
            is_selected = index == self.menu_index or index == hovered_index
            text_color = MENU_BUTTON_ACTIVE_TEXT if is_selected else MENU_BUTTON_INACTIVE_TEXT
            background_color = MENU_BUTTON_ACTIVE_BG if is_selected else MENU_BUTTON_INACTIVE_BG

            label = option
            if option == "Difficulty":
                label = f"{option}: {self.get_difficulty_name(difficulty)}"

            text = item_font.render(label, True, text_color)
            text_rect = text.get_rect(
                center=(WIDTH // 2, panel_rect.y + MENU_ITEM_START_Y + index * MENU_ITEM_SPACING_Y)
            )
            button_rect = text_rect.inflate(*MENU_BUTTON_PADDING)

            pygame.draw.rect(win, background_color, button_rect)
            pygame.draw.rect(win, PANEL_BORDER_COLOR, button_rect, width=4)
            win.blit(text, text_rect)

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

    def draw_how_to_play(self, win: pygame.Surface) -> None:
        title_font = pygame.font.Font(None, 66)
        heading_font = pygame.font.Font(None, 30)
        body_font = pygame.font.Font(None, 24)
        footer_font = pygame.font.Font(None, 24)

        panel_rect = self.draw_panel(win, *HOW_TO_PLAY_PANEL_SIZE)

        title = title_font.render("How to Play", True, PANEL_BORDER_COLOR)
        title_rect = title.get_rect(center=(WIDTH // 2, panel_rect.y + HOW_TO_PLAY_TITLE_CENTER_Y))
        win.blit(title, title_rect)

        current_y = panel_rect.y + HOW_TO_PLAY_START_Y
        body_width = panel_rect.width - HOW_TO_PLAY_BODY_WIDTH_MARGIN
        for heading, bullets in self.how_to_play_sections:
            heading_surface = heading_font.render(heading, True, PANEL_BORDER_COLOR)
            heading_rect = heading_surface.get_rect(topleft=(panel_rect.x + HOW_TO_PLAY_HEADING_INDENT, current_y))
            win.blit(heading_surface, heading_rect)
            current_y += HOW_TO_PLAY_HEADING_SPACING

            for bullet in bullets:
                wrapped_lines = self.wrap_text(f"- {bullet}", body_font, body_width)
                for line in wrapped_lines:
                    body_surface = body_font.render(line, True, BLACK)
                    body_rect = body_surface.get_rect(topleft=(panel_rect.x + HOW_TO_PLAY_BODY_INDENT, current_y))
                    win.blit(body_surface, body_rect)
                    current_y += HOW_TO_PLAY_LINE_HEIGHT + HOW_TO_PLAY_LINE_SPACING
                current_y += HOW_TO_PLAY_SECTION_SPACING

        footer = footer_font.render("Press Esc, Enter, or click to return.", True, PANEL_BORDER_COLOR)
        footer_rect = footer.get_rect(center=(WIDTH // 2, panel_rect.bottom - HOW_TO_PLAY_FOOTER_BOTTOM_OFFSET))
        win.blit(footer, footer_rect)

    def handle_main_menu_event(self, event: pygame.event.Event, difficulty: int) -> Optional[str]:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "quit"
            if event.key == pygame.K_UP:
                self.menu_index = (self.menu_index - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.menu_index = (self.menu_index + 1) % len(self.menu_options)
            elif event.key == pygame.K_LEFT and self.menu_options[self.menu_index] == "Difficulty":
                return "difficulty_prev"
            elif event.key == pygame.K_RIGHT and self.menu_options[self.menu_index] == "Difficulty":
                return "difficulty_next"
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.activate_menu_option(self.menu_options[self.menu_index])

        if event.type == pygame.MOUSEMOTION:
            hovered_index = self.get_hovered_menu_index(event.pos, difficulty)
            if hovered_index is not None:
                self.menu_index = hovered_index

        if event.type == pygame.MOUSEBUTTONDOWN:
            hovered_index = self.get_hovered_menu_index(pygame.mouse.get_pos(), difficulty)
            if hovered_index is not None:
                self.menu_index = hovered_index
                return self.activate_menu_option(self.menu_options[hovered_index])

        return None

    @staticmethod
    def handle_how_to_play_event(event: pygame.event.Event) -> Optional[str]:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
            return "main_menu"
        if event.type == pygame.MOUSEBUTTONDOWN:
            return "main_menu"
        return None

    @staticmethod
    def activate_menu_option(option: str) -> str:
        if option == "Play":
            return "announce_first"
        if option == "Difficulty":
            return "difficulty_next"
        if option == "How to Play":
            return "how_to_play"
        return "quit"
