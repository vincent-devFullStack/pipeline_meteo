import pandas as pd
import os

RAW_FILE = "data/raw/weather_data.csv"
STAGING_FILE = "data/staging/weather_clean.json"

os.makedirs("data/staging", exist_ok=True)

df = pd.read_csv(RAW_FILE)

# --- Typage des colonnes ---
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["city"] = df["city"].astype("category")

numeric_cols = ["temperature_c", "humidity", "wind_kmh", "precip_mm", "is_storm"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ---  Suppression des lignes non valides ---
df = df.dropna(subset=["date"])

# ---  Nettoyage des valeurs aberrantes ---
df = df[(df["humidity"] >= 0) & (df["humidity"] <= 100)]
df = df[(df["temperature_c"] >= -50) & (df["temperature_c"] <= 60)]
df = df[(df["wind_kmh"] >= 0)]
df = df[(df["precip_mm"] >= 0)]

# ---  Tri temporel (bonnes pratiques data engineering) ---
df = df.sort_values("date")

# ---  Export vers STAGING ---
df.to_json(STAGING_FILE, orient="records", lines=True)

print("🧹 Données nettoyées → STAGING OK")
print(f"→ {STAGING_FILE}")
print(f"✔ Lignes après nettoyage : {len(df)}")
print(df.head())
