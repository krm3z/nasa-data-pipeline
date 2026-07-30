import time
from config.config import ROVERS
from scripts.mars.fetch_mars import fetch_mars
from scripts.mars.clean_mars import clean_mars
from scripts.mars.load_mars import load_mars

if __name__ == "__main__":
    debut = time.time()

    print("━" * 50)
    print("🛰️  MARS EXPLORATION PIPELINE")
    print("━" * 50)

    print("\n📡 [1/3] Extraction des manifests de missions...")
    fetch_mars(ROVERS)
    print("✅  Extraction terminée")

    print("\n🔄 [2/3] Transformation des données...")
    clean_mars()
    print("✅  Transformation terminée")

    print("\n💾 [3/3] Chargement dans SQLite...")
    load_mars()
    print("✅  Chargement terminé")

    duree = round(time.time() - debut, 2)

    print("\n" + "━" * 50)
    print("🚀  Pipeline Mars terminé avec succès !")
    print(f"⏱️   Durée totale : {duree} secondes")
    print("━" * 50)
