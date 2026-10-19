"""Airflow DAG: weekly drift check -> branch -> retrain if PSI alert.
Requires apache-airflow (2.x/3.x). Not executed by the tests; shows the orchestration pattern."""
from datetime import datetime

from airflow.decorators import dag, task


@dag(schedule="@weekly", start_date=datetime(2025, 1, 1), catchup=False, tags=["credit", "mlops"])
def credit_pd_monitor():
    @task
    def check_drift() -> bool:
        import pandas as pd
        from src.metrics import psi
        from src.train import ARTIFACTS
        ref = pd.read_csv(ARTIFACTS / "reference.csv")
        cur = pd.read_csv(ARTIFACTS / "portfolio.csv").tail(5000)[ref.columns]
        return any(psi(ref[c], cur[c]) > 0.25 for c in ref.columns)

    @task.short_circuit
    def needs_retrain(drifted: bool) -> bool:
        return drifted

    @task
    def retrain():
        from src.train import main
        main()

    retrain_task = retrain()
    needs_retrain(check_drift()) >> retrain_task


credit_pd_monitor()
