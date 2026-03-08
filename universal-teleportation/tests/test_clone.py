"""
UAT Phase 3: Clone Execution Tests
"""
import pytest
from teleportation_api.clone import clone_process

def test_clone_logic_mapping():
    """Validates that the clone service accepts and processes multiple nodes."""
    source_pid = 2026
    targets = ["node-nbo-1", "node-nbo-2", "node-nbo-3"]
    
    # Trigger the Phase 3 multiplier logic
    success = clone_process(source_pid, targets)
    assert success is True

def test_multi_restore_initialization():
    """Ensures the Multi-Restore engine can be instantiated."""
    from state_reconstruction.multi_restore_manager import MultiRestoreManager
    manager = MultiRestoreManager()
    assert manager is not None

def test_clone_process_basic():
    """Basic regression test for the clone function."""
    # Note: Updated to handle the target as a list for consistency
    result = clone_process(1001, ["node-A"])
    assert result is True
