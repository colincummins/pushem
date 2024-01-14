# PushEm
## Introduction
PushEm is a clone of the board game Ostle, made using Pygame.

This program is for demonstration purposes only.

## Installation/Requirements
1. You will need an existing installation of Python 3
2. Download the code
3. In the `pushem` directory, run the command `pip install -r requirements.txt` to install the necessary libraries
4. Run the game with `python3 play_game.py`

## How to Play
### Goal -
The first player to push two of their opponent's pieces off the board or into the Hole is the winner.

### Movement
* There are two types of pieces - Player pieces and the Hole
* On your turn, you may move one of your player pieces, or the Hole piece, one square up, down, left, or right
* Moving a player piece pushes all player pieces in line with it.

### Eliminating Pieces
* If a player piece is pushed off the board or into the hole, it is eliminated.
* ***Note:*** Not that you should, but you can eliminate your own pieces. Be careful!

### Forbidden Moves
* You may not push the Hole piece on top of a Player Piece or off of the board.
* You may not make a move that restores the board to the same position as your last turn.
