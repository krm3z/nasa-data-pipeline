import json
import sqlite3


def load_donki():
    connexion = sqlite3.connect("data/nasa.db")
    curseur = connexion.cursor()
    curseur.execute("""
            CREATE TABLE IF NOT EXISTS donki (
                id                TEXT PRIMARY KEY,
                time21_5          TEXT,
                latitude          REAL,
                longitude         REAL,
                half_angle        REAL,
                speed_km_s        REAL,
                type              TEXT,
                is_most_accurate  INTEGER,
                note              TEXT
            )
    """)
    with open("data/processed/donki_clean.json", "r") as f:
        data = json.load(f)
        for donki in data:
            curseur.execute("""
                INSERT OR REPLACE INTO donki (id, time21_5, latitude, longitude, half_angle, speed_km_s, type, is_most_accurate, note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                donki["id"],
                donki["time21_5"],
                donki["latitude"],
                donki["longitude"],
                donki["half_angle"],
                donki["speed_km_s"],
                donki["type"],
                1 if donki["is_most_accurate"] else 0,
                donki["note"],
            ))
    connexion.commit()
    connexion.close()
    return data


if __name__ == "__main__":
    data = load_donki()
    print(f"Total : {len(data)} entrées chargées dans la base de données")
