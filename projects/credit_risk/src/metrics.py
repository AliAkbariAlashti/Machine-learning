"""Credit-risk evaluation metrics: AUC/Gini, PR-AUC, KS, calibration, PSI, scorecard points."""
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.calibration import calibration_curve


def ks_statistic(y, p) -> float:
    y, p = np.asarray(y), np.asarray(p)
    o = np.argsort(p)
    y = y[o]
    cum_bad = np.cumsum(y) / y.sum()
    cum_good = np.cumsum(1 - y) / (1 - y).sum()
    return float(np.max(np.abs(cum_bad - cum_good)))


def psi(expected, actual, bins: int = 10) -> float:
    """Population Stability Index. <0.1 stable, 0.1-0.25 watch, >0.25 significant shift.
    Bin edges come from the *expected* (reference) distribution."""
    expected, actual = np.asarray(expected, float), np.asarray(actual, float)
    edges = np.unique(np.quantile(expected, np.linspace(0, 1, bins + 1)))
    edges[0], edges[-1] = -np.inf, np.inf
    e = np.histogram(expected, edges)[0] / len(expected)
    a = np.histogram(actual, edges)[0] / len(actual)
    e, a = np.clip(e, 1e-6, None), np.clip(a, 1e-6, None)
    return float(np.sum((a - e) * np.log(a / e)))


def expected_calibration_error(y, p, bins: int = 10) -> float:
    frac, mean = calibration_curve(y, p, n_bins=bins, strategy="quantile")
    return float(np.mean(np.abs(frac - mean)))


def evaluate(y, p) -> dict:
    auc = roc_auc_score(y, p)
    return dict(auc=auc, gini=2 * auc - 1, pr_auc=average_precision_score(y, p),
                ks=ks_statistic(y, p), brier=brier_score_loss(y, p),
                ece=expected_calibration_error(y, p), base_rate=float(np.mean(y)),
                mean_pred=float(np.mean(p)))


def pd_to_score(p, base_score=600, base_odds=50, pdo=20):
    """Scorecard scaling: `base_score` at good:bad odds of `base_odds`, +`pdo` points doubles the odds."""
    p = np.clip(p, 1e-6, 1 - 1e-6)
    factor = pdo / np.log(2)
    offset = base_score - factor * np.log(base_odds)
    return offset + factor * np.log((1 - p) / p)
