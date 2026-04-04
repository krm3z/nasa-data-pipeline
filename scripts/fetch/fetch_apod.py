import requests
import time
import json
from datetime import datetime
from config.config import START_YEAR, END_YEAR, NASA_API_KEY, APOD_URL

def fetch_apod(START_YEAR, END_YEAR):
    toutes_les_donnees = []
    aujourd_hui = datetime.now().strftime("%Y-%m-%d")

    for year in range(START_YEAR, END_YEAR + 1):

        if year == 1995:
            start_date = "1995-06-16"
        else:
            start_date = f"{year}-01-01"

        if year == END_YEAR:
            end_date = aujourd_hui
        else:
            end_date = f"{year}-12-31"

        params = {
            "api_key": NASA_API_KEY,
            "start_date": start_date,
            "end_date": end_date
        }

        response = requests.get(APOD_URL, params=params)

        if response.status_code == 200:
            donnees = response.json()
            toutes_les_donnees.extend(donnees)
            print(f"{year} : {len(donnees)} entrées récupérées")
        else:
            print(f"Erreur pour {year} : {response.status_code}")

        time.sleep(0.5)

    with open("data/raw/apod_raw.json", "w") as f:
        json.dump(toutes_les_donnees, f)
    print("Données sauvegardées dans data/raw/apod_raw.json")

    return toutes_les_donnees


if __name__ == "__main__":
    donnees = fetch_apod(START_YEAR, END_YEAR)
    print(f"Total : {len(donnees)} entrées récupérées")