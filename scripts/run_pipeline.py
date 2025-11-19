import subprocess
import time
from pathlib import Path
import sys

SCRIPTS_DIR = Path("scripts")
PYTHON = sys.executable 

STEPS = [
    ("🔵 Ingestion des données via API (RAW)", "ingest_weather_api.py"),
    ("🟡 Nettoyage des données (STAGING)", "clean_weather_data.py"),
    ("🟣 Conversion en Parquet (REFINED)", "to_parquet.py"),
    ("🟢 Chargement dans DuckDB (WAREHOUSE)", "load_to_db.py"),
]

def run_step(label, script):
    print(f"\n{'='*60}")
    print(f"{label}")
    print(f"{'-'*60}")

    path_script = SCRIPTS_DIR / script
    if not path_script.exists():
        print(f"❌ Script introuvable : {path_script}")
        raise SystemExit(1)
    

    start = time.time()

    result = subprocess.run(
        [PYTHON, "-X", "utf8", str(SCRIPTS_DIR / script)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace"
    )

    duration = time.time() - start

    if result.returncode != 0:
        print("❌ ERREUR lors de l'exécution")
        print(result.stderr)
        raise SystemExit(1)
    

    print(result.stdout)
    print(f"⏱️  Temps écoulé : {duration:.2f}s")
    print(f"{'='*60}\n")
    
    

def main():
    print("\n🚀 Lancement de la pipeline Météo")
    print("============================================")

    for label, script in STEPS:
        run_step(label, script)

    print("\n🎉 Pipeline terminée avec succès !")


if __name__ == "__main__":
    main()
