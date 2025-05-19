from fastapi import APIRouter, WebSocket
from ..data_store import SESSION_STORE
from ..services.classification import train_classification
from ..services.regression import train_regression
from ..services.clustering import train_clustering
from datetime import datetime

router = APIRouter()

@router.websocket("/ws/train/")
async def websocket_train(ws: WebSocket):
    await ws.accept()
    p = await ws.receive_json()
    sid = p.get("session_id")
    task = p.get("task")
    features = p.get("features", [])
    target = p.get("target")
    hp = p.get("hyperparams", {})

    entry = SESSION_STORE.get(sid)
    if not entry:
        await ws.send_json({"error": "Invalid session"})
        await ws.close()
        return
    df = entry["df"]

    # Validate columns
    for c in features + ([target] if target else []):
        if c not in df.columns:
            await ws.send_json({"error": f"Column '{c}' not found"})
            await ws.close()
            return

    X = df[features]
    y = df[target] if target else None

    # Delegate to service, which sends progress and returns result
    if task == "classification":
        result = await train_classification(ws, X, y, hp)
    elif task == "regression":
        result = await train_regression(ws, X, y, hp)
    elif task == "clustering":
        result = await train_clustering(ws, X, hp)
    else:
        await ws.send_json({"error": "Unknown task"})
        await ws.close()
        return

    # Snapshot
    snapshot = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "task": task,
        "features": features,
        "target": target,
        "hyperparams": hp,
        "result": result
    }
    entry["history"].append(snapshot)

    # Send final result + snapshot
    await ws.send_json({"result": result})
    await ws.send_json({"snapshot": snapshot})
    await ws.close()
