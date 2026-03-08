"""Network transfer helpers for Phase 2."""

import os
import sys
import shutil

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from ssh_transfer import copy_snapshot_ssh


def send_snapshot(snapshot_path, target_host, target_path, protocol="auto", user=None):
    """Transfer snapshot via local copy or scp.

    Returns:
        tuple(bool, str): success flag and destination or error text
    """
    if not os.path.exists(snapshot_path):
        return False, f"source does not exist: {snapshot_path}"

    selected = protocol
    if protocol == "auto":
        selected = "local" if target_host in ("127.0.0.1", "localhost", "::1") else "ssh"

    if selected == "local":
        os.makedirs(target_path, exist_ok=True)
        destination = os.path.join(target_path, os.path.basename(snapshot_path))
        if os.path.isdir(snapshot_path):
            shutil.copytree(snapshot_path, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(snapshot_path, destination)
        return True, destination

    if selected == "ssh":
        return copy_snapshot_ssh(snapshot_path, target_host, target_path, user=user)

    return False, f"unsupported protocol: {selected}"
