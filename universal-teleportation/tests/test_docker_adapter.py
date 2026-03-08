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
