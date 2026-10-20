import json
import sqlite3
from config.config import DB_PATH


def load_neows():
    connexion = sqlite3.connect(DB_PATH)
    curseur = connexion.cursor()

    curseur.execute("""
        CREATE TABLE IF NOT EXISTS neows (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            neo_id           TEXT NOT NULL,
            name             TEXT NOT NULL,
            date             TEXT NOT NULL,
            diameter_min_km  REAL,
            diameter_max_km  REAL,
            is_hazardous     INTEGER NOT NULL,
            velocity_km_s    REAL,
            miss_distance_km REAL,
            UNIQUE (neo_id, date)
        )
    """)

    with open("data/processed/clean_neows.json", "r") as f:
        neows_data = json.load(f)

    for neo in neows_data:
        curseur.execute("""
            INSERT OR IGNORE INTO neows (neo_id, name, date, diameter_min_km, diameter_max_km,
                                         is_hazardous, velocity_km_s, miss_distance_km)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (neo["neo_id"], neo["name"], neo["date"], neo["diameter_min_km"], neo["diameter_max_km"],
              neo["is_hazardous"], neo["velocity_km_s"], neo["miss_distance_km"]))

    connexion.commit()
    connexion.close()
    print(f"Données chargées dans {DB_PATH}")


if __name__ == "__main__":
    load_neows()
