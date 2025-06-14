import os
import json
import pytest
from modules.sigil_drift_plot import load_matrix, build_symbol_grid, build_heat_map, evaluate_heat_zones

@pytest.fixture(autouse=True)
# Override DATA_PATH and write new-style matrix structure
def set_data_path(monkeypatch, tmp_path):
    data = {
        "matrix": [
            {"symbol": "⟁", "x": 0, "y": 1},
            {"symbol": "☍", "x": 1, "y": 0},
            {"symbol": "🜁", "x": -1, "y": 0}
        ],
        "last_updated": "2025-06-13T21:04:00"
    }
    file = tmp_path / "symbol_matrix.json"
    file.write_text(json.dumps(data))
    monkeypatch.setenv("DATA_PATH", str(file))
    yield


def test_load_matrix():
    matrix = load_matrix()
    assert isinstance(matrix, list)
    assert len(matrix) == 3


def test_symbol_grid():
    matrix = load_matrix()
    grid = build_symbol_grid(matrix)
    # Coordinates mapped correctly
    assert grid[1][0] == "⟁"
    assert grid[0][1] == "☍"
    assert grid[0][-1] == "🜁"


def test_heat_and_zones():
    matrix = load_matrix()
    heat = build_heat_map(matrix)
    # All intensities default to 1
    assert heat[(0,1)] == 1
    assert heat[(1,0)] == 1
    assert heat[(-1,0)] == 1
    # With threshold 1, every cell is in neutral_zone
    thresholds = {"neutral_zone": 1}
    zones = evaluate_heat_zones(heat)
    assert "neutral_zone" in zones