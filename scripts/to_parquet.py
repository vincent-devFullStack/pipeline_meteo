import pandas as pd
import os

staging_file = "data/staging/weather_clean.json"
refined_file = "data/refined/weather.parquet"

os.makedirs("data/refined", exist_ok=True)

df = pd.read_json(staging_file, lines=True)
df.to_parquet(refined_file)

print("📦 Données converties → PARQUET (REFINED)")
print(f"→ {refined_file}")