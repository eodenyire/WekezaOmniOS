"""
WekezaOmniOS Phase 15 Tests — Interplanetary Latency Optimization
"""
import os
import pytest
from transfer_layer.latency_optimizer import LatencyOptimizer, PROPAGATION_DELAYS


def test_optimizer_instantiation():
    optimizer = LatencyOptimizer()
    assert optimizer is not None


def test_optimize_latency_returns_params(tmp_path):
    snap = tmp_path / "snap.tar.gz"
    snap.write_bytes(b"x" * 1_000_000)
    optimizer = LatencyOptimizer(bandwidth_mbps=100)
    params = optimizer.optimize_latency(str(snap), rtt_ms=50)
    assert params["chunk_size_kb"] >= 64
    assert params["fec_redundancy_pct"] >= 0
    assert params["estimated_transfer_s"] > 0


def test_high_latency_increases_fec(tmp_path):
    snap = tmp_path / "snap.tar.gz"
    snap.write_bytes(b"x" * 1_000_000)
    optimizer = LatencyOptimizer()
    low_lat = optimizer.optimize_latency(str(snap), rtt_ms=10)
    high_lat = optimizer.optimize_latency(str(snap), rtt_ms=10_000)
    assert high_lat["fec_redundancy_pct"] >= low_lat["fec_redundancy_pct"]


def test_schedule_transfer():
    optimizer = LatencyOptimizer()
    entry = optimizer.schedule_transfer(
        snapshot_path="/snap/test.tar.gz",
        target_node="moon-node-01",
        delay_s=60,
        route="earth_moon",
    )
    assert entry["status"] == "SCHEDULED"
    assert entry["target_node"] == "moon-node-01"
    assert entry["propagation_s"] == PROPAGATION_DELAYS["earth_moon"]


def test_list_scheduled():
    optimizer = LatencyOptimizer()
    optimizer.schedule_transfer("/snap.tar.gz", "node-x", 30, "earth_geostationary")
    optimizer.schedule_transfer("/snap2.tar.gz", "node-y", 60, "earth_moon")
    assert len(optimizer.list_scheduled()) == 2


def test_propagation_delay_known_route():
    optimizer = LatencyOptimizer()
    delay = optimizer.propagation_delay("earth_moon")
    assert delay == pytest.approx(1.28)


def test_propagation_delay_unknown_route():
    optimizer = LatencyOptimizer()
    assert optimizer.propagation_delay("unknown_route") == 0.0
