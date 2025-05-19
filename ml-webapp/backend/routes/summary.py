from fastapi import APIRouter, HTTPException
import pandas as pd
from ..data_store import SESSION_STORE

router = APIRouter()

@router.get("/summary/{session_id}")
def summary(session_id: str):
    entry = SESSION_STORE.get(session_id)
    if not entry:
        raise HTTPException(404, "Session not found")
    df = entry["df"]
    summ = {}
    for col in df.columns:
        s = df[col]
        summ[col] = {
            "dtype": str(s.dtype),
            "count": int(s.count()),
            "nulls": int(s.isnull().sum()),
            "unique": int(s.nunique())
        }
        if pd.api.types.is_numeric_dtype(s):
            d = s.describe()
            summ[col].update({
                "mean": float(d["mean"]),
                "std": float(d["std"]),
                "min": float(d["min"]),
                "max": float(d["max"])
            })
    return {"summary": summ}
