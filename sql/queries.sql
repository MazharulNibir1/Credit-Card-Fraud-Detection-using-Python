

-- 1) Hour-of-day stats (Time is seconds since first transaction)
WITH base AS (
  SELECT
    CAST((Time/3600) AS INT) % 24 AS hour_of_day,
    Amount,
    Class
  FROM transactions
)
SELECT
  hour_of_day,
  COUNT(*) AS txn_count,
  SUM(CASE WHEN Class=1 THEN 1 ELSE 0 END) AS fraud_count,
  AVG(Amount) AS avg_amount,
  MAX(Amount) AS max_amount
FROM base
GROUP BY hour_of_day
ORDER BY hour_of_day;

-- 2) Z-score anomalies by amount (global z-score > 3)
WITH stats AS (
  SELECT AVG(Amount) AS mu, STDDEV_POP(Amount) AS sigma FROM transactions
),
scored AS (
  SELECT
    rowid AS id,
    Amount,
    (Amount - (SELECT mu FROM stats)) / NULLIF((SELECT sigma FROM stats),0) AS z
  FROM transactions
)
SELECT * FROM scored WHERE z > 3 ORDER BY z DESC LIMIT 100;

-- 3) Top 100 largest transactions (often interesting for review)
SELECT rowid AS id, Amount, Time, Class
FROM transactions
ORDER BY Amount DESC
LIMIT 100;
