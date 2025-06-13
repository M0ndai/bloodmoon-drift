# modules/symbolic_registry.py

import yaml
from pathlib import Path
from typing import TypedDict, List

class ResponseOption(TypedDict):
    label: str
    echo: str
    lang: str

ResponseRegistry = dict[str, dict[str, List[ResponseOption]]]

REGISTRY_PATH = Path("config/symbolic_registry.yaml")

def load_responses() -> ResponseRegistry:
    """
    Liest aus symbolic_registry.yaml, erwartet Struktur:
    Symbol → Pattern → Liste von ResponseOption
    """
    text = REGISTRY_PATH.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    # Einfach das dict zurückgeben; Pylance weiß durch die Signatur, was es sein soll
    return data
