# modules/sigil_drift_plot.py

import json
import os
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, DefaultDict, Tuple

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes

DATA_PATH = "data/symbol_matrix.json"
HEAT_LOG_PATH = "logs/zone_heat_sync.log"
FOCUS_STATE: Dict[str, Any] = {"active": False, "start": None}


def load_matrix() -> List[Dict[str, Any]]:
    """Lädt die Symbolmatrix aus DATA_PATH."""
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r") as f:
        return json.load(f).get("matrix", [])


def build_symbol_grid(
    matrix: List[Dict[str, Any]]
) -> DefaultDict[int, DefaultDict[int, str]]:
    """
    Baut ein 2D-Gitter (y → x → symbol) aus der Matrix.
    Unbekannte Felder bleiben als ".".
    """
    grid: DefaultDict[int, DefaultDict[int, str]] = defaultdict(
        lambda: defaultdict(lambda: ".")
    )
    for entry in matrix:
        x = entry.get("x", 0)
        y = entry.get("y", 0)
        symbol = entry.get("symbol", ".")
        grid[y][x] = symbol
    return grid


def build_heat_map(matrix: List[Dict[str, Any]]) -> DefaultDict[Tuple[int, int], int]:
    """
    Aggregiert die Häufigkeit (Intensität) pro Koordinate.
    """
    heat: DefaultDict[Tuple[int, int], int] = defaultdict(int)
    for entry in matrix:
        coord = (entry.get("x", 0), entry.get("y", 0))
        heat[coord] += 1
    return heat


def evaluate_heat_zones(
    heat: DefaultDict[Tuple[int, int], int]
) -> List[str]:
    """
    Bestimmt anhand statischer Schwellen, welche Zonen aktuell aktiv sind,
    und schreibt das Ergebnis in HEAT_LOG_PATH.
    """
    thresholds: Dict[str, float] = {
        "rift_core": 5.0,
        "echo_static": 3.5,
        "neutral_zone": 1.0,
    }
    zone_hits: DefaultDict[str, int] = defaultdict(int)
    for coord, value in heat.items():
        for zone, thr in thresholds.items():
            if value >= thr:
                zone_hits[zone] += 1
                break

    with open(HEAT_LOG_PATH, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] Zonen-Auswertung: {dict(zone_hits)}\n")

    return list(zone_hits.keys())


def render_symbol_plot(grid: DefaultDict[int, DefaultDict[int, str]]) -> None:
    """
    Zeichnet das Symbol-Gitter in einem matplotlib-Plot.
    """
    fig: Figure
    ax: Axes
    fig, ax = plt.subplots(figsize=(8, 8))

    for y, row in grid.items():
        for x, symbol in row.items():
            ax.text(x, y, symbol, ha="center", va="center", fontsize=18)

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_xticks(list(range(-10, 11)))
    ax.set_yticks(list(range(-10, 11)))
    ax.grid(True)
    ax.set_title("Sigil Drift Map")
    ax.invert_yaxis()
    plt.show()


def sync_focus_time() -> None:
    """Zeigt im Terminal an, dass gerade Fokuszeit läuft."""
    now = datetime.now()
    print(f"[⏳] Fokuszeit läuft – gestartet um {now.strftime('%H:%M:%S')}")


def sync_delegations() -> None:
    """Gibt eine symbolische Meldung aus, dass Delegationen aktiv sind."""
    print("[↝] Delegationssystem aktiv – Aufgaben werden abgegeben …")


if __name__ == "__main__":
    matrix = load_matrix()
    symbol_grid = build_symbol_grid(matrix)
    render_symbol_plot(symbol_grid)

    heat = build_heat_map(matrix)
    active_zones = evaluate_heat_zones(heat)
    print("[🔥] Aktive Zonen:", active_zones)

    sync_focus_time()
    sync_delegations()
