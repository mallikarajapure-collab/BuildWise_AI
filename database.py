import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "buildwise.db"


def init_db():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS recommendation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                goal TEXT NOT NULL,
                interests TEXT NOT NULL,
                recommended_projects TEXT NOT NULL
            )
        """)


def save_search(goal, interests, project_names):
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """INSERT INTO recommendation_history
               (goal, interests, recommended_projects)
               VALUES (?, ?, ?)""",
            (goal, ", ".join(interests), ", ".join(project_names))
        )


def get_history(limit=10):
    with sqlite3.connect(DB_PATH) as connection:
        return connection.execute(
            """SELECT created_at, goal, interests, recommended_projects
               FROM recommendation_history
               ORDER BY id DESC LIMIT ?""",
            (limit,)
        ).fetchall()
