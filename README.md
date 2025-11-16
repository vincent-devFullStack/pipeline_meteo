# 🌦️ Pipeline Météo -- Landing → Staging → Refined → Warehouse

Pipeline locale inspirée d'une architecture Data AWS (S3 / Glue /
Athena).

## 🧭 Objectif

Construire une mini-pipeline Data complète avec :

-   **Landing** → données brutes (CSV)
-   **Staging** → données nettoyées (JSON Lines)
-   **Refined** → format optimisé (Parquet + Snappy)
-   **Warehouse** → base analytique locale (DuckDB)
-   **Notebook** → analyse exploratoire et visualisation

> Cette structure imite un vrai **Data Lakehouse**.

------------------------------------------------------------------------

## 🚀 Installation

### 1) Créer un environnement virtuel

``` bash
python -m venv .venv
source .venv/Scripts/activate
```

### 2) Installer les dépendances

``` bash
pip install --upgrade pip
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 🏗️ Pipeline -- Étapes

### 1️⃣ Génération des données météo (Landing - CSV)

``` bash
python scripts/generate_weather_data.py
```

### 2️⃣ Nettoyage des données (Staging - JSON)

``` bash
python scripts/clean_weather_data.py
```

### 3️⃣ Conversion en Parquet (Refined)

``` bash
python scripts/to_parquet.py
```

### 4️⃣ Chargement dans DuckDB (Warehouse)

``` bash
python scripts/load_to_db.py
```

### 5️⃣ Analyse dans le Notebook

``` bash
jupyter notebook analysis/meteo_analysis.ipynb
```

------------------------------------------------------------------------

## ⚡ Pipeline complète automatique (1 seule commande)

``` bash
python scripts/run_pipeline.py
```

------------------------------------------------------------------------

## 📂 Structure du projet

    pipeline_meteo/
    ├── data/
    │   ├── raw/        # Landing
    │   ├── staging/    # Nettoyage
    │   └── refined/    # Parquet optimisé
    │
    ├── warehouse/
    │   └── weather.duckdb   # Entrepôt analytique
    │
    ├── analysis/
    │   └── meteo_analysis.ipynb
    │
    ├── scripts/
    │   ├── generate_weather_data.py
    │   ├── clean_weather_data.py
    │   ├── to_parquet.py
    │   ├── load_to_db.py
    │   └── run_pipeline.py      # Orchestration du pipeline complet
    │
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

## 📊 Pipeline (Diagramme Mermaid)

``` mermaid
graph LR
    A[CSV - Landing] --> B[JSON - Staging]
    B --> C[Parquet - Refined]
    C --> D[DuckDB - Warehouse]
    D --> E[Jupyter Notebook - Analyse]
```

------------------------------------------------------------------------

## 🛠️ Technologies utilisées

  Zone        Technologie
  ----------- -----------------------------
  Landing     CSV
  Staging     JSON Lines
  Refined     Parquet (Snappy)
  Warehouse   DuckDB
  Analyse     Pandas, Matplotlib, Seaborn
  Scripts     Python

------------------------------------------------------------------------

## 📌 Notes

-   Le pipeline est totalement reproductible.
-   Peut être étendu vers **AWS (S3, Glue, Athena)**.
-   DuckDB imite un moteur SQL analytique type **Athena**.
