"""Node controller for Phase 2 cluster endpoints."""

import importlib.util
import os


def _load_module(name, path):
	spec = importlib.util.spec_from_file_location(name, path)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
node_manager_module = _load_module("node_manager", os.path.join(BASE_DIR, "cluster", "node_manager.py"))
NodeManager = node_manager_module.NodeManager


class NodeController:
	def __init__(self):
		self.manager = NodeManager(registry_path=os.path.join(BASE_DIR, "cluster", "node_registry.json"))

	def register(self, node_id, address, role="worker", port=8000):
		return self.manager.add_node(node_id=node_id, address=address, role=role, port=port)

	def list_nodes(self, only_online=False):
		return self.manager.list_nodes(only_online=only_online)

	def get_node(self, node_id):
		return self.manager.get_node(node_id)

	def health(self, node_id):
		return self.manager.check_reachability(node_id)

	def health_all(self):
		nodes = self.manager.list_nodes()
		result = {}
		for node in nodes:
			nid = node.get("id")
			result[nid] = self.manager.check_reachability(nid)
		return result

