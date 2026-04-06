import json

def clean_neow():
    toutes_les_donnees_propres = []

    with open("data/raw/neow_raw.json", "r") as f:
        data = json.load(f)

    for item in data:
        donnees_propres = {
            "id": item.get("id"),
            "name": item.get("name"),
            "close_approach_date": item.get("close_approach_data")[0].get("close_approach_date") if item.get("close_approach_data") else None,
            "diameter_min_km": item.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_min"),
            "diameter_max_km": item.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_max"),
            "velocity_km_h": item.get("close_approach_data")[0].get("relative_velocity", {}).get("kilometers_per_hour") if item.get("close_approach_data") else None,
            "miss_distance_km": item.get("close_approach_data")[0].get("miss_distance", {}).get("kilometers") if item.get("close_approach_data") else None,
            "is_hazardous": item.get("is_potentially_hazardous_asteroid")
        }
        toutes_les_donnees_propres.append(donnees_propres)

    with open("data/processed/neow_clean.json", "w") as f:
        json.dump(toutes_les_donnees_propres, f)
    print("Données sauvegardées dans data/processed/neow_clean.json")

    return toutes_les_donnees_propres

if __name__ == "__main__":
    donnees_propres = clean_neow()
    print(f"Total : {len(donnees_propres)} entrées nettoyées")