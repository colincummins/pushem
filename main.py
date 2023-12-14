import pygame
from pushem.constants import WIDTH, HEIGHT, SQUARE_SIZE
from pushem.board import Board
from random import randint

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
    # Randomly determine starting player
    first_player = randint(0,1)
    print("First Player: ", first_player)

    run = True
    clock = pygame.time.Clock()
    board = Board(first_player)



    """Main logic/rendering loop"""
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = get_row_col(pygame.mouse.get_pos())
                selected = board.get_piece(position)
                if board.selected_piece is None and selected is not None and board.is_turn(selected):
                    board.set_selected(position)
                elif board.selected_piece is not None and board.selected_piece == position:
                    board.set_selected(position)
                elif board.selected_piece is not None:
                    board.take_turn(board.selected_piece[0], board.selected_piece[1], position[0], position[1])




        board.draw_grid(WIN)
        board.draw_pieces(WIN)
        pygame.display.update()

    pygame.quit()


main()
