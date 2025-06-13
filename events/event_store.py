# === events/event_store.py ===

import json
from pathlib import Path
from datetime import datetime

LOG_PATH = Path("logs.jl")

def write_event(event: dict):
    event["timestamp"] = event.get("timestamp", datetime.now().isoformat())
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")