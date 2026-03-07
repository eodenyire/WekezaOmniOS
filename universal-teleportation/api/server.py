from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="WekezaOmniOS Universal Teleportation API",
    description="API for controlling Universal Application Teleportation",
    version="0.1"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "WekezaOmniOS Universal Teleportation API",
        "status": "running"
    }
