import pytest
from modules.zone_threshold import evaluate_heat_zones

@pytest.fixture
def sample_heatmap():
    # Three coordinates with varying intensities
    return {
        (0, 0): 6.0,
        (1, 1): 3.5,
        (2, 2): 1.0,
    }

@pytest.fixture
def thresholds():
    return {
        "rift_core": 5.0,
        "echo_static": 3.5,
        "neutral_zone": 1.0,
    }


def test_evaluate_heat_zones(sample_heatmap, thresholds):
    zones = evaluate_heat_zones(sample_heatmap, thresholds)
    assert "rift_core" in zones
    assert "echo_static" in zones
    assert "neutral_zone" in zones