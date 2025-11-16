import pandas as pd
import os

STAGING_FILE = "data/staging/weather_clean.json"
REFINED_FILE = "data/refined/weather.parquet"

os.makedirs("data/refined", exist_ok=True)

# --- Chargement du STAGING ---
print("📥 Chargement du fichier STAGING...")
df = pd.read_json(STAGING_FILE, lines=True)

# --- Vérification des colonnes attendues ---
expected_cols = {
    "date", "city", "temperature_c",
    "humidity", "wind_kmh", "precip_mm", "is_storm"
}

missing = expected_cols - set(df.columns)
if missing:
    raise ValueError(f"❌ Colonnes manquantes dans STAGING : {missing}")

# --- Typage final (important pour DuckDB et la qualité du Parquet) ---
df["date"] = pd.to_datetime(df["date"])
df["city"] = df["city"].astype("category")

numeric_cols = ["temperature_c", "humidity", "wind_kmh", "precip_mm", "is_storm"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# --- Tri temporel ---
df = df.sort_values("date")

# --- Export Parquet optimisé ---
df.to_parquet(
    REFINED_FILE,
    index=False,
    compression="snappy"  
)

print("📦 Données converties → PARQUET (REFINED)")
print(f"→ {REFINED_FILE}")
print("✔ Compression : snappy")
print("✔ Lignes :", len(df))
print(df.head())
