import os

class StorageManager:
    """
    Manages snapshot storage across different backends.
    """

    def __init__(self, backend):
        self.backend = backend

    def store_snapshot(self, snapshot_path, snapshot_id):
        return self.backend.save(snapshot_path, snapshot_id)

    def retrieve_snapshot(self, snapshot_id):
        return self.backend.load(snapshot_id)

    def list_snapshots(self):
        return self.backend.list()
