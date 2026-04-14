"""
WekezaOmniOS Cloud Desktop Model — Server Entry Point

Usage:
    python start_server.py

The API will be available at http://localhost:8080
Interactive docs at http://localhost:8080/docs
Dashboard UI  at http://localhost:8080/dashboard
"""

import importlib
import os
import sys
import types

# -----------------------------------------------------------------------
# Root of the cloud-desktop-model directory
# -----------------------------------------------------------------------
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)


def _import_hyphenated(module_name: str, dir_name: str):
    """Register a package that lives in a hyphenated directory under a
    Python-friendly alias so that normal `import module_name` works."""
    if module_name in sys.modules:
        return sys.modules[module_name]
    pkg_path = os.path.join(_ROOT, dir_name)
    init_path = os.path.join(pkg_path, "__init__.py")
    spec = importlib.util.spec_from_file_location(
        module_name,
        init_path,
        submodule_search_locations=[pkg_path],
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


for _alias, _dir in [
    ("compute_nodes",   "compute-nodes"),
    ("control_plane",   "control-plane"),
    ("storage_system",  "storage-system"),
    ("workspace_manager", "workspace-manager"),
    ("api_gateway",     "api-gateway"),
]:
    _import_hyphenated(_alias, _dir)

# -----------------------------------------------------------------------
# Launch the server
# -----------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("  WekezaOmniOS Cloud Desktop Model")
    print("  API Gateway  :  http://0.0.0.0:8080")
    print("  Swagger Docs :  http://localhost:8080/docs")
    print("  Dashboard    :  http://localhost:8080/dashboard")
    print("=" * 60)

    uvicorn.run(
        "api_gateway.server:app",
        host="0.0.0.0",
        port=8080,
        reload=False,
    )
