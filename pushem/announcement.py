import pygame
from pushem.constants import BLUE, WHITE, WIDTH, HEIGHT

TEXT_FONT_SIZE = 64
SUBTEXT_FONT_SIZE = 32
TEXT_COLOR = BLUE
BG_FILL = WHITE
BORDER_PX = 8


def show_announcement(message: str, win: pygame.Surface, subtext="--Click to Continue--") -> None:
    """
    Displays an announcement in the center of the pygame surface with a border around for redability

    Args:
        message: Main message to display
        subtext: Smaller message underneath main message
        win: Pygame surface to display message on

    Returns: None

    """
    font = pygame.font.Font(None, TEXT_FONT_SIZE)
    subtitle_font = pygame.font.Font(None, SUBTEXT_FONT_SIZE)
    text = font.render(message, True, TEXT_COLOR)
    subtext = subtitle_font.render(subtext, True, TEXT_COLOR)
    textRect = text.get_rect()
    subtextRect = subtext.get_rect()
    subtextRect.midtop = textRect.midbottom
    allTextRect = pygame.Rect.union(textRect, subtextRect)
    allTextSurf = pygame.Surface((allTextRect.width, allTextRect.height))
    allTextSurf.fill(BG_FILL)
    allTextSurf.blit(text, textRect)
    allTextSurf.blit(subtext, subtextRect)
    allTextRect.center = WIDTH // 2, HEIGHT // 2
    background_rect = allTextRect.inflate(BORDER_PX, BORDER_PX)
    pygame.draw.rect(win, BG_FILL, background_rect)
    win.blit(allTextSurf, allTextRect)
    pygame.display.update()
