#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$ROOT_DIR"

python3 -m pip install pyinstaller
python3 -m PyInstaller \
  --windowed \
  --name pushem \
  --clean \
  play_game.py

echo "Desktop build created in $ROOT_DIR/dist"
