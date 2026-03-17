#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.build-venv"

cd "$ROOT_DIR"

"${PYTHON:-python3}" -m venv "$VENV_DIR"
"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip install -r requirements.txt pyinstaller
"$VENV_DIR/bin/python" -m PyInstaller \
  --windowed \
  --name pushem \
  --clean \
  play_game.py

echo "Desktop build created in $ROOT_DIR/dist"
