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
