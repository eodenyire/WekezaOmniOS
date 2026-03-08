"""
WekezaOmniOS Cluster Manager
Phase 2: Manages node registration, health, and availability.
"""
import json
import os

class ClusterManager:
    def __init__(self, registry_path="cluster/node_registry.json"):
        self.registry_path = registry_path
        self.nodes = self._load_registry()

    def _load_registry(self):
        """Loads nodes from the persistent JSON store."""
        if os.path.exists(self.registry_path):
            try:
                with open(self.registry_path, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {"nodes": []}
        return {"nodes": []}

    def register_node(self, node_id, address, role="worker"):
        """Adds a new teleportation node and persists it."""
        new_node = {
            "id": node_id,
            "address": address,
            "role": role,
            "status": "ONLINE"
        }
        # Check for duplicates
        self.nodes["nodes"] = [n for n in self.nodes["nodes"] if n["id"] != node_id]
        self.nodes["nodes"].append(new_node)
        self._save_registry()
        print(f"[Cluster] Node '{node_id}' registered successfully at {address}.")

    def get_node(self, node_id):
        """Retrieves a specific node by its ID."""
        for node in self.nodes["nodes"]:
            if node["id"] == node_id:
                return node
        return None

    def list_available_nodes(self):
        """Returns all nodes currently marked as ONLINE."""
        return [n for n in self.nodes["nodes"] if n["status"] == "ONLINE"]

    def _save_registry(self):
        """Persists the cluster state to disk."""
        os.makedirs(os.path.dirname(self.registry_path), exist_ok=True)
        with open(self.registry_path, "w") as f:
            json.dump(self.nodes, f, indent=4)

if __name__ == "__main__":
    # Integration Test
    cm = ClusterManager()
    cm.register_node("nairobi-alpha-01", "192.168.1.50")
    print(f"Available Nodes: {cm.list_available_nodes()}")
