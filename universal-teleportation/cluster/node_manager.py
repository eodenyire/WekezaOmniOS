"""
WekezaOmniOS Node Manager
Delegates node operations to the NodeRegistry.
"""
from .node_registry import NodeRegistry


class NodeManager:

    def __init__(self):
        self.registry = NodeRegistry()

    def add_node(self, node_id, address):
        self.registry.register_node(node_id, address)

    def get_node(self, node_id):
        return self.registry.get_node(node_id)

    def list_nodes(self):
        return self.registry.list_nodes()
