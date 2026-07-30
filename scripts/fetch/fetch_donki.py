import requests
import time
import json
from datetime import datetime
from config.config import DONKI_URL, DONKI_START_YEAR, END_YEAR, NASA_API_KEY

def fetch_donki(DONKI_START_YEAR, END_YEAR):
    toutes_les_donnees = []
    aujourd_hui = datetime.now().strftime("%Y-%m-%d")

    for year in range(DONKI_START_YEAR, END_YEAR + 1):
        for month in range(1, 13):

            start_date = f"{year}-{month:02d}-01"
            if datetime.strptime(start_date, "%Y-%m-%d") > datetime.now():
                break

            if month == 12:
                end_date = f"{year}-12-31"
            else:
                end_date = f"{year}-{month + 1:02d}-01"

            if end_date > aujourd_hui:
                end_date = aujourd_hui

            params = {
                "api_key": NASA_API_KEY,
                "startDate": start_date,
                "endDate": end_date
            }

            response = requests.get(DONKI_URL, params=params)

            if response.status_code == 200:
                donnees = response.json()
                toutes_les_donnees.extend(donnees)
                print(f"{year}-{month:02d} : {len(donnees)} entrées récupérées")
            else:
                print(f"Erreur pour {year}-{month:02d} : {response.status_code}")

            time.sleep(0.5)

    with open("data/raw/donki_raw.json", "w") as f:
        json.dump(toutes_les_donnees, f)
    print("Données sauvegardées dans data/raw/donki_raw.json")

    return toutes_les_donnees


if __name__ == "__main__":
    donnees = fetch_donki(DONKI_START_YEAR, END_YEAR)
    print(f"Total : {len(donnees)} entrées récupérées")