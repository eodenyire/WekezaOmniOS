from snapshot_storage.storage_manager import StorageManager
from snapshot_storage.local_storage import LocalStorage

def test_storage():

    backend = LocalStorage()
    manager = StorageManager(backend)

    snapshots = manager.list_snapshots()

    assert isinstance(snapshots, list)
