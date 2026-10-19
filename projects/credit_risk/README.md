# Credit Risk ML: end-to-end (problem → production)

A runnable, self-contained project on a synthetic loan portfolio covering the skills in a Data Scientist (credit risk / ML) role.

```bash
pip install -r requirements.txt   # run from projects/credit_risk
python -m src.train       # models, calibration, MLflow  -> artifacts/
python -m src.explain     # SHAP, permutation importance, reason codes
python -m src.monitor     # PSI drift, performance by vintage
python -m src.backtest    # vintage table, cutoff / profit simulation
python -m src.causal      # difference-in-differences policy impact
pytest -q                 # leakage, metric, split tests
mlflow ui --backend-store-uri artifacts/mlruns
uvicorn src.serve:app --port 8000   # then POST /score
docker build -t credit-pd .
```

## Job requirement → where it lives
| Requirement | File |
|---|---|
| Feature engineering on transactional/behavioral data | `src/features.py` |
| LR vs XGBoost / LightGBM / CatBoost, challengers | `src/train.py` |
| Train/validation strategy (out-of-time), leakage | `src/train.py::time_split`, `tests/` |
| AUC, PR, KS, Calibration, Stability (PSI), scorecard points | `src/metrics.py` |
| Feature importance and explainability | `src/explain.py` |
| Backtesting, cohort/vintage analysis, simulation | `src/backtest.py` |
| Causal inference / policy impact | `src/causal.py` |
| MLflow tracking | `src/train.py` |
| Airflow orchestration | `dags/retrain_monitor_dag.py` |
| FastAPI + Docker serving | `src/serve.py`, `Dockerfile` |
| Drift and monitoring | `src/monitor.py`, `docs/model_card.md` |
| Documentation for stakeholders | `docs/model_card.md` |

## Concepts to be able to explain in an interview
- **Leakage:** random splits across time, features built with future info; guarded by out-of-time split and a test.
- **Class imbalance:** default rate is a few percent; prefer PR-AUC/KS and calibration over accuracy; avoid resampling if you need true PDs (or recalibrate after).
- **Calibration:** a model can rank well (AUC) yet misstate PD; compare ECE raw vs isotonic.
- **PSI:** <0.1 stable, 0.1-0.25 watch, >0.25 act. **KS:** max separation of bad/good cumulative distributions.
- **Trade-offs:** LR is transparent and regulator-friendly; GBMs usually add AUC; the delta must justify the complexity.
- **Vintage analysis / right-censoring**, **selection bias / reject inference**, **parallel-trends assumption** in DiD.

## Ideas to extend
Optuna tuning, monotonic constraints (XGBoost/LightGBM), WoE binning and a classic scorecard, an MLflow model registry, a real dataset (Lending Club, Home Credit), a neural-net challenger.
