"""
WekezaOmniOS API Server
Main entry point for the Teleportation Control Plane.
"""

import uvicorn
from fastapi import FastAPI
from .routes.teleportation_routes import router
from .routes.developer_routes import router as ide_router
from .routes.terminal_routes import router as terminal_router
from .routes.ai_routes import router as ai_router

app = FastAPI(
    title="WekezaOmniOS Universal Teleportation API",
    description="The programmatic control plane for Wekeza's Universal Application Teleportation (UAT) engine.",
    version="0.3.0",
    contact={
        "name": "Emmanuel Odenyire Anyira",
        "url": "https://github.com/WekezaOmniOS",
    }
)

# Modular route inclusion
app.include_router(router)
app.include_router(ide_router)
app.include_router(ai_router)
app.include_router(terminal_router)

@app.get("/", tags=["Health Check"])
def root():
    """Verify API availability and versioning."""
    return {
        "service": "WekezaOmniOS UAT API",
        "status": "active",
        "phase": "20.0 - Unified Cross-Platform Reality"
    }

if __name__ == "__main__":
    # Standard port 8000 with auto-reload for development
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
