"""
WekezaOmniOS Network Transfer Tests
Phase 2: Validates snapshot transfer mechanics.
"""
import os
import pytest
import shutil
import tempfile
from transfer_layer.network_transfer import send_snapshot
from transfer_layer.parallel_transfer import transfer_snapshot, stream_chunk
from cluster.cluster_manager import ClusterManager


# ---------------------------------------------------------------------------
# network_transfer tests
# ---------------------------------------------------------------------------

def test_send_snapshot_copies_file(tmp_path):
    """send_snapshot copies a snapshot file to the target path."""
    src_file = tmp_path / "snapshot.tar.gz"
    src_file.write_bytes(b"dummy snapshot data")
    dest_file = tmp_path / "dest_snapshot.tar.gz"

    send_snapshot(str(src_file), "127.0.0.1", str(dest_file))

    assert dest_file.exists()
    assert dest_file.read_bytes() == b"dummy snapshot data"


# ---------------------------------------------------------------------------
# parallel_transfer tests
# ---------------------------------------------------------------------------

def test_parallel_transfer_with_valid_node(tmp_path):
    """transfer_snapshot succeeds when the target node exists in the registry."""
    registry_file = str(tmp_path / "registry.json")
    cm = ClusterManager(registry_path=registry_file)
    cm.register_node("node-target", "127.0.0.1")

    # Create a dummy snapshot file
    snap = tmp_path / "snap.tar.gz"
    snap.write_bytes(b"data")

    result = transfer_snapshot(str(snap), "node-target", cm)
    assert result is True


def test_parallel_transfer_missing_node(tmp_path):
    """transfer_snapshot returns False when the target node is not registered."""
    registry_file = str(tmp_path / "registry.json")
    cm = ClusterManager(registry_path=registry_file)

    snap = tmp_path / "snap.tar.gz"
    snap.write_bytes(b"data")

    result = transfer_snapshot(str(snap), "ghost-node", cm)
    assert result is False
