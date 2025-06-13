# === vitalum/core.py ===

import json
from pathlib import Path

STATE_PATH = Path("vitalum.snapshot.json")

DEFAULT_STATE = {
    "zones": {"mirror": "active", "seer": "locked"},
    "coherence": 88,
    "entropy": 12,
    "last_symbol": None
}

def update_zone(zone):
    state = get_state()
    state["zones"][zone] = "active"
    save_state(state)

def get_state():
    if not STATE_PATH.exists():
        return DEFAULT_STATE.copy()
    return json.load(open(STATE_PATH))

def save_state(state):
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)