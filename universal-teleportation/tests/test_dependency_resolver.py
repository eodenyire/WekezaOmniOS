"""
WekezaOmniOS Dependency Resolver Tests
Phase 3: Validates runtime dependency resolution and OS compatibility checks.
"""
import pytest
from runtime_adapters.dependency_resolver import DependencyResolver


def test_resolver_instantiation():
    """DependencyResolver can be instantiated."""
    resolver = DependencyResolver()
    assert resolver is not None


def test_resolve_basic_metadata():
    """resolve() returns a dict with the expected keys."""
    resolver = DependencyResolver()
    metadata = {
        "target_os": "linux",
        "runtime": "python3",
        "dependencies": ["psutil", "fastapi"],
        "env_vars": {"PORT": "8000"},
    }
    result = resolver.resolve(metadata)
    assert result["target_os"] == "linux"
    assert result["runtime"] == "python3"
    assert "psutil" in result["libraries"]
    assert result["environment"]["PORT"] == "8000"


def test_resolve_defaults_for_missing_keys():
    """resolve() applies sensible defaults when optional keys are absent."""
    resolver = DependencyResolver()
    result = resolver.resolve({})
    assert result["target_os"] == "linux"
    assert result["runtime"] == "python3"
    assert result["libraries"] == []


def test_compatibility_linux_to_linux():
    """Linux -> Linux is compatible."""
    resolver = DependencyResolver()
    assert resolver.check_compatibility("linux", "linux") is True


def test_compatibility_linux_to_windows():
    """Linux -> Windows is NOT compatible (requires runtime adapter)."""
    resolver = DependencyResolver()
    assert resolver.check_compatibility("linux", "windows") is False


def test_compatibility_linux_to_android():
    """Linux -> Android is compatible."""
    resolver = DependencyResolver()
    assert resolver.check_compatibility("linux", "android") is True
