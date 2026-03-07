"""
WekezaOmniOS Teleportation API Server
The entry point for the Universal Application Teleportation (UAT) control plane.
"""

import uvicorn
from fastapi import FastAPI
from .routes import router

# Initializing the FastAPI application with high-level system metadata
app = FastAPI(
    title="WekezaOmniOS Teleportation API",
    description="Control plane for Universal Application Teleportation (UAT). Orchestrates capture, transfer, and restoration of processes.",
    version="1.0.0",
    contact={
        "name": "Wekeza Bank Engineering Team",
        "url": "https://wekeza.bank/engineering",
    }
)

# Mounting the modular teleportation routes
app.include_router(router)

@app.get("/", tags=["System Health"])
def read_root():
    """
    Landing endpoint to verify the API is online and responsive.
    """
    return {
        "engine": "WekezaOmniOS UAT",
        "status": "online",
        "phase": 1,
        "supported_ops": ["teleport", "health_check"]
    }

if __name__ == "__main__":
    # Launching the server
    # '0.0.0.0' makes the API accessible across the Wekeza Bank internal network
    print("🚀 WekezaOmniOS Teleportation Engine is starting...")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
