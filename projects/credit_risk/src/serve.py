"""FastAPI model server.   uvicorn src.serve:app --port 8000"""
from functools import lru_cache

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .features import add_features
from .metrics import pd_to_score
from .train import ARTIFACTS, CAT, NUM

app = FastAPI(title="Credit PD Scoring API", version="1.0")


class Applicant(BaseModel):
    age: float = Field(ge=18, le=100)
    income: float = Field(gt=0)
    loan_amount: float = Field(gt=0)
    term_months: int = Field(gt=0)
    n_prev_loans: int = Field(ge=0)
    n_late_payments_6m: int = Field(ge=0)
    avg_balance_3m: float = Field(ge=0)
    txn_count_3m: int = Field(ge=0)
    txn_volume_3m: float = Field(ge=0)
    employment: str
    purpose: str


@lru_cache
def model():
    path = ARTIFACTS / "champion.joblib"
    if not path.exists():
        raise HTTPException(503, "model not trained: run `python -m src.train`")
    return joblib.load(path)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/score")
def score(a: Applicant):
    X = add_features(pd.DataFrame([a.model_dump()]))[NUM + CAT]
    p = float(model().predict_proba(X)[0, 1])
    return {"pd": p, "score": float(pd_to_score(p)), "decision": "approve" if p <= 0.08 else "review"}
