import json
import sqlite3


def load_mars():
    connexion = sqlite3.connect("data/nasa.db")
    curseur = connexion.cursor()
    curseur.execute("""
            CREATE TABLE IF NOT EXISTS mars_missions (
                name          TEXT PRIMARY KEY,
                launch_date   TEXT,
                landing_date  TEXT,
                status        TEXT,
                max_sol       INTEGER,
                max_date      TEXT,
                total_photos  INTEGER
            )
    """)
    with open("data/processed/mars_clean.json", "r") as f:
        data = json.load(f)
        for mission in data:
            curseur.execute("""
                INSERT OR REPLACE INTO mars_missions (name, launch_date, landing_date, status, max_sol, max_date, total_photos)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                mission["name"],
                mission["launch_date"],
                mission["landing_date"],
                mission["status"],
                mission["max_sol"],
                mission["max_date"],
                mission["total_photos"]
            ))
    connexion.commit()
    connexion.close()
    return data


if __name__ == "__main__":
    data = load_mars()
    print(f"Total : {len(data)} entrées chargées dans la base de données")
