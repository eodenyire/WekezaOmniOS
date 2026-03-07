"""
WekezaOmniOS State Reconstruction Tests
Verifies the ability to locate, validate, and simulate the restoration of captured processes.
"""

import pytest
import os
import json
from state_reconstruction.restore_manager import RestoreManager

def test_restore_manager_init(tmp_path):
    """
    Verifies that the RestoreManager is initialized with the correct directory context.
    """
    test_dir = str(tmp_path / "snapshot_test")
    manager = RestoreManager(snapshot_dir=test_dir)
    assert manager.snapshot_dir == test_dir

def test_restore_snapshot_missing_fails(tmp_path):
    """
    Ensures that attempting to restore a non-existent PID raises a FileNotFoundError.
    This validates the engine's integrity check before calling CRIU.
    """
    test_dir = str(tmp_path / "snapshot_test")
    manager = RestoreManager(snapshot_dir=test_dir)
    
    # Asserting that the orchestrator blocks restoration for missing data
    with pytest.raises(FileNotFoundError):
        manager.restore_snapshot(9999)

def test_restore_snapshot_flow_simulation(tmp_path):
    """
    Phase 1: Simulates a successful restoration flow by providing a 
    mock snapshot directory and required environment files.
    """
    # 1. Setup mock restoration environment
    test_dir = tmp_path / "snapshot_test"
    test_dir.mkdir()
    
    # Create the folder structure expected by RestoreManager: process_{pid}
    proc_dir = test_dir / "process_1234"
    proc_dir.mkdir()
    
    # Create the env.json file expected by environment_loader.py
    env_file = proc_dir / "env.json"
    env_file.write_text('{"PLATFORM": "WekezaOmniOS", "MODE": "Test"}')
    
    # 2. Initialize Manager
    manager = RestoreManager(snapshot_dir=str(test_dir))
    
    # 3. Execution: This should trigger the load_environment and log the restore
    # In Phase 1, it prints: [RestoreManager] Process 1234 restored successfully.
    manager.restore_snapshot(1234)
    
    # 4. Verify environment rehydration (Mock check)
    assert os.environ.get("PLATFORM") == "WekezaOmniOS"
