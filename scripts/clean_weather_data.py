import boto3
import pandas as pd
import io
from datetime import datetime

LANDING_BUCKET = "weather-pipeline-landing-vincent"
STAGING_BUCKET = "weather-pipeline-staging-vincent"

s3 = boto3.client("s3")


def get_latest_file(bucket):
    """Return the most recent object in a bucket."""
    resp = s3.list_objects_v2(Bucket=bucket)

    if "Contents" not in resp:
        raise ValueError(f"No files found in {bucket}")

    # Sort by last modified date
    latest = sorted(resp["Contents"], key=lambda x: x["LastModified"], reverse=True)[0]
    return latest["Key"]


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """Apply cleaning rules."""

    # Drop duplicates
    df = df.drop_duplicates()

    # Sort by date
    df = df.sort_values("date")

    # Handle missing values (example)
    df = df.fillna({
        "temperature_c": df["temperature_c"].mean(),
        "humidity": df["humidity"].mean(),
        "wind_kmh": df["wind_kmh"].mean(),
        "precip_mm": 0
    })

    return df


def upload_to_staging(df: pd.DataFrame):
    """Upload cleaned CSV to staging bucket."""

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    timestamp = datetime.now().strftime("%Y-%m-%d/%H-%M-%S")
    s3_key = f"{timestamp}/weather_cleaned.csv"

    s3.put_object(
        Bucket=STAGING_BUCKET,
        Key=s3_key,
        Body=buffer.getvalue()
    )

    print(f"✅ Cleaned file uploaded to s3://{STAGING_BUCKET}/{s3_key}")


if __name__ == "__main__":
    print("🟡 Loading latest raw file from Landing...")

    key = get_latest_file(LANDING_BUCKET)
    print(f"→ Latest file : {key}")

    # Download
    obj = s3.get_object(Bucket=LANDING_BUCKET, Key=key)
    df = pd.read_csv(io.BytesIO(obj["Body"].read()))

    print("🧹 Cleaning data...")
    df_clean = clean_df(df)

    print("📤 Uploading to Staging...")
    upload_to_staging(df_clean)

    print("✅ STAGING STEP FINISHED")
