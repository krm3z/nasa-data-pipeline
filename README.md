Voilà le README complet mis à jour :

```markdown
# 🚀 NASA Data Pipeline

> Pipeline ETL qui collecte, transforme et stocke les données ouvertes de la NASA dans une base SQLite.

## 🌌 Problématique

Comment les données ouvertes de la NASA permettent-elles de retracer l'évolution de l'exploration spatiale moderne ?

## 📡 Sources de données

| Source | Description | Statut |
|--------|-------------|--------|
| APOD | Astronomy Picture of the Day | ✅ Disponible |
| NeoWs | Objets proches de la Terre | 🚧 En cours |
| Mars Rover | Photos des rovers | 🚧 En cours |
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

## 📁 Structure du projet

```
nasa-data-pipeline/
├── config/
│   └── config.py         ← paramètres centralisés
├── data/
│   ├── raw/              ← données brutes API
│   └── processed/        ← données nettoyées
├── scripts/
│   ├── fetch/            ← extraction API
│   ├── clean/            ← transformation
│   └── load/             ← chargement SQLite
├── main.py               ← lance tout le pipeline
├── .env.example          ← template clé API
├── requirements.txt
└── README.md
```

## 🛠️ Stack technique

- **Python 3** — langage principal
- **SQLite** — base de données locale
- **requests** — appels API
- **python-dotenv** — gestion des secrets
```
