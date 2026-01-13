"""
Load Kaggle creditcard.csv into a local SQLite database at data/raw/transactions.db
using the schema in sql/schema.sql.
"""
import sqlite3
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "raw" / "creditcard.csv"
DB = ROOT / "data" / "raw" / "transactions.db"
SCHEMA = ROOT / "sql" / "schema.sql"

def main():
    if not CSV.exists():
        raise FileNotFoundError(f"Missing dataset: {CSV}. Please download from Kaggle.")
    with sqlite3.connect(DB) as con:
        con.executescript(SCHEMA.read_text())
        # load in chunks to save memory
        chunks = pd.read_csv(CSV, chunksize=100_000)
        for i, ch in enumerate(chunks, 1):
            ch.to_sql("transactions", con, if_exists="append", index=False)
            print(f"Loaded chunk {i} ({len(ch)} rows)")
    print(f"SQLite DB created at {DB}")

if __name__ == "__main__":
    main()
