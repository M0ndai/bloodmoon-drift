#!/usr/bin/env python3
"""
scripts/bloodmoon.py
CLI-Entrypoint für BloodMoon Drift Framework.
Unterstützte Commands:
  - map       : Zeigt die Drift-Map (Plot + Heat + Fokus + Delegation)
  - synth     : Generiert Sigil aus aktueller Matrix
  - thresholds: Listet aktuelle Heatmap-Schwellen auf
"""
import sys
from pathlib import Path
# Ensure project modules are importable when run via CLI
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse
from modules.sigil_drift_plot import plot_drift, evaluate_heat_zones, load_matrix
from modules.sigil_synth import generate_sigil, fallback_sigil_name


def main():
    parser = argparse.ArgumentParser(
        prog="bloodmoon",
        description="BloodMoon Drift CLI"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # Map command
    sub.add_parser(
        "map",
        help="Zeige komplettes Drift-Display (Map + Heat + Fokus + Delegation)"
    )

    # Synth command
    synth_p = sub.add_parser(
        "synth",
        help="Erzeuge ein Sigil aus der aktuellen Matrix"
    )
    synth_p.add_argument(
        "--name", "-n",
        help="Optionaler Name für das Sigil"
    )

    # Thresholds command
    sub.add_parser(
        "thresholds",
        help="Zeige die aktuellen Heatmap-Schwellen"
    )

    args = parser.parse_args()

    if args.command == "map":
        print("[🜍] Command 'map' gestartet")
        plot_drift()
        print("[🜍] Command 'map' beendet")

    elif args.command == "synth":
        matrix = load_matrix()
        sigil_obj = generate_sigil(matrix, name=args.name)
        try:
            sigil_str = sigil_obj.render(mode="unicode")  # type: ignore[attr-defined]
        except Exception:
            sigil_str = str(sigil_obj)
        print(f"[🧬] Generiertes Sigil: {sigil_str}")

    elif args.command == "thresholds":
        heat = {
            'rift_core': 5.0,
            'echo_static': 3.5,
            'neutral_zone': 1.0
        }
        print("[🔥] Aktuelle Zonen-Schwellen:")
        for z, t in heat.items():
            print(f"  - {z}: {t}")

if __name__ == "__main__":
    main()