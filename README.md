# 🚀 NASA Data Pipeline

> Pipeline ETL qui collecte, transforme et stocke les données ouvertes de la NASA dans une base SQLite.

## 🌌 Problématique
Comment la NASA surveille-t-elle les menaces et phénomènes du système solaire proche de la Terre — objets géocroiseurs et activité solaire — et comment ces données évoluent-elles dans le temps ?

Sous-questions couvertes par le pipeline :
- Comment le nombre et la dangerosité des objets géocroiseurs détectés évoluent-ils par année ? (NeoWs)
- Quelle est la fréquence et la vitesse des éjections de masse coronale, et comment se situent-elles par rapport aux cycles solaires ? (DONKI)
- Quel usage la NASA fait-elle de l'imagerie astronomique quotidienne à des fins de vulgarisation ? (APOD)

### 🛰️ Problématique complémentaire — exploration spatiale

Comment l'exploration robotique de Mars par la NASA a-t-elle évolué au fil des missions (durée, portée, volume de données produites) ?

> Il n'existe pas d'API NASA officielle structurée pour l'historique des vols habités (Apollo, Navette, ISS...) — seule l'exploration robotique (rovers martiens) est documentée par une API officielle (`Mars Rover Photos`). Cette problématique est donc volontairement recentrée sur ce périmètre, et traitée par un **pipeline séparé** (`main_mars.py`, voir plus bas) plutôt que fusionnée avec le pipeline de surveillance ci-dessus.

## 📡 Sources de données

| Source | Description | Statut |
|--------|-------------|--------|
| APOD | Astronomy Picture of the Day | ✅ Disponible |
| NeoWs | Objets proches de la Terre | ✅ Disponible |
| DONKI | Analyses d'éjections de masse coronale (CME) | ✅ Disponible |
| Mars Rover | Manifests de missions des rovers | ⚠️ Code prêt, API NASA actuellement en panne (404 "No such app") |
| Meteorites | Données de météorites | 🚧 En cours |

## ⚙️ Installation

### 1 — Cloner le projet
```bash
git clone ton-repo
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

## 🛰️ Pipeline exploration spatiale (séparé)

Pipeline indépendant du pipeline de surveillance ci-dessus : autre point d'entrée (`main_mars.py`), autres scripts (`scripts/mars/`), même base SQLite (`data/nasa.db`, table `mars_missions`) et même clé API.

```bash
python main_mars.py                         # fetch → clean → load
python -m scripts.mars.analyze_mars          # évolution des missions (durée, sols, photos) par date de lancement
```

⚠️ L'API NASA Mars Rover Photos renvoie actuellement une erreur 404 ("No such app") sur `/manifests` et `/photos`, ce qui indique une panne côté infrastructure NASA (backend indisponible), pas un problème dans ce code. Le pipeline se relancera normalement dès que le service sera rétabli.

## 📊 Analyser les données

Une fois le pipeline exécuté, les scripts du dossier `scripts/analyze/` répondent aux sous-questions de la problématique en agrégeant directement la base SQLite. Ils sont indépendants du pipeline ETL (non appelés par `main.py`) et s'exécutent à la demande :

```bash
python -m scripts.analyze.analyze_neow    # évolution du nombre/dangerosité des géocroiseurs par année
python -m scripts.analyze.analyze_donki   # fréquence et vitesse des CME par année
python -m scripts.analyze.analyze_apod    # usage de l'imagerie APOD par année
```

Chaque script affiche un résumé en console et sauvegarde le détail dans `data/analysis/*.json`.

## 📁 Structure du projet

```
nasa-data-pipeline/
├── config/
│   └── config.py         ← paramètres centralisés
├── data/
│   ├── raw/              ← données brutes API
│   ├── processed/        ← données nettoyées
│   └── analysis/         ← résumés d'analyse
├── scripts/
│   ├── fetch/            ← extraction API (APOD, NeoWs, DONKI)
│   ├── clean/            ← transformation
│   ├── load/              ← chargement SQLite
│   ├── analyze/           ← analyse (répond à la problématique surveillance, séparé de l'ETL)
│   └── mars/              ← pipeline exploration spatiale complet (fetch/clean/load/analyze), séparé du reste
├── main.py               ← lance le pipeline ETL surveillance (fetch → clean → load)
├── main_mars.py          ← lance le pipeline ETL exploration spatiale (fetch → clean → load)
├── .env.example          ← template clé API
├── requirements.txt
└── README.md
```

## 🛠️ Stack technique

- **Python 3** — langage principal
- **SQLite** — base de données locale
- **requests** — appels API
- **python-dotenv** — gestion des secrets
