#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$ROOT_DIR"

python3 -m pip install pygbag
python3 -m pygbag --build play_game.py

echo "Web build created in $ROOT_DIR/build/web"
