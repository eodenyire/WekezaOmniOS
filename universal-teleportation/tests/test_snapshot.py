"""
WekezaOmniOS Snapshot Engine Tests
Verifies that process states are correctly bundled into portable tarball snapshots.
"""

import pytest
import os
import tarfile
import json
from snapshot_engine.snapshot_builder import build_snapshot

def test_build_snapshot_creates_valid_package(tmp_path):
    """
    Validates that the builder creates a compressed snapshot and 
    successfully integrates process metadata.
    """
    # 1. Setup mock source directory and files
    source_dir = tmp_path / "capture_data"
    source_dir.mkdir()
    (source_dir / "memory.dump").write_text("dummy memory data")
    (source_dir / "env.json").write_text('{"VAR": "VAL"}')
    
    output_file = tmp_path / "process_1821_snapshot.tar.gz"
    
    mock_metadata = {
        "process_id": 1821,
        "timestamp": "2026-03-07T20:00:00",
        "os": "ubuntu",
        "memory_size": "120MB"
    }

    # 2. Execute the builder
    # Using the signature defined in Phase 1: (snapshot_dir, output_file, metadata)
    build_snapshot(str(source_dir), str(output_file), mock_metadata)

    # 3. Assertions: Reliability Checks
    assert output_file.exists(), "The snapshot tarball was not created."
    
    # Verify the tarball is a valid gzipped tar file
    assert tarfile.is_tarfile(output_file), "The output file is not a valid tar archive."

    # Verify that metadata.json was generated inside the source_dir by the builder
    metadata_path = source_dir / "metadata.json"
    assert metadata_path.exists(), "Metadata file was not generated in the snapshot directory."
    
    # Verify metadata content integrity
    with open(metadata_path, "r") as f:
        data = json.load(f)
        assert data["process_id"] == 1821
        assert data["os"] == "ubuntu"

    print(f"[Test] Verified snapshot integrity for {output_file.name}")
