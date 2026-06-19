# 🚀 Pipeline Big Data Crypto

## 📌 Contexte du projet

Le marché des cryptomonnaies génère quotidiennement d'importants volumes de données : prix, volumes d'échange, market capitalization, variations de performance, etc.

L'objectif de ce projet est de concevoir et implémenter une plateforme Data complète permettant :

- La collecte automatisée des données depuis l'API CoinGecko
- Leur stockage dans une architecture Medallion
- La modélisation dimensionnelle d'un Data Warehouse
- Le chargement dans Snowflake
- L'orchestration du pipeline avec Apache Airflow
- La visualisation et l'analyse avec Tableau

Le projet reproduit un cas réel de Data Engineering & Data Analytics.

---

# 🏗️ Architecture du projet

## Architecture End-to-End

```text
CoinGecko API
      │
      ▼
Bronze Layer (JSON)
      │
      ▼
Silver Layer (Parquet)
      │
      ▼
Gold Layer (Dimension Model)
      │
      ▼
Snowflake Data Warehouse
      │
      ▼
Tableau Dashboard
```

---

## Technologies utilisées

| Couche | Technologie |
|----------|------------|
| Source | CoinGecko API |
| Data Lake | MinIO |
| Bronze | JSON |
| Silver | Pandas + Parquet |
| Gold | Modèle Dimensionnel |
| Data Warehouse | Snowflake |
| Orchestration | Apache Airflow |
| Visualisation | Tableau Desktop / Tableau Public |
| Langage | Python |
| Conteneurisation | Docker |

---

# 🥉 Bronze Layer

## Objectif

Conserver les données brutes provenant de CoinGecko sans modification.

## Format

JSON

## Structure

```text
bronze/
└── YYYY/
    └── MM/
        └── raw.json
```

## Fonctionnalités

- Connexion API CoinGecko
- Gestion erreurs HTTP
- Gestion timeout
- Sauvegarde brute des données

---

# 🥈 Silver Layer

## Objectif

Nettoyer et standardiser les données.

## Transformations

- Suppression des colonnes inutiles
- Gestion des valeurs nulles
- Normalisation des noms de colonnes
- Conversion des types
- Ajout de colonnes temporelles

## Format

Parquet

## Exemple

```text
silver/
└── crypto_market.parquet
```

---

# 🥇 Gold Layer

## Objectif

Construire le modèle dimensionnel destiné à l'analyse.

---

# 📊 Modèle Dimensionnel

## Schéma choisi

### Star Schema

Le modèle en étoile a été choisi pour :

- simplicité
- performance analytique
- facilité d'utilisation dans Tableau
- maintenance simplifiée

---

## Table de faits

### FACT_CRYPTO_MARKET

Mesures :

- current_price
- high_24h
- low_24h
- total_volume
- market_cap
- price_change_24h
- price_change_percentage_24h

Clés étrangères :

- crypto_id
- date_id
- time_id

Granularité :

> Une ligne = Une cryptomonnaie à une date et heure de collecte donnée.

---

## Dimensions

### DIM_CRYPTO

| Colonne | Description |
|----------|------------|
| Crypto Id | Clé primaire |
| Coin Id | Identifiant CoinGecko |
| Name | Nom |
| Symbol | Symbole |
| Market Cap Rank | Classement |

---

### DIM_DATE

| Colonne | Description |
|----------|------------|
| Date Id | PK |
| Date | Date |
| Year | Année |
| Month | Mois |
| Week | Semaine |
| Day | Jour |

---

### DIM_TIME

| Colonne | Description |
|----------|------------|
| Time Id | PK |
| Hour | Heure |
| Minute | Minute |
| Second | Seconde |

---

# ❄️ Snowflake

## Schéma

```sql
CRYPTO_DB
│
└── CRYPTO_SCHEMA
    │
    ├── DIM_CRYPTO
    ├── DIM_DATE
    ├── DIM_TIME
    └── FACT_CRYPTO_MARKET
```

---

## Chargement

