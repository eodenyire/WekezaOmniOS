"""Node manager orchestration for Phase 2."""

import os
import sys
import socket

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from node_registry import NodeRegistry


class NodeManager:
    def __init__(self, registry_path="cluster/node_registry.json"):
        self.registry = NodeRegistry(registry_path=registry_path)

    def add_node(self, node_id, address, role="worker", port=8000, metadata=None):
        return self.registry.register_node(node_id, address, role=role, port=port, metadata=metadata)

    def remove_node(self, node_id):
        return self.registry.remove_node(node_id)

    def get_node(self, node_id):
        return self.registry.get_node(node_id)

    def list_nodes(self, only_online=False):
        return self.registry.list_nodes(only_online=only_online)

    def heartbeat(self, node_id):
        node = self.registry.get_node(node_id)
        if not node:
            return None
        return self.registry.set_node_status(node_id, "ONLINE")

    def check_reachability(self, node_id, timeout=0.5):
        node = self.registry.get_node(node_id)
        if not node:
            return False
        address = node.get("address")
        port = int(node.get("port", 8000))

        if address in ("127.0.0.1", "localhost", "::1"):
            self.registry.set_node_status(node_id, "ONLINE")
            return True

        try:
            with socket.create_connection((address, port), timeout=timeout):
                self.registry.set_node_status(node_id, "ONLINE")
                return True
        except OSError:
            self.registry.set_node_status(node_id, "OFFLINE")
            return False
