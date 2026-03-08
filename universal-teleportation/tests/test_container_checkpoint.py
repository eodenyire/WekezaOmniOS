import os
import importlib.util


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


container_checkpoint_module = load_module(
    "container_checkpoint", os.path.join(BASE_DIR, "runtime-adapters", "container_checkpoint.py")
)


def test_checkpoint_returns_contract_without_crash():
    ok, checkpoint_name, message = container_checkpoint_module.checkpoint_container("example")
    assert isinstance(ok, bool)
    assert checkpoint_name == "uat-checkpoint"
    assert isinstance(message, str)
