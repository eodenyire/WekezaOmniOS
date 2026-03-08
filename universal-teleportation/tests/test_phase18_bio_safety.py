"""
WekezaOmniOS Phase 18 Tests — Biological Teleportation Safety
"""
import pytest
from state_reconstruction.biological_safety import BiologicalSafetyValidator, BiologicalSafetyReport
from state_capture.biological_layer import BiologicalStateModel


def test_validator_instantiation():
    validator = BiologicalSafetyValidator()
    assert validator is not None


def test_validate_healthy_state():
    validator = BiologicalSafetyValidator()
    model = BiologicalStateModel("entity_healthy")
    bio_state = model.simulate_biological_state(process_id=10)
    report = validator.validate_biological_safety("/snap/healthy.tar.gz", bio_state)
    assert report.verdict in ("PASS", "WARN")  # simulated state should be safe


def test_validate_critical_state_aborts():
    validator = BiologicalSafetyValidator()
    # heartbeat of 5 is clearly outside safe range
    bio_state = {
        "entity_id": "test",
        "variables": {"heartbeat_bpm": {"value": 5, "status": "critical"}},
    }
    report = validator.validate_biological_safety("/snap/critical.tar.gz", bio_state)
    assert report.verdict == "ABORT"


def test_validate_no_state_uses_defaults():
    validator = BiologicalSafetyValidator()
    report = validator.validate_biological_safety("/snap/default.tar.gz", None)
    assert isinstance(report, BiologicalSafetyReport)
    assert report.verdict in ("PASS", "WARN")


def test_report_to_dict():
    validator = BiologicalSafetyValidator()
    report = validator.validate_biological_safety("/snap/test.tar.gz")
    d = report.to_dict()
    assert "verdict" in d
    assert "findings" in d


def test_warning_does_not_block():
    validator = BiologicalSafetyValidator()
    bio_state = {
        "entity_id": "warn_entity",
        "variables": {
            "heartbeat_bpm": {"value": 115, "status": "warning"},
        },
    }
    report = validator.validate_biological_safety("/snap/warn.tar.gz", bio_state)
    assert report.verdict != "ABORT"
