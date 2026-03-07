"""
WekezaOmniOS Transfer Manager
Coordinates the movement of process snapshots between local and remote nodes.
"""

import os
from local_transfer import copy_snapshot_local

class TransferManager:
    def __init__(self, snapshot_dir="./snapshot"):
        """
        Initializes the Transfer Manager with a base directory for snapshots.
        """
        self.snapshot_dir = snapshot_dir

    def send_snapshot(self, process_id, target_path):
        """
        Orchestrates the transfer of a specific process snapshot to a target destination.
        
        Args:
            process_id (int): The PID of the captured process.
            target_path (str): The destination directory or node path.
        """
        # Define the source path for the specific process snapshot
        snapshot_path = os.path.join(self.snapshot_dir, f"process_{process_id}")
        
        # Validation: Ensure the snapshot actually exists before attempting transfer
        if not os.path.exists(snapshot_path):
            error_msg = f"Snapshot {snapshot_path} not found. Ensure capture was successful."
            print(f"[TransferManager] ERROR: {error_msg}")
            raise FileNotFoundError(error_msg)
        
        # Phase 1: Default to local transfer logic
        print(f"[TransferManager] Initiating transfer for PID {process_id}...")
        copy_snapshot_local(snapshot_path, target_path)
        
        print(f"[TransferManager] SUCCESS: Snapshot {process_id} moved to {target_path}")

    def list_local_snapshots(self):
        """
        Helper to list all available snapshots in the storage directory.
        """
        if not os.path.exists(self.snapshot_dir):
            return []
        return [d for d in os.listdir(self.snapshot_dir) if os.path.isdir(os.path.join(self.snapshot_dir, d))]
