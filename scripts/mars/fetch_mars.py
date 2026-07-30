import requests
import time
import json
from config.config import NASA_API_KEY, MARS_URL, ROVERS

def fetch_mars(ROVERS):
    toutes_les_donnees = []

    for rover in ROVERS:
        params = {"api_key": NASA_API_KEY}

        response = requests.get(f"{MARS_URL}/{rover}", params=params)

        if response.status_code == 200:
            donnees = response.json()
            manifest = donnees.get("photo_manifest")
            if manifest:
                toutes_les_donnees.append(manifest)
            print(f"{rover} : manifest récupéré")
        else:
            print(f"Erreur pour {rover} : {response.status_code}")

        time.sleep(0.5)

    with open("data/raw/mars_raw.json", "w") as f:
        json.dump(toutes_les_donnees, f)
    print("Données sauvegardées dans data/raw/mars_raw.json")

    return toutes_les_donnees


if __name__ == "__main__":
    donnees = fetch_mars(ROVERS)
    print(f"Total : {len(donnees)} manifests récupérés")
