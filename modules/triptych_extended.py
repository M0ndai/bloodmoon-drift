# modules/triptych_extended.py

from typing import TypedDict, Sequence, Dict, Any
from .telemetry_collector import log_event
from ..vitalum.gradient_engine import DriftState, load_state
from .threshold_manager import ThresholdConfig, get_thresholds
from .symbolic_registry import ResponseOption, ResponseRegistry, load_responses


class Horizon(TypedDict, total=False):
    pattern_type: str
    resonance_depth: float
    ritual_trigger: Dict[str, Any]


CONFIG: ThresholdConfig = get_thresholds()
RESPONSES: ResponseRegistry = load_responses()


def should_prompt(
    drift_score: float,
    horizon: Horizon
) -> bool:
    state: DriftState = load_state()
    delta: float = state["delta"]

    prompt_index = (
        CONFIG["weights"]["drift"] * drift_score +
        CONFIG["weights"]["resonance"] * horizon.get("resonance_depth", 0.0) +
        CONFIG["weights"]["delta"] * delta
    )

    if horizon.get("ritual_trigger") is not None:
        return True
    if prompt_index >= CONFIG["prompt_threshold"]:
        return True
    if horizon.get("pattern_type") in CONFIG["pattern_types"]:
        return True
    return False


def suggest_responses(
    symbol: str,
    pattern_type: str,
    lang: str = "de"
) -> Sequence[ResponseOption]:
    options: Sequence[ResponseOption] = RESPONSES.get(symbol, {}).get(pattern_type, [])
    filtered = [o for o in options if o["lang"] == lang]

    if not filtered:
        filtered = [o for o in options if o["lang"] == CONFIG["default_lang"]]
    if not filtered:
        filtered = [
            ResponseOption(label="Weitermachen", echo="Das Fragment geht seinen Weg.", lang=lang),
            ResponseOption(label="Verwerfen",    echo="Nicht jedes Muster muss bewahrt werden.", lang=lang)
        ]
    return filtered


def integrate_into_triptych(
    horizon: Horizon,
    drift_score: float,
    symbol: str,
    ritual_active: bool,
    user_lang: str = "de"
) -> Dict[str, Any]:
    do_prompt = should_prompt(drift_score, horizon)

    state: DriftState = load_state()

    result: Dict[str, Any] = {
        "prompted": do_prompt,
        "drift_score": drift_score,
        "pattern_type": horizon.get("pattern_type"),
        "symbol": symbol,
        "resonance_depth": horizon.get("resonance_depth", 0.0),
        "delta_drift": state["delta"]
    }

    if do_prompt:
        result["options"] = suggest_responses(symbol, horizon.get("pattern_type", ""), user_lang)

    log_event(
        category="triptych_decision",
        details={**result, "ritual_active": ritual_active}
    )

    return result
