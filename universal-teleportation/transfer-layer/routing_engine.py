"""
WekezaOmniOS Planet-Scale Teleport Routing Engine
Phase 14: Routes teleportation traffic across globally distributed nodes
          using a combination of geographic proximity, latency, and
          distributed hash table (DHT) lookups.

The routing engine maintains a topology graph of nodes and computes
shortest paths using a simplified Dijkstra algorithm.
"""
from typing import Dict, List, Optional, Tuple
import heapq


class RoutingEngine:
    """
    Phase 14: Finds the optimal multi-hop route between two UAT nodes
              for planet-scale snapshot transfer.
    """

    def __init__(self):
        # Adjacency list: {node_id: [(neighbour_id, latency_ms), ...]}
        self._graph: Dict[str, List[Tuple[str, float]]] = {}
        self._node_metadata: Dict[str, dict] = {}

    # ------------------------------------------------------------------
    # Topology management
    # ------------------------------------------------------------------

    def add_node(self, node_id: str, metadata: Optional[dict] = None) -> None:
        """Register a node in the routing topology."""
        if node_id not in self._graph:
            self._graph[node_id] = []
        self._node_metadata[node_id] = metadata or {"node_id": node_id}
        print(f"[RoutingEngine] Node '{node_id}' added to topology.")

    def add_link(self, node_a: str, node_b: str, latency_ms: float) -> None:
        """
        Add a bidirectional link between two nodes.

        Args:
            node_a: Source node ID.
            node_b: Destination node ID.
            latency_ms: One-way network latency in milliseconds.
        """
        for n in (node_a, node_b):
            if n not in self._graph:
                self._graph[n] = []
                self._node_metadata[n] = {"node_id": n}
        self._graph[node_a].append((node_b, latency_ms))
        self._graph[node_b].append((node_a, latency_ms))
        print(f"[RoutingEngine] Link {node_a} <-> {node_b} ({latency_ms} ms)")

    # ------------------------------------------------------------------
    # Route selection
    # ------------------------------------------------------------------

    def select_route(self, source: str, target: str) -> dict:
        """
        Find the lowest-latency route from source to target.

        Uses Dijkstra's algorithm on the latency-weighted topology.

        Args:
            source: Source node ID.
            target: Target node ID.

        Returns:
            dict with 'path' (list of node IDs), 'total_latency_ms',
                  and 'hop_count'. Returns empty path if unreachable.
        """
        print(f"[RoutingEngine] Computing route: {source} -> {target}")

        if source not in self._graph or target not in self._graph:
            print(f"[RoutingEngine] ⚠️  One or both nodes not in topology.")
            return {"path": [], "total_latency_ms": float("inf"), "hop_count": 0}

        # Dijkstra
        dist = {n: float("inf") for n in self._graph}
        prev: Dict[str, Optional[str]] = {n: None for n in self._graph}
        dist[source] = 0.0
        pq = [(0.0, source)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in self._graph[u]:
                alt = dist[u] + w
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    heapq.heappush(pq, (alt, v))

        if dist[target] == float("inf"):
            print(f"[RoutingEngine] No path found from '{source}' to '{target}'")
            return {"path": [], "total_latency_ms": float("inf"), "hop_count": 0}

        # Reconstruct path
        path = []
        node = target
        while node is not None:
            path.append(node)
            node = prev[node]
        path.reverse()

        result = {
            "path": path,
            "total_latency_ms": round(dist[target], 2),
            "hop_count": len(path) - 1,
        }
        print(f"[RoutingEngine] Route: {' -> '.join(path)} ({result['total_latency_ms']} ms, {result['hop_count']} hops)")
        return result

    def list_nodes(self) -> List[str]:
        """Return all registered node IDs."""
        return list(self._graph.keys())

    def node_metadata(self, node_id: str) -> Optional[dict]:
        """Return metadata for a specific node."""
        return self._node_metadata.get(node_id)

