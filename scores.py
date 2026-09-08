import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".asteroids_scores.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS scores (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  best INTEGER NOT NULL DEFAULT 0
);
INSERT OR IGNORE INTO scores (id, best) VALUES (1, 0);
"""


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA)


def get_best_score() -> int:
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("SELECT best FROM scores WHERE id = 1").fetchone()
        return row[0] if row else 0


def save_best_score(score: int) -> int:
    # Returns new best after conditional update.
    # Single-row upsert avoids unbounded table growth
    # vs INSERT-per-game + SELECT MAX(score).
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE scores SET best = MAX(best, ?) WHERE id = 1",
            (score,),
        )
    return get_best_score()
