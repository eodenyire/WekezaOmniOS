"""
WekezaOmniOS Cluster Tests
Phase 2: Validates cluster node registry and manager functionality.
"""
import pytest
import json
import os
import tempfile
from cluster.cluster_manager import ClusterManager
from cluster.node_registry import NodeRegistry
from cluster.scheduler import Scheduler


# ---------------------------------------------------------------------------
# NodeRegistry tests
# ---------------------------------------------------------------------------

def test_node_registry_register_and_get():
    """NodeRegistry stores and retrieves nodes correctly."""
    registry = NodeRegistry()
    registry.register_node("node-alpha", "192.168.1.100", role="worker")
    node = registry.get_node("node-alpha")
    assert node is not None
    assert node["address"] == "192.168.1.100"
    assert node["role"] == "worker"


def test_node_registry_list_nodes():
    """NodeRegistry.list_nodes() returns all registered nodes."""
    registry = NodeRegistry()
    registry.register_node("n1", "10.0.0.1")
    registry.register_node("n2", "10.0.0.2")
    nodes = registry.list_nodes()
    assert "n1" in nodes
    assert "n2" in nodes


def test_node_registry_missing_node_returns_none():
    """Requesting an unknown node returns None."""
    registry = NodeRegistry()
    assert registry.get_node("nonexistent") is None


# ---------------------------------------------------------------------------
# ClusterManager tests
# ---------------------------------------------------------------------------

def test_cluster_manager_register_and_list(tmp_path):
    """ClusterManager registers a node and lists it as available."""
    registry_file = str(tmp_path / "node_registry.json")
    cm = ClusterManager(registry_path=registry_file)
    cm.register_node("nairobi-01", "192.168.1.50", role="worker")
    available = cm.list_available_nodes()
    ids = [n["id"] for n in available]
    assert "nairobi-01" in ids


def test_cluster_manager_persists_registry(tmp_path):
    """ClusterManager writes the registry to disk."""
    registry_file = str(tmp_path / "registry.json")
    cm = ClusterManager(registry_path=registry_file)
    cm.register_node("node-beta", "10.0.0.5")
    assert os.path.exists(registry_file)
    with open(registry_file) as f:
        data = json.load(f)
    ids = [n["id"] for n in data["nodes"]]
    assert "node-beta" in ids


def test_cluster_manager_get_node(tmp_path):
    """ClusterManager.get_node() returns the correct node dict."""
    registry_file = str(tmp_path / "registry.json")
    cm = ClusterManager(registry_path=registry_file)
    cm.register_node("my-node", "172.16.0.1")
    node = cm.get_node("my-node")
    assert node is not None
    assert node["address"] == "172.16.0.1"


def test_cluster_manager_no_duplicate_nodes(tmp_path):
    """Re-registering a node updates it rather than creating a duplicate."""
    registry_file = str(tmp_path / "registry.json")
    cm = ClusterManager(registry_path=registry_file)
    cm.register_node("dup-node", "1.2.3.4")
    cm.register_node("dup-node", "5.6.7.8")  # update address
    available = cm.list_available_nodes()
    dup_nodes = [n for n in available if n["id"] == "dup-node"]
    assert len(dup_nodes) == 1
    assert dup_nodes[0]["address"] == "5.6.7.8"


# ---------------------------------------------------------------------------
# Scheduler tests
# ---------------------------------------------------------------------------

def test_scheduler_chooses_a_node():
    """Scheduler.choose_target returns one of the available nodes."""
    scheduler = Scheduler()
    nodes = {
        "node-1": {"address": "10.0.0.1", "role": "worker"},
        "node-2": {"address": "10.0.0.2", "role": "cloud"},
    }
    target = scheduler.choose_target(nodes)
    assert target is not None
    assert "address" in target


def test_scheduler_empty_nodes_returns_none():
    """Scheduler.choose_target returns None for an empty node dict."""
    scheduler = Scheduler()
    target = scheduler.choose_target({})
    assert target is None
