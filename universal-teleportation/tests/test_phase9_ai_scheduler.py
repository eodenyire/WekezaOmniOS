"""
WekezaOmniOS Phase 9 Tests — AI-Driven Intelligent Teleportation
"""
import pytest
from ai_scheduler.workload_predictor import WorkloadPredictor
from ai_scheduler.optimal_node_selector import OptimalNodeSelector


# ------ WorkloadPredictor ------

def test_predictor_instantiation():
    predictor = WorkloadPredictor()
    assert predictor is not None


def test_predict_resources_returns_dict():
    predictor = WorkloadPredictor()
    result = predictor.predict_resources(snapshot_size_kb=10_000, target_os="linux")
    assert "estimated_memory_mb" in result
    assert "estimated_cpu_cores" in result
    assert "confidence" in result


def test_predict_resources_linux_baseline():
    predictor = WorkloadPredictor()
    result = predictor.predict_resources(snapshot_size_kb=100_000, target_os="linux")
    assert result["estimated_memory_mb"] > 0
    assert result["estimated_cpu_cores"] >= 1


def test_predict_resources_windows_overhead():
    predictor = WorkloadPredictor()
    linux_pred = predictor.predict_resources(100_000, "linux")
    windows_pred = predictor.predict_resources(100_000, "windows")
    assert windows_pred["estimated_memory_mb"] > linux_pred["estimated_memory_mb"]


def test_record_and_history():
    predictor = WorkloadPredictor()
    predictor.record_teleportation({
        "process_id": 123,
        "memory_mb": 256,
        "cpu_cores": 2,
        "duration_s": 5.2,
        "target_os": "linux",
        "snapshot_size_kb": 50_000,
    })
    history = predictor.history()
    assert len(history) == 1
    assert "recorded_at" in history[0]


def test_confidence_increases_with_history():
    predictor = WorkloadPredictor()
    c0 = predictor.predict_resources(10_000, "linux")["confidence"]
    for i in range(20):
        predictor.record_teleportation({"process_id": i, "duration_s": 1.0})
    c1 = predictor.predict_resources(10_000, "linux")["confidence"]
    assert c1 > c0


# ------ OptimalNodeSelector ------

NODES = [
    {"node_id": "n1", "available_memory_mb": 4096, "available_cpu_cores": 8, "latency_ms": 10, "queue_depth": 0, "status": "online"},
    {"node_id": "n2", "available_memory_mb": 2048, "available_cpu_cores": 4, "latency_ms": 5,  "queue_depth": 2, "status": "online"},
    {"node_id": "n3", "available_memory_mb": 512,  "available_cpu_cores": 2, "latency_ms": 50, "queue_depth": 8, "status": "online"},
    {"node_id": "n4", "available_memory_mb": 8192, "available_cpu_cores": 16,"latency_ms": 100,"queue_depth": 0, "status": "offline"},
]


def test_selector_instantiation():
    selector = OptimalNodeSelector()
    assert selector is not None


def test_select_returns_best_node():
    selector = OptimalNodeSelector()
    best = selector.select(NODES, required_memory_mb=512, required_cpu=2)
    assert best is not None
    assert best["status"] == "online"


def test_select_excludes_offline_nodes():
    selector = OptimalNodeSelector()
    best = selector.select(NODES, required_memory_mb=512, required_cpu=2)
    assert best.get("node_id") != "n4"


def test_select_returns_none_when_no_eligible():
    selector = OptimalNodeSelector()
    # Require more memory than any node has
    best = selector.select(NODES, required_memory_mb=100_000, required_cpu=1)
    assert best is None


def test_rank_returns_sorted_list():
    selector = OptimalNodeSelector()
    ranked = selector.rank(NODES, required_memory_mb=512, required_cpu=2)
    # Offline node excluded
    assert all(n["status"] == "online" for n in ranked)
    # Scores descending
    scores = [n["__score"] for n in ranked]
    assert scores == sorted(scores, reverse=True)
