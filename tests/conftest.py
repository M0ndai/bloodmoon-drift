import sys
from pathlib import Path
# Ensure project modules are importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
import json

@pytest.fixture
def sample_matrix(tmp_path):
    data = [
        {"x": 0, "y": 0, "symbol": "⛧", "intensity": 6},
        {"x": 1, "y": 1, "symbol": "☍", "intensity": 4},
        {"x": 2, "y": 2, "symbol": "🜛", "intensity": 1},
    ]
    file = tmp_path / "symbol_matrix.json"
    file.write_text(json.dumps({"matrix": data}))
    return file