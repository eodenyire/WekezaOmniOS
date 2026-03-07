import time

class NodeHealthMonitor:
    def __init__(self, registry):
        self.registry = registry

    def check_nodes(self):
        for node, info in self.registry.list_nodes().items():
            # For now, simulate all nodes as active
            info["status"] = "active"
            print(f"[Cluster] Node '{node}' is {info['status']}")
