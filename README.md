
# 🌦️ Pipeline Météo – Landing → Staging → Refined
Pipeline locale inspirée des zones AWS S3 / Glue / Athena.

## 🧭 Objectif
Mini-pipeline Data structurée :
- Landing (CSV)
- Staging (JSON nettoyé)
- Refined (Parquet)
- Analyse complète en notebook

## 🚀 Installation

### 1) Créer un environnement virtuel
```bash
python -m venv .venv
source .venv/Scripts/activate
```

### 2) Installer les dépendances
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🏗️ Pipeline – Étapes

### 1️⃣ Génération des données météo
```bash
python scripts/generate_weather_data.py
```

### 2️⃣ Nettoyage (Staging)
```bash
python scripts/clean_weather_data.py
```

### 3️⃣ Conversion en Parquet (Refined)
```bash
python scripts/to_parquet.py
```

### 4️⃣ Analyse
```bash
jupyter notebook analysis/meteo_analysis.ipynb
```

## 📂 Structure du projet

```
pipeline_meteo/
├── data/
│   ├── raw/
│   ├── staging/
│   └── refined/
├── analysis/
│   └── meteo_analysis.ipynb
├── scripts/
├── requirements.txt
└── README.md
```

## 📊 Pipeline (Mermaid)

```mermaid
graph LR
    A[CSV - Landing] --> B[JSON - Staging]
    B --> C[Parquet - Refined]
    C --> D[Notebook Analyse]
```

Projet prêt à être étendu vers AWS S3 / Glue / Athena.
