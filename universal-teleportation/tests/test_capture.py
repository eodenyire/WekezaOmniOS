# 📄 `test_capture.py`

```python id="tc1x9v"
import pytest
from state_capture.capture_manager import CaptureManager

def test_capture_manager_exists():
    manager = CaptureManager(snapshot_dir="./snapshot_test")
    assert manager.snapshot_dir == "./snapshot_test"

def test_capture_process_placeholder():
    # Phase 1: simulate capture without real process
    manager = CaptureManager(snapshot_dir="./snapshot_test")
    info = manager.capture_process(9999)  # PID 9999 is mock
    assert "name" in info
    assert "status" in info
