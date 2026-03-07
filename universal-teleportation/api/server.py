import uvicorn
from fastapi import FastAPI
from routes import router

# Initialize the FastAPI app with comprehensive metadata
app = FastAPI(
    title="WekezaOmniOS Universal Teleportation API",
    description="REST interface for controlling the Universal Application Teleportation (UAT) engine.",
    version="0.1"
)

# Include the modular routes
app.include_router(router)

@app.get("/", tags=["Health Check"])
def root():
    """
    Root endpoint to verify the API status and version.
    """
    return {
        "message": "WekezaOmniOS Universal Teleportation API",
        "status": "running",
        "version": "0.1"
    }

# Entry point for direct script execution
if __name__ == "__main__":
    # Host 0.0.0.0 allows access from external sources/containers
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
