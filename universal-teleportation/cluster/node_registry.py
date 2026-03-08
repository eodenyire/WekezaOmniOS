"""Node registry for Phase 2 cluster teleportation."""


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
import json
import os
from datetime import datetime, timezone


class NodeRegistry:
    """Persistent node registry with basic lifecycle operations."""

    def __init__(self, registry_path="cluster/node_registry.json"):
        self.registry_path = registry_path
        self.nodes = self._load_nodes()

    def _load_nodes(self):
        if os.path.exists(self.registry_path):
            try:
                with open(self.registry_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data.get("nodes", [])
            except (json.JSONDecodeError, OSError):
                return []
        return []

    def _save_nodes(self):
        os.makedirs(os.path.dirname(self.registry_path), exist_ok=True)
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump({"nodes": self.nodes}, f, indent=4)

    def register_node(self, node_id, address, role="worker", port=8000, metadata=None):
        existing = self.get_node(node_id)
        payload = {
            "id": node_id,
            "address": address,
            "role": role,
            "port": port,
            "status": "ONLINE",
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
        }
        if existing:
            existing.update(payload)
        else:
            payload["created_at"] = datetime.now(timezone.utc).isoformat()
            self.nodes.append(payload)
        self._save_nodes()
        return payload

    def set_node_status(self, node_id, status):
        node = self.get_node(node_id)
        if not node:
            return None
        node["status"] = status
        node["updated_at"] = datetime.now(timezone.utc).isoformat()
        self._save_nodes()
        return node

    def remove_node(self, node_id):
        before = len(self.nodes)
        self.nodes = [n for n in self.nodes if n["id"] != node_id]
        changed = len(self.nodes) != before
        if changed:
            self._save_nodes()
        return changed

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
        for node in self.nodes:
            if node["id"] == node_id:
                return node
        return None

    def list_nodes(self, only_online=False):
        if not only_online:
            return self.nodes
        return [n for n in self.nodes if n.get("status") == "ONLINE"]
