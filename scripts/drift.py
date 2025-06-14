#!/usr/bin/env python3
from events.event_store import write_event, read_events
from modules.sigil_drift_plot import plot_drift
from vitalum.gradient_engine import update_state, load_state

def add_pulse():
    write_event({"type": "pulse"})
    events = read_events()
    # Beispiel-Berechnung, hier anpassen
    drift_score = len(events) / 100.0
    delta = update_state(drift_score)
    return delta

def main():
    delta = add_pulse()
    print(f"Drift Δ∇V = {delta}")
    plot_drift()

if __name__ == "__main__":
    main()
