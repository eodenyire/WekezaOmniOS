"""
WekezaOmniOS Phase 13 Tests — Digital Twin Cloning
"""
import pytest
from state_reconstruction.digital_twin import DigitalTwinEngine, DigitalTwin


def test_engine_instantiation():
    engine = DigitalTwinEngine()
    assert engine is not None


def test_create_twin():
    engine = DigitalTwinEngine()
    twin = engine.create_digital_twin(process_id=1001, snapshot_id="snap-abc")
    assert twin is not None
    assert twin.parent_pid == 1001
    assert twin.status == "active"


def test_twin_id_is_unique():
    engine = DigitalTwinEngine()
    t1 = engine.create_digital_twin(1001, "snap-1")
    t2 = engine.create_digital_twin(1001, "snap-1")
    assert t1.twin_id != t2.twin_id


def test_fork_twin():
    engine = DigitalTwinEngine()
    original = engine.create_digital_twin(2000, "snap-fork")
    forked = engine.fork_twin(original.twin_id)
    assert forked is not None
    assert forked.metadata.get("forked_from") == original.twin_id


def test_fork_nonexistent_returns_none():
    engine = DigitalTwinEngine()
    result = engine.fork_twin("nonexistent-id")
    assert result is None


def test_terminate_twin():
    engine = DigitalTwinEngine()
    twin = engine.create_digital_twin(3000, "snap-term")
    terminated = engine.terminate_twin(twin.twin_id)
    assert terminated is True
    assert engine.get_twin(twin.twin_id).status == "terminated"


def test_list_twins_by_status():
    engine = DigitalTwinEngine()
    engine.create_digital_twin(1, "s1")
    t2 = engine.create_digital_twin(2, "s2")
    engine.terminate_twin(t2.twin_id)
    active = engine.list_twins(status="active")
    terminated = engine.list_twins(status="terminated")
    assert len(active) == 1
    assert len(terminated) == 1


def test_compare_twins():
    engine = DigitalTwinEngine()
    a = engine.create_digital_twin(5000, "snap-cmp")
    b = engine.fork_twin(a.twin_id)
    result = engine.compare(a.twin_id, b.twin_id)
    assert result["same_origin"] is True
    assert "delta" in result


def test_divergence_increases_with_events():
    engine = DigitalTwinEngine()
    twin = engine.create_digital_twin(100, "snap-div")
    d0 = twin.divergence_score()
    for _ in range(10):
        twin.record_event("TEST", "step")
    assert twin.divergence_score() > d0
