import pytest
import os
from snapshot_engine.snapshot_builder import build_snapshot

def test_build_snapshot_creates_file(tmp_path):
    output_file = tmp_path / "snapshot_test.tar.gz"
    build_snapshot(tmp_path, output_file)
    assert output_file.exists()
