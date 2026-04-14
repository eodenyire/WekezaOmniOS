"""
Node pool — manages the registry of all compute nodes available in the cloud
desktop cluster.  Supports add / remove / list / lookup by type or status.
"""

import json
import os
from typing import Optional

from .linux_node import LinuxNode
from .windows_node import WindowsNode
from .android_emulator_node import AndroidEmulatorNode
from .node_base import NodeBase

_NODE_CONSTRUCTORS = {
    "linux": LinuxNode,
    "windows": WindowsNode,
    "android-emulator": AndroidEmulatorNode,
}


class NodePool:
    """Registry and lifecycle manager for all compute nodes."""

    def __init__(self, registry_path: Optional[str] = None):
        self.nodes: dict[str, NodeBase] = {}
        self.registry_path = registry_path or os.path.join(
            os.path.dirname(__file__), "node_pool_registry.json"
        )
        self._load()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _load(self) -> None:
        if not os.path.exists(self.registry_path):
            return
        try:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                records = json.load(f)
            for r in records:
                node_type = r.get("node_type", "linux")
                cls = _NODE_CONSTRUCTORS.get(node_type, LinuxNode)
                node = cls(
                    node_id=r["node_id"],
                    address=r["address"],
                    cpu_cores=r.get("cpu_cores", 4),
                    ram_gb=r.get("ram_gb", 8),
                )
                node.status = r.get("status", "idle")
                self.nodes[node.node_id] = node
        except (json.JSONDecodeError, KeyError):
            pass

    def _save(self) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(self.registry_path)), exist_ok=True)
        records = [n.to_dict() for n in self.nodes.values()]
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def add_node(self, node_id: str, node_type: str, address: str,
                 cpu_cores: int = 4, ram_gb: int = 8) -> dict:
        cls = _NODE_CONSTRUCTORS.get(node_type)
        if cls is None:
            raise ValueError(f"Unknown node type: {node_type}. Supported: {list(_NODE_CONSTRUCTORS)}")
        node = cls(node_id=node_id, address=address, cpu_cores=cpu_cores, ram_gb=ram_gb)
        self.nodes[node_id] = node
        self._save()
        return node.to_dict()

    def remove_node(self, node_id: str) -> bool:
        if node_id not in self.nodes:
            return False
        del self.nodes[node_id]
        self._save()
        return True

    def get_node(self, node_id: str) -> Optional[NodeBase]:
        return self.nodes.get(node_id)

    def list_nodes(self, node_type: Optional[str] = None, status: Optional[str] = None) -> list:
        nodes = list(self.nodes.values())
        if node_type:
            nodes = [n for n in nodes if n.NODE_TYPE == node_type]
        if status:
            nodes = [n for n in nodes if n.status == status]
        return [n.to_dict() for n in nodes]

    def pick_available(self, node_type: str) -> Optional[NodeBase]:
        """Return the first idle node of the requested type, or any active node with capacity."""
        candidates = [n for n in self.nodes.values() if n.NODE_TYPE == node_type]
        idle = [n for n in candidates if n.status == "idle"]
        if idle:
            return idle[0]
        # Fallback: return the node with the fewest active sessions
        if candidates:
            return min(candidates, key=lambda n: len(n.sessions))
        return None
