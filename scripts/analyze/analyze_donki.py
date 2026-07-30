import json
import sqlite3


def analyze_donki():
    connexion = sqlite3.connect("data/nasa.db")
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT
            substr(time21_5, 1, 4) AS year,
            COUNT(*) AS total,
            AVG(speed_km_s) AS avg_speed_km_s,
            MAX(speed_km_s) AS max_speed_km_s
        FROM donki
        WHERE time21_5 IS NOT NULL
        GROUP BY year
        ORDER BY year
    """)
    lignes = curseur.fetchall()
    connexion.close()

    resultats = []
    for year, total, avg_speed_km_s, max_speed_km_s in lignes:
        resultats.append({
            "year": year,
            "total": total,
            "avg_speed_km_s": round(avg_speed_km_s, 2) if avg_speed_km_s else None,
            "max_speed_km_s": max_speed_km_s
        })

    print(f"{'Année':<8}{'Total CME':<12}{'Vitesse moy. (km/s)':<22}{'Vitesse max (km/s)':<20}")
    for r in resultats:
        print(f"{r['year']:<8}{r['total']:<12}{r['avg_speed_km_s']:<22}{r['max_speed_km_s']:<20}")

    with open("data/analysis/donki_summary.json", "w") as f:
        json.dump(resultats, f, indent=2)
    print("Résumé sauvegardé dans data/analysis/donki_summary.json")

    return resultats


if __name__ == "__main__":
    analyze_donki()
