# 🚀 NASA Data Pipeline

> Pipeline ETL qui collecte, transforme et stocke les données ouvertes de la NASA dans une base SQLite, puis les analyse en SQL et dans un dashboard Power BI.

Projet réalisé en binôme dans le cadre du Bachelor IA & Data (Ynov).

## 🌌 Problématique

Comment les données ouvertes de la NASA permettent-elles de retracer l'évolution de l'exploration spatiale moderne ?

On part de l'**APOD** (Astronomy Picture of the Day) : depuis le 16 juin 1995, la NASA publie chaque jour une image ou une vidéo d'astronomie avec un titre et une explication. Ces 30 ans de publications servent de fil chronologique : on cherche dans les titres les grandes missions (télescopes, sondes, rovers, navettes) pour voir quand elles apparaissent et ce qu'elles racontent.

## 📡 Sources de données

| Source | Description | Statut |
|--------|-------------|--------|
| APOD | Astronomy Picture of the Day | ✅ Disponible |
| NeoWs | Objets proches de la Terre | 🚧 En cours (branche `dev`) |
| DONKI | Événements de météo spatiale | 🚧 En cours (branche `dev`) |
| Mars Rover | Photos des rovers | 🚧 En cours (branche `dev`) |
| Meteorites | Données de météorites | ⏳ Pas commencé |

## 📋 Avancement

### ✅ Ce qui est fait

**Pipeline APOD**
- Extraction de toutes les publications depuis le 16/06/1995, année par année, via l'API NASA
- Nettoyage : sélection des colonnes utiles, `copyright` vide remplacé par `nasa`
- Chargement dans SQLite (`data/nasa.db`, table `apod`)
- `main.py` qui enchaîne les 3 étapes, et un `Dockerfile` pour lancer le pipeline dans un conteneur

**Analyse SQL et dashboard Power BI** (extraction du 04/04/2026, 11 246 publications)
- Régularité : une publication par jour, sans interruption, depuis 1996
- Format : 96 % d'images, 3,5 % de vidéos
- Origine : environ la moitié des photos vient de photographes extérieurs à la NASA, et cette part augmente avec le temps
- Contrôle croisé SQL / Power BI, qui a permis de repérer une erreur d'agrégation dans Power BI (somme des `id` au lieu d'un comptage)

![Dashboard APOD](docs/dashboard.png)

**Analyse des missions dans les titres** (`analysis/queries.sql`)
- Pluton : pic de titres en juillet 2015, qui correspond au survol par la sonde New Horizons
- Navette spatiale : les titres de 2011 parlent d'Atlantis plutôt que de "Shuttle" ; Atlantis ressort en mai 2010 (STS-132) et juillet 2011 (STS-135, dernière mission des navettes), puis les navettes n'apparaissent plus que dans des musées

### 🚧 En cours

- Requêtes déjà écrites, résultats à interpréter : Hubble, James Webb, Spirit, Curiosity, Perseverance
- Pipelines NeoWs, DONKI et Mars Rover sur la branche `dev`

### 📝 Ce qu'il reste à faire

**Analyse**
- [ ] Interpréter les requêtes Hubble, Webb, Spirit, Curiosity et Perseverance
- [ ] Répondre à la problématique : mettre bout à bout les missions trouvées pour retracer l'exploration spatiale depuis 1995
- [ ] Ajouter au dashboard une page sur les missions, et l'évolution par année de la part vidéo et de la part externe

**Pipeline**
- [ ] Harmoniser `copyright` dans le nettoyage (`nasa` et `NASA` coexistent sur 5 lignes)
- [ ] Nettoyer les titres qui contiennent un retour à la ligne suivi de "Credit:" (184 titres)
- [ ] Éviter les doublons dans `load_apod` : relancer le pipeline réinsère toutes les lignes dans la table existante
- [ ] Ramener NeoWs, DONKI et Mars Rover de `dev` vers `main`
- [ ] Commencer la source Meteorites

## ⚙️ Installation

### 1 — Cloner le projet
```bash
git clone https://github.com/krm3z/nasa-data-pipeline.git
cd nasa-data-pipeline
```

### 2 — Créer et activer le venv
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3 — Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4 — Configurer la clé API NASA
```bash
cp .env.example .env
# Ouvre .env et remplace your_api_key_here par ta vraie clé
```

La clé est gratuite sur https://api.nasa.gov.

## 🔄 Lancer le pipeline APOD

### Option 1 — Tout lancer en une seule commande
```bash
python main.py
```

### Option 2 — Lancer étape par étape
```bash
# Extract — récupère les données depuis 1995
python -m scripts.fetch.fetch_apod

# Transform — nettoie et structure les données
python -m scripts.clean.clean_apod

# Load — insère dans SQLite
python -m scripts.load.load_apod
```

### Option 3 — Avec Docker
```bash
docker build -t nasa-pipeline .
docker run --env-file .env nasa-pipeline
```

## 📊 Lancer l'analyse

```bash
# Requêtes SQL
sqlite3 data/nasa.db < analysis/queries.sql
```

Dashboard : ouvrir `powerbi/apod_dashboard.pbix` avec Power BI Desktop.

## 📁 Structure du projet

```
nasa-data-pipeline/
├── analysis/
│   └── queries.sql       ← requêtes d'analyse
├── config/
│   └── config.py         ← paramètres centralisés
├── data/                 ← non versionné
│   ├── raw/              ← données brutes API
│   ├── processed/        ← données nettoyées
│   └── nasa.db           ← base SQLite
├── docs/
│   └── dashboard.png     ← capture du dashboard
├── powerbi/
│   └── apod_dashboard.pbix
├── scripts/
│   ├── fetch/            ← extraction API
│   ├── clean/            ← transformation
│   └── load/             ← chargement SQLite
├── Dockerfile
├── main.py               ← lance tout le pipeline
├── .env.example          ← template clé API
├── requirements.txt
└── README.md
```

## 🛠️ Stack technique

- **Python 3** — langage principal
- **requests** — appels API
- **python-dotenv** — gestion des secrets
- **SQLite** — base de données locale
- **SQL** — analyse
- **Power BI** — dashboard
- **Docker** — exécution du pipeline

## ⚠️ Limites

- L'APOD montre ce que la NASA choisit de publier, pas l'ensemble de ses missions : une mission absente des titres n'est pas forcément une mission sans importance.
- La recherche se fait par mot-clé dans les titres : une mission citée seulement dans l'explication, ou sous un autre nom (Atlantis au lieu de Shuttle), peut passer inaperçue.
- Pas de données d'audience : on analyse le contenu publié, pas son succès.

## 👥 Équipe

| Membre | Rôle |
|--------|------|
| [HOUDAED](https://github.com/HOUDAED) | Pipeline ETL : extraction API, nettoyage, chargement SQLite, Docker, pipelines NeoWs / DONKI / Mars Rover |
| [krm3z](https://github.com/krm3z) | Analyse : requêtes SQL, dashboard Power BI, contrôle qualité des données, documentation |

## 🤖 Utilisation de l'IA

Un assistant IA a été utilisé comme mentor plutôt que comme générateur de code : les requêtes SQL ont été écrites à la main puis corrigées avec explication de l'erreur, Power BI a été monté avec un guidage étape par étape, et l'IA a aidé ponctuellement sur la structure du pipeline et la rédaction de la documentation. Chaque chiffre a été vérifié en relançant les requêtes SQL et en le comparant à Power BI.
