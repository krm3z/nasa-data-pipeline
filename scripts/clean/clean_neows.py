import json
import os


def transform_neows():
    donnees_transform = []
    with open("data/raw/neows_raw.json", "r") as f:
        donnees = json.load(f)

    for entry in donnees:
        approche = entry["close_approach_data"][0]
        diametre = entry["estimated_diameter"]["kilometers"]
        par = {
            "neo_id":           entry.get("id"),
            "name":             entry.get("name"),
            "date":             approche.get("close_approach_date"),
            "diameter_min_km":  diametre.get("estimated_diameter_min"),
            "diameter_max_km":  diametre.get("estimated_diameter_max"),
            "is_hazardous":     entry.get("is_potentially_hazardous_asteroid"),
            "velocity_km_s":    float(approche["relative_velocity"]["kilometers_per_second"]),
            "miss_distance_km": float(approche["miss_distance"]["kilometers"])
        }
        donnees_transform.append(par)

    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/clean_neows.json", "w") as f:
        json.dump(donnees_transform, f)
    print("Données sauvegardées dans data/processed/clean_neows.json")

    return donnees_transform


if __name__ == "__main__":
    donnees_transform = transform_neows()
    print(f"Total : {len(donnees_transform)} entrées transformées")

