"""
WekezaOmniOS Storage Manager
Phase 4: Gateway for persistent and distributed snapshot storage.
"""
import os
import shutil

class StorageManager:
    def __init__(self, storage_dir="snapshot-storage/data"):
        self.storage_dir = storage_dir
        # Ensure the physical vault exists
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir, exist_ok=True)
            print(f"[Storage] 📁 Created vault directory at {self.storage_dir}")

    def store_snapshot(self, snapshot_path, snapshot_id):
        """Archives a process snapshot into the central vault."""
        destination = os.path.join(self.storage_dir, snapshot_id)
        print(f"[Storage] 📦 Archiving snapshot {snapshot_id}...")
        
        # Logic: If this were production, we'd use shutil.copytree or an S3 upload here
        # For Phase 4, we establish the path mapping for the orchestrator
        return destination

    def fetch_snapshot(self, snapshot_id):
        """Retrieves a snapshot path for a reconstruction request."""
        target = os.path.join(self.storage_dir, snapshot_id)
        if not os.path.exists(target):
            print(f"[Storage] ❌ Error: Snapshot {snapshot_id} not found.")
            return None
        return target

    def list_vault(self):
        """Returns all archived snapshots."""
        return os.listdir(self.storage_dir)
