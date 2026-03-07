"""
WekezaOmniOS Node Health Monitor
Simulates heartbeats and resource checks for cluster nodes.
"""

import time

class NodeHealthMonitor:
    def __init__(self, registry):
        self.registry = registry

    def perform_heartbeat(self):
        """Simulates a health check across the registry."""
        print("\n[Cluster] Initiating node health sweep...")
        for node_id, info in self.registry.list_nodes().items():
            # Phase 1 Mock: All local nodes are assumed healthy
            info["last_heartbeat"] = time.time()
            info["status"] = "active"
            print(f" -> Node: {info['name']} | Status: {info['status']} | Latency: 0.1ms")
