
import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "nirnaya.db"


def init_db():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            rainfall_mm REAL,
            flood_risk TEXT,
            final_decision TEXT,
            full_result TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_analysis(result):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO analysis_history
        (rainfall_mm, flood_risk, final_decision, full_result)
        VALUES (?, ?, ?, ?)
    """, (
        result["input"]["rainfall_mm"],
        result["prediction"]["flood_risk"],
        result["final_decision"],
        json.dumps(result)
    ))

    connection.commit()
    connection.close()


def get_history():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, created_at, rainfall_mm,
               flood_risk, final_decision
        FROM analysis_history
        ORDER BY id DESC
    """)

    records = [dict(row) for row in cursor.fetchall()]
    connection.close()

    return records
