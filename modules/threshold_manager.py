# modules/threshold_manager.py

from pathlib import Path
import yaml
from typing import TypedDict, List

class ThresholdConfig(TypedDict):
    prompt_threshold: float
    weights: dict[str, float]
    pattern_types: List[str]
    default_lang: str

CONFIG_PATH = Path("config/thresholds.yaml")

def get_thresholds() -> ThresholdConfig:
    """
    Lädt Schwellenwerte und Gewichtungen aus thresholds.yaml.
    Erwartete Struktur:
      prompt_threshold: float
      weights:
        drift: float
        resonance: float
        delta: float
      pattern_types: [str, ...]
      default_lang: str
    """
    text = CONFIG_PATH.read_text()
    data = yaml.safe_load(text)
    return ThresholdConfig({
        "prompt_threshold": data["prompt_threshold"],
        "weights": data["weights"],
        "pattern_types": data["pattern_types"],
        "default_lang": data["default_lang"],
    })
