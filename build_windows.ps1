$ErrorActionPreference = "Stop"

uv sync --group dev

uv run pyinstaller --clean --noconfirm --onedir --windowed --name Asteroids `
  --add-data "assets;assets" `
  --add-data "fonts;fonts" `
  main.py
