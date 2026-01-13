"""
Pandas analysis + behavior segmentation (KMeans) + visualizations.
Saves figures to reports/figures and a segment summary CSV.
"""
import json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "raw" / "creditcard.csv"
FIG = ROOT / "reports" / "figures"
OUT = ROOT / "reports"

def main():
    FIG.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(CSV)

    # Basic plots
    plt.figure()
    df["Amount"].plot(kind="hist", bins=60)
    plt.title("Transaction Amount Distribution")
    plt.xlabel("Amount")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(FIG / "amount_hist.png")
    plt.close()

    # Time vs Amount scatter (sample to keep light)
    sample = df.sample(n=min(30000, len(df)), random_state=42)
    plt.figure()
    plt.scatter(sample["Time"], sample["Amount"], s=3, alpha=0.4)
    plt.title("Time vs Amount (sample)")
    plt.xlabel("Time (seconds since first tx)")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig(FIG / "time_vs_amount_scatter.png")
    plt.close()

    # Behavior segments via KMeans on [Amount, Time mod day]
    seg = df.copy()
    seg["hour"] = (seg["Time"] // 3600) % 24
    X = seg[["Amount", "hour"]].values
    Xs = StandardScaler().fit_transform(X)
    km = KMeans(n_clusters=3, random_state=42, n_init=10)
    seg["segment"] = km.fit_predict(Xs)

    # Segment profiles
    prof = seg.groupby("segment").agg(
        txns=("segment", "size"),
        avg_amount=("Amount", "mean"),
        pct_fraud=("Class", lambda s: 100*s.mean())
    ).reset_index().sort_values("segment")
    prof.to_csv(OUT / "segment_summary.csv", index=False)

    # Plot segment profiles (avg amount, % fraud)
    plt.figure()
    x = np.arange(len(prof))
    plt.bar(x - 0.2, prof["avg_amount"], width=0.4, label="Avg Amount")
    plt.bar(x + 0.2, prof["pct_fraud"], width=0.4, label="% Fraud")
    plt.xticks(x, [f"S{i}" for i in prof["segment"]])
    plt.title("Segment Profiles: Avg Amount vs % Fraud")
    plt.xlabel("Segment")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG / "segment_profiles.png")
    plt.close()

if __name__ == "__main__":
    main()
