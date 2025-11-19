import requests
import pandas as pd
import os

API_URL = "https://api.open-meteo.com/v1/forecast"

# Liste de villes → latitude / longitude
CITIES = {
    "Paris":      (48.8566, 2.3522),
    "Lyon":       (45.7640, 4.8357),
    "Marseille":  (43.2965, 5.3698),
    "Nice":       (43.7102, 7.2620),
    "Toulouse":   (43.6045, 1.4442),
}

OUTPUT_PATH = "data/raw/weather_data.csv"
os.makedirs("data/raw", exist_ok=True)

def fetch_weather(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relativehumidity_2m,precipitation,wind_speed_10m",
        "timezone": "Europe/Paris"
    }
    res = requests.get(API_URL, params=params)
    res.raise_for_status()
    return res.json()


def normalize_response(data, city):
    hourly = data["hourly"]

    df = pd.DataFrame({
        "date": pd.to_datetime(hourly["time"]),
        "city": city,
        "temperature_c": hourly["temperature_2m"],
        "humidity": hourly["relativehumidity_2m"],
        "wind_kmh": hourly["wind_speed_10m"],
        "precip_mm": hourly["precipitation"],
    })

    df["is_storm"] = ((df["wind_kmh"] > 50) & (df["precip_mm"] > 5)).astype(int)
    return df


if __name__ == "__main__":
    all_dfs = []

    print("🌍 Fetching real weather data for multiple cities...\n")

    for city, (lat, lon) in CITIES.items():
        print(f"→ {city}")
        raw = fetch_weather(lat, lon)
        df_city = normalize_response(raw, city)
        all_dfs.append(df_city)

    df = pd.concat(all_dfs, ignore_index=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"\n✅ Weather dataset saved to {OUTPUT_PATH}")
    print(df.head())
