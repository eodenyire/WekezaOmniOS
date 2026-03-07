from pydantic import BaseModel
from typing import Optional


class CaptureRequest(BaseModel):
    pid: int


class SnapshotRequest(BaseModel):
    pid: int
    snapshot_name: Optional[str] = None


class RestoreRequest(BaseModel):
    snapshot_name: str


class TeleportStatus(BaseModel):
    status: str
    message: Optional[str] = None
