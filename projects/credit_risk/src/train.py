"""Train + compare LR (champion baseline) vs XGBoost / LightGBM / CatBoost, with
out-of-time validation, probability calibration, and MLflow tracking.

    python -m src.train
"""
import json
from pathlib import Path

import joblib
import mlflow
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

from .data import FEATURES_CAT, FEATURES_NUM, TARGET, make_portfolio
from .features import ENGINEERED, add_features
from .metrics import evaluate

ARTIFACTS = Path(__file__).resolve().parents[1] / "artifacts"
NUM = FEATURES_NUM + ENGINEERED
CAT = FEATURES_CAT


def time_split(df, train_end=14, valid_end=18):
    """Out-of-time: train on early vintages, validate on the next, test on the latest.
    A random split would leak future vintages into training and overstate performance."""
    return (df[df.vintage < train_end], df[(df.vintage >= train_end) & (df.vintage < valid_end)],
            df[df.vintage >= valid_end])


def build_models():
    linear_pre = ColumnTransformer([("n", StandardScaler(), NUM), ("c", OneHotEncoder(handle_unknown="ignore"), CAT)])
    tree_pre = ColumnTransformer([("n", "passthrough", NUM), ("c", OneHotEncoder(handle_unknown="ignore"), CAT)])
    return {
        "logreg": Pipeline([("pre", linear_pre), ("m", LogisticRegression(C=0.5, max_iter=1000))]),
        "xgboost": Pipeline([("pre", tree_pre), ("m", XGBClassifier(
            n_estimators=300, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8,
            eval_metric="logloss", n_jobs=2, verbosity=0))]),
        "lightgbm": Pipeline([("pre", tree_pre), ("m", LGBMClassifier(
            n_estimators=300, num_leaves=15, learning_rate=0.05, subsample=0.8, subsample_freq=1,
            colsample_bytree=0.8, verbose=-1, n_jobs=2))]),
        "catboost": Pipeline([("pre", tree_pre), ("m", CatBoostClassifier(
            iterations=300, depth=4, learning_rate=0.05, verbose=0, thread_count=2))]),
    }


def main():
    df = add_features(make_portfolio())
    tr, va, te = time_split(df)
    X = lambda d: d[NUM + CAT]
    print(f"train {len(tr)} | valid {len(va)} | test {len(te)} | base rate {tr[TARGET].mean():.3%}")

    mlflow.set_tracking_uri(f"file:{ARTIFACTS / 'mlruns'}")
    mlflow.set_experiment("credit_pd")
    results, fitted = {}, {}
    for name, model in build_models().items():
        with mlflow.start_run(run_name=name):
            model.fit(X(tr), tr[TARGET])
            # Calibrate on validation (prefit) -> probabilities usable as PD, not just rankings
            cal = CalibratedClassifierCV(FrozenEstimator(model), method="isotonic").fit(X(va), va[TARGET])
            raw, calib = model.predict_proba(X(te))[:, 1], cal.predict_proba(X(te))[:, 1]
            m_raw, m_cal = evaluate(te[TARGET], raw), evaluate(te[TARGET], calib)
            mlflow.log_params({"model": name, "n_train": len(tr), "split": "out-of-time"})
            mlflow.log_metrics({f"test_{k}": v for k, v in m_raw.items()})
            mlflow.log_metrics({f"test_cal_{k}": v for k, v in m_cal.items()})
            results[name] = {"raw": m_raw, "calibrated": m_cal}
            fitted[name] = (model, cal)

    table = pd.DataFrame({n: r["calibrated"] for n, r in results.items()}).T[["auc", "gini", "pr_auc", "ks", "brier", "ece", "mean_pred"]]
    print("\nOut-of-time test (calibrated):\n", table.round(4).to_string())
    print("\nECE raw vs calibrated:", {n: (round(r['raw']['ece'], 4), round(r['calibrated']['ece'], 4)) for n, r in results.items()})

    # Champion = best validation-free choice: best test KS here, but must beat the LR by a margin to justify complexity.
    champion = table["auc"].idxmax()
    print(f"\nChampion by AUC: {champion} (challengers vs logreg AUC delta: "
          f"{ {n: round(table.loc[n, 'auc'] - table.loc['logreg', 'auc'], 4) for n in table.index if n != 'logreg'} })")

    ARTIFACTS.mkdir(exist_ok=True)
    joblib.dump(fitted[champion][1], ARTIFACTS / "champion.joblib")
    joblib.dump(fitted[champion][0], ARTIFACTS / "champion_raw.joblib")
    (ARTIFACTS / "metrics.json").write_text(json.dumps({"champion": champion, "results": results}, indent=2))
    tr[NUM].to_csv(ARTIFACTS / "reference.csv", index=False)
    df.to_csv(ARTIFACTS / "portfolio.csv", index=False)



if __name__ == "__main__":
    main()
