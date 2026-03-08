"""
WekezaOmniOS Interplanetary Teleportation API
Phase 15: FastAPI routes for scheduling and managing teleportation to
          high-latency interplanetary nodes.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(tags=["Interplanetary"])


PROPAGATION_DELAYS = {
    "earth_low_orbit":    0.005,
    "earth_geostationary": 0.27,
    "earth_moon":         1.28,
    "earth_mars_min":     182.0,
    "earth_mars_max":    1342.0,
    "earth_jupiter":     2610.0,
}


class InterplanetaryTeleportRequest(BaseModel):
    process_id: int
    target_node: str
    route: Optional[str] = "earth_geostationary"
    schedule_delay_s: Optional[float] = 0.0


@router.post("/teleport/interplanetary")
def teleport_interplanetary(request: InterplanetaryTeleportRequest):
    """
    Schedule a teleportation to an interplanetary node.

    Uses delay-tolerant networking (DTN) for routes with high propagation
    delays (e.g., Earth → Mars).
    """
    propagation_s = PROPAGATION_DELAYS.get(request.route, 0.0)
    total_delay_s = request.schedule_delay_s + propagation_s

    print(
        f"[InterplanetaryAPI] Scheduling PID {request.process_id} "
        f"-> {request.target_node} via {request.route} "
        f"(propagation: {propagation_s}s)"
    )

    return {
        "status": "SCHEDULED",
        "process_id": request.process_id,
        "target_node": request.target_node,
        "route": request.route,
        "propagation_delay_s": propagation_s,
        "schedule_delay_s": request.schedule_delay_s,
        "estimated_arrival_s": total_delay_s,
        "mode": "DTN" if propagation_s > 60 else "STANDARD",
    }


@router.get("/teleport/interplanetary/routes")
def list_routes():
    """Return all configured interplanetary routes with propagation delays."""
    return {
        route: {"propagation_delay_s": delay, "dtn_required": delay > 60}
        for route, delay in PROPAGATION_DELAYS.items()
    }
