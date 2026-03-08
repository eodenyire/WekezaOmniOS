"""
WekezaOmniOS Federation Manager
Phase 10: Manages a federation of multiple independent UAT clusters,
          enabling cross-cluster workload teleportation.

A federation is a named group of clusters. Each cluster has its own
node registry and scheduler. The FederationManager routes teleportation
requests to the correct cluster based on policy rules.
"""
from typing import Dict, List, Optional
from datetime import datetime, timezone
import uuid


class FederationManager:
    """
    Top-level controller for a multi-cluster UAT federation.

    Clusters are registered by name and associated with a list of nodes
    and a contact endpoint (simulated here as a plain dict).
    """

    def __init__(self, federation_name: str = "global-uat-fabric"):
        self.federation_name = federation_name
        self._clusters: Dict[str, dict] = {}
        self._routing_table: Dict[str, str] = {}  # workload_tag -> cluster_id

    # ------------------------------------------------------------------
    # Cluster management
    # ------------------------------------------------------------------

    def register_cluster(
        self,
        cluster_id: str,
        endpoint: str,
        region: str = "global",
        nodes: Optional[List[dict]] = None,
    ) -> dict:
        """
        Register a remote cluster with the federation.

        Args:
            cluster_id: Unique identifier for the cluster.
            endpoint: API endpoint URL of the cluster control plane.
            region: Geographic region of the cluster.
            nodes: Optional list of initial node descriptors.

        Returns:
            dict with cluster metadata.
        """
        cluster = {
            "cluster_id": cluster_id,
            "endpoint": endpoint,
            "region": region,
            "nodes": nodes or [],
            "status": "active",
            "registered_at": datetime.now(timezone.utc).isoformat(),
        }
        self._clusters[cluster_id] = cluster
        print(f"[FederationManager] Registered cluster '{cluster_id}' @ {endpoint} ({region})")
        return cluster

    def deregister_cluster(self, cluster_id: str) -> bool:
        """Remove a cluster from the federation."""
        if cluster_id in self._clusters:
            del self._clusters[cluster_id]
            print(f"[FederationManager] Deregistered cluster '{cluster_id}'.")
            return True
        return False

    def get_cluster(self, cluster_id: str) -> Optional[dict]:
        """Retrieve cluster metadata by ID."""
        return self._clusters.get(cluster_id)

    def list_clusters(self) -> List[dict]:
        """Return all registered clusters."""
        return list(self._clusters.values())

    # ------------------------------------------------------------------
    # Routing
    # ------------------------------------------------------------------

    def add_routing_rule(self, workload_tag: str, cluster_id: str) -> None:
        """
        Associate a workload tag with a target cluster.

        Args:
            workload_tag: Label applied to workloads (e.g. 'banking-api', 'ml-batch').
            cluster_id: Target cluster for workloads with this tag.
        """
        self._routing_table[workload_tag] = cluster_id
        print(f"[FederationManager] Route: '{workload_tag}' -> cluster '{cluster_id}'")

    def resolve_cluster(self, workload_tag: str) -> Optional[dict]:
        """
        Resolve a workload tag to the appropriate cluster.

        Args:
            workload_tag: Tag attached to the teleportation request.

        Returns:
            Cluster metadata dict, or None if no rule matches.
        """
        cluster_id = self._routing_table.get(workload_tag)
        if cluster_id is None:
            # Fallback: return any active cluster
            for c in self._clusters.values():
                if c["status"] == "active":
                    print(f"[FederationManager] No route for '{workload_tag}' — using fallback cluster '{c['cluster_id']}'")
                    return c
            print(f"[FederationManager] ⚠️  No cluster available for '{workload_tag}'")
            return None
        cluster = self._clusters.get(cluster_id)
        print(f"[FederationManager] Resolved '{workload_tag}' -> cluster '{cluster_id}'")
        return cluster

    # ------------------------------------------------------------------
    # Teleportation
    # ------------------------------------------------------------------

    def teleport(self, workload_tag: str, snapshot_path: str) -> dict:
        """
        Initiate a cross-cluster teleportation.

        Args:
            workload_tag: Tag identifying the workload type.
            snapshot_path: Local path to the snapshot archive.

        Returns:
            dict with teleportation result.
        """
        cluster = self.resolve_cluster(workload_tag)
        if cluster is None:
            return {"status": "FAILED", "reason": "No eligible cluster found"}

        teleport_id = str(uuid.uuid4())
        print(
            f"[FederationManager] Teleporting '{workload_tag}' "
            f"to cluster '{cluster['cluster_id']}' (teleport_id={teleport_id})"
        )
        return {
            "teleport_id": teleport_id,
            "status": "INITIATED",
            "workload_tag": workload_tag,
            "target_cluster": cluster["cluster_id"],
            "target_endpoint": cluster["endpoint"],
            "snapshot_path": snapshot_path,
        }
