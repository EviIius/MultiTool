from fastapi import APIRouter
from ..config import TASKS_META

router = APIRouter()

@router.get("/tasks/")
def list_tasks():
    return TASKS_META
