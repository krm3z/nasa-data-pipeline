import json
import sqlite3


def analyze_apod():
    connexion = sqlite3.connect("data/nasa.db")
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT
            substr(date, 1, 4) AS year,
            COUNT(*) AS total,
            SUM(CASE WHEN media_type = 'image' THEN 1 ELSE 0 END) AS images,
            SUM(CASE WHEN copyright = 'nasa' THEN 1 ELSE 0 END) AS nasa_only
        FROM apod
        WHERE date IS NOT NULL
        GROUP BY year
        ORDER BY year
    """)
    lignes = curseur.fetchall()
    connexion.close()

    resultats = []
    for year, total, images, nasa_only in lignes:
        resultats.append({
            "year": year,
            "total": total,
            "images": images,
            "videos": total - images,
            "nasa_only_pct": round(100 * nasa_only / total, 2) if total else 0
        })

    print(f"{'Année':<8}{'Total':<10}{'Images':<10}{'Vidéos':<10}{'% Sans copyright':<18}")
    for r in resultats:
        print(f"{r['year']:<8}{r['total']:<10}{r['images']:<10}{r['videos']:<10}{r['nasa_only_pct']:<18}")

    with open("data/analysis/apod_summary.json", "w") as f:
        json.dump(resultats, f, indent=2)
    print("Résumé sauvegardé dans data/analysis/apod_summary.json")

    return resultats


if __name__ == "__main__":
    analyze_apod()
