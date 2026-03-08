"""
WekezaOmniOS Cross-Cluster Router
Phase 10: Routes teleportation traffic between federation clusters
          using a distributed hash table (DHT)-inspired consistent hashing
          algorithm to achieve predictable, balanced load distribution.
"""
import hashlib
from typing import Dict, List, Optional


class CrossClusterRouter:
    """
    Consistent-hash ring router for multi-cluster teleportation.

    Each cluster is placed at one or more points on a virtual ring
    of size 2^32. A snapshot is routed to the cluster whose ring
    position is the smallest value >= hash(snapshot_id).
    """

    RING_SIZE = 2 ** 32
    DEFAULT_REPLICAS = 3  # Virtual nodes per cluster for balance

    def __init__(self, replicas: int = DEFAULT_REPLICAS):
        self.replicas = replicas
        self._ring: Dict[int, str] = {}   # ring_position -> cluster_id
        self._clusters: Dict[str, dict] = {}  # cluster_id -> metadata
        self._sorted_keys: List[int] = []

    # ------------------------------------------------------------------
    # Cluster management
    # ------------------------------------------------------------------

    def add_cluster(self, cluster_id: str, metadata: Optional[dict] = None) -> None:
        """
        Add a cluster to the consistent hash ring.

        Args:
            cluster_id: Unique cluster identifier.
            metadata: Optional dict with cluster details.
        """
        self._clusters[cluster_id] = metadata or {"cluster_id": cluster_id}
        for i in range(self.replicas):
            key = self._hash(f"{cluster_id}#{i}")
            self._ring[key] = cluster_id
        self._sorted_keys = sorted(self._ring.keys())
        print(f"[CrossClusterRouter] Added cluster '{cluster_id}' with {self.replicas} virtual nodes.")

    def remove_cluster(self, cluster_id: str) -> None:
        """Remove a cluster from the ring."""
        for i in range(self.replicas):
            key = self._hash(f"{cluster_id}#{i}")
            self._ring.pop(key, None)
        self._clusters.pop(cluster_id, None)
        self._sorted_keys = sorted(self._ring.keys())
        print(f"[CrossClusterRouter] Removed cluster '{cluster_id}' from ring.")

    # ------------------------------------------------------------------
    # Routing
    # ------------------------------------------------------------------

    def route(self, snapshot_id: str) -> Optional[dict]:
        """
        Route a snapshot to the responsible cluster.

        Args:
            snapshot_id: Unique identifier for the snapshot.

        Returns:
            Cluster metadata dict, or None if no clusters registered.
        """
        if not self._sorted_keys:
            print("[CrossClusterRouter] ⚠️  No clusters registered.")
            return None

        h = self._hash(snapshot_id)
        # Find the first ring position >= h (wrap around if needed)
        target_key = None
        for key in self._sorted_keys:
            if key >= h:
                target_key = key
                break
        if target_key is None:
            target_key = self._sorted_keys[0]  # Wrap-around

        cluster_id = self._ring[target_key]
        cluster = self._clusters[cluster_id]
        print(f"[CrossClusterRouter] Routed snapshot '{snapshot_id}' -> cluster '{cluster_id}'")
        return cluster

    def list_clusters(self) -> List[dict]:
        """Return all clusters registered in the router."""
        return list(self._clusters.values())

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _hash(key: str) -> int:
        """Compute a consistent 32-bit hash for a string key."""
        digest = hashlib.md5(key.encode()).hexdigest()
        return int(digest[:8], 16)
