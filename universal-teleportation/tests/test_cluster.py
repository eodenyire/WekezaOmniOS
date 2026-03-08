import os
import sys
import importlib.util


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLUSTER_DIR = os.path.join(BASE_DIR, "cluster")
if CLUSTER_DIR not in sys.path:
	sys.path.insert(0, CLUSTER_DIR)


def load_module(name, path):
	spec = importlib.util.spec_from_file_location(name, path)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


node_manager_module = load_module("node_manager", os.path.join(CLUSTER_DIR, "node_manager.py"))
scheduler_module = load_module("scheduler", os.path.join(CLUSTER_DIR, "scheduler.py"))


def test_node_registration_and_lookup(tmp_path):
	NodeManager = node_manager_module.NodeManager
	manager = NodeManager(registry_path=str(tmp_path / "node_registry.json"))

	node = manager.add_node("node-a", "127.0.0.1", role="worker", port=8080)
	assert node["id"] == "node-a"
	found = manager.get_node("node-a")
	assert found is not None
	assert found["address"] == "127.0.0.1"


def test_scheduler_picks_online_node():
	Scheduler = scheduler_module.Scheduler
	scheduler = Scheduler()
	nodes = [
		{"id": "n1", "status": "OFFLINE", "metadata": {"load": 0.1}},
		{"id": "n2", "status": "ONLINE", "metadata": {"load": 0.8}},
		{"id": "n3", "status": "ONLINE", "metadata": {"load": 0.2}},
	]
	target = scheduler.choose_target(nodes)
	assert target is not None
	assert target["id"] == "n3"


def test_reachability_localhost(tmp_path):
	NodeManager = node_manager_module.NodeManager
	manager = NodeManager(registry_path=str(tmp_path / "node_registry.json"))
	manager.add_node("local", "127.0.0.1", role="controller")
	assert manager.check_reachability("local") is True

