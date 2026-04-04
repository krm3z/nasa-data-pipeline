
from config.config import START_YEAR, END_YEAR
from scripts.fetch.fetch_apod import fetch_apod
from scripts.clean.clean_apod import transform_apod
from scripts.load.load_apod import load_apod

if __name__ == "__main__":
    print("━" * 50)
    print("🚀  NASA DATA PIPELINE")
    print("━" * 50)

    print("\n📡 [1/3] Extraction des données NASA...")
    fetch_apod(START_YEAR, END_YEAR)
    print("✅  Extraction terminée")

    print("\n🔄 [2/3] Transformation des données...")
    transform_apod()
    print("✅  Transformation terminée")

    print("\n💾 [3/3] Chargement dans SQLite...")
    load_apod()
    print("✅  Chargement terminé")

    print("\n" + "━" * 50)
    print("🌌  Pipeline terminé avec succès !")
    print("━" * 50)