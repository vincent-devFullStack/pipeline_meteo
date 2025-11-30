import pandas as pd
import boto3
import io
from datetime import datetime

STAGING_BUCKET = "weather-pipeline-staging-vincent"
REFINED_BUCKET = "weather-pipeline-refined-vincent"

s3 = boto3.client("s3")


def get_latest_staging_file():
    """Retourne la clé du dernier fichier staging."""
    resp = s3.list_objects_v2(Bucket=STAGING_BUCKET)

    if "Contents" not in resp:
        raise FileNotFoundError("❌ Aucun fichier trouvé dans le bucket STAGING")

    latest = max(resp["Contents"], key=lambda x: x["LastModified"])
    return latest["Key"]


def load_staging_df(s3_key: str) -> pd.DataFrame:
    """Charge le fichier STAGING depuis S3 en DataFrame."""
    obj = s3.get_object(Bucket=STAGING_BUCKET, Key=s3_key)
    return pd.read_csv(io.BytesIO(obj["Body"].read()))


def upload_refined(df: pd.DataFrame):
    """Upload du fichier Parquet dans le bucket REFINED."""
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False, compression="snappy")
    buffer.seek(0)

    timestamp = datetime.now().strftime("%Y-%m-%d/%H-%M-%S")
    key = f"{timestamp}/weather_refined.parquet"

    s3.put_object(
        Bucket=REFINED_BUCKET,
        Key=key,
        Body=buffer.getvalue()
    )

    print(f"✅ Parquet uploaded → s3://{REFINED_BUCKET}/{key}")


if __name__ == "__main__":
    print("📥 Récupération du dernier fichier STAGING...")
    latest_key = get_latest_staging_file()
    print(f"→ {latest_key}")

    df = load_staging_df(latest_key)

    print("🔍 Vérification des colonnes...")
    expected_cols = {
        "date", "city", "temperature_c",
        "humidity", "wind_kmh", "precip_mm", "is_storm"
    }

    missing = expected_cols - set(df.columns)
    if missing:
        raise ValueError(f"❌ Colonnes manquantes : {missing}")

    print("🛠 Typage des colonnes...")
    df["date"] = pd.to_datetime(df["date"])
    df["city"] = df["city"].astype("category")

    for c in ["temperature_c", "humidity", "wind_kmh", "precip_mm", "is_storm"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    print("📊 Tri temporel...")
    df = df.sort_values("date")

    print("📤 Upload vers REFINED...")
    upload_refined(df)

    print("🎉 Conversion PARQUET terminée !")
