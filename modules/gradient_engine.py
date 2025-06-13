# modules/gradient_engine.py

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict, List

# TypedDict für einzelne Historieneinträge
class DriftHistoryEntry(TypedDict):
    timestamp: str
    delta: float

# TypedDict für den Gesamtzustand
class DriftState(TypedDict):
    history: List[DriftHistoryEntry]
    delta: float

STATE_PATH = Path("data/drift_state.json")

def load_state() -> DriftState:
    """
    Lädt den aktuellen Drift-Zustand mit Historie.
    Gibt ein DriftState-TypedDict zurück.
    """
    if not STATE_PATH.exists():
        return DriftState({"history": [], "delta": 0.0})
    raw = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    # Erwartet: {"history": [...], "delta": float}
    return DriftState(raw)

def update_state(drift_score: float) -> float:
    """
    Aktualisiert den Drift-Zustand:
    - Hängt einen neuen Eintrag an die Historie
    - Berechnet den delta als Differenz der letzten beiden Werte
    - Speichert und gibt den aktuellen delta zurück
    """
    state = load_state()
    history = state["history"]

    now = datetime.now(timezone.utc).isoformat()
    entry: DriftHistoryEntry = {"timestamp": now, "delta": drift_score}
    history.append(entry)

    if len(history) >= 2:
        prev = history[-2]["delta"]
        diff: float = drift_score - prev
    else:
        diff = 0.0

    rounded = round(diff, 4)
    # Aktualisieren des Gesamt-delta
    state["delta"] = rounded
    # Historie auf die letzten 50 Einträge beschränken
    state["history"] = history[-50:]

    # Persistieren
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    return rounded
