import time
from config.config import START_YEAR, END_YEAR, DONKI_START_YEAR
from scripts.fetch.fetch_apod import fetch_apod
from scripts.fetch.fetch_neow import fetch_neow
from scripts.fetch.fetch_donki import fetch_donki
from scripts.clean.clean_apod import transform_apod
from scripts.clean.clean_neow import clean_neow
from scripts.clean.clean_donki import clean_donki
from scripts.load.load_apod import load_apod
from scripts.load.load_neow import load_neow
from scripts.load.load_donki import load_donki

if __name__ == "__main__":
    debut = time.time()

    print("━" * 50)
    print("🚀  NASA DATA PIPELINE")
    print("━" * 50)

    print("\n📡 [1/3] Extraction des données NASA...")
    fetch_apod(START_YEAR, END_YEAR)
    fetch_neow(START_YEAR, END_YEAR)
    fetch_donki(DONKI_START_YEAR, END_YEAR)
    print("✅  Extraction terminée")

    print("\n🔄 [2/3] Transformation des données...")
    transform_apod()
    clean_neow()
    clean_donki()
    print("✅  Transformation terminée")

    print("\n💾 [3/3] Chargement dans SQLite...")
    load_apod()
    load_neow()
    load_donki()
    print("✅  Chargement terminé")

    duree = round(time.time() - debut, 2)

    print("\n" + "━" * 50)
    print("🌌  Pipeline terminé avec succès !")
    print(f"⏱️   Durée totale : {duree} secondes")
    print("━" * 50) 