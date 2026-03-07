"""
WekezaOmniOS Snapshot Builder
Packages raw process states into portable, compressed archives.
"""

import tarfile
import os
import json
import logging

def build_snapshot(snapshot_dir, output_file, metadata):
    """
    Orchestrates the packaging of a process snapshot.
    1. Injects metadata into the source directory.
    2. Compresses the directory into a .tar.gz archive.
    
    Args:
        snapshot_dir (str): Path to the raw captured data (memory, env, etc).
        output_file (str): The destination path for the .tar.gz package.
        metadata (dict): Telemetry data for the snapshot manifest.
    """
    
    # 1. Integrity Check: Ensure source exists
    if not os.path.exists(snapshot_dir):
        raise FileNotFoundError(f"Source directory {snapshot_dir} does not exist.")

    # 2. Manifest Injection: Save metadata.json into the folder BEFORE archiving
    metadata_path = os.path.join(snapshot_dir, "metadata.json")
    try:
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)
        print(f"[Snapshot Builder] Manifest injected: {metadata_path}")
    except Exception as e:
        print(f"[Snapshot Builder] Error saving metadata: {e}")
        return False

    # 3. Packaging: Create the compressed portable cargo
    print(f"[Snapshot Builder] Compressing snapshot to {output_file}...")
    try:
        with tarfile.open(output_file, "w:gz") as tar:
            # arcname ensures we don't include absolute paths in the archive
            tar.add(snapshot_dir, arcname=os.path.basename(snapshot_dir))
        
        print(f"[Snapshot Builder] ✅ SUCCESS: Snapshot created at {output_file}")
        return True
    except Exception as e:
        print(f"[Snapshot Builder] ❌ Compression failed: {e}")
        return False

# Example Phase 1 Execution
if __name__ == "__main__":
    # Mock data for testing the engine
    metadata_example = {
        "process_id": 1821,
        "timestamp": "2026-03-07T18:20:00",
        "os": "ubuntu-24.04",
        "architecture": "x86_64",
        "memory_size": "120MB"
    }
    
    # Ensure local test directories exist
    os.makedirs("./temp/demo_capture", exist_ok=True)
    os.makedirs("./snapshots", exist_ok=True)
    
    # Run the builder
    build_snapshot(
        "./temp/demo_capture", 
        "./snapshots/process_1821_snapshot.tar.gz", 
        metadata_example
    )
