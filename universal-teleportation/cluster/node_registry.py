"""
WekezaOmniOS Node Registry
Maintains the inventory of valid teleportation targets.
"""

class NodeRegistry:
    def __init__(self):
        # Nodes stored as {node_id: metadata_dict}
        self.nodes = {}

    def add_node(self, name, ip="127.0.0.1", status="active"):
        node_id = f"node_{name.lower().replace(' ', '_')}"
        self.nodes[node_id] = {
            "name": name,
            "ip": ip,
            "status": status,
            "architecture": "x86_64"  # Default for Phase 1
        }
        print(f"[Cluster] Node '{name}' registered successfully with ID: {node_id}")

    def remove_node(self, node_id):
        if node_id in self.nodes:
            del self.nodes[node_id]
            print(f"[Cluster] Node ID '{node_id}' removed from registry.")

    def list_nodes(self):
        """Returns the current fleet of nodes."""
        return self.nodes



class NodeRegistry:
    """
    Keeps track of all nodes capable of receiving teleported workloads.
    """

    def __init__(self):
        self.nodes = {}

    def register_node(self, node_id, address, role="worker"):
        self.nodes[node_id] = {
            "address": address,
            "role": role,
        }

    def get_node(self, node_id):
        return self.nodes.get(node_id)

    def list_nodes(self):
        return self.nodes
