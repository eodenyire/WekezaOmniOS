"""
WekezaOmniOS Docker Adapter Tests
Phase 3: Validates DockerAdapter interface methods.
"""
import pytest
from unittest.mock import patch, MagicMock
from runtime_adapters.docker_adapter import DockerAdapter


def test_docker_adapter_instantiation():
    """DockerAdapter can be instantiated without errors."""
    adapter = DockerAdapter()
    assert adapter is not None


@patch("runtime_adapters.docker_adapter.subprocess.run")
def test_list_containers_returns_list(mock_run):
    """list_containers returns a list of container IDs."""
    mock_run.return_value = MagicMock(stdout="abc123\ndef456\n", returncode=0)
    adapter = DockerAdapter()
    containers = adapter.list_containers()
    assert isinstance(containers, list)
    assert "abc123" in containers


@patch("runtime_adapters.docker_adapter.subprocess.run")
def test_list_containers_empty_daemon(mock_run):
    """list_containers handles an empty Docker daemon gracefully."""
    mock_run.return_value = MagicMock(stdout="", returncode=0)
    adapter = DockerAdapter()
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


@patch("runtime_adapters.docker_adapter.subprocess.run")
def test_inspect_container_returns_string(mock_run):
    """inspect_container returns JSON string output."""
    mock_run.return_value = MagicMock(stdout='[{"Id": "abc123"}]', returncode=0)
    adapter = DockerAdapter()
    result = adapter.inspect_container("abc123")
    assert isinstance(result, str)
    assert "abc123" in result
def test_container_adapter_detect_runtime_valid_value():
    adapter = container_adapter_module.ContainerAdapter()
    runtime = adapter.detect_runtime()
    assert runtime in (None, "docker", "containerd")
