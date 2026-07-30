import json
import sqlite3


def analyze_neow():
    connexion = sqlite3.connect("data/nasa.db")
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT
            substr(close_approach_date, 1, 4) AS year,
            COUNT(*) AS total,
            SUM(is_hazardous) AS hazardous,
            AVG(diameter_max_km) AS avg_diameter_km
        FROM neow
        WHERE close_approach_date IS NOT NULL
        GROUP BY year
        ORDER BY year
    """)
    lignes = curseur.fetchall()
    connexion.close()

    resultats = []
    for year, total, hazardous, avg_diameter_km in lignes:
        resultats.append({
            "year": year,
            "total": total,
            "hazardous": hazardous,
            "hazardous_pct": round(100 * hazardous / total, 2) if total else 0,
            "avg_diameter_km": round(avg_diameter_km, 4) if avg_diameter_km else None
        })

    print(f"{'Année':<8}{'Total':<10}{'Dangereux':<12}{'% Dangereux':<14}{'Diamètre moy. (km)':<20}")
    for r in resultats:
        print(f"{r['year']:<8}{r['total']:<10}{r['hazardous']:<12}{r['hazardous_pct']:<14}{r['avg_diameter_km']:<20}")

    with open("data/analysis/neow_summary.json", "w") as f:
        json.dump(resultats, f, indent=2)
    print("Résumé sauvegardé dans data/analysis/neow_summary.json")

    return resultats


if __name__ == "__main__":
    analyze_neow()
