import duckdb
import boto3
import pandas as pd
import configparser
import os

# ---------------------------------------------------------
#  CONFIGURATION S3
# ---------------------------------------------------------
REFINED_BUCKET = "weather-pipeline-refined-vincent"
TABLE_NAME = "weather"
DB_PATH = "warehouse/weather.duckdb"
REGION = "eu-north-1"

EXPECTED_COLS = {
    "date", "city", "temperature_c",
    "humidity", "wind_kmh", "precip_mm", "is_storm"
}

# ---------------------------------------------------------
#  LECTURE DES CREDENTIALS AWS
# ---------------------------------------------------------
def load_aws_credentials():
    creds_path = os.path.expanduser("~/.aws/credentials")

    config = configparser.RawConfigParser()
    config.read(creds_path)

    profile = "default"

    return (
        config[profile]["aws_access_key_id"],
        config[profile]["aws_secret_access_key"]
    )

ACCESS_KEY, SECRET_KEY = load_aws_credentials()


# ---------------------------------------------------------
#  TROUVER LE DERNIER FICHIER PARQUET SUR S3
# ---------------------------------------------------------
def get_latest_refined_file():
    s3 = boto3.client("s3")

    objects = s3.list_objects_v2(
        Bucket=REFINED_BUCKET,
    )

    if "Contents" not in objects:
        raise FileNotFoundError("❌ Aucun fichier trouvé dans le bucket REFINED.")

    parquet_files = [
        obj for obj in objects["Contents"]
        if obj["Key"].endswith(".parquet")
    ]

    if not parquet_files:
        raise FileNotFoundError("❌ Aucun fichier .parquet trouvé dans REFINED.")

    latest = max(parquet_files, key=lambda x: x["LastModified"])
    return latest["Key"]


# ---------------------------------------------------------
#  LOAD S3 PARQUET → DUCKDB
# ---------------------------------------------------------
def load_s3_parquet_to_duckdb():

    print("\n📦 Loading refined data from S3 into DuckDB warehouse...")

    latest_key = get_latest_refined_file()
    print(f"→ Latest refined file: {latest_key}")

    parquet_path = f"s3://{REFINED_BUCKET}/{latest_key}"

    con = duckdb.connect(DB_PATH)
    con.execute("INSTALL httpfs;")
    con.execute("LOAD httpfs;")

    con.execute(f"SET s3_region='{REGION}';")
    con.execute(f"SET s3_access_key_id='{ACCESS_KEY}';")
    con.execute(f"SET s3_secret_access_key='{SECRET_KEY}';")

    con.execute("SET s3_endpoint='s3.eu-north-1.amazonaws.com';")
    con.execute("SET s3_use_ssl=1;")
    con.execute("SET s3_url_style='path';")

    print("\n🔍 Vérification du schéma...")
    df = con.execute(f"SELECT * FROM read_parquet('{parquet_path}') LIMIT 5").df()

    missing = EXPECTED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"❌ Colonnes manquantes : {missing}")

    print("✔ Schéma OK")

    print("\n📥 Ingestion dans DuckDB...")
    con.execute(f"""
        CREATE OR REPLACE TABLE {TABLE_NAME} AS
        SELECT * FROM read_parquet('{parquet_path}')
    """)

    con.execute(f"CREATE INDEX IF NOT EXISTS idx_weather_date ON {TABLE_NAME}(date);")

    preview = con.execute(f"SELECT * FROM {TABLE_NAME} LIMIT 5").df()
    print("\n📊 Preview:")
    print(preview)

    con.close()
    print("\n🎉 DuckDB warehouse load complete!\n")


if __name__ == "__main__":
    load_s3_parquet_to_duckdb()
