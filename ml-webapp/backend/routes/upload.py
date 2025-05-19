import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd, io
from ..data_store import SESSION_STORE, UPLOAD_DIR

router = APIRouter()

@router.post("/upload/")
async def upload_csv(file: UploadFile = File(...)):
    fname = file.filename
    ext = fname.split('.')[-1].lower()
    data = await file.read()

    # Create session
    session_id = str(uuid.uuid4())
    save_path = UPLOAD_DIR / f"{session_id}_{fname}"
    save_path.write_bytes(data)

    # Parse file by extension
    if ext == "csv":
        df = pd.read_csv(io.BytesIO(data))
    elif ext in ("xls", "xlsx"):
        df = pd.read_excel(io.BytesIO(data))
    elif ext == "json":
        df = pd.read_json(io.BytesIO(data))
    else:
        raise HTTPException(400, "Unsupported file type")

    # Store in session
    SESSION_STORE[session_id] = {"df": df, "path": save_path, "history": []}

    preview = df.head(5).to_dict(orient="records")
    return {
        "session_id": session_id,
        "columns": df.columns.tolist(),
        "shape": df.shape,
        "preview": preview
    }
