import requests
import pandas as pd
import io
from datetime import datetime
import boto3

API_URL = "https://api.open-meteo.com/v1/forecast"

# Villes : latitude / longitude
CITIES = {
    "Paris": (48.8566, 2.3522),
    "Lyon": (45.7640, 4.8357),
    "Marseille": (43.2965, 5.3698),
    "Nice": (43.7102, 7.2620),
    "Toulouse": (43.6045, 1.4442),
}

# Bucket S3 (zone landing)
LANDING_BUCKET = "weather-pipeline-landing-vincent"

# Client S3
s3 = boto3.client("s3")


def fetch_weather(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relativehumidity_2m,precipitation,wind_speed_10m",
        "timezone": "Europe/Paris"
    }

    res = requests.get(API_URL, params=params, timeout=15)
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

    # Détection basique de tempête
    df["is_storm"] = ((df["wind_kmh"] > 50) & (df["precip_mm"] > 5)).astype(int)

    return df


def upload_to_s3(df: pd.DataFrame):
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    timestamp = datetime.now().strftime("%Y-%m-%d/%H-%M-%S")
    s3_key = f"{timestamp}/weather_data.csv"

    s3.put_object(
        Bucket=LANDING_BUCKET,
        Key=s3_key,
        Body=buffer.getvalue()
    )

    print(f"✅ Uploaded to s3://{LANDING_BUCKET}/{s3_key}")


if __name__ == "__main__":
    all_dfs = []

    print("🌍 Fetching REAL weather data for multiple cities...\n")

    for city, (lat, lon) in CITIES.items():
        try:
            print(f"→ {city}")
            raw = fetch_weather(lat, lon)
            df_city = normalize_response(raw, city)
            all_dfs.append(df_city)

        except Exception as e:
            print(f"❌ Error for {city}: {e}")

    if not all_dfs:
        raise ValueError("❌ Aucun jeu de données n'a été récupéré. Arrêt du script.")

    final_df = pd.concat(all_dfs, ignore_index=True)

    print("\n✅ Données récupérées avec succès")
    print(final_df.head())

    upload_to_s3(final_df)
