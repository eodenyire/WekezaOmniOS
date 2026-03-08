"""
WekezaOmniOS SSH Transfer Module
Phase 2: Sends snapshots to remote nodes via SSH/SCP.
"""
import subprocess


def copy_snapshot_ssh(snapshot_path, remote_host, remote_path):
    """
    Send a snapshot to a remote node using SCP.

    Args:
        snapshot_path (str): Local path to the snapshot directory or archive.
        remote_host (str): IP address or hostname of the target environment.
        remote_path (str): Destination path on the remote machine.

    Returns:
        bool: True on success, False otherwise.
    """
    print(f"\n[SSH Transfer] {snapshot_path} -> {remote_host}:{remote_path}")
    result = subprocess.run(
        ["scp", "-r", snapshot_path, f"{remote_host}:{remote_path}"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print("[SSH Transfer] Transfer successful.")
        return True
    print(f"[SSH Transfer] Transfer failed: {result.stderr.strip()}")
    return False


# Alias for backwards compatibility
send_via_ssh = copy_snapshot_ssh
"""SSH/SCP transfer utilities for Phase 2."""

import os
import shutil
import subprocess


def copy_snapshot_ssh(snapshot_path, remote_host, remote_path, user=None, port=22, strict_host_key=False):
    """Copy snapshot to remote host using scp if available.

    Falls back to local copy when remote_host is localhost.
    """
    if remote_host in ("127.0.0.1", "localhost", "::1"):
        os.makedirs(remote_path, exist_ok=True)
        dest = os.path.join(remote_path, os.path.basename(snapshot_path))
        if os.path.isdir(snapshot_path):
            shutil.copytree(snapshot_path, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(snapshot_path, dest)
        return True, dest

    target = f"{remote_host}:{remote_path}" if not user else f"{user}@{remote_host}:{remote_path}"
    cmd = ["scp", "-P", str(port)]
    if not strict_host_key:
        cmd.extend(["-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null"])
    cmd.extend(["-r", snapshot_path, target])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            return False, result.stderr.strip() or "scp failed"
        return True, target
    except FileNotFoundError:
        return False, "scp command not available"


def send_via_ssh(snapshot_path, host, path, user=None, port=22):
    return copy_snapshot_ssh(snapshot_path, host, path, user=user, port=port)
