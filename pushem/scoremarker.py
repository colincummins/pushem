from .constants import P1_COLOR, P2_COLOR, WIDTH, HEIGHT, SQUARE_SIZE, SQUARE_PAD, ROWS, COLS
import pygame

SCALE = .25


class ScoreMarker:
    def __init__(self, color, num):
        self.color = color
        self.edge_length = SQUARE_SIZE * SCALE
        self.x = num * (WIDTH // COLS) + ((WIDTH // COLS - self.edge_length) // 2)
        self.y = ((HEIGHT // COLS) - self.edge_length) // 2

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.edge_length, self.edge_length))

