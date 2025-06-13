# modules/telemetry_collector.py

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict, Any

class TelemetryEntry(TypedDict):
    timestamp: str
    category: str
    details: dict[str, Any]

LOG_PATH = Path("data/telemetry.log")

def log_event(category: str, details: dict[str, Any]) -> None:
    """
    Protokolliert eine Telemetrie-Entscheidung als JSON-Line.
    details kann beliebige zusätzliche Informationen enthalten.
    """
    entry: TelemetryEntry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "category": category,
        "details": details
    }
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
