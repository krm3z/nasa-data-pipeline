import json
import sqlite3
from datetime import datetime


def analyze_mars():
    connexion = sqlite3.connect("data/nasa.db")
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT name, launch_date, landing_date, status, max_sol, max_date, total_photos
        FROM mars_missions
        ORDER BY launch_date
    """)
    lignes = curseur.fetchall()
    connexion.close()

    resultats = []
    for name, launch_date, landing_date, status, max_sol, max_date, total_photos in lignes:
        duree_jours = None
        if landing_date and max_date:
            duree_jours = (
                datetime.strptime(max_date, "%Y-%m-%d") - datetime.strptime(landing_date, "%Y-%m-%d")
            ).days

        resultats.append({
            "name": name,
            "launch_date": launch_date,
            "landing_date": landing_date,
            "status": status,
            "max_sol": max_sol,
            "duree_jours": duree_jours,
            "total_photos": total_photos
        })

    print(f"{'Mission':<14}{'Lancement':<14}{'Atterrissage':<14}{'Statut':<10}{'Sols':<8}{'Durée (j)':<12}{'Photos':<10}")
    for r in resultats:
        print(f"{r['name']:<14}{r['launch_date']:<14}{r['landing_date']:<14}{r['status']:<10}"
              f"{r['max_sol']:<8}{str(r['duree_jours']):<12}{r['total_photos']:<10}")

    with open("data/analysis/mars_summary.json", "w") as f:
        json.dump(resultats, f, indent=2)
    print("Résumé sauvegardé dans data/analysis/mars_summary.json")

    return resultats


if __name__ == "__main__":
    analyze_mars()
