"""
WekezaOmniOS Clone Endpoint
Phase 3: Programmatic interface for forking process states.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class CloneRequest(BaseModel):
    process_id: int
    target_node_ids: List[str]  # List enables simultaneous cluster-wide cloning

@router.post("/teleport/clone", tags=["Orchestration"])
def initiate_clone(request: CloneRequest):
    """
    Triggers the Phase 3 pipeline:
    1. Single State Capture
    2. Multi-Node distribution
    """
    print(f"[API] 👥 Clone Request Received: PID {request.process_id} -> Targets: {request.target_node_ids}")
    
    if not request.target_node_ids:
        raise HTTPException(status_code=400, detail="At least one target node must be specified.")

    # Logic Handoff: In production, this calls teleportation_api.clone.clone_process
    return {
        "status": "CLONE_INITIATED",
        "details": {
            "source_pid": request.process_id,
            "replica_count": len(request.target_node_ids),
            "target_nodes": request.target_node_ids
        }
    }
