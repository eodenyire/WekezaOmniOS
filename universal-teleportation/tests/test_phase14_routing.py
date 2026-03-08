"""
WekezaOmniOS Phase 14 Tests — Planet-Scale Teleport Routing
"""
import pytest
from transfer_layer.routing_engine import RoutingEngine


def test_routing_engine_instantiation():
    engine = RoutingEngine()
    assert engine is not None


def test_add_node():
    engine = RoutingEngine()
    engine.add_node("nairobi-1")
    assert "nairobi-1" in engine.list_nodes()


def test_add_link_and_route():
    engine = RoutingEngine()
    engine.add_node("a")
    engine.add_node("b")
    engine.add_link("a", "b", 10.0)
    result = engine.select_route("a", "b")
    assert result["path"] == ["a", "b"]
    assert result["total_latency_ms"] == 10.0


def test_multi_hop_route():
    engine = RoutingEngine()
    engine.add_link("a", "b", 10.0)
    engine.add_link("b", "c", 20.0)
    engine.add_link("a", "c", 100.0)
    result = engine.select_route("a", "c")
    # Shortest path should go a->b->c (30ms) not a->c (100ms)
    assert result["total_latency_ms"] == 30.0
    assert result["path"] == ["a", "b", "c"]


def test_unreachable_route():
    engine = RoutingEngine()
    engine.add_node("isolated-a")
    engine.add_node("isolated-b")
    result = engine.select_route("isolated-a", "isolated-b")
    assert result["path"] == []


def test_missing_node_returns_empty_path():
    engine = RoutingEngine()
    engine.add_node("real-node")
    result = engine.select_route("real-node", "ghost-node")
    assert result["path"] == []


def test_hop_count():
    engine = RoutingEngine()
    engine.add_link("x", "y", 5.0)
    engine.add_link("y", "z", 5.0)
    result = engine.select_route("x", "z")
    assert result["hop_count"] == 2


def test_node_metadata():
    engine = RoutingEngine()
    engine.add_node("meta-node", metadata={"region": "africa"})
    meta = engine.node_metadata("meta-node")
    assert meta["region"] == "africa"
