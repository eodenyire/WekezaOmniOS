"""
WekezaOmniOS Network Transfer Module
Phase 2: Moves snapshots between nodes over the network.
"""
import shutil
import socket


def send_snapshot(snapshot_path, target_host, target_path):
    """
    Transfer a snapshot to a remote node.

    In the current prototype this copies to a local path to simulate the transfer.
    Phase 4+ will replace this with gRPC / streaming transfer.

    Args:
        snapshot_path (str): Local path to the snapshot file or directory.
        target_host (str): Hostname or IP of the target node.
        target_path (str): Destination path on the target node.
    """
    print(f"[NetworkTransfer] Sending {snapshot_path} -> {target_host}:{target_path}")
    shutil.copy(snapshot_path, target_path)
    print(f"[NetworkTransfer] Transfer complete.")
    return True
