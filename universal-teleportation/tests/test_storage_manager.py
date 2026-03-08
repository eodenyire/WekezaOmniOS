"""
WekezaOmniOS Storage Manager Tests
Phase 4: Validates distributed snapshot storage backends.
"""
import os
import pytest
import shutil
from snapshot_storage.storage_manager import StorageManager
from snapshot_storage.local_storage import LocalStorage
from snapshot_storage.storage_index import StorageIndex
from snapshot_storage.distributed_cache import DistributedCache


# ---------------------------------------------------------------------------
# LocalStorage backend
# ---------------------------------------------------------------------------

def test_local_storage_save_and_load(tmp_path):
    """LocalStorage saves a snapshot directory and returns its path on load."""
    source_dir = tmp_path / "snap_source"
    source_dir.mkdir()
    (source_dir / "metadata.json").write_text('{"pid": 42}')

    storage = LocalStorage(storage_dir=str(tmp_path / "storage"))
    dest = storage.save(str(source_dir), "snap-001")
    assert os.path.exists(dest)

    loaded_path = storage.load("snap-001")
    assert "snap-001" in loaded_path


def test_local_storage_list(tmp_path):
    """LocalStorage.list() returns stored snapshot IDs."""
    source = tmp_path / "src"
    source.mkdir()
    (source / "data.txt").write_text("data")

    storage = LocalStorage(storage_dir=str(tmp_path / "store"))
    storage.save(str(source), "snap-A")

    snapshots = storage.list()
    assert "snap-A" in snapshots


# ---------------------------------------------------------------------------
# StorageManager
# ---------------------------------------------------------------------------

def test_storage_manager_store_and_retrieve(tmp_path):
    """StorageManager stores and retrieves a snapshot via the backend."""
    source = tmp_path / "src"
    source.mkdir()
    (source / "mem.dump").write_bytes(b"\x00" * 100)

    backend = LocalStorage(storage_dir=str(tmp_path / "backend"))
    manager = StorageManager(backend)

    manager.store_snapshot(str(source), "snap-100")
    retrieved_path = manager.retrieve_snapshot("snap-100")
    assert "snap-100" in retrieved_path


def test_storage_manager_list_snapshots(tmp_path):
    """StorageManager.list_snapshots() proxies the backend list."""
    backend = LocalStorage(storage_dir=str(tmp_path / "bk"))
    manager = StorageManager(backend)
    snapshots = manager.list_snapshots()
    assert isinstance(snapshots, list)


# ---------------------------------------------------------------------------
# StorageIndex
# ---------------------------------------------------------------------------

def test_storage_index_register_and_get():
    """StorageIndex stores and retrieves snapshot locations."""
    index = StorageIndex()
    index.register_snapshot("snap-X", "/storage/snap-X")
    assert index.get_snapshot("snap-X") == "/storage/snap-X"


def test_storage_index_list():
    """StorageIndex.list_snapshots returns all registered IDs."""
    index = StorageIndex()
    index.register_snapshot("s1", "/p/s1")
    index.register_snapshot("s2", "/p/s2")
    listing = index.list_snapshots()
    assert "s1" in listing
    assert "s2" in listing


def test_storage_index_missing_returns_none():
    """Accessing an unknown snapshot ID returns None."""
    index = StorageIndex()
    assert index.get_snapshot("nonexistent") is None


# ---------------------------------------------------------------------------
# DistributedCache
# ---------------------------------------------------------------------------

def test_distributed_cache_put_and_get():
    """DistributedCache stores bytes and retrieves them."""
    cache = DistributedCache()
    cache.put("snap-C", b"snapshot data")
    data = cache.get("snap-C")
    assert data == b"snapshot data"


def test_distributed_cache_miss():
    """DistributedCache returns None for unknown keys."""
    cache = DistributedCache()
    assert cache.get("unknown") is None


def test_distributed_cache_invalidate():
    """Invalidating a cached snapshot removes it."""
    cache = DistributedCache()
    cache.put("snap-D", b"data")
    cache.invalidate("snap-D")
    assert cache.get("snap-D") is None


def test_distributed_cache_stats():
    """Cache stats correctly report hit/miss counts."""
    cache = DistributedCache()
    cache.put("s1", b"a")
    cache.get("s1")    # hit
    cache.get("s2")    # miss
    stats = cache.stats()
    assert stats["hits"] == 1
    assert stats["misses"] == 1


def test_distributed_cache_eviction():
    """Cache evicts oldest entry when capacity is exceeded."""
    cache = DistributedCache(capacity=2)
    cache.put("a", b"1")
    cache.put("b", b"2")
    cache.put("c", b"3")  # should evict "a"
    assert cache.get("a") is None
    assert cache.get("b") == b"2"
    assert cache.get("c") == b"3"
