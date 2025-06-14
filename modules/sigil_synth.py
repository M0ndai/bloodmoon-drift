# modules/sigil_synth.py

from typing import Any, Dict, List, Optional, Set, Tuple
import random
import time
from collections import defaultdict


SYMBOL_POOL: List[str] = ['🜏', '☍', '🩸', '⛧', '🧬', '🪬', '🜛', '🜍', '☌', '⟡']


def generate_symbol_sequence(length: int = 3) -> str:
    """Erstellt eine zufällige Sequenz aus SYMBOL_POOL."""
    return ''.join(random.choice(SYMBOL_POOL) for _ in range(length))


def fallback_sigil_name(prefix: str = "sigil", entropy: bool = True) -> str:
    """Generiert einen Fallback-Namen basierend auf Symbolsequenz und Timestamp."""
    base: str = generate_symbol_sequence()
    timestamp: str = str(int(time.time()))[-4:] if entropy else ""
    return f"{prefix}_{base}{timestamp}"


def map_zones(matrix: List[Dict[str, Any]]) -> Dict[Tuple[int, int], Set[str]]:
    """
    Ordnet jeder Koordinate das Set an Symbol-Zonen zu, basierend auf 'zone'-Feld.
    Erwartet in jedem Entry: {'x': int, 'y': int, 'zone': str, …}
    """
    result: Dict[Tuple[int, int], Set[str]] = defaultdict(set)
    for entry in matrix:
        x = entry.get("x")   # type: ignore
        y = entry.get("y")   # type: ignore
        zone = entry.get("zone", "neutral")  # type: ignore
        if isinstance(x, int) and isinstance(y, int) and isinstance(zone, str):
            result[(x, y)].add(zone)
    return result


def count_intensities(matrix: List[Dict[str, Any]]) -> Dict[Tuple[int, int], int]:
    """
    Summiert die 'intensity'-Werte pro Koordinate.
    Erwartet in jedem Entry: {'x': int, 'y': int, 'intensity': float, …}
    """
    heat: Dict[Tuple[int, int], int] = defaultdict(int)
    for entry in matrix:
        x = entry.get("x")   # type: ignore
        y = entry.get("y")   # type: ignore
        intensity = entry.get("intensity", 1.0)  # type: ignore
        if isinstance(x, int) and isinstance(y, int) and isinstance(intensity, (int, float)):
            heat[(x, y)] += int(intensity)
    return heat


def generate_sigil(
    matrix: List[Dict[str, Any]],
    mode: str = "unicode",
    name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Erzeugt ein Sigil-Objekt als Dict mit folgenden Feldern:
      - 'name': Name (gegeben oder Fallback)
      - 'sequence': Zufallssymbolsequenz
      - 'zone_map': Mapping Koordinate→Zonenset
      - 'heat_map': Mapping Koordinate→Intensitätssumme
      - 'mode': 'unicode' | 'svg' | 'seed'
    """
    sigil_name: str = name or fallback_sigil_name()
    zone_map: Dict[Tuple[int, int], Set[str]] = map_zones(matrix)
    heat_map: Dict[Tuple[int, int], int] = count_intensities(matrix)

    # Beispiel für Seed-Modus: gib einfach hex-Timestamp zurück
    if mode == "seed":
        return {
            "name": sigil_name,
            "seed": hex(int(time.time())),
        }

    # Unicode-Anzeige: kombiniere die ersten drei Zonen-Symbole
    if mode == "unicode":
        # nehme aus jeder Koordinate eine zufällige Zone
        symbols: List[str] = []
        for zones in zone_map.values():
            if zones:
                symbols.append(random.choice(list(zones)))
        # auf drei schneiden
        sequence = ''.join(symbols[:3]) or generate_symbol_sequence()
        return {
            "name": sigil_name,
            "sequence": sequence,
            "mode": mode,
        }

    # SVG-Support (Platzhalter, noch nicht implementiert)
    if mode == "svg":
        return {
            "name": sigil_name,
            "svg": f"<svg><!-- SVG für {sigil_name} --></svg>",
            "mode": mode,
        }

    # Fallback-Modus
    return {
        "name": sigil_name,
        "mode": mode,
    }
