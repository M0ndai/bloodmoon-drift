import os
import subprocess
import sys
from pathlib import Path

def test_dashboard_help():
    env = os.environ.copy()
    env['PYTHONPATH'] = str(Path(__file__).resolve().parent.parent)
    result = subprocess.run([
        sys.executable, "scripts/bloodmoon.py", "--help"
    ], capture_output=True, text=True, env=env)
    assert result.returncode == 0
    assert "BloodMoon Drift CLI" in result.stdout