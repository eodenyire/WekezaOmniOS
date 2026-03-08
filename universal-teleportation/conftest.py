"""
WekezaOmniOS Test Configuration
Registers hyphenated package directories as importable Python modules.
"""
import sys
import os
import importlib.util

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)


def register_hyphenated_module(underscore_name, hyphen_name):
    """Register a directory with hyphens as a Python module using an underscore alias."""
    dir_path = os.path.join(BASE_DIR, hyphen_name)
    if not os.path.isdir(dir_path):
        return
    init_file = os.path.join(dir_path, "__init__.py")
    if not os.path.exists(init_file):
        return
    spec = importlib.util.spec_from_file_location(
        underscore_name,
        init_file,
        submodule_search_locations=[dir_path],
    )
    module = importlib.util.module_from_spec(spec)
    module.__path__ = [dir_path]
    module.__package__ = underscore_name
    sys.modules[underscore_name] = module
    spec.loader.exec_module(module)


# Register all hyphenated package directories
register_hyphenated_module("state_capture", "state-capture")
register_hyphenated_module("snapshot_engine", "snapshot-engine")
register_hyphenated_module("state_reconstruction", "state-reconstruction")
register_hyphenated_module("snapshot_storage", "snapshot-storage")
register_hyphenated_module("live_migration", "live-migration")
register_hyphenated_module("runtime_adapters", "runtime-adapters")
register_hyphenated_module("teleportation_api", "teleportation-api")
register_hyphenated_module("transfer_layer", "transfer-layer")
