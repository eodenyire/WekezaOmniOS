"""
WekezaOmniOS Phase 17 Tests — Atomic Reconstruction
"""
import pytest
from state_reconstruction.atomic_reconstructor import (
    AtomicReconstructor, AtomicReconstructionPlan, AtomicUnit
)


def test_atomic_unit_valid():
    unit = AtomicUnit(0x1000, b"\xDE\xAD\xBE\xEF")
    assert unit.verify() is True


def test_atomic_unit_wrong_size():
    with pytest.raises(ValueError):
        AtomicUnit(0x1000, b"\xDE\xAD")


def test_plan_add_and_verify():
    plan = AtomicReconstructionPlan(process_id=42, snapshot_id="test-snap")
    plan.add_unit(0x1000, b"\x00\x01\x02\x03")
    plan.add_unit(0x1004, b"\x04\x05\x06\x07")
    assert plan.verify_all() is True


def test_plan_summary():
    plan = AtomicReconstructionPlan(process_id=99, snapshot_id="snap-sum")
    plan.add_unit(0x0, b"\xFF\xFF\xFF\xFF")
    summary = plan.summary()
    assert summary["unit_count"] == 1
    assert summary["integrity"] == "PASS"


def test_reconstructor_success():
    reconstructor = AtomicReconstructor()
    result = reconstructor.reconstruct_atomically("/snapshots/process_1234")
    assert result["status"] == "SUCCESS"
    assert result["summary"]["integrity"] == "PASS"


def test_reconstructor_stores_plan():
    reconstructor = AtomicReconstructor()
    reconstructor.reconstruct_atomically("/snapshots/unique-snap-id")
    plan = reconstructor.get_plan("unique-snap-id")
    assert plan is not None
    assert plan.verify_all() is True
