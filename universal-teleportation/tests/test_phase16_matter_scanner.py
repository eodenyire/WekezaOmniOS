"""
WekezaOmniOS Phase 16 Tests — Matter Scanning Engine
"""
import pytest
from snapshot_engine.matter_scanner import MatterScanner, MatterStateRecord


def test_scanner_instantiation():
    scanner = MatterScanner()
    assert scanner is not None


def test_scan_matter_state():
    scanner = MatterScanner()
    result = scanner.scan_matter_state(process_id=1234)
    assert result["process_id"] == 1234
    assert result["resource_count"] > 0
    assert len(result["resources"]) == result["resource_count"]


def test_scan_contains_file_resources():
    scanner = MatterScanner()
    result = scanner.scan_matter_state(process_id=99)
    types = [r["resource_type"] for r in result["resources"]]
    assert "file" in types


def test_scan_contains_socket_resources():
    scanner = MatterScanner()
    result = scanner.scan_matter_state(process_id=99)
    types = [r["resource_type"] for r in result["resources"]]
    assert "socket" in types


def test_scan_contains_shared_memory():
    scanner = MatterScanner()
    result = scanner.scan_matter_state(process_id=99)
    types = [r["resource_type"] for r in result["resources"]]
    assert "shared_memory" in types


def test_matter_state_record_integrity():
    scanner = MatterScanner()
    scanner.scan_matter_state(process_id=5000)
    for record in scanner.get_records():
        # integrity_hash is computed during scan_matter_state
        assert record.integrity_hash is not None
        assert len(record.integrity_hash) > 0


def test_matter_record_invalid_type():
    with pytest.raises(ValueError, match="Unknown resource type"):
        MatterStateRecord("unknown_type", "x", {})


def test_matter_record_to_dict():
    record = MatterStateRecord("file", "fd:0", {"path": "/dev/stdin"})
    d = record.to_dict()
    assert d["resource_type"] == "file"
    assert "integrity_hash" in d
