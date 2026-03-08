"""
WekezaOmniOS Phase 7 Tests — Cross-OS Runtime Dispatcher
"""
import pytest
from runtime_adapters.runtime_dispatcher import RuntimeDispatcher


def test_dispatcher_instantiation():
    dispatcher = RuntimeDispatcher()
    assert dispatcher is not None


def test_supported_os_list():
    dispatcher = RuntimeDispatcher()
    supported = dispatcher.supported_os_list()
    assert "linux" in supported
    assert "windows" in supported
    assert "android" in supported


def test_get_adapter_linux():
    dispatcher = RuntimeDispatcher()
    adapter = dispatcher.get_adapter("linux")
    assert adapter is not None


def test_get_adapter_windows():
    dispatcher = RuntimeDispatcher()
    adapter = dispatcher.get_adapter("windows")
    assert adapter is not None


def test_get_adapter_unsupported_raises():
    dispatcher = RuntimeDispatcher()
    with pytest.raises(ValueError, match="Unsupported OS"):
        dispatcher.get_adapter("beos")


def test_dispatch_linux_to_linux():
    dispatcher = RuntimeDispatcher()
    snapshot = {"pid": 123, "env_vars": {"HOME": "/home/user"}, "target_os": "linux"}
    result = dispatcher.dispatch(snapshot, "linux", "linux")
    assert result["target_os"] == "linux"


def test_dispatch_linux_to_windows():
    dispatcher = RuntimeDispatcher()
    snapshot = {"pid": 456, "env_vars": {"HOME": "/home/user"}, "paths": ["/usr/bin"]}
    result = dispatcher.dispatch(snapshot, "linux", "windows")
    assert result["target_os"] == "windows"
    assert result["path_format"] == "NTFS"


def test_dispatch_linux_to_android():
    dispatcher = RuntimeDispatcher()
    snapshot = {"pid": 789, "env_vars": {"APP": "demo"}}
    result = dispatcher.dispatch(snapshot, "linux", "android")
    assert result["target_os"] == "android"
