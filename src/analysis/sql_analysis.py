"""
Run the SQL analyses from sql/queries.sql and export CSVs with results.
"""
import sqlite3
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "data" / "raw" / "transactions.db"
OUT_DIR = ROOT / "reports"

def _query_to_csv(con, sql, out_path):
    df = pd.read_sql_query(sql, con)
    df.to_csv(out_path, index=False)
    print(f"Wrote {out_path} ({len(df)} rows)")
    return df

def main():
    with sqlite3.connect(DB) as con:
        # Hourly stats
        hourly_sql = """
        WITH base AS (
          SELECT CAST((Time/3600) AS INT) % 24 AS hour_of_day, Amount, Class
          FROM transactions
        )
        SELECT hour_of_day, COUNT(*) AS txn_count,
               SUM(CASE WHEN Class=1 THEN 1 ELSE 0 END) AS fraud_count,
               AVG(Amount) AS avg_amount, MAX(Amount) AS max_amount
        FROM base
        GROUP BY hour_of_day ORDER BY hour_of_day;
        """
        _query_to_csv(con, hourly_sql, OUT_DIR / "sql_hourly_stats.csv")

        # Global z-score anomalies by amount
        z_sql = """
        WITH stats AS (SELECT AVG(Amount) AS mu, STDDEV_POP(Amount) AS sigma FROM transactions),
        scored AS (
          SELECT rowid AS id, Amount,
                 (Amount - (SELECT mu FROM stats)) / NULLIF((SELECT sigma FROM stats),0) AS z
          FROM transactions
        )
        SELECT * FROM scored WHERE z > 3 ORDER BY z DESC LIMIT 1000;
        """
        _query_to_csv(con, z_sql, OUT_DIR / "sql_amount_zscore_outliers.csv")

        # Top amounts
        top_sql = "SELECT rowid AS id, Amount, Time, Class FROM transactions ORDER BY Amount DESC LIMIT 1000;"
        _query_to_csv(con, top_sql, OUT_DIR / "sql_top_amounts.csv")

if __name__ == "__main__":
    main()
