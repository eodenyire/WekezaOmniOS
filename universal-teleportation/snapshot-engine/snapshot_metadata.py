"""
WekezaOmniOS Snapshot Metadata Manager
Handles the persistence of process telemetry and identification data.
"""

import json
import os
import logging

def save_metadata(metadata: dict, path: str) -> bool:
    """
    Serializes process metadata into a JSON manifest.
    Ensures the target directory is structured correctly before writing.
    
    Args:
        metadata (dict): The dictionary containing process ID, OS, and timestamps.
        path (str): The full file path (including filename) to save the JSON.
    """
    try:
        # 1. Directory Guard: Ensure the destination path is ready
        target_dir = os.path.dirname(path)
        if target_dir:
            os.makedirs(target_dir, exist_ok=True)
        
        # 2. Persistence: Write the manifest to disk
        with open(path, "w") as f:
            json.dump(metadata, f, indent=4)
        
        print(f"[Snapshot Metadata] ✅ Manifest saved: {path}")
        return True

    except PermissionError:
        print(f"[Snapshot Metadata] ❌ ERROR: Permission denied at {path}")
        return False
    except Exception as e:
        print(f"[Snapshot Metadata] ❌ ERROR: Failed to save metadata: {str(e)}")
        return False

# --- Example Metadata (Phase 1) ---
example_metadata = {
    "process_id": 1821,
    "timestamp": "2026-03-07T21:30:00", # Current Date
    "os": "ubuntu-24.04",
    "architecture": "x86_64",
    "memory_size": "120MB",
    "snapshot_name": "process_1821_snapshot.tar.gz"
}

if __name__ == "__main__":
    # Test execution for the WekezaOmniOS dev team
    test_path = "./snapshot/process_1821/metadata.json"
    save_metadata(example_metadata, test_path)
