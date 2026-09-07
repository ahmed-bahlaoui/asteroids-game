#!/usr/bin/env bash
set -euo pipefail

uv sync --group dev
uv run pyinstaller --clean --noconfirm --onedir --name asteroids \
  --add-data "assets:assets" \
  --add-data "fonts:fonts" \
  main.py

## Execute built binary (pass --run, requires a display)
if [[ "${1:-}" == "--run" ]]; then
  ./dist/asteroids/asteroids
fi


