"""
WekezaOmniOS Storage Index
Phase 4: Registry for all stored process states.
"""

class StorageIndex:
    def __init__(self):
        # In-memory index (to be backed by DB in Phase 9)
        self.index = {}

    def register_snapshot(self, snapshot_id, location, metadata=None):
        """Records a snapshot's location and attributes."""
        self.index[snapshot_id] = {
            "location": location,
            "metadata": metadata or {},
            "status": "READY"
        }
        print(f"[Index] 📝 Snapshot {snapshot_id} registered in vault.")

    def get_snapshot(self, snapshot_id):
        """Look up where a process state is stored."""
        return self.index.get(snapshot_id)

    def list_snapshots(self):
        """List all tracked snapshots in the system."""
        return list(self.index.keys())
