"""Feature engineering. Pure function of one row's own columns -> no leakage possible
(nothing here uses the target or other rows' future)."""
import numpy as np
import pandas as pd


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["monthly_payment"] = d["loan_amount"] / d["term_months"]
    d["payment_to_income"] = d["monthly_payment"] / (d["income"] / 12)
    d["loan_to_income"] = d["loan_amount"] / d["income"]
    d["balance_to_income"] = d["avg_balance_3m"] / d["income"]
    d["avg_txn_size"] = d["txn_volume_3m"] / d["txn_count_3m"].clip(lower=1)
    d["late_rate"] = d["n_late_payments_6m"] / (d["n_prev_loans"] + 1)
    d["log_income"] = np.log1p(d["income"])
    return d


ENGINEERED = ["monthly_payment", "payment_to_income", "loan_to_income", "balance_to_income",
              "avg_txn_size", "late_rate", "log_income"]
