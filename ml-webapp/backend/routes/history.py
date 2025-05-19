from fastapi import APIRouter, HTTPException
from ..data_store import SESSION_STORE

router = APIRouter()

@router.get("/history/{session_id}")
def get_history(session_id: str):
    entry = SESSION_STORE.get(session_id)
    if not entry:
        raise HTTPException(404, "Session not found")
    return entry["history"]
