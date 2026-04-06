import json
import sqlite3

def load_neow():
    connexion = sqlite3.connect("data/nasa.db")
    curseur = connexion.cursor()
    curseur.execute("""
            CREATE TABLE IF NOT EXISTS neow (
                id                 TEXT PRIMARY KEY,
                name               TEXT NOT NULL,
                close_approach_date TEXT,
                diameter_min_km    REAL,
                diameter_max_km    REAL,
                velocity_km_h      REAL,
                miss_distance_km   REAL,
                is_hazardous       INTEGER
            )
    """)
    with open("data/processed/neow_clean.json", "r") as f:
        data = json.load(f)
        for neow in data:
            curseur.execute("""
                INSERT OR REPLACE INTO neow (id, name, close_approach_date, diameter_min_km, diameter_max_km, velocity_km_h, miss_distance_km, is_hazardous)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                neow["id"],
                neow["name"],
                neow["close_approach_date"],
                neow["diameter_min_km"],
                neow["diameter_max_km"],
                neow["velocity_km_h"],
                neow["miss_distance_km"],
                1 if neow["is_hazardous"] else 0
            ))
    connexion.commit()
    connexion.close()
    return data


if __name__ == "__main__":
    data = load_neow()
    print(f"Total : {len(data)} entrées chargées dans la base de données")