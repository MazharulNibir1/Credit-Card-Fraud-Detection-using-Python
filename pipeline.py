"""
Orchestrate: CSV -> SQLite -> SQL outputs -> Python analysis -> Fraud model
"""
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable

steps = [
    ["python", "src/data/load_db.py"],
    ["python", "src/analysis/sql_analysis.py"],
    ["python", "src/analysis/python_analysis.py"],
    ["python", "src/models/fraud_model.py"],
]

def run(cmd):
    if cmd[0] == "python":
        cmd[0] = PY
    print(f"\n=== Running: {' '.join(cmd)} ===")
    subprocess.run(cmd, cwd=ROOT, check=True)

def main():
    for s in steps:
        run(s)

if __name__ == "__main__":
    main()
