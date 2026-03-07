from pydantic import BaseModel, Field
from typing import Optional

# --- Orchestration Models ---

class TeleportRequest(BaseModel):
    """Schema for high-level environment-to-environment migration."""
    process_id: int
    source_env: str
    target_env: str

class TeleportResponse(BaseModel):
    """Standardized response for orchestration commands."""
    status: str
    message: str

# --- Atomic Operation Models ---

class CaptureRequest(BaseModel):
    """Request schema for freezing a local process state."""
    pid: int

class SnapshotRequest(BaseModel):
    """Request schema for turning captured state into a portable file."""
    pid: int
    snapshot_name: Optional[str] = Field(None, description="Optional name for the generated snapshot file.")

class RestoreRequest(BaseModel):
    """Request schema for rehydrating a process on a new host."""
    snapshot_name: str

# --- Health & Status Models ---

class TeleportStatus(BaseModel):
    """Schema for engine health and migration progress updates."""
    status: str
    message: Optional[str] = None
