# Financial Transactions Analysis (SQL + Python, real dataset)

**End-to-end pipeline** that loads the public *Credit Card Fraud Detection* dataset (Kaggle) into SQLite,
runs **SQL** analyses for unusual patterns, and uses **Python** (pandas, matplotlib, scikit-learn)
to segment behavior and simulate a simple fraud-detection model.

> ⚠️ You must download the dataset yourself (Kaggle terms). File name should be `creditcard.csv`.

## Dataset
- Kaggle: *Credit Card Fraud Detection* by ULB (European cardholders, Sept 2013).
- Columns: `Time, V1..V28, Amount, Class` (1 = fraud).
- Place `creditcard.csv` here: `data/raw/creditcard.csv`

## Project layout
```
financial-transactions-analysis/
├── data/
│   └── raw/creditcard.csv              # <- you add this
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── src/
│   ├── data/load_db.py                 # CSV -> SQLite
│   ├── analysis/sql_analysis.py        # run SQL patterns & export to CSV
│   ├── analysis/python_analysis.py     # pandas + KMeans segments + plots
│   └── models/fraud_model.py           # baseline fraud classifier
├── reports/
│   ├── figures/
│   └── metrics.json
├── pipeline.py
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Add the dataset
# (download from Kaggle and place at data/raw/creditcard.csv)

# Run the pipeline
python pipeline.py
```

### Outputs
- `reports/metrics.json` — model metrics (ROC AUC, PR AUC, etc.).
- `reports/figures/` — charts:
  - `amount_hist.png`
  - `time_vs_amount_scatter.png`
  - `segment_profiles.png`
  - `roc_curve.png`
  - `pr_curve.png`
- `reports/sql_*.csv` — results from SQL analyses (hourly stats, z-score outliers, top amounts).
- `models/model.joblib` — saved classifier.


---

## 📝 Project Notes

**Why this project?**  
Built this to apply my ML knowledge to a real-world financial problem and demonstrate end-to-end project development skills.

**Key takeaways:**  
- Learned to handle severely imbalanced datasets using SMOTE
- Understood that accuracy isn't always the right metric
- Gained experience with modular code design and Git workflows
- Discovered the importance of model interpretability in financial applications

---
**Date**: 13 January 2026  
**Author**: Nibir  
**Duration**: 1 week (including learning and implementation)
