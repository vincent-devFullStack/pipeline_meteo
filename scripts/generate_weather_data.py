import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_weather_data(n=2000):
    np.random.seed(42)

    cities = ["Paris", "Lyon", "Marseille", "Nice", "Toulouse"]
    start_date = datetime(2024, 1, 1)

    dates = [start_date + timedelta(days=i) for i in range(n)]

    df = pd.DataFrame({
        "date": np.random.choice(dates, n),
        "city": np.random.choice(cities, n),
        "temperature_c": np.random.normal(15, 10, n).round(1),
        "humidity": np.random.uniform(30, 90, n).round(1),
        "wind_kmh": np.random.uniform(0, 80, n).round(1),
        "precip_mm": np.random.exponential(scale=3, size=n).round(1)
    })

    df["is_storm"] = (df["wind_kmh"] > 50) & (df["precip_mm"] > 5)
    df["is_storm"] = df["is_storm"].astype(int)

    return df

if __name__ == "__main__":
    output_path = "data/raw/weather_data.csv"
    os.makedirs("data/raw", exist_ok=True)

    df = generate_weather_data()
    df.to_csv(output_path, index=False)

    print("🌦️ Dataset météo généré !")
    print(f"→ Lignes : {len(df)}")
    print(f"→ Fichier : {output_path}")
    print("\nAperçu :")
    print(df.head())
