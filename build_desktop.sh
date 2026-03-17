#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.build-venv"

cd "$ROOT_DIR"

if [[ "$OSTYPE" == msys* || "$OSTYPE" == cygwin* || "$OSTYPE" == win32* ]]; then
  PYTHON_BIN="$VENV_DIR/Scripts/python.exe"
else
  PYTHON_BIN="$VENV_DIR/bin/python"
fi

"${PYTHON:-python3}" -m venv "$VENV_DIR"
"$PYTHON_BIN" -m pip install --upgrade pip
"$PYTHON_BIN" -m pip install -r requirements.txt pyinstaller
"$PYTHON_BIN" -m PyInstaller \
  --windowed \
  --onefile \
  --name pushem \
  --clean \
  play_game.py

echo "Desktop build created in $ROOT_DIR/dist"
