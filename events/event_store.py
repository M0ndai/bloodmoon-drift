# === events/event_store.py ===

import json
from pathlib import Path
from datetime import datetime

LOG_PATH = Path("logs.jl")

def write_event(event: dict):
    event["timestamp"] = event.get("timestamp", datetime.now().isoformat())
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")

def read_events() -> list[dict]:
    """
    Liest alle JSON-Zeilen aus LOG_PATH und gibt sie als Liste von Dicts zurück.
    """
    if not LOG_PATH.exists():
        return []
    events = []
    with open(LOG_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                # fehlerhafte Zeile überspringen
                continue
    return events
