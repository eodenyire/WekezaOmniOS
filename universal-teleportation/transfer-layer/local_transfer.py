import shutil
import os

def copy_snapshot_local(snapshot_path, target_path):
    os.makedirs(target_path, exist_ok=True)
    dest_path = os.path.join(target_path, os.path.basename(snapshot_path))
    shutil.copytree(snapshot_path, dest_path, dirs_exist_ok=True)
    print(f"[Local Transfer] Copied snapshot from {snapshot_path} → {dest_path}")
