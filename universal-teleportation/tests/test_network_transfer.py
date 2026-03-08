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
import os
import importlib.util


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE_PATH = os.path.join(BASE_DIR, "transfer-layer", "network_transfer_engine.py")


def load_module(name, path):
	spec = importlib.util.spec_from_file_location(name, path)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


network_transfer_engine = load_module("network_transfer_engine", MODULE_PATH)


def test_local_transfer_file(tmp_path):
	engine = network_transfer_engine.LocalTransferEngine()
	src = tmp_path / "src.tar.gz"
	dst = tmp_path / "dst.tar.gz"
	src.write_bytes(b"snapshot-data" * 100)

	success, stats = engine.transfer_file(str(src), str(dst))
	assert success is True
	assert dst.exists()
	assert stats.get("success") is True


def test_manifest_for_directory(tmp_path):
	transfer = network_transfer_engine.ManifestTransfer()
	root = tmp_path / "artifact"
	root.mkdir()
	(root / "a.bin").write_bytes(b"abc")
	(root / "b.txt").write_text("hello", encoding="utf-8")

	manifest = transfer.create_manifest(str(root))
	assert "files" in manifest
	assert len(manifest["files"]) == 2

	out = tmp_path / "manifest.json"
	path = transfer.save_manifest(manifest, str(out))
	assert os.path.exists(path)


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
