"""
WekezaOmniOS Phase 10 Tests — Global Teleportation Fabric
"""
import pytest
from global_fabric.federation_manager import FederationManager
from global_fabric.cross_cluster_router import CrossClusterRouter


# ------ FederationManager ------

def test_federation_register_cluster():
    fm = FederationManager()
    cluster = fm.register_cluster("nairobi-1", "http://nairobi.uat.local", region="africa-east")
    assert cluster["cluster_id"] == "nairobi-1"
    assert cluster["status"] == "active"


def test_federation_list_clusters():
    fm = FederationManager()
    fm.register_cluster("c1", "http://c1.local")
    fm.register_cluster("c2", "http://c2.local")
    clusters = fm.list_clusters()
    assert len(clusters) == 2


def test_federation_deregister_cluster():
    fm = FederationManager()
    fm.register_cluster("temp", "http://temp.local")
    removed = fm.deregister_cluster("temp")
    assert removed is True
    assert fm.get_cluster("temp") is None


def test_federation_get_cluster():
    fm = FederationManager()
    fm.register_cluster("eu-1", "http://eu1.local", region="europe")
    c = fm.get_cluster("eu-1")
    assert c["region"] == "europe"


def test_federation_routing_rule():
    fm = FederationManager()
    fm.register_cluster("finance-cluster", "http://finance.local")
    fm.add_routing_rule("banking-api", "finance-cluster")
    resolved = fm.resolve_cluster("banking-api")
    assert resolved["cluster_id"] == "finance-cluster"


def test_federation_teleport():
    fm = FederationManager()
    fm.register_cluster("prod", "http://prod.local")
    fm.add_routing_rule("web-app", "prod")
    result = fm.teleport("web-app", "/snapshots/snap-001.tar.gz")
    assert result["status"] == "INITIATED"
    assert result["target_cluster"] == "prod"


def test_federation_fallback_no_rule():
    fm = FederationManager()
    fm.register_cluster("default-cluster", "http://default.local")
    # No routing rule — should use fallback
    resolved = fm.resolve_cluster("unknown-tag")
    assert resolved is not None


# ------ CrossClusterRouter ------

def test_router_add_cluster():
    router = CrossClusterRouter()
    router.add_cluster("cluster-a")
    assert "cluster-a" in router.list_clusters()[0]["cluster_id"]


def test_router_route_snapshot():
    router = CrossClusterRouter()
    router.add_cluster("cluster-a")
    router.add_cluster("cluster-b")
    result = router.route("snap-12345")
    assert result is not None
    assert "cluster_id" in result


def test_router_remove_cluster():
    router = CrossClusterRouter()
    router.add_cluster("temp-cluster")
    router.remove_cluster("temp-cluster")
    assert len(router.list_clusters()) == 0


def test_router_empty_returns_none():
    router = CrossClusterRouter()
    result = router.route("any-snap")
    assert result is None


def test_router_deterministic_routing():
    """Same snapshot_id should always route to the same cluster."""
    router = CrossClusterRouter()
    for i in range(5):
        router.add_cluster(f"cluster-{i}")
    c1 = router.route("snap-deterministic-abc")["cluster_id"]
    c2 = router.route("snap-deterministic-abc")["cluster_id"]
    assert c1 == c2
