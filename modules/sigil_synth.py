# modules/sigil_synth.py
import random
import time
from typing import Optional

SYMBOL_POOL = ['🜏', '☍', '🩸', '⛧', '🧬', '🪬', '🜛', '🜍', '☌', '⟡']

class Sigil:
    """
    Repräsentiert ein generiertes Sigil mit Render-Funktion.
    """
    def __init__(self, name: str, sequence: str, mode: str = "unicode"):
        self.name = name
        self.sequence = sequence
        self.mode = mode

    def render(self, mode: Optional[str] = None) -> str:
        m = mode or self.mode
        if m == "unicode":
            return self.sequence
        elif m == "seed":
            return f"{self.name}:{hash(self.sequence) & 0xFFFF:X}"
        elif m == "svg":
            # Platzhalter für SVG-Rendering
            return f"<svg><text>{self.sequence}</text></svg>"
        else:
            return self.sequence


def generate_symbol_sequence(length: int = 3) -> str:
    return ''.join(random.choice(SYMBOL_POOL) for _ in range(length))


def fallback_sigil_name(prefix: str = "sigil", entropy: bool = True) -> str:
    base = generate_symbol_sequence()
    timestamp = str(int(time.time()))[-4:] if entropy else ""
    return f"{prefix}_{base}{timestamp}"


def generate_sigil(matrix: list, name: Optional[str] = None) -> Sigil:
    """
    Erzeugt ein Sigil aus der Symbolmatrix.
    Wenn kein Name übergeben, wird ein Fallback-Name generiert.
    """
    seq = generate_symbol_sequence()
    sigil_name = name if name is not None else fallback_sigil_name()
    # Option: Ableiten der Sequenz aus Matrix-Häufigkeiten
    return Sigil(name=sigil_name, sequence=seq)
