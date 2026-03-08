"""Transfer manager for local and cross-node snapshot movement."""

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from local_transfer import copy_snapshot_local
from network_transfer import send_snapshot

class TransferManager:
    def __init__(self, snapshot_dir="./snapshot"):
        """
        Initializes the Transfer Manager with a base directory for snapshots.
        """
        self.snapshot_dir = snapshot_dir

    def send_snapshot(self, process_id, target_path, target_host="127.0.0.1", protocol="auto", user=None):
        """
        Orchestrates the transfer of a specific process snapshot to a target destination.
        
        Args:
            process_id (int): The PID of the captured process.
            target_path (str): The destination directory or node path.
            target_host (str): host/IP of target node.
            protocol (str): auto|local|ssh
            user (str): optional ssh user
        """
        # Define the source path for the specific process snapshot
        snapshot_path = os.path.join(self.snapshot_dir, f"process_{process_id}")
        
        # Validation: Ensure the snapshot actually exists before attempting transfer
        if not os.path.exists(snapshot_path):
            error_msg = f"Snapshot {snapshot_path} not found. Ensure capture was successful."
            print(f"[TransferManager] ERROR: {error_msg}")
            raise FileNotFoundError(error_msg)
        
        print(f"[TransferManager] Initiating transfer for PID {process_id} ({protocol})...")

        if protocol == "local" or (protocol == "auto" and target_host in ("127.0.0.1", "localhost", "::1")):
            destination = copy_snapshot_local(snapshot_path, target_path)
            print(f"[TransferManager] SUCCESS: Snapshot {process_id} moved to {destination}")
            return {"success": True, "destination": destination, "protocol": "local"}

        success, result = send_snapshot(
            snapshot_path=snapshot_path,
            target_host=target_host,
            target_path=target_path,
            protocol=protocol,
            user=user,
        )
        if not success:
            raise RuntimeError(f"snapshot transfer failed: {result}")

        print(f"[TransferManager] SUCCESS: Snapshot {process_id} transferred to {result}")
        return {"success": True, "destination": result, "protocol": protocol}

    def list_local_snapshots(self):
        """
        Helper to list all available snapshots in the storage directory.
        """
        if not os.path.exists(self.snapshot_dir):
            return []
        return [d for d in os.listdir(self.snapshot_dir) if os.path.isdir(os.path.join(self.snapshot_dir, d))]

    def send_artifact(self, artifact_path, target_path, target_host="127.0.0.1", protocol="auto", user=None):
        """
        Transfer any snapshot artifact (file or directory), used by Phase 3 container checkpoints.
        """
        if not os.path.exists(artifact_path):
            raise FileNotFoundError(f"artifact not found: {artifact_path}")

        if protocol == "local" or (protocol == "auto" and target_host in ("127.0.0.1", "localhost", "::1")):
            destination = copy_snapshot_local(artifact_path, target_path)
            return {"success": True, "destination": destination, "protocol": "local"}

        success, result = send_snapshot(
            snapshot_path=artifact_path,
            target_host=target_host,
            target_path=target_path,
            protocol=protocol,
            user=user,
        )
        if not success:
            raise RuntimeError(f"artifact transfer failed: {result}")
        return {"success": True, "destination": result, "protocol": protocol}
