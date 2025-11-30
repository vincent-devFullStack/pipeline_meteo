import subprocess
import time
from datetime import datetime
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
    print(f"[{datetime.now()}] ▶ Running: {script}\n")

    path_script = SCRIPTS_DIR / script
    if not path_script.exists():
        print(f"❌ Script introuvable : {path_script}")
        raise SystemExit(1)

    start = time.time()

    process = subprocess.Popen(
    [PYTHON, "-X", "utf8", str(path_script)],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    encoding="utf-8",
    errors="replace"
    )


    # 🔥 Logs live
    for line in process.stdout:
        print(line, end="")

    process.wait()
    duration = time.time() - start

    if process.returncode != 0:
        print("❌ ERREUR lors de l'exécution")
        raise SystemExit(1)

    print(f"\n⏱️  Temps écoulé : {duration:.2f}s")
    print(f"{'='*60}\n")


def main():
    print("\n🚀 Lancement de la pipeline Météo")
    print("============================================")

    for label, script in STEPS:
        run_step(label, script)

    print("\n🎉 Pipeline terminée avec succès !")


if __name__ == "__main__":
    main()
