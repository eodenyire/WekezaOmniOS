"""
WekezaOmniOS Optimal Node Selector
Phase 9: Selects the best available cluster node for a teleportation
         workload using a scoring heuristic.

Scoring factors:
  - Available memory
  - Available CPU
  - Network latency to source
  - Current load (teleportation queue depth)
"""
from typing import List, Dict, Optional


class OptimalNodeSelector:
    """
    Evaluates candidate nodes and returns the best one for a given workload.

    Each candidate node dict should have the keys:
      - node_id (str)
      - available_memory_mb (float)
      - available_cpu_cores (int)
      - latency_ms (float)      — network latency from source
      - queue_depth (int)       — pending teleportation jobs
      - status (str)            — 'online', 'degraded', 'offline'
    """

    # Scoring weights (must sum to 1.0)
    WEIGHT_MEMORY = 0.30
    WEIGHT_CPU = 0.25
    WEIGHT_LATENCY = 0.25
    WEIGHT_QUEUE = 0.20

    def score_node(self, node: dict, required_memory_mb: float, required_cpu: int) -> float:
        """
        Compute a fitness score [0.0 – 1.0] for a candidate node.

        Higher is better.

        Args:
            node: Candidate node metadata dict.
            required_memory_mb: Memory needed by the workload.
            required_cpu: CPU cores needed by the workload.

        Returns:
            float score, or -1.0 if the node cannot satisfy requirements.
        """
        if node.get("status") != "online":
            return -1.0

        avail_mem = node.get("available_memory_mb", 0)
        avail_cpu = node.get("available_cpu_cores", 0)
        latency = node.get("latency_ms", 9999)
        queue = node.get("queue_depth", 0)

        # Hard constraints
        if avail_mem < required_memory_mb or avail_cpu < required_cpu:
            return -1.0

        # Normalised scores (higher = better)
        mem_score = min(1.0, avail_mem / max(required_memory_mb * 2, 1))
        cpu_score = min(1.0, avail_cpu / max(required_cpu * 2, 1))
        lat_score = max(0.0, 1.0 - latency / 1000)     # 0 ms → 1.0, 1000 ms → 0.0
        queue_score = max(0.0, 1.0 - queue / 10)         # 0 jobs → 1.0, 10+ → 0.0

        score = (
            self.WEIGHT_MEMORY * mem_score
            + self.WEIGHT_CPU * cpu_score
            + self.WEIGHT_LATENCY * lat_score
            + self.WEIGHT_QUEUE * queue_score
        )
        return round(score, 4)

    def select(
        self,
        candidates: List[Dict],
        required_memory_mb: float = 64.0,
        required_cpu: int = 1,
    ) -> Optional[Dict]:
        """
        Select the optimal node from a list of candidates.

        Args:
            candidates: List of node metadata dicts.
            required_memory_mb: Minimum memory the workload needs.
            required_cpu: Minimum CPU cores the workload needs.

        Returns:
            The best candidate dict, or None if no suitable node exists.
        """
        scored = []
        for node in candidates:
            s = self.score_node(node, required_memory_mb, required_cpu)
            if s >= 0:
                scored.append((s, node))

        if not scored:
            print("[OptimalNodeSelector] ⚠️  No eligible nodes found.")
            return None

        scored.sort(key=lambda x: x[0], reverse=True)
        best_score, best_node = scored[0]
        print(
            f"[OptimalNodeSelector] ✅ Selected node '{best_node.get('node_id')}' "
            f"(score: {best_score:.4f})"
        )
        return best_node

    def rank(
        self,
        candidates: List[Dict],
        required_memory_mb: float = 64.0,
        required_cpu: int = 1,
    ) -> List[Dict]:
        """
        Return all eligible nodes sorted best-first with scores attached.

        Args:
            candidates: List of node metadata dicts.
            required_memory_mb: Minimum memory.
            required_cpu: Minimum CPU cores.

        Returns:
            List of dicts with an added '__score' key, sorted descending.
        """
        ranked = []
        for node in candidates:
            s = self.score_node(node, required_memory_mb, required_cpu)
            if s >= 0:
                ranked.append({**node, "__score": s})
        ranked.sort(key=lambda x: x["__score"], reverse=True)
        return ranked
