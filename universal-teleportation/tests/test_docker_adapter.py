import os
import importlib.util


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


docker_adapter_module = load_module(
    "docker_adapter", os.path.join(BASE_DIR, "runtime-adapters", "docker_adapter.py")
)
container_adapter_module = load_module(
    "container_adapter", os.path.join(BASE_DIR, "runtime-adapters", "container_adapter.py")
)


def test_list_containers_returns_list():
    adapter = docker_adapter_module.DockerAdapter()
    containers = adapter.list_containers()
    assert isinstance(containers, list)


def test_container_adapter_detect_runtime_valid_value():
    adapter = container_adapter_module.ContainerAdapter()
    runtime = adapter.detect_runtime()
    assert runtime in (None, "docker", "containerd")
