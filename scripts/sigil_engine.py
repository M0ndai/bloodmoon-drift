# sigil_engine.py
import hashlib
import random
import time

SYMBOL_POOL = [
    "☌", "☋", "☊", "☍", "⚯", "⚷",
    "⟁", "⛧", "✶", "✵", "⚚", "⚘",
    "☿", "♅", "♆", "⚖", "☖", "☓"
]

def generate_drift_sigils(entropy: float, pulse: int, salt: str = "⛽bloodmoon"):
    base = f"{entropy:.2f}|{pulse}|{salt}"
    digest = hashlib.sha256(base.encode()).hexdigest()
    rng = random.Random(int(digest[:8], 16))
    return [rng.choice(SYMBOL_POOL) for _ in range(3)]

# Interpreter-Loop (für CLI oder Notebook)
def interpret_sigils(sigils):
    interpretations = {
        "☌": "Instabile Orbitallogik",
        "☋": "Verdichtete Kausalität",
        "☊": "Rückfluss erkannt",
        "☍": "Verdächtiger Transfer",
        "⚯": "Unkontrollierte Expansion",
        "⚷": "Injektionsvektor",
        "⟁": "Zone-Chaos",
        "⛧": "Grenzverletzung",
        "✶": "Heuristische Mutation",
        "✵": "Autonomes Pattern",
        "⚚": "Verlorene Signatur",
        "⚘": "Systemhunger",
        "☿": "Feedback-Kollision",
        "♅": "Entropische Schwelle",
        "♆": "Subversive Drift",
        "⚖": "Meta-Ausgleich",
        "☖": "Signal-Fragment",
        "☓": "Retentionsbruch"
    }
    for s in sigils:
        print(f"{s} → {interpretations.get(s, 'Unbekanntes Muster')}")

if __name__ == "__main__":
    # Beispiel für CLI-Ausgabe
    entropy = random.uniform(0, 100)
    pulse = int(time.time()) % 100
    sigils = generate_drift_sigils(entropy, pulse)

    print("\n\u2728 Aktuelle Drift-Sigils:")
    print(" ".join(sigils))
    print("\n🧠 Interpretation:")
    interpret_sigils(sigils)
