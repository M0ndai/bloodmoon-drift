# === scripts/bloodmoon.py ===
import argparse
from scripts import rituals, drift, mirror, ascii_map

parser = argparse.ArgumentParser(description="BloodMoon CLI")
parser.add_argument("command", choices=["ritual", "drift", "mirror", "map"])
parser.add_argument("target", nargs="?")
args = parser.parse_args()

if args.command == "ritual":
    if args.target == "echo":
        rituals.echo_trace()
    elif args.target == "rubedo":
        rituals.rubedo()
    else:
        print("Unbekanntes Ritual.")
elif args.command == "drift":
    drift.add_pulse()
    drift.plot_drift()
elif args.command == "mirror":
    mirror.mirror_readout()
elif args.command == "map":
    print(ascii_map.render_map())