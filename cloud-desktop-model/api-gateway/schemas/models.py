"""
WekezaOmniOS Cloud Desktop API — Pydantic request / response schemas.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ======================================================================
# Auth schemas
# ======================================================================

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=64, example="alice")
    password: str = Field(..., min_length=8, example="s3cr3t!!")
    email: Optional[str] = Field(None, example="alice@example.com")


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str


class UserProfile(BaseModel):
    user_id: str
    username: str
    email: Optional[str] = None
    created_at: str


# ======================================================================
# Node schemas
# ======================================================================

class NodeRegisterRequest(BaseModel):
    node_id: str = Field(..., example="linux-node-01")
    node_type: str = Field(..., example="linux", description="linux | windows | android-emulator")
    address: str = Field(..., example="10.0.0.5")
    cpu_cores: int = Field(4, ge=1)
    ram_gb: int = Field(8, ge=1)


class NodeResponse(BaseModel):
    node_id: str
    node_type: str
    address: str
    status: str
    cpu_cores: int
    ram_gb: int
    active_sessions: int
    created_at: str


# ======================================================================
# Session / OS launcher schemas
# ======================================================================

class LaunchSessionRequest(BaseModel):
    user_id: str = Field(..., example="alice")
    os_profile: str = Field("ubuntu-22.04", example="ubuntu-22.04",
                             description="ubuntu-22.04 | windows-11 | android-14 | ...")
    cpu_cores: int = Field(2, ge=1, le=32)
    ram_gb: int = Field(4, ge=1, le=256)


class SessionResponse(BaseModel):
    session_id: str
    user_id: str
    os_profile: str
    node_id: str
    node_type: str
    status: str
    started_at: str
    connect_url: str
    allocated_cpu: Optional[int] = None
    allocated_ram_gb: Optional[int] = None


class TerminateSessionRequest(BaseModel):
    session_id: str


class SessionStatusResponse(BaseModel):
    status: str
    session_id: str
    message: Optional[str] = None


# ======================================================================
# Workspace schemas
# ======================================================================

class CreateWorkspaceRequest(BaseModel):
    user_id: str = Field(..., example="alice")
    name: str = Field(..., example="my-dev-env")
    os_profile: str = Field("ubuntu-22.04", example="ubuntu-22.04")
    cpu_cores: int = Field(2, ge=1, le=32)
    ram_gb: int = Field(4, ge=1, le=256)


class CloneWorkspaceRequest(BaseModel):
    source_workspace_id: str
    new_name: str
    new_user_id: Optional[str] = None


class SnapshotWorkspaceRequest(BaseModel):
    workspace_id: str
    snapshot_name: Optional[str] = None


class WorkspaceResponse(BaseModel):
    workspace_id: str
    user_id: str
    name: str
    os_profile: str
    status: str
    session: Optional[Dict[str, Any]] = None
    snapshots: List[str] = []
    created_at: str
    updated_at: str


# ======================================================================
# Cluster / health schemas
# ======================================================================

class ClusterStatusResponse(BaseModel):
    status: str
    total_nodes: int
    active_sessions: int
    resource_usage: Dict[str, Any]
    nodes: List[Dict[str, Any]]
