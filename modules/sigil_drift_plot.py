# modules/sigil_drift_plot.py
import json
import os
import yaml
from collections import defaultdict
from datetime import datetime

# Optional import for visualization fallback
try:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle
except ImportError:
    plt = None
    Circle = None
    print("[⚠️] matplotlib nicht gefunden – Visualisierung deaktiviert.")

# Import ZoneThreshold at module level for type checking
try:
    from modules.zone_threshold import ZoneThreshold # type: ignore[attr-defined]
except ImportError:
    ZoneThreshold = None
    print("[⚠️] ZoneThreshold-Modul nicht gefunden – Heat-Zonen-Funktion deaktiviert.")

# Paths and logs
import os
HEAT_LOG_PATH = "logs/zone_heat_sync.log"
DATA_PATH = os.environ.get("DATA_PATH") or "data/symbol_matrix.json"


# Load matrix data from JSON file
def load_matrix() -> list:
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r") as f:
        return json.load(f).get("matrix", [])

# Build a grid of symbols
def build_symbol_grid(matrix: list) -> dict:
    grid = defaultdict(lambda: defaultdict(str))
    for entry in matrix:
        x, y = entry.get("x"), entry.get("y")
        symbol = entry.get("symbol", ".")
        grid[y][x] = symbol
    return grid

# Build a heat map counting occurrences
def build_heat_map(matrix: list) -> dict:
    heat = defaultdict(int)
    for entry in matrix:
        x, y = entry.get("x"), entry.get("y")
        heat[(x, y)] += entry.get("intensity", 1)
    return heat

# Evaluate zones based on thresholds and log
def evaluate_heat_zones(heat: dict) -> list:
    thresholds = yaml.safe_load(open('configs/thresholds.yaml'))
    zone_hits = defaultdict(int)
    for coord, val in heat.items():
        for zone, thresh in thresholds.items():
            if val >= thresh:
                zone_hits[zone] += 1
                break
    os.makedirs(os.path.dirname(HEAT_LOG_PATH), exist_ok=True)
    with open(HEAT_LOG_PATH, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] Zonen-Auswertung: {dict(zone_hits)}\n")
    return list(zone_hits.keys())

# Render the symbol plot
def render_symbol_plot(grid: dict) -> None:
    if plt is None:
        print("[🚫] Plot-Funktion übersprungen (matplotlib fehlt).")
        return
    fig, ax = plt.subplots(figsize=(8, 8))
    for y, row in grid.items():
        for x, symbol in row.items():
            ax.text(x, y, symbol, ha='center', va='center', fontsize=18)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_xticks(range(-10, 11))
    ax.set_yticks(range(-10, 11))
    ax.grid(True)
    ax.set_title("Sigil Drift Map")
    ax.invert_yaxis()
    plt.show()

# Render with heat and transitions overlay
def render_with_heat_and_transitions(matrix: list, thresholds: dict) -> None:
    """
    Render with heat overlay and zone transitions.
    """
    if plt is None or Circle is None or ZoneThreshold is None:
        print("[🚫] Heat-Overlay übersprungen (Abhängigkeiten fehlen).")
        render_symbol_plot(build_symbol_grid(matrix))
        return
    # Build grid and heatmap
    grid = build_symbol_grid(matrix)
    heatmap = build_heat_map(matrix)
    # Create visualization
    fig, ax = plt.subplots(figsize=(8, 8))  # type: ignore[attr-defined]
    # Draw base symbols
    for y, row in grid.items():
        for x, symbol in row.items():
            ax.text(x, y, symbol, ha='center', va='center', fontsize=18)
    # Instantiate threshold evaluator
    zt = ZoneThreshold(heatmap, thresholds)  # type: ignore[name-defined]
    computed = zt.compute_heatmap()  # type: ignore[attr-defined]
    # Overlay heat circles
    max_thresh = max(thresholds.values()) if thresholds else 1
    for (x, y), intensity in computed.items():
        alpha = min(intensity / max_thresh, 0.8)
        ax.add_patch(Circle((x, y), radius=0.4, alpha=alpha, color='red'))  # type: ignore[attr-defined]
    # Label transitions
    transitions = zt.identify_transition_cells()  # type: ignore[attr-defined]
    for (x, y), zone in transitions.items():
        ax.text(x, y+0.3, zone, ha='center', va='center', fontsize=10, color='white')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.grid(True)
    ax.set_title("Sigil Drift Map with Heat & Zones")
    ax.invert_yaxis()  # type: ignore[attr-defined]
    plt.show()  # type: ignore[attr-defined]()

# Sync focus time hint
def sync_focus_time() -> None:
    now = datetime.now()
    print(f"[⏳] Fokuszeit läuft – gestartet um {now.strftime('%H:%M:%S')}")

# Sync delegations hint
def sync_delegations() -> None:
    print("[↝] Delegationssystem aktiv – Aufgaben werden abgegeben …")

# Combined drift display function
def plot_drift() -> None:
    """
    Komplettes Drift-Display:
    1) Matrix laden
    2) Symbol-Gitter + Heat-Overlay + Zonenlabels rendern
    3) Fokuszeit- und Delegations-Hinweis
    """
    matrix = load_matrix()
    thresholds = yaml.safe_load(open('configs/thresholds.yaml'))
    render_with_heat_and_transitions(matrix, thresholds)

    active_zones = evaluate_heat_zones(build_heat_map(matrix))
    print("[🔥] Aktive Zonen:", active_zones)

    sync_focus_time()
    sync_delegations()

# Entry point
if __name__ == "__main__":
    plot_drift()