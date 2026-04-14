"""
WekezaOmniOS Cloud Desktop Model — API Gateway Server

Wires together all routes and initialises the shared ControlPlane,
WorkspaceManager, and OSLauncherController singletons.
"""

import os
import sys

# Allow imports from sibling packages (compute-nodes, control-plane, etc.)
_CLOUD_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CLOUD_DIR not in sys.path:
    sys.path.insert(0, _CLOUD_DIR)

# Patch package names that use hyphens
import importlib, types

def _import_hyphenated(module_name: str, dir_name: str):
    """Import a package that lives in a hyphenated directory."""
    pkg_path = os.path.join(_CLOUD_DIR, dir_name)
    spec = importlib.util.spec_from_file_location(
        module_name,
        os.path.join(pkg_path, "__init__.py"),
        submodule_search_locations=[pkg_path],
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod

for _alias, _dir in [
    ("compute_nodes", "compute-nodes"),
    ("control_plane", "control-plane"),
    ("storage_system", "storage-system"),
    ("workspace_manager", "workspace-manager"),
]:
    if _alias not in sys.modules:
        _import_hyphenated(_alias, _dir)

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .routes.auth_routes import router as auth_router
from .routes.os_launcher_routes import router as session_router, set_os_launcher
from .routes.workspace_routes import router as workspace_router, set_workspace_controller
from .routes.cluster_routes import router as cluster_router, set_control_plane

from control_plane.control_plane import ControlPlane
from workspace_manager.workspace_manager import WorkspaceManager
from .controllers.os_launcher_controller import OSLauncherController
from .controllers.workspace_controller import WorkspaceController

# ------------------------------------------------------------------
# Shared singletons
# ------------------------------------------------------------------

_cp = ControlPlane()
_cp.start_monitor()

_wm = WorkspaceManager(control_plane=_cp)
_launcher = OSLauncherController(control_plane=_cp)
_ws_ctrl = WorkspaceController(workspace_manager=_wm)

set_control_plane(_cp)
set_os_launcher(_launcher)
set_workspace_controller(_ws_ctrl)

# ------------------------------------------------------------------
# FastAPI application
# ------------------------------------------------------------------

app = FastAPI(
    title="WekezaOmniOS Cloud Desktop API",
    description=(
        "The programmatic control plane for the WekezaOmniOS Cloud Desktop Model. "
        "Provides auth, OS session launching, workspace management, and cluster orchestration."
    ),
    version="1.0.0",
    contact={"name": "Emmanuel Odenyire Anyira", "url": "https://github.com/eodenyire/WekezaOmniOS"},
)

app.include_router(auth_router)
app.include_router(session_router)
app.include_router(workspace_router)
app.include_router(cluster_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "service": "WekezaOmniOS Cloud Desktop API",
        "status": "active",
        "version": "1.0.0",
    }


@app.get("/status", tags=["Health"])
def status():
    usage = _cp.resource_usage()
    nodes = _cp.list_nodes()
    return {
        "status": "online",
        "active_sessions": usage.get("active_sessions", 0),
        "total_nodes": len(nodes),
        "resource_usage": usage,
    }


@app.get("/dashboard", response_class=HTMLResponse, tags=["Web Platform"],
         include_in_schema=False)
def dashboard():
    ui_path = os.path.join(os.path.dirname(__file__), "ui", "dashboard.html")
    try:
        with open(ui_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Dashboard UI not found</h1>"
