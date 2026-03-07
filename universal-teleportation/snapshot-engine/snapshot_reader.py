"""
WekezaOmniOS Snapshot Reader
Inspects and validates the contents of portable process snapshots.
"""

import tarfile
import os
import json

def read_snapshot(snapshot_file: str):
    """
    Opens a compressed snapshot to list its internal files and 
    retrieves associated process metadata.
    
    Args:
        snapshot_file (str): Path to the .tar.gz snapshot archive.
    """
    # 1. Archive Integrity Check
    if not os.path.exists(snapshot_file):
        print(f"[Snapshot Reader] ❌ ERROR: Snapshot file not found: {snapshot_file}")
        return None

    try:
        # 2. Inspect the "Cargo"
        with tarfile.open(snapshot_file, "r:gz") as tar:
            print(f"\n📦 [Snapshot Reader] Inspecting: {os.path.basename(snapshot_file)}")
            print("-" * 50)
            print("Internal File Manifest:")
            # Lists all files inside the compressed archive
            tar.list()
            print("-" * 50)

        # 3. Locate and Read Metadata
        # We look for metadata.json in the same directory as the tarball
        metadata_file = os.path.join(os.path.dirname(snapshot_file), "metadata.json")
        
        if os.path.exists(metadata_file):
            with open(metadata_file, "r") as f:
                metadata = json.load(f)
            print("📄 [Snapshot Reader] Metadata Manifest Found:")
            # Pretty-print the metadata for better CLI readability
            print(json.dumps(metadata, indent=4))
            return metadata
        else:
            print("⚠️ [Snapshot Reader] WARNING: No external metadata.json found.")
            return None

    except tarfile.ReadError:
        print(f"[Snapshot Reader] ❌ CRITICAL: {snapshot_file} is corrupted or not a valid GZIP archive.")
    except Exception as e:
        print(f"[Snapshot Reader] ❌ UNEXPECTED ERROR: {str(e)}")

# --- Example Usage ---
if __name__ == "__main__":
    # Test path - pointing to a generated Phase 1 snapshot
    test_snapshot = "./snapshots/process_1821_snapshot.tar.gz"
    read_snapshot(test_snapshot)
