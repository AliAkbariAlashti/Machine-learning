# Model Card: 12-month Probability of Default (PD)

**Purpose:** rank and price consumer-loan applicants; PD feeds an approve/review cutoff.
**Data:** synthetic portfolio (`src/data.py`), 24 monthly vintages. Replace with real data; keep the interfaces.
**Target:** 90+ DPD within 12 months of origination.
**Validation:** out-of-time (train vintages 0-13, calibrate 14-17, test 18-23). No random splits.
**Models compared:** Logistic Regression (baseline), XGBoost, LightGBM, CatBoost; isotonic calibration on a held-out window.
**Metrics:** AUC/Gini, PR-AUC, KS, Brier, ECE, PSI (features and score).

## Assumptions and limitations
- Only approved loans have outcomes (selection bias); reject inference is not modelled, so cutoff simulations are optimistic.
- Last vintages are right-censored in real data: wait 12 months or use a shorter window before scoring them as "final".
- Final vintages in the synthetic data have an injected shift; monitoring should flag it.

## Monitoring and actions
| Signal | Threshold | Action |
|---|---|---|
| Feature/score PSI | >0.10 watch, >0.25 alert | investigate, consider retrain |
| Predicted vs actual DR gap, AUC stable | >20% relative | recalibrate |
| AUC/KS drop | >0.03 vs test | retrain / challenger |

## Fairness and use
Protected attributes are not used. Check proxies (age) and reason codes (`src/explain.py`) before production use.
