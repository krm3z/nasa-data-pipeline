# NASA Data Pipeline

Projet réalisé en binôme dans le cadre du Bachelor IA & Data (Ynov).

Pipeline ETL en Python qui récupère les données de l'API APOD (Astronomy Picture of the Day) de la NASA, les nettoie et les stocke dans une base SQLite. Les données sont ensuite analysées en SQL et présentées dans un dashboard Power BI.

## Équipe

| Membre | Rôle |
|--------|------|
| [HOUDAED](https://github.com/HOUDAED) | Pipeline ETL : extraction API, nettoyage, chargement SQLite, Docker, pipelines NeoWs / DONKI / Mars Rover (branche `dev`) |
| [krm3z](https://github.com/krm3z) | Analyse : requêtes SQL, dashboard Power BI, contrôle qualité des données, documentation |

## Problématique

Comment la NASA communique-t-elle avec le grand public à travers l'APOD depuis 1995 ?

Pour y répondre, nous nous sommes concentrés sur 3 questions :
- Est-ce que la publication est régulière dans le temps ?
- Quelle place prennent les vidéos par rapport aux images ?
- Les photos publiées viennent-elles de la NASA ou de photographes extérieurs ?

## Données

| Source | Description | Statut |
|--------|-------------|--------|
| APOD | Une image ou vidéo d'astronomie publiée chaque jour depuis le 16/06/1995 | Pipeline + analyse |
| NeoWs | Objets proches de la Terre | Pipeline en cours (branche `dev`) |
| DONKI | Événements de météo spatiale | Pipeline en cours (branche `dev`) |
| Mars Rover | Photos des rovers martiens | Pipeline en cours (branche `dev`) |

Les données APOD vont du 16/06/1995 au 04/04/2026, soit 11 246 publications.

Table `apod` :

| Colonne | Description |
|---------|-------------|
| id | identifiant |
| date | date de publication |
| title | titre |
| media_type | image, video ou other |
| url | lien vers le média |
| copyright | auteur de la photo (`nasa` si pas d'auteur indiqué) |

## Pipeline

1. **Extract** (`scripts/fetch/fetch_apod.py`) : appel de l'API APOD année par année, sauvegarde du JSON brut dans `data/raw/`
2. **Transform** (`scripts/clean/clean_apod.py`) : sélection des colonnes utiles, valeurs manquantes, sauvegarde dans `data/processed/`
3. **Load** (`scripts/load/load_apod.py`) : insertion dans la base SQLite `data/nasa.db`

## Installation

```bash
git clone https://github.com/krm3z/nasa-data-pipeline.git
cd nasa-data-pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Clé API : en créer une gratuitement sur https://api.nasa.gov, puis :

```bash
cp .env.example .env
```

et mettre la clé dans `.env`.

## Lancer le pipeline

Tout d'un coup :

```bash
python main.py
```

Ou étape par étape :

```bash
python -m scripts.fetch.fetch_apod
python -m scripts.clean.clean_apod
python -m scripts.load.load_apod
```

Avec Docker :

```bash
docker build -t nasa-pipeline .
docker run --env-file .env nasa-pipeline
```

## Analyse SQL

Les requêtes sont dans `analysis/queries.sql`. Pour les lancer :

```bash
sqlite3 data/nasa.db < analysis/queries.sql
```

## Dashboard Power BI

![Dashboard](docs/dashboard.png)

Le fichier du dashboard est dans `powerbi/apod_dashboard.pbix` (à ouvrir avec Power BI Desktop).

**Préparation des données**

Power BI ne lit pas SQLite directement, donc la table `apod` a été exportée en CSV :

```bash
sqlite3 -header -csv data/nasa.db "select * from apod;" > apod.csv
```

Dans Power Query, nous avons ajouté deux colonnes :
- `Année`, extraite de la date
- `source photo`, une colonne conditionnelle : `NASA` si `copyright` vaut `nasa` ou `NASA`, sinon `EXTERNE`. Elle corrige au passage l'incohérence de casse dans les données.

**Visuels**

| Visuel | Ce qu'il montre | Équivalent SQL |
|--------|-----------------|----------------|
| Carte "Total des publications" | 11 246 publications | `count(*)` |
| Histogramme par année | une publication par jour depuis 1996 | `group by` sur l'année |
| Anneau images / vidéos | 96 % d'images, 3,5 % de vidéos | `group by media_type` |
| Anneau NASA / Externe | 50,8 % NASA, 49,2 % externe | colonne conditionnelle (`case when`) |

Point d'attention rencontré : par défaut, Power BI faisait la **somme** des `id` au lieu de les **compter**, ce qui donnait des chiffres faux (63 millions au lieu de 11 246, et 5,3 % de vidéos au lieu de 3,5 %). La colonne `id` a été passée en "Ne pas résumer" pour éviter l'erreur.

## Résultats

- **11 246 publications** entre juin 1995 et avril 2026.
- **Une publication par jour sans interruption** depuis 1996 (365 ou 366 par an). 1995 et 2026 sont incomplètes car les données commencent en juin 1995 et s'arrêtent en avril 2026.
- **96 % d'images** (10 828) contre **3,5 % de vidéos** (393). L'APOD reste surtout un format photo.
- **Environ la moitié des photos viennent de photographes extérieurs** à la NASA (5 533, soit 49 %). L'APOD sert aussi de vitrine aux astronomes amateurs et indépendants.

En résumé, la NASA utilise l'APOD comme un rendez-vous quotidien très régulier, basé sur l'image, et ouvert aux contributions extérieures.

## Limites

- L'APOD ne parle pas directement des missions spatiales, donc ces données seules ne permettent pas d'analyser l'exploration spatiale en elle-même.
- La colonne `copyright` contient à la fois `nasa` et `NASA` (5 lignes). C'est corrigé dans Power BI mais pas encore dans le script de nettoyage.
- 184 titres contiennent un retour à la ligne suivi de "Credit:", ce qui vient de l'API. Le nettoyage des titres est à améliorer.
- Les autres sources (NeoWs, DONKI, Mars Rover) ne sont pas encore fusionnées sur `main` ni analysées.

## Utilisation de l'IA

Nous avons utilisé un assistant IA pendant le projet, comme un mentor plutôt que comme un générateur de code :

- **SQL** : les requêtes ont été écrites à la main, l'IA les corrigeait en m'expliquant l'erreur (virgule oubliée entre deux colonnes, `GROUP BY` manquant, `SELECT *` au lieu de `COUNT(*)`).
- **Power BI** : guidage étape par étape, notamment pour repérer que Power BI additionnait les `id` (Somme) au lieu de les compter (Nombre), ce qui faussait les pourcentages.
- **Pipeline** : aide ponctuelle sur la structure du projet et la mise en place du pipeline Mars Rover.
- **Qualité des données** : en vérifiant les résultats, nous avons repéré l'incohérence `nasa` / `NASA` et les titres contenant "Credit:".
- **Débogage et documentation** : aide sur Git, le `.gitignore` et la rédaction de ce README.

Chaque résultat a été vérifié en relançant les requêtes SQL et en comparant avec les chiffres de Power BI. L'intérêt de l'IA pour nous : aller plus vite tout en comprenant ce qu'on fait. Chacun peut expliquer la partie qu'il a réalisée, ligne par ligne.

## Prochaines étapes

- Corriger le nettoyage de `copyright` et des titres
- Ajouter NeoWs et Mars Rover
- Analyser les mots les plus fréquents dans les titres (Mars, Hubble, JWST...) pour voir quelles missions ressortent selon les années

## Stack

Python, requests, python-dotenv, SQLite, SQL, Power BI, Docker

## Structure

```
nasa-data-pipeline/
├── analysis/
│   └── queries.sql
├── config/
│   └── config.py
├── data/            (non versionné)
│   ├── raw/
│   └── processed/
├── docs/
│   └── dashboard.png
├── powerbi/
│   └── apod_dashboard.pbix
├── scripts/
│   ├── fetch/
│   ├── clean/
│   └── load/
├── Dockerfile
├── main.py
├── requirements.txt
└── .env.example
```
