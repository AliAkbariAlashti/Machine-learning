"""Production monitoring: feature drift (PSI), score drift, and performance by cohort.

    python -m src.monitor
"""
import joblib
import pandas as pd

from .metrics import evaluate, psi
from .train import ARTIFACTS, CAT, NUM


def drift_report(reference: pd.DataFrame, current: pd.DataFrame) -> pd.DataFrame:
    rows = [(c, psi(reference[c], current[c])) for c in reference.columns]
    out = pd.DataFrame(rows, columns=["feature", "psi"]).sort_values("psi", ascending=False)
    out["status"] = pd.cut(out["psi"], [-1, 0.1, 0.25, 99], labels=["ok", "watch", "ALERT"])
    return out


def main():
    df = pd.read_csv(ARTIFACTS / "portfolio.csv")
    ref = pd.read_csv(ARTIFACTS / "reference.csv")
    model = joblib.load(ARTIFACTS / "champion.joblib")
    df["pd"] = model.predict_proba(df[NUM + CAT])[:, 1]

    cur = df[df.vintage >= 18]
    print("Feature drift, reference (train) vs vintages 18+:\n", drift_report(ref, cur[NUM]).head(8).round(3).to_string(index=False))
    print(f"\nScore PSI: {psi(df[df.vintage < 14]['pd'], cur['pd']):.3f}")

    print("\nPerformance by vintage (post-training vintages):")
    rows = []
    for v, g in df[df.vintage >= 14].groupby("vintage"):
        m = evaluate(g["default_12m"], g["pd"])
        rows.append(dict(vintage=v, n=len(g), auc=m["auc"], ks=m["ks"], actual=m["base_rate"], predicted=m["mean_pred"]))
    print(pd.DataFrame(rows).round(3).to_string(index=False))
    print("\nA widening actual-vs-predicted gap with stable AUC = calibration/base-rate drift (recalibrate); falling AUC = concept drift (retrain).")


if __name__ == "__main__":
    main()
