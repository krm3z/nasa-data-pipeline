import requests
import time
import json
import os
from datetime import datetime, timedelta
from config.config import NASA_API_KEY, NEOWS_URL, START_YEAR, END_YEAR


def fetch_neows(start, end):
    toutes_les_donnees = []
    debut = datetime(start, 1, 1)
    fin = min(datetime(end, 12, 31), datetime.now())

    while debut <= fin:
        fin_fenetre = min(debut + timedelta(days=6), fin)

        params = {
            "api_key": NASA_API_KEY,
            "start_date": debut.strftime("%Y-%m-%d"),
            "end_date": fin_fenetre.strftime("%Y-%m-%d")
        }

        try:
            response = requests.get(NEOWS_URL, params=params, timeout=30)
            response.raise_for_status()
            for asteroides in response.json()["near_earth_objects"].values():
                toutes_les_donnees.extend(asteroides)
            print(f"{params['start_date']} → {params['end_date']} : OK")
        except requests.exceptions.RequestException as e:
            print(f"Erreur pour {params['start_date']} : {e}")

        debut = fin_fenetre + timedelta(days=1)
        time.sleep(4)

    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/neows_raw.json", "w") as f:
        json.dump(toutes_les_donnees, f)
    print("Données sauvegardées dans data/raw/neows_raw.json")

    return toutes_les_donnees


if __name__ == "__main__":
    donnees = fetch_neows(START_YEAR, END_YEAR)
    print(f"Total : {len(donnees)} astéroïdes récupérés")
