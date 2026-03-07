"""
WekezaOmniOS API Routes
Handles the routing logic for process teleportation operations.
"""

from fastapi import APIRouter, HTTPException
from models import (
    TeleportRequest, 
    TeleportResponse, 
    CaptureRequest, 
    SnapshotRequest, 
    RestoreRequest,
    TeleportStatus
)

router = APIRouter()

# --- High-Level Orchestration ---

@router.post("/teleport", response_model=TeleportResponse, tags=["Orchestration"])
def teleport_process(request: TeleportRequest):
    """
    The 'One-Click' Jump. 
    Triggers: Capture → Snapshot → Transfer → Restore.
    """
    print(f"[API] 🚀 Teleporting PID {request.process_id} from {request.source_env} to {request.target_env}")
    
    # In Phase 1, we simulate the sequence
    # Phase 2 will involve awaiting the state-capture and transfer-layer results
    return TeleportResponse(
        status="initiated",
        message=f"Teleportation of PID {request.process_id} to {request.target_env} is in progress.",
        tracking_id="jump-9921-X"
    )

# --- Atomic Operations ---

@router.post("/capture", tags=["Process Control"])
def capture_process(request: CaptureRequest):
    """Freeze and capture the current state of a running process."""
    print(f"[API] 🧊 Capturing PID: {request.pid}")
    return {"status": "capturing", "pid": request.pid}

@router.post("/snapshot", tags=["Process Control"])
def create_snapshot(request: SnapshotRequest):
    """Package captured state into a portable .tar.gz snapshot."""
    name = request.snapshot_name or f"snapshot_pid_{request.pid}"
    print(f"[API] 📦 Creating snapshot '{name}'")
    return {"status": "snapshot_created", "snapshot": name}

@router.post("/restore", tags=["Process Control"])
def restore_process(request: RestoreRequest):
    """Reanimate a process from a saved snapshot."""
    print(f"[API] ⚡ Restoring from: {request.snapshot_name}")
    return {"status": "restoring", "snapshot": request.snapshot_name}

# --- System Status ---

@router.get("/status", response_model=TeleportStatus, tags=["System"])
def get_engine_status():
    """Verify the health and availability of the Teleportation Engine."""
    return TeleportStatus(
        status="online",
        message="WekezaOmniOS UAT Engine is ready for jumps.",
        engine_load=0.15
    )
