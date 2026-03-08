"""
WekezaOmniOS Hardware API Endpoint
Phase 20: FastAPI routes for hardware-assisted teleportation.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(tags=["Hardware Interface"])


class HardwareTransferRequest(BaseModel):
    snapshot_path: str
    target_device: str
    device_id: Optional[str] = "UAT-HW-001"


class HardwareStatusRequest(BaseModel):
    transfer_id: str


@router.post("/teleport/hardware/initiate")
def initiate_hardware_teleport(request: HardwareTransferRequest):
    """
    Initiate a hardware-assisted teleportation.

    Phase 20 endpoint: delegates to the HardwareInterface abstraction layer.
    """
    print(f"[HardwareAPI] Initiating hardware transfer: {request.snapshot_path} -> {request.target_device}")
    # In production: delegate to HardwareInterface instance from dependency injection
    return {
        "status": "INITIATED",
        "snapshot_path": request.snapshot_path,
        "target_device": request.target_device,
        "device_id": request.device_id,
        "message": "Hardware transfer initiated. Poll /teleport/hardware/status for updates.",
    }


@router.post("/teleport/hardware/status")
def get_hardware_status(request: HardwareStatusRequest):
    """Return the current status of a hardware transfer."""
    return {
        "transfer_id": request.transfer_id,
        "status": "TRANSMITTING",
        "progress_pct": 50.0,
    }


@router.get("/teleport/hardware/device")
def get_device_info():
    """Return hardware device metadata."""
    return {
        "device_id": "UAT-HW-001",
        "status": "ONLINE",
        "protocol_version": "UAT/2.0",
        "max_payload_gb": 1024,
    }
