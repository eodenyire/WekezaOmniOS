"""
WekezaOmniOS Runtime Mapper Tests
Phase 3: Validates path and signal mapping across OS boundaries.
"""
import pytest
from runtime_adapters.runtime_mapper import RuntimeMapper


def test_mapper_instantiation():
    """RuntimeMapper can be created with source and target OS."""
    mapper = RuntimeMapper(source_os="linux", target_os="windows")
    assert mapper.source_os == "linux"
    assert mapper.target_os == "windows"


def test_map_paths_linux_to_windows():
    """POSIX paths are converted to Windows backslash format."""
    mapper = RuntimeMapper(source_os="linux", target_os="windows")
    result = mapper.map_paths(["/usr/bin/python", "/home/user/app"])
    assert result[0] == "\\usr\\bin\\python"
    assert result[1] == "\\home\\user\\app"


def test_map_paths_linux_to_linux():
    """Paths remain unchanged for Linux -> Linux."""
    mapper = RuntimeMapper(source_os="linux", target_os="linux")
    paths = ["/usr/bin/python", "/home/user/app"]
    assert mapper.map_paths(paths) == paths


def test_map_signal_linux_to_windows():
    """SIGTERM maps to CTRL_C_EVENT on Windows."""
    mapper = RuntimeMapper(source_os="linux", target_os="windows")
    assert mapper.map_signal("SIGTERM") == "CTRL_C_EVENT"


def test_map_signal_unknown_returns_original():
    """Unknown signals are returned unchanged."""
    mapper = RuntimeMapper(source_os="linux", target_os="android")
    assert mapper.map_signal("SIGUSR1") == "SIGUSR1"


def test_map_environment_windows():
    """Windows environment mapping sets OS to Windows_NT."""
    mapper = RuntimeMapper(source_os="linux", target_os="windows")
    env = {"PORT": "8080", "PATH": "/usr/bin"}
    result = mapper.map_environment(env)
    assert result["OS"] == "Windows_NT"


def test_map_environment_android():
    """Android environment mapping sets OS to Android."""
    mapper = RuntimeMapper(source_os="linux", target_os="android")
    env = {"PORT": "8080"}
    result = mapper.map_environment(env)
    assert result["OS"] == "Android"
