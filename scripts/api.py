# === scripts/api.py ===
from fastapi import FastAPI
from vitalum.core import get_state
from events.event_store import read_events

app = FastAPI()

@app.get("/state")
def get_system():
    return get_state()

@app.get("/symbols")
def get_last_symbols():
    events = read_events()
    return [e for e in events[-10:] if e.get("symbol")]

@app.get("/entropy")
def entropy():
    from scripts.drift import calculate_entropy
    return {"entropy": calculate_entropy()}

@app.get("/zones")
def get_zones():
    return get_state().get("zones", {})
