import json
import sqlite3
def load_apod():
        connexion = sqlite3.connect("data/nasa.db")
        curseur = connexion.cursor()

        # tes requêtes SQL ici
        curseur.execute("""
                CREATE TABLE IF NOT EXISTS apod (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    date      TEXT NOT NULL,
                    title     TEXT NOT NULL,
                    media_type TEXT NOT NULL,
                    url TEXT,
                    copyright TEXT NOT NULL DEFAULT 'NASA'
                )
        """)
        curseur.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS ux_apod_date ON apod(date)
        """)
        with open("data/processed/clean_apod.json", "r") as f:
            apod_data = json.load(f)
            for apod in apod_data:
                curseur.execute("""
                    INSERT OR REPLACE INTO apod (date, title, media_type, url, copyright)
                    VALUES (?, ?, ?, ?, ?)
                """, (apod["date"], apod["title"], apod["media_type"], apod["url"], apod["copyright"]))
        connexion.commit()
        connexion.close()

if __name__ == "__main__":    
     load_apod()
