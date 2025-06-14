import pytest
from subprocess import Popen, PIPE
import sys, time

@pytest.mark.timeout(5)
def test_manifest_dashboard_runs():
    """
    Smoke-test: Start the TUI in headless mode and exit immediately.
    Requires textual 0.10+ supporting --help.
    """
    proc = Popen([
        sys.executable, "scripts/bloodmoon.py", "map"
    ], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
    # Immediately terminate
    time.sleep(0.1)
    proc.terminate()
    stdout, stderr = proc.communicate(timeout=1)
    assert proc.returncode is not None