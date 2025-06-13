# symbol_heatmap.py
import json
import matplotlib.pyplot as plt
import os
from collections import defaultdict
from datetime import datetime
from vitalum.core import update_zone

DATA_PATH = "data/symbol_matrix.json"
LOG_PATH = "data/zone_transitions.log"

ZONE_TRIGGER_THRESHOLD = 3
SPECIAL_COMBO = [("mirror", "⟁"), ("seer", "☍")]


def load_matrix():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r") as f:
        return json.load(f).get("matrix", [])

def build_heatmap(matrix):
    heat = defaultdict(int)
    for entry in matrix:
        x, y = entry["x"], entry["y"]
        heat[(x, y)] += 1
    return heat

def render_heatmap(heat):
    xs, ys, values = zip(*[(x, y, count) for (x, y), count in heat.items()])
    plt.figure(figsize=(6, 6))
    plt.scatter(xs, ys, s=[v * 100 for v in values], c=values, cmap='plasma', alpha=0.7)
    plt.colorbar(label='Symbol Frequency')
    plt.grid(True)
    plt.title("Symbol Placement Heatmap")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axhline(0, color='black', lw=0.5)
    plt.axvline(0, color='black', lw=0.5)
    plt.show()

def evaluate_zone_logic(matrix):
    zone_counts = defaultdict(int)
    zone_symbol_map = defaultdict(set)
    triggered_zones = set()
    for entry in matrix:
        zone = entry.get("zone")
        symbol = entry.get("symbol")
        zone_counts[zone] += 1
        if symbol:
            zone_symbol_map[zone].add(symbol)

    transitions = []
    for zone, count in zone_counts.items():
        if count >= ZONE_TRIGGER_THRESHOLD:
            transitions.append(f"Zone {zone} reached threshold ({count})")
            triggered_zones.add(zone)

    for zone, symset in zone_symbol_map.items():
        for z, s in SPECIAL_COMBO:
            if z == zone and s in symset:
                transitions.append(f"Special combo triggered in {zone}: {s}")
                triggered_zones.add(zone)

    return transitions, triggered_zones

def log_transitions(transitions):
    with open(LOG_PATH, "a") as f:
        for t in transitions:
            f.write(f"[{datetime.now().isoformat()}] {t}\n")

def apply_zone_updates(zones):
    for z in zones:
        update_zone(z, status="active")

if __name__ == "__main__":
    matrix = load_matrix()
    heat = build_heatmap(matrix)
    render_heatmap(heat)

    transitions, zones_to_activate = evaluate_zone_logic(matrix)
    if transitions:
        print("[!] Zone transitions detected:")
        for t in transitions:
            print(" -", t)
        log_transitions(transitions)
        apply_zone_updates(zones_to_activate)