Les tables Gold sont chargées dans Snowflake via :

```python
snowflake-connector-python
```

Étapes :

1. Création du schéma
2. Création des tables
3. Chargement des dimensions
4. Chargement des faits
5. Validation

---

# 🔄 Orchestration Airflow

## DAG

```text
cryptopipelinedag
```

## Workflow

```text
ingest_bronze
      >>
transform_silver
      >>
build_gold_model
      >>
load_snowflake
```

## Fonctionnalités

- Scheduling quotidien
- Retries automatiques
- Logs Airflow
- Monitoring du pipeline

---

# 📂 Structure du projet

```text
PIPELINE-BIG-DATA-CRYPTO
│
├── dags/
│   └── cryptopipelinedag.py
│
├── dashboards/
│
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── docs/
│   ├── architecture.png
│   └── ERD.png
│
├── src/
│   ├── ingestion/
│   │   └── ingestion_crypto.py
│   │
│   ├── transformation/
│   │   └── silver_layer.py
│   │
│   ├── modelisation/
│   │   └── gold_layer.py
│   │
│   └── snowflake/
│       ├── schema.sql
│       └── load_snowflake.py
│
├── .env
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## 1. Cloner le projet

```bash
git clone https://github.com/votre-compte/pipeline-big-data-crypto.git
```

```bash
cd pipeline-big-data-crypto
```

---

## 2. Créer un environnement virtuel

```bash
python -m venv venv
```

Activation :

Windows

```bash
venv\Scripts\activate
```

Linux

```bash
source venv/bin/activate
```

---

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

# 🔐 Variables d'environnement

Créer un fichier `.env`

```env
COINGECKO_API_URL=https://api.coingecko.com/api/v3

MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio123

SNOWFLAKE_ACCOUNT=xxxx
SNOWFLAKE_USER=xxxx
SNOWFLAKE_PASSWORD=xxxx
SNOWFLAKE_DATABASE=CRYPTO_DB
SNOWFLAKE_SCHEMA=CRYPTO_SCHEMA
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
```

---

# ▶️ Exécution

## Ingestion

```bash
python src/ingestion/ingestion_crypto.py
```

## Silver

```bash
python src/transformation/silver_layer.py
```

## Gold

```bash
python src/modelisation/gold_layer.py
```

## Snowflake

```bash
python src/snowflake/load_snowflake.py
```

---

# 📈 Dashboard Tableau

## Visualisations réalisées

### Evolution du prix

Graphique en ligne montrant l'évolution du prix des cryptomonnaies.

### Top 10 Volumes

Classement des cryptomonnaies par volume moyen.

### Heatmap

Variation journalière des prix.

### KPI Cards

- Prix actuel
- Variation 24h
- Volume total
- Market Cap

### Scatter Plot

Corrélation :

```text
Volume ↔ Variation de Prix
```

### Vue Détail

Analyse complète d'une cryptomonnaie.

---

# 🎯 Dashboards

## Dashboard Comparatif

Permet :

- comparaison multi-cryptos
- filtres dynamiques
- analyse globale

## Dashboard Détail

Permet :

- historique complet
- indicateurs détaillés
- navigation depuis le dashboard principal

---

# 📸 Livrables

## Conception

- Architecture End-to-End
- Diagramme ERD
- Justification du modèle

## Implémentation

- DAG Airflow
- Bronze / Silver / Gold
- Snowflake
- Docker Compose

## Tableau

- Dashboard principal
- Dashboard détail
- KPI
- Tableau Public

---

# 📚 Résultats

Ce projet met en œuvre une chaîne Data complète :

✅ Ingestion API

✅ Data Lake Medallion

✅ Modélisation Dimensionnelle

✅ Snowflake Data Warehouse

✅ Apache Airflow

✅ Tableau Dashboard

✅ Analyse décisionnelle des cryptomonnaies

---

## 👩‍💻 Auteur

**Manal Beshar**

Projet Big Data & Business Intelligence – Analyse des Cryptomonnaies