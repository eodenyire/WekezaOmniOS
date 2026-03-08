"""Node registry for cluster teleportation."""

import json
import os


class NodeRegistry:
    """
    In-memory node registry with optional file-backed persistence.

    When ``registry_path`` is provided the registry is loaded from that JSON
    file on startup and persisted after every mutation, enabling multiple
    ``NodeManager`` / ``NodeController`` instances to share the same node
    catalogue through the file-system.
    """

    def __init__(self, registry_path=None):
        self.registry_path = registry_path
        self.nodes = {}
        if registry_path:
            self._load_from_file()

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------

    def _load_from_file(self):
        if not self.registry_path or not os.path.exists(self.registry_path):
            return
        try:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for node in data.get("nodes", []):
                nid = node.get("id")
                if nid:
                    self.nodes[nid] = node
        except (json.JSONDecodeError, OSError):
            pass

    def _save_to_file(self):
        if not self.registry_path:
            return
        os.makedirs(os.path.dirname(self.registry_path), exist_ok=True)
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump({"nodes": list(self.nodes.values())}, f, indent=4)

    # ------------------------------------------------------------------
    # Core API
    # ------------------------------------------------------------------

    def register_node(self, node_id, address, role="worker", port=8000, metadata=None):
        """Register or update a node by ID."""
        self.nodes[node_id] = {
            "id": node_id,
            "name": node_id,
            "address": address,
            "ip": address,
            "role": role,
            "port": port,
            "status": "active",
            "metadata": metadata or {},
        }
        print(f"[NodeRegistry] Node '{node_id}' registered at {address}.")
        self._save_to_file()
        return self.nodes[node_id]

    def add_node(self, name, ip="127.0.0.1", status="active"):
        """Register a node by name (Phase 1 compatibility)."""
        node_id = f"node_{name.lower().replace(' ', '_')}"
        return self.register_node(node_id, ip, role="worker")

    def remove_node(self, node_id):
        """Remove a node from the registry."""
        if node_id in self.nodes:
            del self.nodes[node_id]
            print(f"[NodeRegistry] Node '{node_id}' removed.")
            self._save_to_file()
            return True
        return False

    def get_node(self, node_id):
        """Retrieve a specific node by ID."""
        if self.registry_path:
            self._load_from_file()
        return self.nodes.get(node_id)

    def set_node_status(self, node_id, status):
        """Update the status of a registered node."""
        node = self.nodes.get(node_id)
        if node:
            node["status"] = status
            self._save_to_file()
            return node
        return None

    def list_nodes(self, only_online=False):
        """
        Return the node registry dict.

        Use ``node_id in registry.list_nodes()`` to check membership.
        When ``only_online=True`` only nodes with active/ONLINE status are returned.
        """
        if self.registry_path:
            self._load_from_file()
        if only_online:
            return {k: v for k, v in self.nodes.items()
                    if v.get("status") in ("active", "ONLINE")}
        return self.nodes

