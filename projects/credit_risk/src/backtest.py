"""Backtesting + vintage analysis + approval-policy simulation.

    python -m src.backtest
"""
import joblib
import numpy as np
import pandas as pd

from .train import ARTIFACTS, CAT, NUM


def vintage_table(df: pd.DataFrame) -> pd.DataFrame:
    """Cohort view: default rate and avg predicted PD by origination vintage."""
    return df.groupby("vintage").agg(n=("pd", "size"), actual_dr=("default_12m", "mean"), predicted_pd=("pd", "mean")).round(4)


def simulate_cutoff(df: pd.DataFrame, cutoffs, lgd=0.6, margin=0.12) -> pd.DataFrame:
    """Approve if PD <= cutoff. Per approved loan: earn `margin * amount` if good, lose `lgd * amount` if default.
    (Counterfactual only valid for loans we actually observed -> reject inference is ignored here; flag it in docs.)"""
    rows = []
    for c in cutoffs:
        a = df[df["pd"] <= c]
        profit = np.where(a["default_12m"] == 1, -lgd, margin) * a["loan_amount"]
        rows.append(dict(cutoff=c, approval_rate=len(a) / len(df), bad_rate=a["default_12m"].mean(), profit=profit.sum() / 1e6))
    return pd.DataFrame(rows).round(4)


def main():
    df = pd.read_csv(ARTIFACTS / "portfolio.csv")
    model = joblib.load(ARTIFACTS / "champion.joblib")
    df["pd"] = model.predict_proba(df[NUM + CAT])[:, 1]
    test = df[df.vintage >= 18]
    print("Vintage table (last vintages):\n", vintage_table(df).tail(8).to_string())
    print("\nCutoff simulation on out-of-time vintages (profit in millions):\n",
          simulate_cutoff(test, [0.02, 0.04, 0.06, 0.08, 0.12, 0.2, 1.0]).to_string(index=False))


if __name__ == "__main__":
    main()
