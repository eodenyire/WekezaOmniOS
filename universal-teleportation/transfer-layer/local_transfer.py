"""
WekezaOmniOS Local Transfer Module
Handles the physical movement of snapshot directories within the local filesystem.
"""

import shutil
import os

def copy_snapshot_local(snapshot_path, target_path):
    """
    Copies a snapshot directory from a source to a local target destination.
    
    Args:
        snapshot_path (str): The full path to the source snapshot directory.
        target_path (str): The parent directory where the snapshot should be moved.
    """
    try:
        # Ensure the target parent directory exists
        os.makedirs(target_path, exist_ok=True)
        
        # Construct the final destination path (e.g., /target/process_1921)
        snapshot_name = os.path.basename(snapshot_path)
        dest_path = os.path.join(target_path, snapshot_name)
        
        # Perform the copy operation
        # dirs_exist_ok=True ensures we can overwrite/update an existing snapshot
        shutil.copytree(snapshot_path, dest_path, dirs_exist_ok=True)
        
        print(f"[Local Transfer] SUCCESS: Snapshot copied from {snapshot_path} → {dest_path}")
        return dest_path

    except Exception as e:
        print(f"[Local Transfer] ERROR: Failed to copy snapshot. Reason: {e}")
        raise
