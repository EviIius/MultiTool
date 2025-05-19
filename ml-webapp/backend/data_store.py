import uuid
from pathlib import Path

# Where uploads go
UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# session_id → { df: DataFrame, path: Path, history: [snapshots] }
SESSION_STORE = {}
