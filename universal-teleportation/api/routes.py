from fastapi import APIRouter
from models import CaptureRequest, SnapshotRequest, RestoreRequest

router = APIRouter()


@router.post("/capture")
def capture_process(request: CaptureRequest):
    return {
        "status": "capturing",
        "pid": request.pid
    }


@router.post("/snapshot")
def create_snapshot(request: SnapshotRequest):
    return {
        "status": "snapshot_created",
        "pid": request.pid,
        "snapshot": request.snapshot_name
    }


@router.post("/restore")
def restore_process(request: RestoreRequest):
    return {
        "status": "restoring",
        "snapshot": request.snapshot_name
    }


@router.get("/status")
def status():
    return {
        "status": "teleportation_engine_running"
    }
