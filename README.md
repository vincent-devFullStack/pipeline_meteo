# 🌦️ Pipeline Météo — API → Landing → Staging → Refined → Warehouse

Pipeline locale inspirée d’une architecture Data AWS (S3 / Glue / Athena),
avec ingestion **réelle** des données météo via API.

## 🧭 Objectif

Construire une mini-pipeline Data complète avec :

- **Ingestion API** → données brutes (CSV en Landing)
- **Staging** → nettoyage + normalisation (JSON Lines)
- **Refined** → format optimisé (Parquet + Snappy)
- **Warehouse** → entrepôt analytique local (DuckDB)
- **Notebook** → analyse exploratoire et visualisation

> L’objectif est pédagogique : reproduire les concepts d’un **Data Lakehouse**
> mais en local, avant de migrer vers AWS (S3 → Glue → Athena).

---

## 🚀 Installation

### 1) Environnement virtuel

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### 2) Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🏗️ Pipeline — Étapes

### 1️⃣ Ingestion météo via API (Landing - CSV)

```bash
python scripts/ingest_weather_api.py
```

### 2️⃣ Nettoyage des données (Staging - JSON)

```bash
python scripts/clean_weather_data.py
```

### 3️⃣ Conversion en Parquet (Refined)

```bash
python scripts/to_parquet.py
```

### 4️⃣ Chargement dans DuckDB (Warehouse)

```bash
python scripts/load_to_db.py
```

### 5️⃣ Analyse dans le Notebook

```bash
jupyter notebook analysis/meteo_analysis.ipynb
```

---

## ⚡ Pipeline complète en une seule commande

```bash
python scripts/run_pipeline.py
```

---

## 📂 Structure du projet

```
pipeline_meteo/
├── data/
│   ├── raw/           # Landing (CSV depuis l'API)
│   ├── staging/       # Données nettoyées (JSON Lines)
│   └── refined/       # Parquet optimisé
│
├── warehouse/
│   └── weather.duckdb   # Entrepôt analytique
│
├── analysis/
│   └── meteo_analysis.ipynb
│
├── scripts/
│   ├── ingest_weather_api.py
│   ├── clean_weather_data.py
│   ├── to_parquet.py
│   ├── load_to_db.py
│   └── run_pipeline.py
│
├── requirements.txt
└── README.md
```

---

## 📊 Pipeline (Diagramme Mermaid)

```mermaid
graph LR
    A[API Weather → CSV (Landing)]
        --> B[JSON Lines (Staging)]
    B --> C[Parquet Snappy (Refined)]
    C --> D[DuckDB (Warehouse)]
    D --> E[Jupyter Notebook (Analyse)]
```

---

## 🛠️ Technologies utilisées

| Zone        | Technologie                        |
|-------------|------------------------------------|
| Landing     | API Open-Meteo → CSV               |
| Staging     | JSON Lines                         |
| Refined     | Parquet (Snappy)                   |
| Warehouse   | DuckDB                             |
| Analyse     | Pandas, Matplotlib, Seaborn        |
| Scripts     | Python                             |

---

## 📌 Notes

- Pipeline totalement reproductible et exécutable en local.
- Conçu pour être migré vers **AWS (S3, Glue, Athena)**.
- DuckDB simule un moteur analytique type **Athena**.
