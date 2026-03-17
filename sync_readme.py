from pathlib import Path

from pushem.how_to_play import render_markdown

README_PATH = Path(__file__).resolve().parent / "README.md"
START_MARKER = "<!-- how-to-play:start -->"
END_MARKER = "<!-- how-to-play:end -->"


def main() -> None:
    readme = README_PATH.read_text()
    start_index = readme.index(START_MARKER) + len(START_MARKER)
    end_index = readme.index(END_MARKER)
    replacement = f"\n{render_markdown()}\n"
    updated = readme[:start_index] + replacement + readme[end_index:]
    README_PATH.write_text(updated)


if __name__ == "__main__":
    main()
