import json


def clean_mars():
    donnees_transform = []
    with open("data/raw/mars_raw.json", "r") as f:
        donnees = json.load(f)

    for entry in donnees:
        par = {
            "name": entry.get("name"),
            "launch_date": entry.get("launch_date"),
            "landing_date": entry.get("landing_date"),
            "status": entry.get("status"),
            "max_sol": entry.get("max_sol"),
            "max_date": entry.get("max_date"),
            "total_photos": entry.get("total_photos")
        }
        donnees_transform.append(par)

    with open("data/processed/mars_clean.json", "w") as f:
        json.dump(donnees_transform, f)
    print("Données sauvegardées dans data/processed/mars_clean.json")

    return donnees_transform


if __name__ == "__main__":
    donnees_transform = clean_mars()
    print(f"Total : {len(donnees_transform)} entrées transformées")
