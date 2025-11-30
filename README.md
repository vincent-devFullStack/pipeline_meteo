# 🌦️ Pipeline Météo — API → Landing → Staging → Refined → Warehouse

Pipeline locale inspirée d’une architecture Data AWS (S3 / Glue / Athena),  
avec ingestion **réelle** des données météo via API Open‑Meteo.

## 🧭 Objectif

Construire une mini‑pipeline Data complète :

- **Ingestion API** → CSV dans **S3 Landing**
- **Staging** → nettoyage → JSON Lines dans **S3 Staging**
- **Refined** → conversion Parquet + compression Snappy dans **S3 Refined**
- **Warehouse** → chargement dans **DuckDB** en local
- **Notebook** → analyse exploratoire & visualisation

Cette structure reproduit les concepts d’un **Data Lakehouse** moderne.

---

## 🚀 Installation

### 1) Créer un environnement virtuel

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows
```

### 2) Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Configuration AWS

Le pipeline utilise automatiquement les credentials AWS configurés via :

```bash
aws configure
```

Les buckets S3 utilisés sont :

- `weather-pipeline-landing-vincent`
- `weather-pipeline-staging-vincent`
- `weather-pipeline-refined-vincent`

---

## 🏗️ Pipeline — Étapes

### 1️⃣ Ingestion météo via API → **S3 Landing**

```bash
python scripts/ingest_weather_api.py
```

### 2️⃣ Nettoyage → **S3 Staging**

```bash
python scripts/clean_weather_data.py
```

### 3️⃣ Conversion Parquet → **S3 Refined**

```bash
python scripts/to_parquet.py
```

### 4️⃣ Chargement dans DuckDB (Warehouse local)

```bash
python scripts/load_to_db.py
```

### 5️⃣ Analyse Notebook

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
├── warehouse/
│   └── weather.duckdb        # Entrepôt analytique local
│
├── analysis/
│   └── meteo_analysis.ipynb
│
├── scripts/
│   ├── ingest_weather_api.py   # API → Landing (S3)
│   ├── clean_weather_data.py   # Landing → Staging (S3)
│   ├── to_parquet.py           # Staging → Refined (S3)
│   ├── load_to_db.py           # Refined (S3) → DuckDB
│   └── run_pipeline.py         # Orchestration complète
│
├── requirements.txt
└── README.md
```

Les dossiers `data/raw`, `data/staging` et `data/refined` existent uniquement pour compatibilité,  
mais **les fichiers sont désormais stockés dans S3**, pas en local.

---

## 📊 Schéma du pipeline (Mermaid)

```mermaid
graph LR
    A[API Open‑Meteo] --> B[S3 Landing (CSV)]
    B --> C[S3 Staging (JSON Lines)]
    C --> D[S3 Refined (Parquet Snappy)]
    D --> E[DuckDB (Warehouse local)]
    E --> F[Jupyter Notebook Analyse]
```

---

## 🛠️ Technologies utilisées

| Zone        | Technologie |
|-------------|-------------|
| Ingestion   | API Open‑Meteo |
| Landing     | S3 (CSV) |
| Staging     | S3 (JSON Lines) |
| Refined     | S3 (Parquet Snappy) |
| Warehouse   | DuckDB |
| Analyse     | Pandas, Matplotlib, Seaborn |
| Orchestration | Python |

---

## 📌 Notes

- Pipeline entièrement reproductible.
- Prévu pour migrer facilement vers **AWS Glue**, **AWS Athena**, **Step Functions**.
- DuckDB est utilisé ici comme moteur analytique local (équivalent Athena S3).
