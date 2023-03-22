import pygame
from pushem.constants import WIDTH, HEIGHT, SQUARE_SIZE
from pushem.board import Board

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
pygame.display.set_caption("PushEm")


def get_row_col(pos: (int, int)) -> (int, int):
    """
    Get grid row and column from mouse position
    :param pos: mouse pos from pygame
    :return: row and column (int, int)
    """
    return pos[1]//SQUARE_SIZE, pos[0]//SQUARE_SIZE


def main():
    """
    Sets up new game, provides user input to same.
    :return:
    """
    run = True
    clock = pygame.time.Clock()
    board = Board()

    """Main logic/rendering loop"""
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(get_row_col(pygame.mouse.get_pos()))

        board.draw_grid(WIN)
        board.draw_pieces(WIN)
        pygame.display.update()

    pygame.quit()


main()
