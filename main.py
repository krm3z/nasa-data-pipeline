from config.config import START_YEAR, END_YEAR
from scripts.fetch.fetch_apod import fetch_apod
from scripts.clean.clean_apod import transform_apod
from scripts.load.load_apod import load_apod
from scripts.fetch.fetch_neows import fetch_neows
from scripts.clean.clean_neows import transform_neows
from scripts.load.load_neows import load_neows

if __name__ == "__main__":
    print("━" * 50)
    print("🚀  NASA DATA PIPELINE")
    print("━" * 50)

    print("\n📡 [1/6] Extraction APOD...")
    fetch_apod(START_YEAR, END_YEAR)

    print("\n🔄 [2/6] Transformation APOD...")
    transform_apod()

    print("\n💾 [3/6] Chargement APOD...")
    load_apod()

    print("\n📡 [4/6] Extraction NeoWs...")
    fetch_neows(START_YEAR, END_YEAR)

    print("\n🔄 [5/6] Transformation NeoWs...")
    transform_neows()

    print("\n💾 [6/6] Chargement NeoWs...")
    load_neows()

    print("\n" + "━" * 50)
    print("🌌  Pipeline terminé avec succès !")
    print("━" * 50)
