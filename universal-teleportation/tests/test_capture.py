"""
WekezaOmniOS State Capture Tests
Verifies the initialization and process metadata retrieval of the Capture Manager.
"""

import pytest
import os
import shutil
from state_capture.capture_manager import CaptureManager

# --- Test Configuration ---
TEST_SNAPSHOT_DIR = "./snapshot_test"

@pytest.fixture(autouse=True)
def run_around_tests():
    """
    Setup and Teardown fixture: Ensures a clean test environment 
    before and after each test case.
    """
    # Setup: Ensure clean start
    if os.path.exists(TEST_SNAPSHOT_DIR):
        shutil.rmtree(TEST_SNAPSHOT_DIR)
    
    yield  # Run the actual test
    
    # Teardown: Remove test artifacts
    if os.path.exists(TEST_SNAPSHOT_DIR):
        shutil.rmtree(TEST_SNAPSHOT_DIR)

# --- Test Cases ---

def test_capture_manager_initialization():
    """
    Ensures that the CaptureManager correctly assigns its snapshot directory.
    """
    manager = CaptureManager(snapshot_dir=TEST_SNAPSHOT_DIR)
    assert manager.snapshot_dir == TEST_SNAPSHOT_DIR
    # Note: Manager should have created the directory automatically via utils.ensure_dir
    assert os.path.exists(TEST_SNAPSHOT_DIR)

def test_capture_process_metadata():
    """
    Phase 1: Simulates the capture of a mock process (PID 9999).
    Verifies that the returned data structure contains essential process metadata.
    """
    manager = CaptureManager(snapshot_dir=TEST_SNAPSHOT_DIR)
    
    # Executing the capture logic with a placeholder PID
    # In Phase 1, capture_process should return a dict with process info
    info = manager.capture_process(9999)
    
    # Validating the response contract
    assert isinstance(info, dict)
    assert "name" in info
    assert "status" in info
    assert "pid" in info
    
    # Verify the directory for this specific process was created
    expected_proc_dir = os.path.join(TEST_SNAPSHOT_DIR, "process_9999")
    assert os.path.exists(expected_proc_dir)
