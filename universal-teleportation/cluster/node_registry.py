"""
WekezaOmniOS Node Registry
Maintains the inventory of valid teleportation targets.
"""


class NodeRegistry:
    """
    Keeps track of all nodes capable of receiving teleported workloads.
    Supports both named registration (Phase 1) and address-based registration (Phase 2+).
    """

    def __init__(self):
        self.nodes = {}

    def add_node(self, name, ip="127.0.0.1", status="active"):
        """Register a node by name (Phase 1 compatibility)."""
        node_id = f"node_{name.lower().replace(' ', '_')}"
        self.nodes[node_id] = {
            "name": name,
            "ip": ip,
            "address": ip,
            "status": status,
            "role": "worker",
            "architecture": "x86_64",
        }
        print(f"[Cluster] Node '{name}' registered successfully with ID: {node_id}")
        return node_id

    def register_node(self, node_id, address, role="worker"):
        """Register a node by explicit ID and address (Phase 2+)."""
        self.nodes[node_id] = {
            "name": node_id,
            "ip": address,
            "address": address,
            "role": role,
            "status": "active",
        }

    def remove_node(self, node_id):
        """Remove a node from the registry."""
        if node_id in self.nodes:
            del self.nodes[node_id]
            print(f"[Cluster] Node ID '{node_id}' removed from registry.")

    def get_node(self, node_id):
        """Retrieve a specific node by its ID."""
        return self.nodes.get(node_id)

    def list_nodes(self):
        """Returns the current fleet of nodes."""
        return self.nodes
