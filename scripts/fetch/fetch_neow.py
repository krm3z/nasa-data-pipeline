import requests
import time
import json
from datetime import datetime, timedelta
from config.config import START_YEAR, END_YEAR, NASA_API_KEY, NEOWS_URL

def fetch_neow(START_YEAR, END_YEAR):
    toutes_les_donnees = []

    for year in range(START_YEAR, END_YEAR + 1):
        for month in range(1, 13):

            if year == 1995 and month < 6:
                continue

            for week in range(4):
                day = 1 + (week * 7)

                start_date = f"{year}-{month:02d}-{day:02d}"
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = start + timedelta(days=6)

                if end > datetime.now():
                    end = datetime.now()

                end_date = end.strftime("%Y-%m-%d")

                params = {
                    "api_key": NASA_API_KEY,
                    "start_date": start_date,
                    "end_date": end_date
                }

                response = requests.get(NEOWS_URL, params=params)

                if response.status_code == 200:
                    donnees = response.json()
                    neo_objects = donnees["near_earth_objects"]
                    for date, objets in neo_objects.items():
                        for objet in objets:
                            toutes_les_donnees.append(objet)
                    print(f"{year}-{month:02d} semaine {week+1} : ok")
                else:
                    print(f"Erreur {year}-{month:02d} : {response.status_code}")

                time.sleep(0.5)

    with open("data/raw/neow_raw.json", "w") as f:
        json.dump(toutes_les_donnees, f)
    print("Données sauvegardées dans data/raw/neow_raw.json")

    return toutes_les_donnees


if __name__ == "__main__":
    donnees = fetch_neow(START_YEAR, END_YEAR)
    print(f"Total : {len(donnees)} entrées récupérées")