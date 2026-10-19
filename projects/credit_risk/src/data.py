"""Synthetic consumer-lending portfolio (no download needed).

Each row is one loan with an origination month (its *vintage*). `default_12m` is
the target: did the loan go 90+ days past due within 12 months of origination.
Later vintages have a macro shock and a shifted income distribution, so drift,
backtesting and vintage analysis have something real to find.
"""
import numpy as np
import pandas as pd

FEATURES_NUM = ["age", "income", "loan_amount", "term_months", "n_prev_loans",
                "n_late_payments_6m", "avg_balance_3m", "txn_count_3m", "txn_volume_3m"]
FEATURES_CAT = ["employment", "purpose"]
TARGET = "default_12m"


def make_portfolio(n: int = 40_000, months: int = 24, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    vintage = rng.integers(0, months, n)
    drift = (vintage >= months * 0.75).astype(float)           # last quarter: shifted population + shock

    age = rng.normal(38, 11, n).clip(18, 75)
    income = rng.lognormal(8.3 + 0.15 * drift, 0.5, n)
    loan_amount = income * rng.uniform(0.5, 6, n)
    term = rng.choice([12, 24, 36, 48], n)
    prev = rng.poisson(1.5, n)
    late = rng.poisson(0.4 + 0.3 * (prev > 3), n)
    bal = income * rng.uniform(0.1, 2, n) * rng.lognormal(0, 0.3, n)
    txn_count = rng.poisson(40, n)
    txn_vol = txn_count * rng.lognormal(4.5, 0.4, n)
    employment = rng.choice(["salaried", "self_employed", "unemployed", "retired"], n, p=[.6, .2, .08, .12])
    purpose = rng.choice(["consumer", "car", "home_improvement", "debt_consolidation"], n)

    dti = loan_amount / term / (income / 12)                      # payment-to-income
    logit = (-3.4 + 2.2 * dti + 0.55 * late - 0.00004 * bal
             + 0.9 * (employment == "unemployed") + 0.25 * (employment == "self_employed")
             + 0.4 * (purpose == "debt_consolidation") - 0.012 * (age - 38)
             + 0.35 * (dti * late > 0.5) + 0.5 * drift)
    p = 1 / (1 + np.exp(-logit))
    df = pd.DataFrame(dict(vintage=vintage, age=age, income=income, loan_amount=loan_amount,
                           term_months=term, n_prev_loans=prev, n_late_payments_6m=late,
                           avg_balance_3m=bal, txn_count_3m=txn_count, txn_volume_3m=txn_vol,
                           employment=employment, purpose=purpose))
    df[TARGET] = rng.binomial(1, p)
    return df
