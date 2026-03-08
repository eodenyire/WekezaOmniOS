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
    target_node_ids: List[str]  # Multiple nodes for simultaneous cloning

@router.post("/teleport/clone", tags=["Orchestration"])
def initiate_clone(request: CloneRequest):
    """
    Triggers the Phase 3 pipeline:
    1. Single State Capture
    2. One-to-Many Distribution
    3. Multi-Node Reanimation
    """
    print(f"[API] 👥 Clone Request: PID {request.process_id} -> Nodes {request.target_node_ids}")
    
    if not request.target_node_ids:
        raise HTTPException(status_code=400, detail="At least one target node must be specified.")

    return {
        "status": "CLONE_INITIATED",
        "details": {
            "source_pid": request.process_id,
            "replica_count": len(request.target_node_ids),
            "targets": request.target_node_ids
        }
    }
