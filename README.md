# Analyse de l'APOD de la NASA (1995 - 2026)

Projet réalisé en binôme dans le cadre du Bachelor IA & Data (Ynov) : collecte des données de l'API NASA, stockage en base SQLite, analyse SQL et restitution dans un dashboard Power BI.

## Contexte

Depuis le 16 juin 1995, la NASA publie chaque jour l'**APOD** (Astronomy Picture of the Day) : une image ou une vidéo d'astronomie accompagnée d'une explication. C'est l'un des plus anciens canaux de communication grand public de la NASA.

**Question posée :** comment la NASA communique-t-elle avec le grand public à travers l'APOD depuis 1995 ?

Pour y répondre, nous avons découpé la question en 3 :
1. La publication est-elle régulière dans le temps ?
2. Quelle place prend la vidéo par rapport à l'image ?
3. Les contenus viennent-ils de la NASA ou de photographes extérieurs ?

## Ce qu'il faut retenir

1. **Une régularité totale** : une publication par jour, tous les jours, depuis 1996. Aucun jour manqué en 30 ans.
2. **L'image reste le format roi** : 96 % d'images, seulement 3,5 % de vidéos.
3. **La moitié des contenus vient de l'extérieur** : 49 % des photos sont signées par des photographes non-NASA, et cette part a fortement augmenté avec le temps.

## Le dashboard

![Dashboard APOD](docs/dashboard.png)

Il se lit en 4 blocs, de haut en bas.

### 1. Total des publications : 11 246

C'est le volume total de publications entre le 16/06/1995 et le 04/04/2026. Ce chiffre sert de base à tous les pourcentages du dashboard.

### 2. Publications APOD par année

Toutes les barres sont à la même hauteur : **365 publications par an (366 les années bissextiles)** de 1996 à 2025. Les deux barres plus basses ne sont pas des baisses d'activité : 1995 commence en juin, et 2026 s'arrête au 4 avril, date de notre extraction.

**Ce que ça veut dire :** l'APOD est un rendez-vous quotidien fiable. Le public sait qu'il trouvera un nouveau contenu chaque jour, et c'est la base de la fidélité de l'audience.

### 3. Répartition images / vidéos

- Images : 10 828 (96,3 %)
- Vidéos : 393 (3,5 %)
- Autres : 25 (0,2 %)

**Ce que ça veut dire :** l'APOD reste avant tout un format photo. En regardant par année, la vidéo n'apparaît vraiment qu'en **2011**, atteint un pic à **10 % en 2021**, puis redescend autour de 6 %. Elle reste donc un format secondaire.

### 4. Origine des photos : NASA / Externe

- NASA : 5 713 (50,8 %)
- Externe : 5 533 (49,2 %)

**Ce que ça veut dire :** l'APOD ne montre pas seulement les images de la NASA. Une photo sur deux vient d'astronomes amateurs ou indépendants. Et la tendance est nette quand on regarde par année :

| Période | Part de photos externes |
|---------|------------------------|
| 1995 - 2000 | entre 12 et 24 % |
| 2001 - 2006 | entre 27 et 48 % |
| 2007 - 2026 | entre 51 et 68 %, environ 60 % en moyenne |

L'APOD est passé d'une vitrine des images NASA à une **plateforme qui met en avant la communauté** des astronomes.

## Conclusion et recommandations

La NASA utilise l'APOD comme un **rendez-vous quotidien, très régulier, centré sur l'image et de plus en plus ouvert aux contributeurs extérieurs**.

Si on devait conseiller l'équipe communication :
- **Garder le rythme quotidien** : c'est le point fort du format, il n'a jamais été interrompu.
- **Tester davantage la vidéo** : elle représente moins de 10 % des contenus alors que c'est le format dominant sur les réseaux sociaux aujourd'hui.
- **Continuer à valoriser la communauté** : les photographes externes fournissent plus de la moitié des contenus, c'est un atout (contenu varié, public impliqué).

## Méthode

```
API NASA  →  Python (extraction, nettoyage)  →  SQLite  →  SQL (analyse)  →  Power BI (dashboard)
```

**1. Collecte et stockage** : un pipeline ETL en Python récupère les données de l'API APOD année par année, les nettoie et les charge dans une base SQLite (`data/nasa.db`, table `apod`).

**2. Analyse SQL** : les indicateurs ont d'abord été calculés en SQL (`analysis/queries.sql`).

| Indicateur | Requête |
|------------|---------|
| Total des publications | `select count(*) from apod;` |
| Images / vidéos | `select media_type, count(*) from apod group by media_type;` |
| Photos externes | `select count(*) from apod where copyright != 'nasa';` |
| Publications par année | `select substr(date, 1, 4), count(*) from apod group by substr(date, 1, 4);` |

