"""
WekezaOmniOS Teleportation API Server
The entry point for the Universal Application Teleportation (UAT) control plane.
Phases 1-6 are wired here.
"""

import uvicorn
from fastapi import FastAPI
from .routes import router
from .teleport import router as remote_router

# Initializing the FastAPI application with high-level system metadata
app = FastAPI(
    title="WekezaOmniOS Teleportation API",
    description=(
        "Control plane for Universal Application Teleportation (UAT). "
        "Orchestrates capture, transfer, and restoration of processes across nodes. "
        "Phases 1–6: local checkpointing, cross-node teleportation, container runtime "
        "integration, distributed snapshot storage, live migration, and security."
    ),
    version="2.0.0",
    contact={
        "name": "Wekeza Bank Engineering Team",
        "url": "https://wekeza.bank/engineering",
    },
)

# Phase 1 routes (local teleport, snapshot, restore)
app.include_router(router)

# Phase 2 routes (cross-node remote teleport)
app.include_router(remote_router)


@app.get("/", tags=["System Health"])
def read_root():
    """
    Landing endpoint to verify the API is online and responsive.
    """
    return {
        "engine": "WekezaOmniOS UAT",
        "status": "online",
        "phase": "2+",
        "supported_ops": [
            "teleport/local",
            "teleport/remote",
            "teleport/clone",
            "health_check",
        ],
    }


if __name__ == "__main__":
    print("🚀 WekezaOmniOS Teleportation Engine is starting...")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
