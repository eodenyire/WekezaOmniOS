"""
Workspace routes — create, list, get, delete, clone, snapshot workspaces.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from ..schemas.models import (
    CloneWorkspaceRequest,
    CreateWorkspaceRequest,
    SnapshotWorkspaceRequest,
    WorkspaceResponse,
)
from ..middleware.auth_middleware import get_current_user_id

router = APIRouter(prefix="/workspaces", tags=["Workspaces"])

_workspace_ctrl = None


def set_workspace_controller(ctrl) -> None:
    global _workspace_ctrl
    _workspace_ctrl = ctrl


def _ctrl():
    if _workspace_ctrl is None:
        raise HTTPException(status_code=503, detail="Workspace controller not initialised")
    return _workspace_ctrl


@router.post("", response_model=WorkspaceResponse, status_code=201)
def create_workspace(request: CreateWorkspaceRequest,
                     _uid: str = Depends(get_current_user_id)):
    """Create and start a new developer workspace."""
    try:
        ws = _ctrl().create(
            user_id=request.user_id,
            name=request.name,
            os_profile=request.os_profile,
            cpu_cores=request.cpu_cores,
            ram_gb=request.ram_gb,
        )
        return ws
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.get("", summary="List workspaces")
def list_workspaces(user_id: Optional[str] = None,
                    _uid: str = Depends(get_current_user_id)):
    workspaces = _ctrl().list_all(user_id=user_id)
    return {"status": "ok", "count": len(workspaces), "workspaces": workspaces}


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
def get_workspace(workspace_id: str, _uid: str = Depends(get_current_user_id)):
    ws = _ctrl().get(workspace_id)
    if ws is None:
        raise HTTPException(status_code=404, detail=f"Workspace not found: {workspace_id}")
    return ws


@router.delete("/{workspace_id}", summary="Delete a workspace")
def delete_workspace(workspace_id: str, _uid: str = Depends(get_current_user_id)):
    result = _ctrl().delete(workspace_id)
    return result


@router.post("/{workspace_id}/stop", summary="Stop a running workspace")
def stop_workspace(workspace_id: str, _uid: str = Depends(get_current_user_id)):
    result = _ctrl().stop(workspace_id)
    return result


@router.post("/clone", response_model=WorkspaceResponse)
def clone_workspace(request: CloneWorkspaceRequest,
                    _uid: str = Depends(get_current_user_id)):
    """Fork an existing workspace."""
    try:
        ws = _ctrl().clone(
            source_id=request.source_workspace_id,
            new_name=request.new_name,
            new_user_id=request.new_user_id,
        )
        return ws
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/snapshot", summary="Snapshot a workspace")
def snapshot_workspace(request: SnapshotWorkspaceRequest,
                       _uid: str = Depends(get_current_user_id)):
    try:
        result = _ctrl().snapshot(
            workspace_id=request.workspace_id,
            snapshot_name=request.snapshot_name,
        )
        return result
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
