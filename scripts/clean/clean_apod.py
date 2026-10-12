import json


def transform_apod():
    donnees_transform =[]
    with open("data/raw/apod_raw.json","r") as f:
        donnees = json.load(f)

    for entry in donnees :
        par = {
            "date" : entry.get("date"),
            "title": entry.get("title"),
            "media_type": entry.get("media_type"),
            "url": entry.get("url") or entry.get("hdurl", ""),
            "copyright":   entry.get("copyright") or "nasa"
        }
        donnees_transform.append(par)
        

    with open("data/processed/clean_apod.json","w") as f:
        json.dump(donnees_transform, f)
    print("Données sauvegardées dans data/processed/clean_apod.json")
    
    return donnees_transform


if __name__ == "__main__":
    donnees_transform = transform_apod()
    print(f"Total : {len(donnees_transform)} entrées transformées")