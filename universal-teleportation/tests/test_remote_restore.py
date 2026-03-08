"""
WekezaOmniOS Remote Restore Tests
Phase 2: Validates that snapshots can be located and restored from remote node paths.
"""
import os
import json
import pytest
from state_reconstruction.restore_manager import RestoreManager
from state_reconstruction.multi_restore_manager import MultiRestoreManager


# ---------------------------------------------------------------------------
# RestoreManager — remote path simulation
# ---------------------------------------------------------------------------

def test_restore_from_simulated_remote_path(tmp_path):
    """
    Validates restoration from a path that simulates a remote node's storage.
    """
    # Simulate a remote snapshot directory
    remote_dir = tmp_path / "remote_node" / "snapshots"
    proc_dir = remote_dir / "process_5678"
    proc_dir.mkdir(parents=True)

    env_file = proc_dir / "env.json"
    env_file.write_text('{"REMOTE_NODE": "node-2", "APP": "demo"}')

    manager = RestoreManager(snapshot_dir=str(remote_dir))
    # Should complete without raising
    manager.restore_snapshot(5678)

    assert os.environ.get("REMOTE_NODE") == "node-2"


def test_restore_missing_remote_snapshot(tmp_path):
    """
    Attempting to restore a non-existent remote snapshot raises FileNotFoundError.
    """
    remote_dir = tmp_path / "remote_node" / "snapshots"
    remote_dir.mkdir(parents=True)

    manager = RestoreManager(snapshot_dir=str(remote_dir))
    with pytest.raises(FileNotFoundError):
        manager.restore_snapshot(9999)


# ---------------------------------------------------------------------------
# MultiRestoreManager
# ---------------------------------------------------------------------------

def test_multi_restore_manager_instantiation():
    """MultiRestoreManager can be created without a ClusterManager."""
    manager = MultiRestoreManager()
    assert manager is not None


def test_multi_restore_distribute_and_thaw():
    """distribute_and_thaw returns a status dict for each target node."""
    manager = MultiRestoreManager()
    results = manager.distribute_and_thaw("snap-001", ["node-A", "node-B", "node-C"])
    assert len(results) == 3
    statuses = {r["node"]: r["status"] for r in results}
    assert statuses["node-A"] == "RESUMED"
    assert statuses["node-B"] == "RESUMED"
    assert statuses["node-C"] == "RESUMED"
