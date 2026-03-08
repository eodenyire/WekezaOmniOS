import shutil
import socket

def send_snapshot(snapshot_path, target_host, target_path):
    """
    Transfer snapshot to remote node
    """
    shutil.copy(snapshot_path, target_path)
