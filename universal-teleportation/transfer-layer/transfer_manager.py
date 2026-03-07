import os
from local_transfer import copy_snapshot_local

class TransferManager:
    def __init__(self, snapshot_dir="./snapshot"):
        self.snapshot_dir = snapshot_dir

    def send_snapshot(self, process_id, target_path):
        snapshot_path = os.path.join(self.snapshot_dir, f"process_{process_id}")
        if not os.path.exists(snapshot_path):
            raise FileNotFoundError(f"Snapshot {snapshot_path} not found")
        copy_snapshot_local(snapshot_path, target_path)
        print(f"[TransferManager] Snapshot {process_id} sent to {target_path}")
