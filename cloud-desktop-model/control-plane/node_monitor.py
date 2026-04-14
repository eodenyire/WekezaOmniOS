"""
Node Monitor — periodically polls compute nodes for health and updates
their status in the NodePool registry.
"""

import datetime
import threading
import time
from typing import Optional


class NodeMonitor:
    """Background monitor that tracks the health of compute nodes."""

    def __init__(self, node_pool, poll_interval_seconds: int = 30):
        self.node_pool = node_pool
        self.poll_interval = poll_interval_seconds
        self._health_cache: dict[str, dict] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None

    # ------------------------------------------------------------------
    # Background polling
    # ------------------------------------------------------------------

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)

    def _poll_loop(self) -> None:
        while self._running:
            self._poll_all()
            time.sleep(self.poll_interval)

    def _poll_all(self) -> None:
        for node_id, node in list(self.node_pool.nodes.items()):
            self._health_cache[node_id] = self._probe(node)

    def _probe(self, node) -> dict:
        """
        In production this would open a TCP/HTTP connection to the node's health
        endpoint.  In this implementation we simulate the result using node state.
        """
        reachable = node.status in ("idle", "active")
        return {
            "node_id": node.node_id,
            "node_type": node.NODE_TYPE,
            "reachable": reachable,
            "status": node.status,
            "active_sessions": len(node.sessions),
            "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def health(self, node_id: str) -> Optional[dict]:
        node = self.node_pool.get_node(node_id)
        if node is None:
            return None
        result = self._probe(node)
        self._health_cache[node_id] = result
        return result

    def health_all(self) -> list:
        self._poll_all()
        return list(self._health_cache.values())
