import json


def clean_donki():
    toutes_les_donnees_propres = []

    with open("data/raw/donki_raw.json", "r") as f:
        data = json.load(f)

    for item in data:
        donnees_propres = {
            "id": item.get("associatedCMEID") or item.get("link"),
            "time21_5": item.get("time21_5"),
            "latitude": item.get("latitude"),
            "longitude": item.get("longitude"),
            "half_angle": item.get("halfAngle"),
            "speed_km_s": item.get("speed"),
            "type": item.get("type"),
            "is_most_accurate": item.get("isMostAccurate"),
            "note": item.get("note"),
        }
        if donnees_propres["id"]:
            toutes_les_donnees_propres.append(donnees_propres)

    with open("data/processed/donki_clean.json", "w") as f:
        json.dump(toutes_les_donnees_propres, f)
    print("Données sauvegardées dans data/processed/donki_clean.json")

    return toutes_les_donnees_propres


if __name__ == "__main__":
    donnees_propres = clean_donki()
    print(f"Total : {len(donnees_propres)} entrées nettoyées")
