# matrix_tracker.py
import json
import os
from datetime import datetime

DATA_PATH = "data/symbol_matrix.json"

class MatrixTracker:
    def __init__(self):
        self.matrix = self.load()

    def load(self):
        if not os.path.exists(DATA_PATH):
            return []
        with open(DATA_PATH, "r") as f:
            return json.load(f).get("matrix", [])

    def save(self):
        with open(DATA_PATH, "w") as f:
            json.dump({"matrix": self.matrix}, f, indent=2)

    def add_symbol(self, x, y, symbol, zone=None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "x": x,
            "y": y,
            "symbol": symbol,
            "zone": zone
        }
        self.matrix.append(entry)
        self.save()

    def get_recent(self, n=5):
        return self.matrix[-n:]

    def get_symbols_by_zone(self, zone):
        return [e for e in self.matrix if e.get("zone") == zone]

if __name__ == "__main__":
    tracker = MatrixTracker()
    tracker.add_symbol(3, -1, "⟁", zone="mirror")
    tracker.add_symbol(-2, 2, "☍", zone="support")
    print(tracker.get_recent())