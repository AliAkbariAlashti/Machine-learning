"""Explainability: global SHAP importance, permutation importance, and per-loan reason codes.

    python -m src.explain
"""
import joblib
import numpy as np
import pandas as pd
import shap
from sklearn.inspection import permutation_importance

from .train import ARTIFACTS, CAT, NUM, time_split


def reason_codes(model, row: pd.DataFrame, top: int = 3):
    """Top features pushing this applicant's risk UP (adverse-action style reasons)."""
    pre, est = model.named_steps["pre"], model.named_steps["m"]
    names = pre.get_feature_names_out()
    sv = shap.TreeExplainer(est).shap_values(pre.transform(row))
    sv = sv[1] if isinstance(sv, list) else sv
    order = np.argsort(-sv[0])[:top]
    return [(names[i], float(sv[0][i])) for i in order if sv[0][i] > 0]


def main():
    df = pd.read_csv(ARTIFACTS / "portfolio.csv")
    _, _, te = time_split(df)
    raw = joblib.load(ARTIFACTS / "champion_raw.joblib")
    X = te[NUM + CAT].sample(2000, random_state=0)

    pre, est = raw.named_steps["pre"], raw.named_steps["m"]
    names = pre.get_feature_names_out()
    sv = shap.TreeExplainer(est).shap_values(pre.transform(X))
    sv = sv[1] if isinstance(sv, list) else sv
    shap_imp = pd.Series(np.abs(sv).mean(0), index=names).sort_values(ascending=False)
    print("Mean |SHAP| (top 10):\n", shap_imp.head(10).round(4).to_string())

    pi = permutation_importance(raw, X, te.loc[X.index, "default_12m"], scoring="roc_auc", n_repeats=5, random_state=0)
    pi = pd.Series(pi.importances_mean, index=X.columns).sort_values(ascending=False)
    print("\nPermutation importance, AUC drop (top 10):\n", pi.head(10).round(4).to_string())
    print("\nReason codes for the riskiest applicant in sample:")
    p = raw.predict_proba(X)[:, 1]
    print(reason_codes(raw, X.iloc[[int(p.argmax())]]))


if __name__ == "__main__":
    main()
