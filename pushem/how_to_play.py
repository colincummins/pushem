HOW_TO_PLAY_SECTIONS = [
    (
        "Goal",
        [
            "The first player to push two of their opponent's pieces off the board or into the Hole is the winner.",
        ],
    ),
    (
        "Movement",
        [
            "There are two types of pieces - Player pieces and the Hole",
            "On your turn, you may move one of your player pieces, or the Hole piece, one square up, down, left, or right",
            "Moving a player piece pushes all player pieces in line with it.",
        ],
    ),
    (
        "Eliminating Pieces",
        [
            "If a player piece is pushed off the board or into the hole, it is eliminated.",
            "Note: Not that you should, but you can eliminate your own pieces. Be careful!",
        ],
    ),
    (
        "Forbidden Moves",
        [
            "You may not push the Hole piece on top of a Player Piece or off of the board.",
            "You may not make a move that restores the board to the same position as your last turn.",
        ],
    ),
]


def render_markdown() -> str:
    lines = ["## How to Play"]
    for heading, bullets in HOW_TO_PLAY_SECTIONS:
        lines.append(f"### {heading}")
        for bullet in bullets:
            if bullet.startswith("Note:"):
                bullet = bullet.replace("Note:", "***Note:***", 1)
            lines.append(f"* {bullet}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
