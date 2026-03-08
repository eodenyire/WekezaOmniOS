"""
WekezaOmniOS Storage Manager
Phase 4: Gateway for persistent and distributed snapshot storage.
"""
import os


class StorageManager:
    def __init__(self, backend):
        """
        Initialize with a storage backend (e.g. LocalStorage).

        Args:
            backend: A storage backend object with save(), load(), and list() methods.
        """
        self.backend = backend

    def store_snapshot(self, snapshot_path, snapshot_id):
        """Archives a process snapshot into the backend storage."""
        print(f"[Storage] 📦 Archiving snapshot {snapshot_id}...")
        return self.backend.save(snapshot_path, snapshot_id)

    def retrieve_snapshot(self, snapshot_id):
        """Retrieves a snapshot path from the backend storage."""
        return self.backend.load(snapshot_id)

    def list_snapshots(self):
        """Returns all archived snapshot IDs."""
        return self.backend.list()

