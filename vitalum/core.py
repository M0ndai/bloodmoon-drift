# vitalum/core.py

from pathlib import Path
import json
from datetime import datetime, timezone
from typing import TypedDict, Optional

# TypedDict für den Default-Zustand
class VitalState(TypedDict):
    last_commit: str
    pulse: list[str]

# Standardzustand mit klar typisierten Feldern
DEFAULT_STATE: VitalState = {
    "last_commit": datetime.now(timezone.utc).isoformat(),
    "pulse": []
}

STATE_PATH = Path("data/vitalum.core.json")

def initialize_vitalum() -> None:
    """
    Legt initialen VitalState an, wenn noch keiner existiert.
    """
    if not STATE_PATH.exists():
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        STATE_PATH.write_text(json.dumps(DEFAULT_STATE, ensure_ascii=False, indent=2), encoding="utf-8")

def load_state() -> VitalState:
    """
    Lädt den aktuellen VitalState aus Datei oder gibt DEFAULT_STATE zurück.
    """
    if not STATE_PATH.exists():
        return DEFAULT_STATE.copy()
    data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return VitalState(data)

def update_zone(zone: str, status: Optional[str] = None) -> None:
    """
    Setzt den Status einer Zone im VitalState.
    Args:
        zone: Name der Zone, z.B. 'mirror' oder 'seer'
        status: optionaler Status-String
    """
    state = load_state()
    entry = f"{datetime.now(timezone.utc).isoformat()} | zone:{zone} status:{status or 'active'}"
    state["pulse"].append(entry)
    state["last_commit"] = datetime.now(timezone.utc).isoformat()
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
