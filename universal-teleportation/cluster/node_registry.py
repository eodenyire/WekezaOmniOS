"""Node registry for Phase 2 cluster teleportation."""

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

    def get_node(self, node_id):
        for node in self.nodes:
            if node["id"] == node_id:
                return node
        return None

    def list_nodes(self, only_online=False):
        if not only_online:
            return self.nodes
        return [n for n in self.nodes if n.get("status") == "ONLINE"]
