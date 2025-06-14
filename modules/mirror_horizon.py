# modules/mirror_horizon.py

import json
from collections import Counter
from datetime import datetime

HORIZON_PATH = "mirror_horizon_log.json"

def load_horizon():
    try:
        with open(HORIZON_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"entries": []}

def save_horizon(data):
    with open(HORIZON_PATH, "w") as f:
        json.dump(data, f, indent=2)

def analyze_longterm(fragment, symbol, drift_score):
    horizon = load_horizon()
    horizon["entries"].append({
        "timestamp": datetime.now().isoformat(),
        "symbol": symbol,
        "fragment": fragment,
        "drift": drift_score
    })
    horizon["entries"] = horizon["entries"][-100:]
    save_horizon(horizon)

    symbols = [entry["symbol"] for entry in horizon["entries"]]
    counts = Counter(symbols)
    recent = symbols[-5:]

    if len(set(recent)) == 1:
        pattern_type = "Fixierung"
    elif recent == recent[::-1]:
        pattern_type = "Spiegelung"
    elif len(set(recent)) == len(recent):
        pattern_type = "Dissoziation"
    else:
        pattern_type = "Fragmentierung"

    ritual_trigger = None
    for sym, count in counts.items():
        if count >= 5:
            ritual_trigger = {
                "symbol": sym,
                "message": f"⨀ RITUAL ERWACHT: Symbol '{sym}' überschreitet Schwelle (x{count})",
                "effect": "Systemverhalten darf mutieren"
            }
            break

    echo_comment = None
    if pattern_type == "Spiegelung":
        echo_comment = "🜞 Echo: Deine Muster sprechen zurück. Lausche nicht nur – *antworte*."

    return {
        "pattern_type": pattern_type,
        "dominant_symbol": counts.most_common(1)[0][0],
        "symbol_history": recent,
        "resonance_depth": round(sum(entry["drift"] for entry in horizon["entries"]) / len(horizon["entries"]), 3),
        "ritual_trigger": ritual_trigger,
        "echo": echo_comment
    }