**3. Dashboard Power BI** : la table a été exportée en CSV puis chargée dans Power BI. Dans Power Query, nous avons ajouté :
- une colonne `Année`, extraite de la date
- une colonne conditionnelle `source photo` : `NASA` si `copyright` vaut `nasa` ou `NASA`, sinon `EXTERNE`

Les chiffres de Power BI ont été comparés à ceux du SQL pour vérifier qu'ils correspondent. Cela nous a permis de repérer une erreur : par défaut, Power BI faisait la **somme** des `id` au lieu de les **compter**, ce qui donnait 63 millions de publications et 5,3 % de vidéos au lieu de 11 246 et 3,5 %.

## Limites

- **Le périmètre** : l'APOD montre comment la NASA communique, pas ce qu'elle fait. Ces données ne permettent pas d'analyser les missions spatiales elles-mêmes.
- **Pas de données d'audience** : on ne sait pas combien de personnes voient chaque publication. On analyse l'offre de contenu, pas son succès.
- **Qualité des données** :
  - la colonne `copyright` contient à la fois `nasa` et `NASA` (5 lignes). C'est corrigé dans Power BI, mais pas encore dans le script de nettoyage. C'est pour ça que le SQL donne 5 538 photos externes et Power BI 5 533.
  - 184 titres contiennent un retour à la ligne suivi de "Credit:", hérité de l'API.

## Prochaines étapes

- Ajouter au dashboard l'évolution par année de la part vidéo et de la part externe
- Corriger le nettoyage de `copyright` et des titres dans le pipeline
- Intégrer les autres sources NASA déjà collectées sur la branche `dev` (NeoWs, DONKI, Mars Rover)
- Analyser les mots les plus fréquents dans les titres (Mars, Hubble, JWST...) pour voir quelles missions ressortent selon les années

## Équipe

| Membre | Rôle |
|--------|------|
| [HOUDAED](https://github.com/HOUDAED) | Pipeline ETL : extraction API, nettoyage, chargement SQLite, Docker, pipelines NeoWs / DONKI / Mars Rover (branche `dev`) |
| [krm3z](https://github.com/krm3z) | Analyse : requêtes SQL, dashboard Power BI, contrôle qualité des données, documentation |

## Utilisation de l'IA

Nous avons utilisé un assistant IA pendant le projet, comme un mentor plutôt que comme un générateur de code :

- **SQL** : les requêtes ont été écrites à la main, l'IA les corrigeait en expliquant l'erreur (virgule oubliée entre deux colonnes, `GROUP BY` manquant, `SELECT *` au lieu de `COUNT(*)`).
- **Power BI** : guidage étape par étape, notamment pour repérer que Power BI additionnait les `id` au lieu de les compter.
- **Pipeline** : aide ponctuelle sur la structure du projet et le pipeline Mars Rover.
- **Analyse et documentation** : aide pour vérifier les tendances par année et rédiger ce README.

Chaque chiffre a été vérifié en relançant les requêtes SQL et en le comparant à Power BI. Chacun peut expliquer la partie qu'il a réalisée.

## Lancer le projet

**Installation**

```bash
git clone https://github.com/krm3z/nasa-data-pipeline.git
cd nasa-data-pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Mettre ensuite une clé API NASA (gratuite sur https://api.nasa.gov) dans `.env`.

**Pipeline**

```bash
python main.py
```

ou avec Docker :

```bash
docker build -t nasa-pipeline .
docker run --env-file .env nasa-pipeline
```

**Analyse SQL**

```bash
sqlite3 data/nasa.db < analysis/queries.sql
```

**Dashboard** : ouvrir `powerbi/apod_dashboard.pbix` avec Power BI Desktop.

## Structure du projet

```
nasa-data-pipeline/
├── analysis/
│   └── queries.sql        requêtes d'analyse
├── config/
│   └── config.py          paramètres (années, chemins)
├── data/                  non versionné
│   ├── raw/               JSON brut de l'API
│   └── processed/         JSON nettoyé
├── docs/
│   └── dashboard.png      capture du dashboard
├── powerbi/
│   └── apod_dashboard.pbix
├── scripts/
│   ├── fetch/             extraction API
│   ├── clean/             nettoyage
│   └── load/              chargement SQLite
├── Dockerfile
├── main.py                lance tout le pipeline
├── requirements.txt
└── .env.example
```

**Stack :** Python, requests, python-dotenv, SQLite, SQL, Power BI, Docker
