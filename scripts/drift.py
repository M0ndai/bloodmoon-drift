# === scripts/drift.py ===

from events.event_store import read_events
from vitalum.core import get_state, add_pulse
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


def calculate_entropy():
    events = read_events()
    recent = [e for e in events if e.get("type") == "ritual"]
    unique = len(set(e["symbol"] for e in recent[-20:] if "symbol" in e))
    return max(0, 20 - unique)  # simple inverse entropy proxy


def plot_drift():
    state = get_state()
    pulse = state.get("pulse", [])
    if not pulse:
        print("No pulse data.")
        return

    times = [datetime.fromisoformat(ts) for ts in pulse]
    diffs = [(t2 - t1).total_seconds() / 60 for t1, t2 in zip(times, times[1:])]

    plt.plot(diffs, marker="o")
    plt.title("Drift Pulse Intervals (minutes)")
    plt.xlabel("Event Index")
    plt.ylabel("Interval")
    plt.grid(True)
    plt.show()