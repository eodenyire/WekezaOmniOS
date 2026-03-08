"""
WekezaOmniOS Network Transfer Module
Phase 2+: Moves snapshots between nodes over the network.
"""

import os
import sys
import shutil

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from ssh_transfer import copy_snapshot_ssh


def send_snapshot(snapshot_path, target_host, target_path, protocol="auto", user=None):
    """
    Transfer a snapshot to a remote node.

    In the current prototype this copies to a local path to simulate the transfer.
    Phase 4+ will replace this with gRPC / streaming transfer.

    Args:
        snapshot_path (str): Local path to the snapshot file or directory.
        target_host (str): Hostname or IP of the target node.
        target_path (str): Destination path on the target node.
        protocol (str): auto|local|ssh
        user (str): optional ssh user

    Returns:
        tuple(bool, str): success flag and destination path or error text.
    """
    if not os.path.exists(snapshot_path):
        return False, f"source does not exist: {snapshot_path}"

    selected = protocol
    if protocol == "auto":
        selected = "local" if target_host in ("127.0.0.1", "localhost", "::1") else "ssh"

    if selected == "local":
        print(f"[NetworkTransfer] Sending {snapshot_path} -> {target_host}:{target_path}")
        dest_dir = os.path.dirname(target_path)
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)
        if os.path.isdir(snapshot_path):
            shutil.copytree(snapshot_path, target_path, dirs_exist_ok=True)
        else:
            shutil.copy2(snapshot_path, target_path)
        print(f"[NetworkTransfer] Transfer complete.")
        return True, target_path

    if selected == "ssh":
        return copy_snapshot_ssh(snapshot_path, target_host, target_path, user=user)

    return False, f"unsupported protocol: {selected}"

