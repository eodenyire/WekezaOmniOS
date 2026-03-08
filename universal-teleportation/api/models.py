"""
WekezaOmniOS API Models
Defines the request and response schemas for UAT orchestration.
"""

from pydantic import BaseModel, Field
from typing import Optional

# --- Orchestration Models ---

class TeleportRequest(BaseModel):
    """Schema for high-level environment-to-environment migration."""
    process_id: int = Field(..., example=1921)
    source_env: str = Field(..., example="nairobi-node-01")
    target_env: str = Field(..., example="cloud-node-us-east")

class TeleportResponse(BaseModel):
    """Standardized response for orchestration commands."""
    status: str
    message: str
    tracking_id: Optional[str] = None

# --- Atomic Operation Models ---

class CaptureRequest(BaseModel):
    """Request schema for freezing a local process state."""
    pid: int

class SnapshotRequest(BaseModel):
    """Request schema for turning captured state into a portable file."""
    pid: int
    snapshot_name: Optional[str] = Field(None, description="Optional name for the generated snapshot.")

class RestoreRequest(BaseModel):
    """Request schema for rehydrating a process on a new host."""
    snapshot_name: str

# --- Health & Status Models ---

class TeleportStatus(BaseModel):
    """Schema for engine health and migration progress updates."""
    status: str
    message: Optional[str] = None
    engine_load: float = 0.0


# --- Phase 2 Cluster Models ---

class NodeRegisterRequest(BaseModel):
    node_id: str
    address: str
    role: str = "worker"
    port: int = 8000


class NodeRegisterResponse(BaseModel):
    status: str
    node: dict


class RemoteTeleportRequest(BaseModel):
    process_id: int
    target_node_id: str
    protocol: str = "auto"


class RemoteTeleportResponse(BaseModel):
    status: str
    tracking_id: str
    target_node_id: str
    transfer_protocol: str
