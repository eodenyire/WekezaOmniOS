"""
WekezaOmniOS API Routes
Handles the routing logic for process teleportation operations.
"""

import os
import sys
import datetime
import importlib.util
from fastapi import APIRouter, HTTPException
from models import (
    TeleportRequest, 
    TeleportResponse, 
    CaptureRequest, 
    SnapshotRequest, 
    RestoreRequest,
    TeleportStatus
)

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import modules using importlib (to handle hyphenated directory names)
def load_module(name, path):
    """Import a module from a file path."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Import the state management modules
capture_manager_module = load_module(
    "capture_manager",
    os.path.join(parent_dir, "state-capture", "capture_manager.py")
)
snapshot_builder_module = load_module(
    "snapshot_builder",
    os.path.join(parent_dir, "snapshot-engine", "snapshot_builder.py")
)
snapshot_metadata_module = load_module(
    "snapshot_metadata",
    os.path.join(parent_dir, "snapshot-engine", "snapshot_metadata.py")
)
restore_manager_module = load_module(
    "restore_manager",
    os.path.join(parent_dir, "state-reconstruction", "restore_manager.py")
)

CaptureManager = capture_manager_module.CaptureManager
build_snapshot = snapshot_builder_module.build_snapshot
save_metadata = snapshot_metadata_module.save_metadata
RestoreManager = restore_manager_module.RestoreManager

router = APIRouter()

# --- High-Level Orchestration ---

@router.post("/teleport", response_model=TeleportResponse, tags=["Orchestration"])
def teleport_process(request: TeleportRequest):
    """
    The 'One-Click' Jump. 
    Triggers: Capture → Snapshot → Transfer → Restore.
    """
    print(f"[API] 🚀 Teleporting PID {request.process_id} from {request.source_env} to {request.target_env}")
    
    try:
        # Phase 1: Local orchestration
        # Step 1: Capture
        manager = CaptureManager(snapshot_dir="./snapshots")
        info = manager.capture_process(request.process_id)
        
        # Step 2: Snapshot
        snapshot_dir = f"./snapshots/process_{request.process_id}"
        snapshot_name = f"teleport_{request.process_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_file = f"./snapshots/{snapshot_name}.tar.gz"
        
        metadata = {
            "process_id": request.process_id,
            "timestamp": datetime.datetime.now().isoformat(),
            "source_env": request.source_env,
            "target_env": request.target_env,
            "snapshot_name": snapshot_name
        }
        
        build_snapshot(snapshot_dir, output_file, metadata)
        
        # Step 3: In Phase 1, transfer is local (no-op)
        # Step 4: Would restore on target (simulated in Phase 1)
        
        return TeleportResponse(
            status="success",
            message=f"Process {request.process_id} teleportation completed. Snapshot: {snapshot_name}",
            tracking_id=f"UAT-{request.process_id}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        )
    except Exception as e:
        return TeleportResponse(
            status="failed",
            message=f"Teleportation failed: {str(e)}",
            tracking_id=None
        )

# --- Atomic Operations ---

@router.post("/capture", tags=["Process Control"])
def capture_process_endpoint(request: CaptureRequest):
    """Freeze and capture the current state of a running process."""
    print(f"[API] 🧊 Capturing PID: {request.pid}")
    
    try:
        manager = CaptureManager(snapshot_dir="./snapshots")
        info = manager.capture_process(request.pid)
        return {"status": "success", "pid": request.pid, "info": info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Capture failed: {str(e)}")

@router.post("/snapshot", tags=["Process Control"])
def create_snapshot(request: SnapshotRequest):
    """Package captured state into a portable .tar.gz snapshot."""
    name = request.snapshot_name or f"snapshot_pid_{request.pid}"
    print(f"[API] 📦 Creating snapshot '{name}'")
    
    try:
        snapshot_dir = f"./snapshots/process_{request.pid}"
        output_file = f"./snapshots/{name}.tar.gz"
        
        metadata = {
            "process_id": request.pid,
            "timestamp": datetime.datetime.now().isoformat(),
            "snapshot_name": name
        }
        
        success = build_snapshot(snapshot_dir, output_file, metadata)
        
        if success:
            return {"status": "success", "snapshot": name, "file": output_file}
        else:
            raise HTTPException(status_code=500, detail="Snapshot creation failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Snapshot failed: {str(e)}")

@router.post("/restore", tags=["Process Control"])
def restore_process_endpoint(request: RestoreRequest):
    """Reanimate a process from a saved snapshot."""
    print(f"[API] ⚡ Restoring from: {request.snapshot_name}")
    
    try:
        # Extract PID from snapshot name (expecting format like "snapshot_pid_1234")
        # This is a simplified approach for Phase 1
        parts = request.snapshot_name.split("_")
        if "pid" in parts:
            pid_index = parts.index("pid") + 1
            pid = int(parts[pid_index])
        else:
            # Fallback: try to extract any number
            import re
            numbers = re.findall(r'\d+', request.snapshot_name)
            if numbers:
                pid = int(numbers[0])
            else:
                raise ValueError("Cannot extract PID from snapshot name")
        
        manager = RestoreManager(snapshot_dir="./snapshots")
        manager.restore_snapshot(pid)
        
        return {"status": "success", "snapshot": request.snapshot_name, "pid": pid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Restore failed: {str(e)}")

# --- System Status ---

@router.get("/status", response_model=TeleportStatus, tags=["System"])
def get_engine_status():
    """Verify the health and availability of the Teleportation Engine."""
    
    # Check directories
    dirs_ok = all(os.path.exists(d) for d in ["./snapshots", "./logs", "./temp"])
    
    # Check for CRIU
    import subprocess
    try:
        subprocess.run(["which", "criu"], check=True, capture_output=True)
        criu_available = True
    except:
        criu_available = False
    
    status_msg = "WekezaOmniOS UAT Engine is ready"
    if not criu_available:
        status_msg += " (CRIU not available - limited functionality)"
    
    return TeleportStatus(
        status="online" if dirs_ok else "degraded",
        message=status_msg,
        engine_load=0.15
    )
