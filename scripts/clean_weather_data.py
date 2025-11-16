import pandas as pd
import os

raw_file = "data/raw/weather_data.csv"
staging_file = "data/staging/weather_clean.json"

os.makedirs("data/staging", exist_ok=True)

df = pd.read_csv(raw_file)

# Nettoyage simple
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna()

df.to_json(staging_file, orient="records", lines=True)

print("🧹 Données nettoyées → STAGING")
print(f"→ {staging_file}")