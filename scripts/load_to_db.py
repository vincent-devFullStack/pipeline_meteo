import duckdb
import pandas as pd
from pathlib import Path

# -------------------------------------
# CONFIGURATION
# -------------------------------------
PARQUET_FILE = Path("data/refined/weather.parquet")
DB_PATH = Path("warehouse/weather.duckdb")
TABLE_NAME = "weather"

# Colonnes attendues pour validation
EXPECTED_COLS = {
    "date", "city", "temperature_c",
    "humidity", "wind_kmh", "precip_mm", "is_storm"
}

# -------------------------------------
# MAIN
# -------------------------------------
def load_parquet_to_duckdb():
    print("\n📦 Loading data into DuckDB warehouse...")
    print(f"📁 Parquet file: {PARQUET_FILE}")

    if not PARQUET_FILE.exists():
        raise FileNotFoundError(f"❌ Parquet file not found: {PARQUET_FILE}")

    # Connect to DB (auto-creates file)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH))

    print("🔗 Connected to DuckDB.")

    # --- Validation du schéma ---
    df = pd.read_parquet(PARQUET_FILE)
    missing_cols = EXPECTED_COLS - set(df.columns)

    if missing_cols:
        raise ValueError(f"❌ Missing columns in Parquet: {missing_cols}")

    print("✔ Schema validation OK")

    # --- Ingestion dans DuckDB ---
    con.execute(f"""
        CREATE OR REPLACE TABLE {TABLE_NAME} AS
        SELECT 
            date,
            city,
            temperature_c,
            humidity,
            wind_kmh,
            precip_mm,
            is_storm
        FROM read_parquet('{PARQUET_FILE}')
    """)

    print(f"✅ Table '{TABLE_NAME}' successfully loaded.")

    # --- Optimisation ---
    con.execute(f"CREATE INDEX IF NOT EXISTS idx_weather_date ON {TABLE_NAME}(date)")
    print("✔ Index created (date)")

    # --- Aperçu ---
    preview = con.execute(f"SELECT * FROM {TABLE_NAME} LIMIT 5").df()
    print("\n📊 Preview:")
    print(preview)

    con.close()
    print("\n🎉 DuckDB load complete.\n")


if __name__ == "__main__":
    load_parquet_to_duckdb()
