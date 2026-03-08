# Phase 2: Cluster node manager for teleportation
class ClusterManager:
    def __init__(self):
        self.nodes = []

    def register_node(self, node_id, address):
        self.nodes.append({"id": node_id, "address": address})

    def get_node(self, node_id):
        for node in self.nodes:
            if node["id"] == node_id:
                return node
        return None
