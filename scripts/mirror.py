# === scripts/mirror.py ===
from events.event_store import read_events
from collections import Counter

SYMBOL_MAP = {
    "☍": "Ambivalenz",
    "⛽": "Transformation",
    "✴": "Stillstand",
}

def mirror_readout():
    events = read_events()
    symbols = [e.get("symbol") for e in events if e.get("symbol")]
    counts = Counter(symbols[-20:])
    print("Letzte Symbole:")
    for sym, count in counts.most_common():
        desc = SYMBOL_MAP.get(sym, "?")
        print(f" {sym} ({desc}) × {count}")
    if len(set(symbols[-3:])) == 1:
        print("\n🜂 Hinweis: Symbol-Stillstand erkannt – keine Wandlung.")

if __name__ == "__main__":
    mirror_readout()