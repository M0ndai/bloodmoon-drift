# === scripts/rituals.py ===

from events.event_store import write_event
from vitalum.core import update_zone
from datetime import datetime


def echo_trace():
    _perform_ritual("echo_trace", zone="mirror", symbol="☍")

def rubedo():
    _perform_ritual("rubedo", zone="mirror", symbol="⛽")

def _perform_ritual(ritual, zone, symbol):
    print(f"\ud83c\udf5c Ritual: {ritual} | Symbol: {symbol}")
    write_event({
        "type": "ritual",
        "ritual": ritual,
        "zone": zone,
        "symbol": symbol,
        "timestamp": datetime.now().isoformat()
    })
    update_zone(zone)